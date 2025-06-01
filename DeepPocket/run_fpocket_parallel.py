#!/usr/bin/env python3
import os
import argparse
import subprocess
from multiprocessing import Pool, cpu_count

def run_fpocket(pdb_path):
    if not os.path.exists(pdb_path):
        return f"[MISSING] {pdb_path}"
    
    out_dir = pdb_path.replace(".pdb", "_out")
    if os.path.exists(out_dir):
        return f"[SKIP] {os.path.basename(pdb_path)} (already processed)"

    try:
        subprocess.run(["fpocket", "-f", pdb_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return f"[OK] {os.path.basename(pdb_path)}"
    except subprocess.CalledProcessError as e:
        return f"[ERROR] {os.path.basename(pdb_path)}: {e}"

def main(input_dir, n_workers):
    pdb_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".pdb")
    ]
    print(f"Found {len(pdb_files)} PDB files. Starting fpocket with {n_workers} workers...")

    with Pool(processes=n_workers) as pool:
        for result in pool.imap_unordered(run_fpocket, pdb_files):
            print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run fpocket in parallel on cleaned PDB files.")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing cleaned .pdb files")
    parser.add_argument("--n_workers", type=int, default=8, help="Number of parallel processes to use")
    args = parser.parse_args()

    main(args.input_dir, args.n_workers)
