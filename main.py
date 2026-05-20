import os
import sys
import shutil
import re
from  src.helpers import markdown_to_html_node, text_node_to_html_node, text_to_textnodes

"""
    Write a recursive function that copies all the contents from a source directory to a destination directory (in our case, static to public)
    It should first delete all the contents of the destination directory (public) to ensure that the copy is clean.
    It should copy all files and subdirectories, nested files, etc.
    I recommend logging the path of each file you copy, so you can see what's happening as you run and debug your code.
    os.path.exists, os.listdir, os.path.join, os.path.isfile, os.mkdir, shutil.copy, shutil.rmtree
"""

def copy_dir_recursive(src, dst):
    # Delete destination directory if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)

    # Recreate destination directory
    os.mkdir(dst)

    # Iterate through all items in source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)

        else:
            print(f"Entering directory: {src_path}")
            copy_dir_recursive(src_path, dst_path)
    

"""
    Generate Page
"""
def extract_title(markdown):
    # pull h1 header from the markdown file (line that starts with a single #) and return it.
    for line in markdown.split('\n'):
        if re.findall(r'\#{1}', line):
            return line.strip().strip('#')
    raise Exception('No h1 title found...')


"""

"""
def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    # markdown file
    with open(from_path, "r") as file:
        markdown = file.read()
    
    # template file
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    # convert markdown file to an HTML string
    html = markdown_to_html_node(markdown).to_html()
    
    # extract title 
    title = extract_title(markdown=markdown)
    
    # replaece {{ Title }} and {{ Content }} in template
    page_content = template_content.replace(r'{{ Title }}', title)
    page_content = page_content.replace(r'{{ Content }}', html)
    
    # repalce any instances of href="/ with href={basepath}
    # replace any instances of src="/ with src={basepath}
    page_content = page_content.replace(r'href="/', f'href="{basepath}')
    page_content = page_content.replace(r'src="/', f'src="{basepath}')
    
    # write new full HTML page to a file at dest_path
    with open(dest_path, 'w') as file:
        file.write(page_content)
    
"""

"""    
def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        # Recurse into subdirectories
        if os.path.isdir(from_path):
            os.mkdir(dest_path)

            generate_pages_recursively(
                from_path,
                template_path,
                dest_path,
                basepath
            )

        # Generate HTML pages from markdown files
        elif entry.endswith(".md"):
            dest_file = dest_path.replace(".md", ".html")

            generate_page(
                from_path,
                template_path,
                dest_file,
                basepath
            )
    
    
    # generate_page(from_path, template_path, dest_path)



""" Main application driver """
if __name__ == "__main__":
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    copy_dir_recursive('static', 'docs')
    generate_pages_recursively('content', 'template.html', 'docs', basepath)
#    markdown= """
#     - You can spend years studying the legendarium and still not understand its depths
#     - It can be enjoyed by children and adults alike
#     - Disney _didn't ruin it_ (okay, but Amazon might have)
#     - It created an entirely new genre of fantasy
#     """
#    text_nodes = text_to_textnodes(markdown)
#    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
#    html = html_nodes.to_html()
    