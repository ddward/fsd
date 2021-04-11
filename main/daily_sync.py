import sys
import subprocess
from pathlib import Path
import schedule
import time

dir_path = Path(__file__).resolve().parent


def sync():
    execute_script(["bash", dir_path / "fsd_venv_script_0.sh"])
    execute_script(["bash", dir_path / "fsd_venv_script_1.sh"])
    execute_script(["bash", dir_path / "api_venv_script_0.sh"])
    print("Daily update completed.")


def execute_script(cmd):
    subprocess.run(cmd, stdout=sys.stdout, stderr=subprocess.STDOUT)


if __name__ == "__main__":
    schedule.every().day.at("00:30").do(sync)
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute"""
