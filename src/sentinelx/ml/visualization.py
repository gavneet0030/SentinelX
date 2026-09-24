from pathlib import Path

import matplotlib.pyplot as plt

from sklearn.metrics import (
    RocCurveDisplay,
    PrecisionRecallDisplay,
)


def create_curves(
    model,
    X,
    y,
    output_dir,
    name,
):

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


    RocCurveDisplay.from_estimator(
        model,
        X,
        y,
    )

    plt.savefig(
        output_dir / f"{name}_roc_curve.png",
        bbox_inches="tight",
    )

    plt.close()



    PrecisionRecallDisplay.from_estimator(
        model,
        X,
        y,
    )


    plt.savefig(
        output_dir /
        f"{name}_precision_recall_curve.png",
        bbox_inches="tight",
    )


    plt.close()
