import csv
import glob
import os
import subprocess
from collections import defaultdict

relative_dir = os.path.dirname(os.path.abspath(__file__))
CATALOG_DIR = relative_dir
FETCH_SCRIPT_PATH = os.path.join(relative_dir, "fetch_catalog.sh")
ACCELERATORS_FILE = os.path.join(CATALOG_DIR, os.path.join("data", "accelerators.csv"))


def fetch_catalog():
    with subprocess.Popen(
        FETCH_SCRIPT_PATH, shell=True, start_new_session=True
    ) as process:
        process.wait()
        if process.returncode == 0:
            print("Successfully retrieved SkyPilot catalog.")
        else:
            print("Failed to retrieve SkyPilot catalog. Did link move?")


def parse_accelerators():
    accelerators_to_providers = defaultdict(set)

    file_pattern = os.path.join(CATALOG_DIR, "**", "vms.csv")
    for csv_file in glob.glob(file_pattern, recursive=True):
        provider = os.path.basename(os.path.dirname(csv_file))

        with open(csv_file, mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                accelerator_name = row.get("AcceleratorName")
                if accelerator_name:
                    accelerators_to_providers[accelerator_name].add(provider)

    outpath = os.path.join(CATALOG_DIR, ACCELERATORS_FILE)
    with open(outpath, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["AcceleratorName", "Providers"])
        for accelerator, providers in dict(
            sorted(accelerators_to_providers.items())
        ).items():
            providers_list = ",".join(sorted(providers))
            csv_writer.writerow([accelerator, providers_list])
        print(f"Parsed accelerators: {outpath}")


def load_catalog():
    fetch_catalog()
    parse_accelerators()


if __name__ == "__main__":
    load_catalog()