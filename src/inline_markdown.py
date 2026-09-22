import re
from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
        elif old_node.text_type == TextType.PLAIN_TEXT:
            node_split = old_node.text.split(delimiter)

            if len(node_split) % 2 == 0:
                raise Exception("invalid Markdown syntax")

            for i, n in enumerate(node_split):
                if i %2:
                    #odd case
                    new_node = TextNode(n, text_type)
                else:
                    #even case
                    new_node = TextNode(n, TextType.PLAIN_TEXT)
                new_nodes.append(new_node)
    return new_nodes


"""
When you split it on the backtick delimiter, you get:
["This is text with a ", "code block", " word"]
Look at what each piece represents:
Index 0: "This is text with a " → this was outside the backticks → regular text
Index 1: "code block" → this was inside the backticks → this is the special type (CODE, BOLD, etc.)
Index 2: " word" → this was outside the backticks again → regular text
"""

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
    

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
        if old_node.text_type == TextType.PLAIN_TEXT:
            image = extract_markdown_images(old_node.text)

            if not image:
                new_nodes.append(old_node)

            if image:
                original_text = old_node.text

                for link in image:
                    sections = original_text.split(f"![{link[0]}]({link[1]})", 1)
                    if len(sections) != 2: 
                        raise ValueError("Format not found")

                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

                    new_nodes.append(TextNode(link[0], TextType.IMAGES_TEXT, link[1]))
                    original_text = sections[1]

                if original_text != "":
                    new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
        if old_node.text_type == TextType.PLAIN_TEXT:
            links_node = extract_markdown_links(old_node.text)

            if not links_node:
                new_nodes.append(old_node)

            if links_node:
                original_text = old_node.text

                for link in links_node:
                    sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
                    if len(sections) != 2: 
                        raise ValueError("Format not found")

                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.PLAIN_TEXT))

                    new_nodes.append(TextNode(link[0], TextType.LINKS_TEXT, link[1]))
                    original_text = sections[1]

                if original_text != "":
                    new_nodes.append(TextNode(original_text, TextType.PLAIN_TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text,  TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    