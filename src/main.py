import sys
from textnode import TextNode, TextType
from copystatic import static_to_public
from gencontent import generate_page, generate_pages_recursive

#print(sys.argv)

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    static_to_public("static","docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()