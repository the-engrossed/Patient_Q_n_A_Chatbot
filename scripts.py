import os
import subprocess

structure = {
    "data": ["medquad_clean.csv"],
    "retrieval": ["loader.py", "vectordb.py"],
    "chains": ["rag_chain.py", "prompt_templates.py"],
    "ui": ["app.py"],
    "utils": ["safety.py"],
}

root_files = ["main.py", "requirements.txt", "README.md"]

# Create directories and placeholder files
for folder, files in structure.items():
    os.makedirs(folder, exist_ok=True)
    for file in files:
        file_path = os.path.join(folder, file)
        if not os.path.exists(file_path):
            open(file_path, "w").close()

for file in root_files:
    if not os.path.exists(file):
        open(file, "w").close()

# Download and rename medquad.csv if not present or empty
medquad_path = "data/medquad_clean.csv"
if (not os.path.exists(medquad_path)) or os.stat(medquad_path).st_size == 0:
    print("Downloading MedQuAD from Kaggle...")
    try:
        subprocess.run([
            "kaggle", "datasets", "download",
            "-d", "pythonafroz/medquad-medical-question-answer-for-ai-research",
            "--unzip", "-p", "data/"
        ], check=True)
        original_csv = "data/medquad.csv"
        if os.path.exists(original_csv):
            os.rename(original_csv, medquad_path)
            print("Renamed medquad.csv to medquad_clean.csv")
        else:
            print("medquad.csv not found after download!")
    except Exception as e:
        print("Failed to download or rename MedQuAD:", e)
else:
    print("Found existing data/medquad_clean.csv. Skipping download.")

print("Project structure (and dataset) ready!")
