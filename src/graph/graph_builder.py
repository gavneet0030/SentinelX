"""
Graph intelligence foundation.

NetworkX is intentionally used for the first implementation.
Advanced graph ML can be added later.
"""

import networkx as nx
import pandas as pd


def build_transaction_graph(
    dataframe: pd.DataFrame,
) -> nx.Graph:

    graph = nx.Graph()

    for _, row in dataframe.iterrows():

        customer = row.get("customer_id")
        device = row.get("device_id")
        merchant = row.get("merchant_id")

        if pd.notna(customer):
            graph.add_node(
                str(customer),
                node_type="customer",
            )

        if pd.notna(device):
            graph.add_node(
                str(device),
                node_type="device",
            )

        if pd.notna(merchant):
            graph.add_node(
                str(merchant),
                node_type="merchant",
            )

        if pd.notna(customer) and pd.notna(device):
            graph.add_edge(
                str(customer),
                str(device),
                relationship="USES",
            )

        if pd.notna(customer) and pd.notna(merchant):
            graph.add_edge(
                str(customer),
                str(merchant),
                relationship="PAYS",
            )

    return graph


def calculate_degree_features(
    graph: nx.Graph,
) -> dict[str, int]:

    return dict(graph.degree())
