from textnode import TextNode, TextType

def main():
    text_type = TextType.LINK
    text_node = TextNode("This is some anchor text", text_type, "https://www.boot.dev")
    print(repr(text_node))

if __name__ == "__main__":
    main()