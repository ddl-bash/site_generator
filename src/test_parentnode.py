import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):

    def test_parent_node_creation(self):
        child = LeafNode("p", "Hello")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.tag, "div")
        self.assertEqual(len(parent.children), 1)
        self.assertIsInstance(parent.children[0], LeafNode)
        self.assertEqual(parent.children[0].tag, "p")
        self.assertEqual(parent.children[0].value, "Hello")

    def test_to_html_with_no_children(self):    
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()
        
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_node_with_children(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "Paragraph 1")
        self.assertEqual(parent.children[1].value, "Paragraph 2")

    def test_parent_node_to_html(self):
        child = LeafNode("span", "Hello")
        parent = ParentNode("div", [child])
        expected_html = "<div><span>Hello</span></div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_nested_parent_nodes(self):
        inner_child = LeafNode("em", "Emphasized")
        inner_parent = ParentNode("p", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        expected_html = "<div><p><em>Emphasized</em></p></div>"
        self.assertEqual(outer_parent.to_html(), expected_html)

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        child3 = LeafNode("span", "Some span content")
        parent = ParentNode("div", [child1, child2, child3])
        self.assertEqual(parent.tag, "div")
        self.assertEqual(len(parent.children), 3)
        self.assertEqual(parent.children[0].value, "First paragraph")
        self.assertEqual(parent.children[1].value, "Second paragraph")
        self.assertEqual(parent.children[2].value, "Some span content")
    
    def test_parent_node_with_props(self):
        child = LeafNode("span", "Content")
        parent = ParentNode("div", [child], {"class": "container"})
        expected_html = '<div class="container"><span>Content</span></div>'
        self.assertEqual(parent.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()