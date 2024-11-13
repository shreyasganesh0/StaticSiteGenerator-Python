import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)


    def test_eq_url(self):
        node = TextNode("text", TextType.BOLD,"https://myurl")
        node2 = TextNode("text", TextType.BOLD, "https://myurl")
        self.assertEqual(node, node2)

    def test_eq_type(self):
        node = TextNode("text", TextType.ITALIC, "https://myurl")
        node2 = TextNode("text", TextType.ITALIC, "https://myurl")
        self.assertEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("text", TextType.BOLD, None)
        node2 = TextNode("text", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_bold(self):
        node = TextNode("value_bold", TextType.BOLD)
        nodeleaf  = LeafNode("b", "value_bold")
        self.assertEqual(node.text_node_to_html(), nodeleaf)
    def test_itlaic(self):
        node = TextNode("value_italic", TextType.ITALIC)
        nodeleaf  = LeafNode("i", "value_italic")
        self.assertEqual(node.text_node_to_html(), nodeleaf)
        
    def test_normal(self):
        node = TextNode("value_normal", TextType.NORMAL)
        nodeleaf  = LeafNode(None, "value_normal")
        self.assertEqual(node.text_node_to_html(), nodeleaf)
    def test_code(self):
        node = TextNode("value_code", TextType.CODE)
        nodeleaf  = LeafNode("code", "value_code")
        self.assertEqual(node.text_node_to_html(), nodeleaf)
    def test_link(self):
        node = TextNode("value_link", TextType.LINK, "https://mylink")
        nodeleaf  = LeafNode("a", "value_link", {"href":"https://mylink"})
        self.assertEqual(node.text_node_to_html(), nodeleaf)
    def test_img(self):
        node = TextNode("my image", TextType.IMAGE, "/usr/myimg")
        nodeleaf  = LeafNode("img", "", {"src":"/usr/myimg", "alt":"my image"})
        self.assertEqual(node.text_node_to_html(), nodeleaf)
    def test_fail(self):
        node = TextNode("my image","not a type" , "/usr/myimg")
        self.assertRaises(TypeError,TextNode.text_node_to_html,node)
        
if __name__ == "__main__":
    unittest.main()
