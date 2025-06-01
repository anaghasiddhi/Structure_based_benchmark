import os
import subprocess
from multiprocessing import Pool, cpu_count

# CONFIG
input_dir = "/home/scratch1/asiddhi/benchmarking_model2/Dataset/scPDB/scPDB"
obabel_path = "/home/asiddhi/openbabel/install/bin/obabel"
n_workers = min(cpu_count(), 16)

def convert_mol2_to_pdb(entry):
    subdir = os.path.join(input_dir, entry)
    mol2_file = os.path.join(subdir, "protein.mol2")
    pdb_file = os.path.join(subdir, "protein.pdb")

    if not os.path.isfile(mol2_file) or os.path.getsize(mol2_file) == 0:
        return f"[SKIP] {mol2_file} missing or empty"

    cmd = [
        obabel_path,
        "-imol2", mol2_file,
        "-opdb", "-O", pdb_file
    ]

    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )

        # Check output
        out = result.stdout.decode()
        err = result.stderr.decode()
        if "0 molecules converted" in out or "0 molecules converted" in err:
            return f"[FAIL] {mol2_file} - No molecules converted"
        else:
            return f"[OK] {mol2_file}"
    except subprocess.CalledProcessError as e:
        return f"[ERROR] {mol2_file}:\n{e.stderr.decode()}"

if __name__ == "__main__":
    entries = sorted(os.listdir(input_dir))
    with Pool(n_workers) as pool:
        for result in pool.imap_unordered(convert_mol2_to_pdb, entries):
            print(result)
