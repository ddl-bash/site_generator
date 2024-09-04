import unittest

from textnode import TextNode
from splitnodes import *

class TestSplitNodesDelimiter(unittest.TestCase): 
    def test_basic_split(self):
        node = TextNode("Hello `world`", 'text')
        expected = [
            TextNode("Hello ", 'text'),
            TextNode("world", 'code')
        ]
        result = split_nodes_delimiter([node], "`", 'code')
        self.assertEqual(result, expected)

    def test_basic_split_delimiter_first(self):
        node = TextNode("`Hello` world", 'text')
        expected = [
            TextNode("Hello", 'code'),
            TextNode(" world", 'text')
        ]
        result = split_nodes_delimiter([node], "`", 'code')
        self.assertEqual(result, expected)
    
    def test_no_delimiter(self):
        node = TextNode("Hello world", 'text')
        expected = [TextNode("Hello world", 'text')]
        result = split_nodes_delimiter([node], "`", 'code')
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode("Hello `first` and `second`", 'text')
        expected = [
            TextNode("Hello ", 'text'),
            TextNode("first", 'code'),
            TextNode(" and ", 'text'),
            TextNode("second", 'code')
        ]
        result = split_nodes_delimiter([node], "`", 'code')
        self.assertEqual(result, expected)
    
    def test_multiple_nodes(self):
        nodes = [
            TextNode("Hello ", 'text'),
            TextNode("world", 'code'),
            TextNode("! ", 'text'),
            TextNode("Another `example`", 'text')
        ]
        expected = [
            TextNode("Hello ", 'text'),
            TextNode("world", 'code'),
            TextNode("! ", 'text'),
            TextNode("Another ", 'text'),
            TextNode("example", 'code')
        ]
        result = split_nodes_delimiter(nodes, "`", 'code')
        self.assertEqual(result, expected)

    def test_empty_string(self):
        node = TextNode("", 'text')
        expected = []
        result = split_nodes_delimiter([node], "`", 'code')
        self.assertEqual(result, expected)
    
    def test_delimiter_at_edges(self):
        node = TextNode("`start` middle `end`", 'text')
        expected = [
            TextNode("start", 'code'),
            TextNode(" middle ", 'text'),
            TextNode("end", 'code')
        ]
        result = split_nodes_delimiter([node], "`", 'code')
        self.assertEqual(result, expected)
    
    def test_basic_split_bold(self):
        node = TextNode("Hello **world**", 'text')
        expected = [
            TextNode("Hello ", 'text'),
            TextNode("world", 'bold')
        ]
        result = split_nodes_delimiter([node], "**", 'bold')
        self.assertEqual(result, expected)

    def test_basic_split_italic(self):
        node = TextNode("*Hello* ", 'text')
        expected = [
            TextNode("Hello", 'italic'),
            TextNode(" ", 'text')
        ]
        result = split_nodes_delimiter([node], "*", 'italic')
        self.assertEqual(result, expected)

    def test_no_delimiter_bold(self):
        node = TextNode("Hello world", 'text')
        expected = [TextNode("Hello world", 'text')]
        result = split_nodes_delimiter([node], "**", 'bold')
        self.assertEqual(result, expected)

    def test_no_delimiter_italic(self):
        node = TextNode("Hello world", 'text')
        expected = [TextNode("Hello world", 'text')]
        result = split_nodes_delimiter([node], "*", 'italic')
        self.assertEqual(result, expected)

    def test_multiple_delimiters_bold(self):
        node = TextNode("**Hello** **world**", 'text')
        expected = [
            TextNode("Hello", 'bold'),
            TextNode(" ", 'text'),
            TextNode("world", 'bold')
        ]
        result = split_nodes_delimiter([node], "**", 'bold')
        self.assertEqual(result, expected)

    def test_multiple_delimiters_italic(self):
        node = TextNode("*Hello* *world*", 'text')
        expected = [
            TextNode("Hello", 'italic'),
            TextNode(" ", 'text'),
            TextNode("world", 'italic')
        ]
        result = split_nodes_delimiter([node], "*", 'italic')
        self.assertEqual(result, expected)

class TestSplitNodesImage(unittest.TestCase):
    
    def test_single_image(self):
        nodes = [TextNode("Look at this ![alt](link).", 'text')]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [
            TextNode("Look at this ", 'text'),
            TextNode("alt", 'image', "link"),
            TextNode(".", 'text')
        ])

    def test_multiple_images(self):
        nodes = [TextNode("Here is ![image1](link1) and ![image2](link2).", 'text')]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [
            TextNode("Here is ", 'text'),
            TextNode("image1", 'image', "link1"),
            TextNode(" and ", 'text'),
            TextNode("image2", 'image', "link2"),
            TextNode(".", 'text')
        ])

    def test_no_images(self):
        nodes = [TextNode("Just plain text.", 'text')]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [
            TextNode("Just plain text.", 'text')
        ])

    def test_empty_text(self):
        nodes = [TextNode("", 'text')]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [])

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        nodes = [TextNode("Visit [Boot Dev](https://boot.dev) now.", 'text')]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [
            TextNode("Visit ", 'text'),
            TextNode("Boot Dev", 'link', "https://boot.dev"),
            TextNode(" now.", 'text')
        ])

    def test_multiple_links(self):
        nodes = [TextNode("Here are [Google](https://google.com) and [YouTube](https://youtube.com).", 'text')]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [
            TextNode("Here are ", 'text'),
            TextNode("Google", 'link', "https://google.com"),
            TextNode(" and ", 'text'),
            TextNode("YouTube", 'link', "https://youtube.com"),
            TextNode(".", 'text')
        ])

    def test_no_links(self):
        nodes = [TextNode("Plain text with no links.", 'text')]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [
            TextNode("Plain text with no links.", 'text')
        ])

    def test_empty_text(self):
        nodes = [TextNode("", 'text')]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [])

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_text_node(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_text_node(text)
        self.assertEqual(result, [
            TextNode("This is ", 'text'),
            TextNode("text", 'bold'),
            TextNode(" with an ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(" word and a ", 'text'),
            TextNode("code block", 'code'),
            TextNode(" and an ", 'text'),
            TextNode("obi wan image", 'image', "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", 'text'),
            TextNode("link", 'link', "https://boot.dev"),
        ])

if __name__ == "__main__":
    unittest.main()