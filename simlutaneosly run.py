import threading
import subprocess

def run_script(script_name):
    subprocess.run(["python3", script_name])

if __name__ == "__main__":
    # List of scripts to run
    scripts = ["lcd_test.py", "plant_project.py"]

    # Creating thread for each script
    threads = []
    for script in scripts:
        thread = threading.Thread(target=run_script, args=(script,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All scripts have finished execution.")