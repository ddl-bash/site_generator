from htmlnode import LeafNode

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text is None:
        raise Exception("text_node missing text")
    if not text_node.text_type:
        raise Exception(f"text_node missing text_type ({text_node.text_type})")

    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)   
        case "link":
            if not text_node.url:
                raise Exception(f"link text_node missing url, provided ({text_node.url})")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            if not text_node.url:
                raise Exception(f"image text_node missing url, provided ({text_node.url})")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})      
        case _:
            raise Exception(f"invalid text_type: {text_node.text_type}")