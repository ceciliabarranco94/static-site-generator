import os
from markdown_blocks import markdown_to_html_node, extract_title
from pathlib import Path


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as file:
        content_from_path = file.read()

    with open(template_path) as file:
        content_template_path = file.read()

    html_string = markdown_to_html_node(content_from_path).to_html()
    title = extract_title(content_from_path)

    replace_placeholders = content_template_path.replace("{{ Title }}", title)
    replace_placeholders = replace_placeholders.replace("{{ Content }}", html_string)
    replace_placeholders = replace_placeholders.replace('href="/', 'href="' + basepath)
    replace_placeholders = replace_placeholders.replace('src="/', 'src="' + basepath)

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(replace_placeholders)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
     for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)

        if os.path.isfile(from_path):
            p = Path(dest_path)
            new_p = p.with_suffix(".html")
            generate_page(from_path, template_path, new_p, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


    
    


"""
for file in list_source:
            entry_full_path = os.path.join(source, file)
            destination_path = os.path.join(destination, file)
            if os.path.isfile(entry_full_path):
                shutil.copy(entry_full_path, destination_path)
            else:
                static_to_public(entry_full_path, destination_path)
"""