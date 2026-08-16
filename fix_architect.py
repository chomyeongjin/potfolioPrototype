import os
import glob

folder = '/Users/myeongjin/Documents/GitHub/projectCHnF-Portfolio'

files = glob.glob(f'{folder}/*.html')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # works.html, project-detail.html
    if "const architect = acf.architecture || acf.archiecture" in content:
        content = content.replace(
            "const architect = acf.architecture || acf.archiecture || 'Unknown Architect';",
            "const architect = acf.architect || acf.archiect || acf.architecture || 'Unknown Architect';"
        )
        modified = True
        
    # index.html (landing)
    if "const architect = acf.architect || acf.architecture ||" in content:
        content = content.replace(
            "const architect = acf.architect || acf.architecture || '';",
            "const architect = acf.architect || acf.archiect || acf.architecture || '';"
        )
        modified = True
        
    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)

print("Architect field fixed in projectCHnF-Portfolio")
