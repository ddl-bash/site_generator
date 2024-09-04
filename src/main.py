import os
import shutil
from markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path) and os.path.exists(template_path):
        with open(from_path, 'r') as file:
            file_content = file.read()
        with open(template_path, 'r') as template:
            template_content = template.read()
        
        title = extract_title(file_content)
        content = markdown_to_html_node(file_content).to_html()
        
        template_content = template_content.replace('{{ Title }}', title)
        template_content = template_content.replace('{{ Content }}', content)

        directory_path = os.path.dirname(dest_path)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        with open(dest_path, 'w') as file:
            file.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + '.html')
                generate_page(from_path, template_path, dest_path)

def clear_directory(directory_path):
    """Delete all contents of the given directory."""
    for root, dirs, files in os.walk(directory_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        for name in dirs:
            dir_path = os.path.join(root, name)
            os.rmdir(dir_path)
            print(f"Deleted directory: {dir_path}")

def copy_directory(src, dst):
    """Recursively copy contents from src directory to dst directory."""
    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"Created directory: {dst}")

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        
        if os.path.isdir(s):
            # Recursively copy subdirectories
            copy_directory(s, d)
        else:
            # Copy files
            shutil.copy2(s, d)
            print(f"Copied file: {s} to {d}")

def main():
    source_dir = 'static/'
    destination_dir = 'public/'

    RUN_FILES = True
     
    if RUN_FILES:
        # Ensure destination directory exists
        if os.path.exists(destination_dir):
            # Clear the destination directory
            clear_directory(destination_dir)
        else:
            os.makedirs(destination_dir)
            print(f"Created destination directory: {destination_dir}")

        # Copy contents from source to destination
        copy_directory(source_dir, destination_dir)

        generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()