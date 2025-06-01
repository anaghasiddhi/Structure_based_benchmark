import os
import subprocess
from multiprocessing import Pool, cpu_count

def process_out_dir(out_path):
    bary_file = os.path.join(out_path, "bary_centers.txt")
    if os.path.exists(bary_file):
        return f"[SKIP] {os.path.basename(out_path)}"

    try:
        subprocess.run(
            ["python", "get_centers.py", out_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return f"[OK] {os.path.basename(out_path)}"
    except subprocess.CalledProcessError:
        return f"[ERROR] {os.path.basename(out_path)}"

def main():
    base_dir = "../Dataset/scPDB/scPDB/cleaned"
    out_dirs = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if d.endswith("_out") and os.path.isdir(os.path.join(base_dir, d))
    ]

    print(f"Found {len(out_dirs)} _out directories. Starting with {cpu_count()} workers...")

    with Pool(cpu_count()) as pool:
        for result in pool.imap_unordered(process_out_dir, out_dirs):
            print(result)

if __name__ == "__main__":
    main()
