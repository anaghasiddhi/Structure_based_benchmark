import os
import subprocess

base_dir = "../Dataset/scPDB/scPDB/cleaned"
model_ckpt = "checkpoints/first_model_fold1_best_test_auc_85001.pth.tar"
seg_ckpt = "checkpoints/seg0_best_test_IOU_91.pth.tar"

pdb_files = sorted([f for f in os.listdir(base_dir) if f.endswith(".pdb")])

for pdb in pdb_files:
    pdb_path = os.path.join(base_dir, pdb)
    out_base = pdb_path.replace(".pdb", "_out")
    ranked_types_path = os.path.join(out_base, "bary_centers_ranked.types")

    if os.path.exists(ranked_types_path):
        print(f"[SKIP] {pdb}")
        continue

    print(f"[RUNNING] {pdb}")
    try:
        subprocess.run([
            "python", "predict.py",
            "-p", pdb_path,
            "-c", model_ckpt,
            "-s", seg_ckpt,
            "-r", "3"
        ], check=True)
        print(f"[OK] {pdb}")
    except subprocess.CalledProcessError:
        print(f"[FAIL] {pdb}")
