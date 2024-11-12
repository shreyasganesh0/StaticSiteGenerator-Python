from htmlnode import HTMLNode, LeafNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            'class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(tag = p, value = What a strange world, children = None, props = {'class': 'primary'})",
        )

    def test_case_dt(self):
        childlist = [HTMLNode(None,"child b"),HTMLNode(None,"child b")]
        node = HTMLNode("a", "inside a", childlist, {"testval":"testprop"})
        self.assertEqual(node.props_to_html(),f'''testval="testprop"''') 

    def test_case_none(self):
        node =  HTMLNode("a", "inside a",None )
        
        self.assertEqual(node.props_to_html(),"") 
        
    def test_case_two_val(self):
        node =  HTMLNode("a", "inside a",None ,{"testval1":"test", "testval2":"test"})
        
        self.assertEqual(node.props_to_html(),f'''testval1="test" testval2="test"''') 
    
    def test_case_hflag(self):
        node = LeafNode("p", "inside a", {"testval1":"test", "testval2":"test"})
        self.assertEqual(node.to_html(), f'''<p testval1="test" testval2="test">inside a</p>''')
    
    def test_case_no_value_leaf(self):
        node = LeafNode("p", None, {"testval1":"test", "testval2":"test"})
        self.assertRaises(ValueError,LeafNode.to_html,node)
    
    def test_case_no_tag_leaf(self):
        node = LeafNode(None, "inside a", {"testval1":"test", "testval2":"test"})
        self.assertEqual(node.to_html(),"inside a")
if __name__ == "__main__":
    unittest.main()
