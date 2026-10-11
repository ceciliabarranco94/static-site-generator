from textnode import TextNode, TextType
from copystatic import static_to_public


print("hello world")


def main():
    result = TextNode("dummy1", TextType.BOLD_TEXT, "dummy3")
    print(result)
    static_to_public("static","public")


main()


