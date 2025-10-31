import requests
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

# --------------------------
# CONFIG
# --------------------------
GITHUB_USER = "KSUhippiebus"
GITHUB_REPO = "cosmoTed"
BRANCH = "main"
EXCLUDE_FILE = "launcher.py"
# --------------------------

API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/git/trees/{BRANCH}?recursive=1"

def fetch_py_files():
    """Fetch all .py files from the repo, excluding EXCLUDE_FILE"""
    try:
        resp = requests.get(API_URL)
        resp.raise_for_status()
        data = resp.json()
        files = [item["path"]
                 for item in data.get("tree", [])
                 if item["type"] == "blob"
                 and item["path"].endswith(".py")
                 and EXCLUDE_FILE not in item["path"]]
        return files
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch file list:\n{e}")
        return []

# Folder of the launcher file
LAUNCHER_DIR = os.path.dirname(os.path.abspath(__file__))

def run_script_in_cmd(file_path):
    raw_url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/{file_path}"
    try:
        # Save the script in the same folder as the launcher
        local_path = os.path.join(LAUNCHER_DIR, os.path.basename(file_path))

        r = requests.get(raw_url)
        r.raise_for_status()
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(r.text)

        # Run the script in a new CMD window with cwd = launcher folder
        subprocess.Popen(
            ["python", os.path.basename(local_path)],
            cwd=LAUNCHER_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as e:
        print(f"Failed to run {file_path}: {e}")
# --------------------------
# TKINTER GUI
# --------------------------
root = tk.Tk()
root.title(f"{GITHUB_REPO} Python Files")

main_frame = ttk.Frame(root, padding=(10,10))
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas_frame = canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Fetch and display buttons
files = fetch_py_files()
if not files:
    ttk.Label(scrollable_frame, text="No Python files found or fetch failed.").pack(pady=10)
else:
    for fpath in files:
        btn = ttk.Button(scrollable_frame, text=fpath,
                         command=lambda p=fpath: run_script_in_cmd(p))
        btn.pack(fill="x", pady=2)

root.mainloop()
