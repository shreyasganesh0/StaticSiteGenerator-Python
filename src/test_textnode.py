import unittest

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
if __name__ == "__main__":
    unittest.main()
