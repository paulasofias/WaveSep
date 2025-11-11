import os
import yaml
import sys


project_folder = sys.argv[1]
yml_output_dir = "/scratch/user/uqpstoll/qsm-source-separation/Chisep_modules/WaveSep/data/yml"  # where outputs go
os.makedirs(yml_output_dir, exist_ok=True)

# ------------------------------
# Iterate through subject folders
# ------------------------------
for subj_name in sorted(os.listdir(project_folder)):
    subj_path = os.path.join(project_folder, subj_name)

    # Skip if not a folder
    if not os.path.isdir(subj_path) or not "sub" in subj_name:
        continue

    output_folder = os.path.join("/scratch/user/uqpstoll/chi_separation_output", os.path.basename(project_folder), subj_name, 'wavesep')
    # --------------------------
    # Define expected file paths
    # --------------------------
    qsm_fn = os.path.join(project_folder, "derivatives", "estimates", subj_name, f"{subj_name}_Chimap_estimate.nii")
    params_fn = '/scratch/user/uqpstoll/qsm-source-separation/Chisep_modules/WaveSep/data/yml/params.json'
    # gt_xp_fn = os.path.join(subj_path, "groundtruth", f"{subj_name}_Dr_pos.nii")
    # gt_xn_fn = os.path.join(subj_path, "groundtruth", f"{subj_name}_Dr_neg.nii")

    # Example: automatically collect all R2' and H0 files under orientation folders
    R2p_fn_list = []
    H0_fn_list = []

    r2p_file = os.path.join(project_folder, "derivatives", "estimates", subj_name, f"{subj_name}_R2prime_estimate.nii")
    R2p_fn_list.append(r2p_file)
    h0_file = '/scratch/user/uqpstoll/qsm-source-separation/Chisep_modules/WaveSep/data/yml/H0_orient.txt'
    H0_fn_list.append(h0_file)

    mask_fn = os.path.join(project_folder, "derivatives", subj_name, f'{subj_name}_mask.nii')

    # If mask does not exist, try in folder/qsm
    if not os.path.exists(mask_fn):
        mask_fn = os.path.join(project_folder, "derivatives", 'qsm_forward', subj_name, 'anat', f'{subj_name}_mask.nii')

    # --------------------------
    # Create YAML dictionary
    # --------------------------
    data_entry = [{
        "name": subj_name,
        "output_folder": output_folder,
        "qsm_fn": qsm_fn,
        "R2p_fn_list": R2p_fn_list,
        "mask_fn": mask_fn,
        "H0_fn_list": H0_fn_list,
        "params_fn": params_fn,
    }]

    # --------------------------
    # Write YAML file
    # --------------------------
    yml_path = os.path.join(yml_output_dir, f"{subj_name}.yml")
    with open(yml_path, "w") as f:
        yaml.dump(data_entry, f, sort_keys=False)

    print(f"Created: {yml_path}")

print(f"\nAll YAML files saved in: {yml_output_dir}")
