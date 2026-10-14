from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
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

    return ParentNode(head_string, heading_ch)


#helper function for code
def code_to_html_node(block):
    raw_code = block[4:-3]
    plain_code = TextNode(raw_code, TextType.PLAIN_TEXT)
    node_code = text_node_to_html_node(plain_code)

    code_ch = ParentNode("code", [node_code])
    pre_ch = ParentNode("pre", [code_ch])

    return pre_ch


#helper fucntion for quotes
def quote_to_html_node(block):
    quote_line = block.split("\n")
    clean_quote = []

    for line in quote_line:
        clean_quote.append(line.lstrip(">").strip())

    joined_text = " " .join(clean_quote)
    node_quote = text_to_children(joined_text)
    quote_ch = ParentNode("blockquote", node_quote)

    return quote_ch


#helper fucntion for unordered_list
def un_list_to_html_node(block):
    un_list = block.split("\n")
    clean_list = []

    for line in un_list:
        list_strip = (line.lstrip("- "))
        node_ulist = text_to_children(list_strip)
        ulist_ch = ParentNode("li", node_ulist)
        clean_list.append(ulist_ch)
    wrap_ulist = ParentNode("ul", clean_list)

    return wrap_ulist


#helper fucntion for ordered_list
def or_list_to_html_node(block):
    or_list = block.split("\n")
    clean_list = []

    for line in or_list:
        list_strip = (line.split(". ", 1))
        node_olist = text_to_children(list_strip[1])
        olist_ch = ParentNode("li", node_olist)
        clean_list.append(olist_ch)
    wrap_olist = ParentNode("ol", clean_list)

    return wrap_olist
        

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
            outer_children.append(quote_to_html_node(block))
        elif block_type == BlockType.U_LIST:
            outer_children.append(un_list_to_html_node(block))
        elif block_type == BlockType.O_LIST:
            outer_children.append(or_list_to_html_node(block))
        else:
            paragraph_text = block.replace("\n", " ")
            paragraph_ch = text_to_children(paragraph_text)
            outer_children.append(ParentNode("p", paragraph_ch))

    return ParentNode("div",  outer_children)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            line_strip = line[2:]
            return line_strip.strip()
    raise Exception("No heading found")