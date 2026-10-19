from __future__ import annotations

import pandas as pd


def build_graph_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build historical graph features using only strictly earlier timestamps."""
    required = {
        "transaction_id",
        "customer_id",
        "merchant_id",
        "device_id",
        "timestamp",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    work = df.copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True, errors="raise")

    if work["transaction_id"].isna().any():
        raise ValueError("transaction_id cannot contain missing values.")
    if work["transaction_id"].duplicated().any():
        raise ValueError("transaction_id values must be unique.")

    work = work.sort_values(
        ["timestamp", "transaction_id"], kind="mergesort"
    ).reset_index(drop=True)

    results = []

    customer_devices = {}
    customer_merchants = {}
    device_customers = {}
    merchant_customers = {}

    # Process a timestamp batch against one frozen historical graph state.
    # Only after all rows in the batch are scored is the graph updated.
    for timestamp, batch in work.groupby("timestamp", sort=True):
        batch_rows = list(batch.itertuples(index=False))
        pending_updates = []

        for row in batch_rows:
            customer = str(row.customer_id)
            merchant = str(row.merchant_id)
            device = str(row.device_id)

            previous_customer_devices = customer_devices.get(customer, set())
            previous_customer_merchants = customer_merchants.get(customer, set())
            previous_device_customers = device_customers.get(device, set())
            previous_merchant_customers = merchant_customers.get(merchant, set())

            customer_device_degree = len(previous_customer_devices)
            customer_merchant_degree = len(previous_customer_merchants)
            device_customer_degree = len(previous_device_customers)
            merchant_customer_degree = len(previous_merchant_customers)

            shared_device = int(
                customer not in previous_device_customers
                and device_customer_degree > 0
            )
            shared_merchant = int(
                customer not in previous_merchant_customers
                and merchant_customer_degree > 0
            )

            new_device = int(device not in previous_customer_devices)
            new_merchant = int(merchant not in previous_customer_merchants)

            graph_risk_score = min(
                float(
                    shared_device * 35
                    + shared_merchant * 15
                    + new_device * 10
                    + new_merchant * 5
                    + min(device_customer_degree, 5) * 5
                    + min(merchant_customer_degree, 10)
                ),
                100.0,
            )

            results.append(
                {
                    "transaction_id": row.transaction_id,
                    "customer_id": customer,
                    "merchant_id": merchant,
                    "device_id": device,
                    "timestamp": timestamp,
                    "customer_device_degree": customer_device_degree,
                    "customer_merchant_degree": customer_merchant_degree,
                    "device_customer_degree": device_customer_degree,
                    "merchant_customer_degree": merchant_customer_degree,
                    "shared_device": shared_device,
                    "shared_merchant": shared_merchant,
                    "new_device": new_device,
                    "new_merchant": new_merchant,
                    "graph_risk_score": graph_risk_score,
                }
            )

            pending_updates.append((customer, merchant, device))

        # Update only after the entire timestamp batch has been scored.
        for customer, merchant, device in pending_updates:
            customer_devices.setdefault(customer, set()).add(device)
            customer_merchants.setdefault(customer, set()).add(merchant)
            device_customers.setdefault(device, set()).add(customer)
            merchant_customers.setdefault(merchant, set()).add(customer)

    return pd.DataFrame(results)
