import os
from pathlib import Path

list_of_files = [
    "app/__init__.py",
    "app/main.py",
    "app/scraper.py",
    "app/embeddings.py",
    "app/vector_store.py",
    "app/recommender.py",
    "app/utils.py",
    "data/.gitkeep",
    "models/.gitkeep",
    "requirements.txt",
    "README.md",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")