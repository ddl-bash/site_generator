import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_html_node_creation(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_html_node_with_children(self):
        child1 = HTMLNode("span", "Child 1")
        child2 = HTMLNode("em", "Child 2")
        parent = HTMLNode("div", children=[child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "Child 1")
        self.assertEqual(parent.children[1].tag, "em")

    def test_html_node_with_props(self):
        node = HTMLNode("a", "Click me", props={"href": "https://example.com", "class": "link"})
        self.assertEqual(node.props["href"], "https://example.com")
        self.assertEqual(node.props["class"], "link")

    def test_props_to_html_method(self):
        node = HTMLNode("p", "Test", props={"class": "text"})
        expected_html = ' class="text"'
        self.assertEqual(node.props_to_html(), expected_html)

    def test_props_to_html_with_no_props(self):
        child = HTMLNode("strong", "Bold")
        parent = HTMLNode("p", children=[child])
        expected_html = ''
        self.assertEqual(parent.props_to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()