import os
import subprocess
from multiprocessing import Pool

base_dir = "../Dataset/scPDB/scPDB/cleaned"

def run_types_and_gninatyper(subdir):
    bary_file = os.path.join(base_dir, subdir, "bary_centers.txt")
    protein_file = os.path.join(base_dir, subdir.replace("_out", ".pdb"))
    if os.path.exists(bary_file) and os.path.exists(protein_file):
        try:
            print(f"[RUNNING] {subdir}")
            subprocess.run(["python", "types_and_gninatyper.py", protein_file, bary_file], check=True)
            print(f"[OK] {subdir}")
        except subprocess.CalledProcessError:
            print(f"[FAIL] {subdir}")

if __name__ == "__main__":
    subdirs = [d for d in os.listdir(base_dir) if d.endswith("_out")]
    with Pool(processes=16) as pool:
        pool.map(run_types_and_gninatyper, subdirs)
