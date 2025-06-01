import os
import subprocess


def run_deeppocket(pdb_file, output_dir, model_dir=None, device="cuda:0"):
    """
    Run DeepPocket's prediction on a given PDB file.

    Args:
        pdb_file (str): Path to the input PDB file.
        output_dir (str): Path to the directory where output should be saved.
        model_dir (str, optional): Path to trained DeepPocket model directory. If None, uses default.
        device (str): Device to run inference on (e.g., "cuda:0" or "cpu").
    """
    if not os.path.exists(pdb_file):
        raise FileNotFoundError(f"PDB file not found: {pdb_file}")

    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python",
        "predict.py",
        "--pdb", pdb_file,
        "--out_dir", output_dir,
        "--device", device
    ]

    if model_dir:
        command += ["--model_dir", model_dir]

    try:
        print(f"Running DeepPocket on {pdb_file}...")
        subprocess.run(command, check=True)
        print(f"DeepPocket output saved to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"DeepPocket prediction failed for {pdb_file}")
        print(e)


def load_prediction_centers(output_dir, filename="predicted_centers.csv"):
    """
    Load DeepPocket's predicted pocket centers (if available).

    Args:
        output_dir (str): Path where DeepPocket saved output.
        filename (str): Name of the file containing center coordinates.

    Returns:
        List of center coordinates (or empty list if not found).
    """
    file_path = os.path.join(output_dir, filename)
    if not os.path.exists(file_path):
        print(f"Warning: Prediction file not found: {file_path}")
        return []

    centers = []
    with open(file_path, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                try:
                    x, y, z = map(float, line.strip().split(","))
                    centers.append((x, y, z))
                except ValueError:
                    continue
    return centers


# Example usage:
# run_deeppocket("Dataset/protein1.pdb", "Results/DeepPocket/protein1")
# centers = load_prediction_centers("Results/DeepPocket/protein1")
