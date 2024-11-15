import re
from textnode import TextType, TextNode


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
