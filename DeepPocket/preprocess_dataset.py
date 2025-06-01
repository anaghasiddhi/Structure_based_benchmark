#!/usr/bin/env python3
import os
import argparse
import subprocess

def run_cmd(cmd, cwd=None, check=True):
    print(f"[RUNNING] {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0 and check:
        print(f"[ERROR] Command failed with stderr:\n{result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, cmd)
    return result.stdout

def preprocess_dataset(dataset_name):
    dataset_root = os.path.abspath(f"../Dataset/{dataset_name}/{dataset_name}")
    print(f"Using dataset directory: {dataset_root}")
    
    cleaned_dir = os.path.join(dataset_root, "cleaned")
    pockets_dir = os.path.join(dataset_root, "pockets")
    gninatypes_dir = os.path.join(dataset_root, "gninatypes")
    types_dir = os.path.join(dataset_root, "types")
    molcache_dir = os.path.join(dataset_root, "molcache")

    os.makedirs(cleaned_dir, exist_ok=True)
    os.makedirs(pockets_dir, exist_ok=True)
    os.makedirs(gninatypes_dir, exist_ok=True)
    os.makedirs(types_dir, exist_ok=True)
    os.makedirs(molcache_dir, exist_ok=True)

    # Step 1: Clean PDBs
    for entry in sorted(os.listdir(dataset_root)):
        subdir = os.path.join(dataset_root, entry)
        if os.path.isdir(subdir):
            raw_pdb = os.path.join(subdir, "protein.pdb")
            cleaned_pdb = os.path.join(cleaned_dir, f"{entry}.pdb")
            if os.path.exists(raw_pdb) and os.path.getsize(raw_pdb) > 0:
                run_cmd(["python", "clean_pdb.py", raw_pdb, cleaned_pdb])
            else:
                print(f"[SKIP] {raw_pdb} is missing or empty")

    # Step 2: Run fpocket
    pdb_files = [f for f in os.listdir(cleaned_dir) if f.endswith(".pdb")]
    for pdb_file in pdb_files:
        run_cmd(["fpocket", "-f", os.path.join(cleaned_dir, pdb_file)])

    # Step 3: Get Centers
    run_cmd(["python", "get_centers.py", "-i", cleaned_dir])

    # Step 4: Create gninatypes and types
    run_cmd(["python", "types_and_gninatyper.py", "-i", cleaned_dir, "-o", gninatypes_dir])

    # Step 5: Create train/test types
    run_cmd(["python", "make_types.py", "-i", gninatypes_dir, "-o", types_dir])

    # Step 6: Create molcache
    train_type_path = os.path.join(types_dir, f"{dataset_name}_train0.types")
    test_type_path = os.path.join(types_dir, f"{dataset_name}_test0.types")
    molcache_path = os.path.join(molcache_dir, f"{dataset_name}.molcache2")
    run_cmd([
        "python", "create_molcache2.py", "-c", "4",
        "--recmolcache", molcache_path,
        "-d", cleaned_dir,
        train_type_path, test_type_path
    ])

    print(f"[DONE] Preprocessing complete for dataset: {dataset_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess DeepPocket dataset.")
    parser.add_argument("--dataset_name", type=str, required=True, help="Name of the dataset (e.g., scPDB, BioLiP)")
    args = parser.parse_args()
    preprocess_dataset(args.dataset_name)
