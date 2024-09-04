import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leaf_node_creation(self):
        node = LeafNode("span", "Hello")
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, None)

    def test_leaf_node_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertEqual(node.props["href"], "https://example.com")

    def test_leaf_node_to_html(self):
        node = LeafNode("em", "Emphasized")
        expected_html = "<em>Emphasized</em>"
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_node_to_html_with_props(self):
        node = LeafNode("a", "image link", {"href": "image.jpg"})
        expected_html = '<a href="image.jpg">image link</a>'
        self.assertEqual(node.to_html(), expected_html)

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

if __name__ == "__main__":
    unittest.main()