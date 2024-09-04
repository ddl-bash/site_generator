import unittest

from extract import *

class TestExtract(unittest.TestCase):    
    def test_extract_markdown_images(self):
        text = "Here is an image ![alt text](http://example.com/image.png) and another ![second](http://example.com/second.png)."
        expected = [("alt text", "http://example.com/image.png"), ("second", "http://example.com/second.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_empty(self):
        text = "No images here!"
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links(self):
        text = "Here is a link [example](http://example.com) and another [example2](http://example.org). !![not a link](http://example.net)."
        expected = [("example", "http://example.com"), ("example2", "http://example.org")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_empty(self):
        text = "No links here!"
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()