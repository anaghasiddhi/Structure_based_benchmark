import os
import subprocess

def run_deeppocket_prediction(
    pdb_path,
    model_dir="checkpoints/",
    segmentation=True,
    verbose=True
):
    base_name = os.path.splitext(os.path.basename(pdb_path))[0]

    if verbose:
        print("Running DeepPocket on:", pdb_path)

    # Use the actual pretrained filenames from the publication
    classifier_model = os.path.join(model_dir, "first_model_fold1_best_test_auc_85001.pth.tar")
    segmentation_model = os.path.join(model_dir, "seg0_best_test_IOU_91.pth.tar")

    output_dir = os.path.join("Results", "scPDB_predictions", base_name)
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "python", "DeepPocket/predict.py",
        "-p", pdb_path,
        "-c", classifier_model
    ]

    if segmentation:
        command.extend(["-s", segmentation_model])

    if verbose:
        print("Command:", " ".join(command))

    try:
        subprocess.run(command, check=True)
        print("DeepPocket run completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print("DeepPocket run failed.")
        print("Error:", e)

    return output_dir
