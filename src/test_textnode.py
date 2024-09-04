import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_text_node_creation(self):
        node = TextNode("Hello", "text")
        self.assertEqual(node.text, "Hello")
        self.assertEqual(node.text_type, "text")
        self.assertIsNone(node.url)

    def test_text_node_with_url(self):
        node = TextNode("Click here", "link", "https://example.com")
        self.assertEqual(node.text, "Click here")
        self.assertEqual(node.text_type, "link")
        self.assertEqual(node.url, "https://example.com")

    def test_eq_method(self):
        node1 = TextNode("Same", "text")
        node2 = TextNode("Same", "text")
        node3 = TextNode("Different", "text")
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_str_representation(self):
        node = TextNode("Test", "bold")
        expected_str = "TextNode(Test, bold, None)"
        self.assertEqual(str(node), expected_str)

class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text_node(self):
        text_node = TextNode("Hello, world!", "text")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello, world!")

    def test_bold_node(self):
        text_node = TextNode("Bold text", "bold")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_link_node(self):
        text_node = TextNode("Click me", "link", "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
    
    def test_image(self):
        node = TextNode("This is an image", "image", "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image"},)
        
    def test_invalid_type(self):
        text_node = TextNode("Invalid type", "invalid")
        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()