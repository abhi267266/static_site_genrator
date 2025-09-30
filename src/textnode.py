from enum import Enum
from src.htmlnode import LeafNode



class TextType(Enum):
    TEXT = "text"                     # plain text
    BOLD = "bold"            # **Bold text**
    ITALIC = "italic"                # _Italic text_
    CODE = "code"                 # `Code text`
    LINK = "link"       # [anchor text](url)
    IMAGE = "image"     # ![alt text](url)


class TextNode:
    def __init__(self, text, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (
            value.text == self.text 
            and value.text_type == self.text_type 
            and value.url == self.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value ="" , props={"alt": text_node.text, "src": text_node.url})
        case _:
            raise Exception("not valid")
