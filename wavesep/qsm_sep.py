import argparse
import yaml
import os
import glob

from utils.run_wavesep_qsm import run_wavesep_qsm


parser = argparse.ArgumentParser()
parser.add_argument("--data_folder", type=str, default="data/yml",
                    help="Folder containing YAML configuration files")
args = parser.parse_args()

# ----------------------------
# 2. Find all YAML files
# ----------------------------
yaml_files = sorted(glob.glob(os.path.join(args.data_folder, "*.yml")))

if not yaml_files:
    print(f"No YAML files found in {args.data_folder}")
    exit(1)

print(f"Found {len(yaml_files)} YAML files in {args.data_folder}.")


alg_config = {}
alg_config["alpha"] = 0.2
alg_config["wavelet"] = "db4"
alg_config["level"] = 1  # code adaptation chisep: change level to 1
alg_config["Lambda"] = 0.02


for yaml_path in yaml_files:
    print(f"\nProcessing {yaml_path} ...")

    # Load YAML
    with open(yaml_path, "r") as f:
        data_list = yaml.safe_load(f)

    # Run algorithm for each dataset in that YAML file
    for data_info in data_list:
        run_wavesep_qsm(data_info, alg_config)