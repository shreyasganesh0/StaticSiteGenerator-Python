import re
from textnode import TextType, TextNode
from enum import Enum
from htmlnode import ParentNode

class BlockType(Enum):
    PARA = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QOUTE = "quote"
    OLIST = "ordered_list"
    LIST = "unordered_list"

class RawTextParser:
    def text_to_textnodes(self, text):
        nodes = [TextNode(text, TextType.NORMAL)]
        nodes = self.text_node_delimiter(nodes,"**", TextType.BOLD)
        nodes = self.text_node_delimiter(nodes, "*", TextType.ITALIC)
        nodes = self.text_node_delimiter(nodes, "`", TextType.CODE)
        nodes = self.split_nodes_image(nodes)
        nodes = self.split_nodes_link(nodes)
        return nodes

    def text_node_delimiter(self, old_nodes, delimiter, text_type):
        """
        Function takes a list of TextNodes and a delimiter that may be contained
        in the text block of each node. It splits the node in a group of TextNodes
        of respective type and returns a list of corrected TextNodes
        """
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.NORMAL:
                new_nodes.append(old_node)
                continue
            split_nodes = []
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.NORMAL))
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
        return new_nodes

    def split_nodes_image(self, old_nodes):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.NORMAL:
                new_nodes.append(old_node)
                continue
            original_text = old_node.text
            images = self.extract_markdown_images(original_text)
            if len(images) == 0:
                new_nodes.append(old_node)
                continue
            for image in images:
                sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, image section not closed")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                new_nodes.append(
                    TextNode(
                        image[0],
                        TextType.IMAGE,
                        image[1],
                    )
                )
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.NORMAL))
        return new_nodes


    def split_nodes_link(self, old_nodes):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.NORMAL:
                new_nodes.append(old_node)
                continue
            original_text = old_node.text
            links = self.extract_markdown_links(original_text)
            if len(links) == 0:
                new_nodes.append(old_node)
                continue
            for link in links:
                sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
                if len(sections) != 2:
                    raise ValueError("Invalid markdown, link section not closed")
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                original_text = sections[1]
            if original_text != "":
                new_nodes.append(TextNode(original_text, TextType.NORMAL))
        return new_nodes
    def extract_markdown_images(self,text):
        pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(pattern, text)
        return matches


    def extract_markdown_links(self, text):
        pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(pattern, text)
        return matches
                        
class BlockHandler:
    def markdown_to_blocks(self, markdown):
        block_delimiter = "\n\n"
        markdownlist = markdown.split(block_delimiter)
        anslist =[]
        for block in markdownlist:
            if block == "":
                continue
            anslist.append(block.strip())
        return anslist

    def block_to_block_type(self,block):
        lines = block.split("\n")

        if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
        if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
            return BlockType.CODE 
        if block.startswith(">"):
            for line in lines:
                if not line.startswith(">"):
                    return BlockType.PARA
            return BlockType.QOUTE
        if block.startswith("* "):
            for line in lines:
                if not line.startswith("* "):
                    return BlockType.PARA
            return BlockType.LIST
        if block.startswith("- "):
            for line in lines:
                if not line.startswith("- "):
                    return BlockType.PARA
                return BlockType.LIST
        if block.startswith("1. "):
            i = 1
            for line in lines:
                if not line.startswith(f"{i}. "):
                    return BlockType.PARA
                i += 1
            return BlockType.OLIST
        return BlockType.PARA

    def markdown_to_html_node(self,markdown):
        blocks = self.markdown_to_blocks(markdown)
        children = []
        for block in blocks:
            html_node = self.block_to_html_node(block)
            children.append(html_node)
        return ParentNode("div", children, None)


    def block_to_html_node(self,block):
        block_type = self.block_to_block_type(block)
        if block_type == BlockType.PARA:
            return self.paragraph_to_html_node(block)
        if block_type == BlockType.HEADING:
            return self.heading_to_html_node(block)
        if block_type == BlockType.CODE:
            return self.code_to_html_node(block)
        if block_type == BlockType.OLIST:
            return self.olist_to_html_node(block)
        if block_type == BlockType.LIST:
            return self.ulist_to_html_node(block)
        if block_type == BlockType.QOUTE:
            return self.quote_to_html_node(block)
        raise ValueError("Invalid block type")


    def text_to_children(self,text):
        text_obj = RawTextParser()
        text_nodes = text_obj.text_to_textnodes(text)

        children = []
        for text_node in text_nodes:
            textnodeobj= TextNode(text_node.text, text_node.text_type,text_node.url)
            html_node = textnodeobj.text_node_to_html()
            children.append(html_node)
        return children


    def paragraph_to_html_node(self,block):
        lines = block.split("\n")
        paragraph = " ".join(lines)
        children = self.text_to_children(paragraph)
        return ParentNode("p", children)


    def heading_to_html_node(self, block):
        level = 0
        for char in block:
            if char == "#":
                level += 1
            else:
                break
        if level + 1 >= len(block):
            raise ValueError(f"Invalid heading level: {level}")
        text = block[level + 1 :]
        children = self.text_to_children(text)
        return ParentNode(f"h{level}", children)


    def code_to_html_node(self,block):
        if not block.startswith("```") or not block.endswith("```"):
            raise ValueError("Invalid code block")
        text = block[4:-3]
        children = self.text_to_children(text)
        code = ParentNode("code", children)
        return ParentNode("pre", [code])


    def olist_to_html_node(self,block):
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[3:]
            children = self.text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ol", html_items)


    def ulist_to_html_node(self,block):
        items = block.split("\n")
        html_items = []
        for item in items:
            text = item[2:]
            children = self.text_to_children(text)
            html_items.append(ParentNode("li", children))
        return ParentNode("ul", html_items)


    def quote_to_html_node(self, block):
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            if not line.startswith(">"):
                raise ValueError("Invalid quote block")
            new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = self.text_to_children(content)
        return ParentNode("blockquote", children)
