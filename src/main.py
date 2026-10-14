from textnode import TextNode, TextType
from copystatic import static_to_public
from gencontent import generate_page, generate_pages_recursive


print("hello world")


def main():
    result = TextNode("dummy1", TextType.BOLD_TEXT, "dummy3")
    print(result)
    static_to_public("static","public")
    #generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


main()


