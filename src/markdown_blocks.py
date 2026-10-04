from enum import Enum
from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    U_LIST = "unordered_list" 
    O_LIST = "ordered_list" 


def markdown_to_blocks(markdown):
    mark_split = markdown.split("\n\n")

    strip_line = []

    for m in mark_split:
        to_strip = m.strip()
        if to_strip != "":
            strip_line.append(to_strip)

    return strip_line


def block_to_block_type(text):
    count_gato = 0
    lines = text.split("\n")

    for gato in text:
        if gato == "#":
            count_gato += 1
        else: 
            break

    if count_gato >= 1 and count_gato <= 6 and count_gato < len(text)  and text[count_gato] == " ":
        return BlockType.HEADING

    elif text.startswith("```\n") and text.endswith("```") and len(text) >= 8:
        return BlockType.CODE
    
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    elif all(line.startswith("- ") for line in lines):
        return  BlockType.U_LIST
    
    elif all(line.startswith(f"{l}. ") for l, line in enumerate(lines, start=1)):
        return BlockType.O_LIST
    
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for t in text_nodes:
        html_node = text_node_to_html_node(t)
        children.append(html_node)

    return children


#helper function for the heading
def heading_to_html_node(block):
    heading_level = 0
    for header in block:
        if header == "#":
            heading_level += 1
        else: 
            break

    head_string = f"h{heading_level}"
    sliced_text = block[heading_level + 1:]
    heading_ch = text_to_children(sliced_text)

    return HTMLNode(head_string, None, heading_ch)


#helper function for code
def code_to_html_node(block):
    raw_code = block[4:-3]
    plain_code = TextNode(raw_code, TextType.PLAIN_TEXT)
    node_code = text_node_to_html_node(plain_code)

    code_ch = HTMLNode("code", None, [node_code])
    pre_ch = HTMLNode("pre", None, [code_ch])

    return pre_ch

        

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    outer_children =[]
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            outer_children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            outer_children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            outer_children.append(HTMLNode(data))
        elif block_type == BlockType.U_LIST:
            outer_children.append(HTMLNode(data))
        elif block_type == BlockType.O_LIST:
            outer_children.append(HTMLNode(data))
        else:
            paragraph_text = block.replace("\n", " ")
            paragraph_ch = text_to_children(paragraph_text)
            outer_children.append(HTMLNode("p", None, paragraph_ch))