import re
from textnode import TextType, TextNode


class RawTextParser:

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

    def extract_markdown_images(self,text):
        pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(pattern, text)
        return matches


    def extract_markdown_links(self, text):
        pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(pattern, text)
        return matches
                        

