from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html(self):
        match(self.text_type):
            case TextType.NORMAL:
                leaf = LeafNode(None, self.text)
            case TextType.BOLD:
                leaf = LeafNode("b", self.text)
            case TextType.ITALIC:
                leaf = LeafNode("i", self.text)
            case TextType.CODE:
                leaf = LeafNode("code", self.text)

            case TextType.LINK:
                leaf = LeafNode("a", self.text,{"href":self.url})

            case TextType.IMAGE:
                leaf = LeafNode("img","",{"src":self.url, "alt":self.text})
            case _:
                raise TypeError("Not a valid type")
        return leaf

    def __eq__(self, obj):
        return self.text == obj.text and self.text_type == obj.text_type and self.url == obj.url
    
    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type}, {self.url})")
