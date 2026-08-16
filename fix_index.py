import os
import glob

folder = '/Users/myeongjin/Documents/GitHub/projectCHnF-Portfolio'

# Rename landing.html to index.html
landing_path = os.path.join(folder, 'landing.html')
index_path = os.path.join(folder, 'index.html')
if os.path.exists(landing_path):
    os.rename(landing_path, index_path)

# Update links in all html files
files = glob.glob(f'{folder}/*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace href="landing.html" with href="index.html"
    if 'href="landing.html"' in content:
        content = content.replace('href="landing.html"', 'href="index.html"')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Fixed index.html and updated links.")
