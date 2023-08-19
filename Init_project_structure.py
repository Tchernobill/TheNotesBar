import os

base_path = "TheNotesBar"
folders = [
    "assets",
    "data",
    "views",
    "models",
    "viewmodels",
]

files = [
    ("views", ["main_bar.py", "main_bar_ui.py", "notes_manager.py", "notes_manager_ui.py", "settings.py", "settings_ui.py"]),
    ("models", ["notes_model.py", "settings_model.py"]),
    ("viewmodels", ["main_bar_viewmodel.py", "settings_viewmodel.py", "notes_manager_viewmodel.py"]),
    ("", ["main.py"])
]

# Create base directory
os.makedirs(base_path, exist_ok=True)

# Create folders
for folder in folders:
    os.makedirs(os.path.join(base_path, folder), exist_ok=True)

# Create files
for folder, file_list in files:
    for file in file_list:
        open(os.path.join(base_path, folder, file), 'a').close()

print("Project structure initialized.")