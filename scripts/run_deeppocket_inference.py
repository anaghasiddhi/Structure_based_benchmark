import os
import subprocess
from tqdm import tqdm

# Paths
dataset_dir = "Dataset/scPDB/scPDB"
output_root = "Results/scPDB_predictions"
classifier_ckpt = "checkpoints/first_model_fold1_best_test_auc_85001.pth.tar"
segmenter_ckpt = "checkpoints/seg0_best_test_IOU_91.pth.tar"

# Make sure output directory exists
os.makedirs(output_root, exist_ok=True)

# Collect protein folders
protein_dirs = sorted([f for f in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, f))])
print(f"Running DeepPocket on {len(protein_dirs)} proteins...")

env = os.environ.copy()
env["CUDA_VISIBLE_DEVICES"] = "0"

for protein_id in tqdm(protein_dirs):
    input_dir = os.path.join(dataset_dir, protein_id)
    output_dir = os.path.join(output_root, protein_id)
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python", "predict.py",
        "-p", os.path.join(input_dir, "protein.mol2"),
        "-l", os.path.join(input_dir, "ligand.mol2"),
        "-c", classifier_ckpt,
        "-s", segmenter_ckpt,
        "-o", output_dir
    ]

    try:
        subprocess.run(command, check=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"Error running {protein_id}: {e}")

print("Inference complete.")
