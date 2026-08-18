from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINKS_TEXT = "links" #revisar
    IMAGES_TEXT = "images" #revisar

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")

    

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if TextType.PLAIN_TEXT == text_node.text_type:
        return LeafNode(None, text_node.text, None)
    elif TextType.BOLD_TEXT == text_node.text_type:
        return LeafNode("b", text_node.text, None)
    elif TextType.ITALIC_TEXT == text_node.text_type:
        return LeafNode("i", text_node.text, None)
    elif TextType.CODE_TEXT == text_node.text_type:
        return LeafNode("code", text_node.text, None)
    elif TextType.LINKS_TEXT == text_node.text_type:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif TextType.IMAGES_TEXT == text_node.text_type:
        return LeafNode("img", "",  {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("invalid text type")
        