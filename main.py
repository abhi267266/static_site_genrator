import os
import shutil

from src.block_markdown import extract_title, markdown_to_html_node

def copy_directory(src, dst):
    """
    Recursively copies all contents from source directory to destination directory.
    Deletes destination directory contents before copying.
    
    Args:
        src: Source directory path
        dst: Destination directory path
    """
    # Delete destination directory if it exists
    if os.path.exists(dst):
        print(f"Deleting existing directory: {dst}")
        shutil.rmtree(dst)
    
    # Create the destination directory
    print(f"Creating directory: {dst}")
    os.mkdir(dst)
    
    # Recursively copy contents
    _copy_contents(src, dst)
    

def _copy_contents(src, dst):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        src: Source directory path
        dst: Destination directory path
    """
    # List all items in the source directory
    items = os.listdir(src)
    
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        
        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # Create subdirectory and recursively copy its contents
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_contents(src_path, dst_path)


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.

    Args:
        from_path (str): Path to the markdown file.
        template_path (str): Path to the HTML template file.
        dest_path (str): Path to save the generated HTML file.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read the markdown file
    with open(from_path, "r") as markdown_file:
        markdown_content = markdown_file.read()

    # Read the template file
    with open(template_path, "r") as template_file:
        template_content = template_file.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract the title
    title = extract_title(markdown_content)

    # Replace placeholders in the template
    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the generated HTML to the destination file
    with open(dest_path, "w") as dest_file:
        dest_file.write(full_html)

def generate_pages_recursive(content_dir, template_path, output_dir):
    """
    Process all markdown files in the content directory (including subdirectories),
    convert them to HTML using the template, and save them in the output directory.

    Args:
        content_dir (str): Path to the content directory containing markdown files.
        template_path (str): Path to the HTML template file.
        output_dir (str): Path to the output directory for generated HTML files.
    """
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                # Construct full paths
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, content_dir)
                dest_path = os.path.join(output_dir, relative_path.replace(".md", ".html"))

                # Generate the HTML page
                generate_page(from_path, template_path, dest_path)

# Example usage
if __name__ == "__main__":
    # delete all the files from public and Copy all the static files from static to public
    copy_directory("static", "public")
    print("\nCopy complete!")

    # Process all markdown files in the content directory
    generate_pages_recursive("content", "template.html", "public")
    print("\nAll pages generated successfully!")