class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("must inherit to html class")

    def props_to_html(self):
        if self.props is None:
            return ""
        ans_str =""
        for tag in self.props:
            ans_str += f"{tag}=\"{self.props[tag]}\" "
        return ans_str[:-1]
    
    def __repr__(self):
        return(f"HTMLNode(tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})")
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props):
        super().__init__(tag, value, None, props)

    def to_html(self):
        
        resp = ""
        if self.value == None:

            raise ValueError("leaf has no value")

        if self.tag == None:
            resp = f"{self.value}"
        
        else:
            resp = f"<{self.tag} {super().props_to_html()}>{self.value}</{self.tag}>"
        return resp



