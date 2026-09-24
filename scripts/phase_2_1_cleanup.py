from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]


source_files = {
    ROOT /
    "models" /
    "logistic_regression" /
    "model.joblib":

    ROOT /
    "models" /
    "baseline_logistic" /
    "model.joblib",


    ROOT /
    "models" /
    "xgboost" /
    "model.joblib":

    ROOT /
    "models" /
    "baseline_xgboost" /
    "model.joblib",
}



for source, target in source_files.items():

    if source.exists():

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            target,
        )

        print(
            f"[COPIED] {target}"
        )


report = {
    "phase":
    "2.1",

    "status":
    "baseline hardened",

    "improvements":
    [
        "threshold optimization",
        "model documentation",
        "artifact structure cleanup",
        "imbalance handling",
    ]
}


with open(
    ROOT /
    "reports" /
    "baseline" /
    "phase_2_1_summary.json",
    "w",
) as file:

    json.dump(
        report,
        file,
        indent=2,
    )


print(
    "[PASS] Phase 2.1 summary generated"
)
