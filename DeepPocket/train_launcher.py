import os
import argparse
import subprocess
from datetime import datetime

def run_trial(dataset, freeze_pattern, trial_num, output_dir):
    run_name = f"trial_{trial_num:02d}"
    run_dir = os.path.join(output_dir, run_name)
    os.makedirs(run_dir, exist_ok=True)

    log_path = os.path.join(run_dir, "train.log")
    model_path = os.path.join(run_dir, "model.pth.tar")

    freeze_args = f"--freeze {freeze_pattern}" if freeze_pattern else ""

    train_cmd = (
        f"python train.py "
        f"-m default "
        f"--train_types ../Dataset/{dataset}/{dataset}_train0.types "
        f"--test_types ../Dataset/{dataset}/{dataset}_test0.types "
        f"--train_recmolcache ../Dataset/{dataset}/{dataset}.molcache2 "
        f"--test_recmolcache ../Dataset/{dataset}/{dataset}.molcache2 "
        f"-o {model_path} "
        f"{freeze_args}"
    )

    print(f"[{datetime.now()}] Starting {run_name}")
    print(f"[CMD] {train_cmd}")

    with open(log_path, "w") as log_file:
        result = subprocess.run(train_cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT)
        if result.returncode == 0:
            print(f"[OK] {run_name} completed.")
        else:
            print(f"[ERROR] {run_name} failed. Check log at {log_path}")

def main():
    parser = argparse.ArgumentParser(description="Train DeepPocket model with optional layer freezing.")
    parser.add_argument("--dataset", type=str, required=True, help="Dataset name (e.g., scPDB, BioLiP)")
    parser.add_argument("--freeze", type=str, default="", help="Layer keywords to freeze (e.g., 'unit0 unit1')")
    parser.add_argument("--trials", type=int, default=3, help="Number of trials to run")
    args = parser.parse_args()

    output_dir = os.path.join("logs", args.dataset)
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, args.trials + 1):
        run_trial(args.dataset, args.freeze, i, output_dir)

if __name__ == "__main__":
    main()
