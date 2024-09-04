import unittest

from markdown import *
from splitnodes import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = "# Main Heading\n\n## Subheading 1\n\nThis is the first paragraph.\n\nThis is the second paragraph.\n\n## Subheading 2\n\nThis is a final paragraph."
        result = markdown_to_blocks(text)
        self.assertEqual(result, [
            "# Main Heading",
            "## Subheading 1",
            "This is the first paragraph.",
            "This is the second paragraph.",
            "## Subheading 2",
            "This is a final paragraph.",
        ])

    def test_markdown_to_blocks_empty(self):
        text = ""
        result = markdown_to_blocks(text)
        self.assertEqual(result, [])

    def test_markdown_to_blocks_list(self):
        text = "* Item 1\n* Item 2\n* Item 3"
        result = markdown_to_blocks(text)
        self.assertEqual(result, [
            "* Item 1\n* Item 2\n* Item 3",
        ])

   
    def test_markdown_to_blocks_extra_blanks(self):
        text = "# Heading\n\n\nThis is a paragraph with extra blank lines.\n\n\nAnother paragraph."
        result = markdown_to_blocks(text)
        self.assertEqual(result, [
                "# Heading",
                "This is a paragraph with extra blank lines.",
                "Another paragraph.",
            ],)
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "ulist")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "olist")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_extract_title(self):
        md = "This is a line\n## this is h2\n#   This is a heading!\n## This is h2\nAnother line"
        self.assertEqual(extract_title(md), "This is a heading!")

    def test_extract_title_exception_raised(self):
        md = "This is a line\n## this is h2\n## This is h2\nAnother line"
        with self.assertRaises(Exception):
            extract_title(md)
            
if __name__ == "__main__":
    unittest.main()