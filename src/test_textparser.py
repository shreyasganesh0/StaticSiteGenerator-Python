import unittest

from textparser import RawTextParser, BlockHandler, BlockType 


from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        parser_obj = RawTextParser()
        node = TextNode("This is text with a **bolded** word", TextType.NORMAL)
        new_nodes = parser_obj.text_node_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        parser_obj = RawTextParser()
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.NORMAL
        )
        new_nodes = parser_obj.text_node_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        parser_obj = RawTextParser()
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.NORMAL
        )
        new_nodes = parser_obj.text_node_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        parser_obj = RawTextParser()
        node = TextNode("This is text with an *italic* word", TextType.NORMAL)
        new_nodes = parser_obj.text_node_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        parser_obj = RawTextParser()
        node = TextNode("**bold** and *italic*", TextType.NORMAL)
        new_nodes = parser_obj.text_node_delimiter([node], "**", TextType.BOLD)
        new_nodes = parser_obj.text_node_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        parser_obj = RawTextParser()
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = parser_obj.text_node_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.NORMAL),
            ],
            new_nodes,
        )
    def test_extract_markdown_images(self):
        parser_obj = RawTextParser()
        matches = parser_obj.extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        parser_obj = RawTextParser()
        matches = parser_obj.extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,)
    def test_split_image(self):
        parser_obj = RawTextParser()
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        new_nodes = parser_obj.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        parser_obj = RawTextParser()
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
        new_nodes = parser_obj.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        parser_obj = RawTextParser()
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = parser_obj.split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        parser_obj = RawTextParser()
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.NORMAL,
        )
        new_nodes = parser_obj.split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        parser_obj = RawTextParser()
        nodes =parser_obj.text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        block_obj = BlockHandler()
        blocks = block_obj.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        block_obj = BlockHandler()
        blocks = block_obj.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
    def test_block_to_block_types(self):
        block_obj = BlockHandler()
        block = "# heading"
        self.assertEqual(block_obj.block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_obj.block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_obj.block_to_block_type(block), BlockType.QOUTE)
        block = "* list\n* items"
        self.assertEqual(block_obj.block_to_block_type(block), BlockType.LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_obj.block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_obj.block_to_block_type(block),BlockType.PARA )
    def test_paragraph(self):
        blockobj = BlockHandler()
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = blockobj.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        blockobj = BlockHandler()
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = blockobj.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        blockobj = BlockHandler()
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = blockobj.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        blockobj = BlockHandler()
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = blockobj.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        blockobj = BlockHandler()
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = blockobj.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )
if __name__ == "__main__":
    unittest.main()
