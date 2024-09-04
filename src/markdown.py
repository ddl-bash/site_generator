from htmlnode import ParentNode
from textnode import text_node_to_html_node
from splitnodes import text_to_text_node

def markdown_to_blocks(document):
    lines = document.split("\n")
    blocks = []
    block = []

    for line in lines:
        if line.strip() == "":
            if block:
                blocks.append("\n".join(block))
                block = []
        else:
            block.append(line)

    if block:
        blocks.append("\n".join(block))

    return blocks

def block_to_block_type(block):
    lines = block.splitlines()

    if not lines:
        return "paragraph"

    # Check for code block
    if lines[0] == '```' and lines[-1] == '```':
        # Code blocks must have at least one line of code between the backticks
        if len(lines) > 2:
            return "code"
    
    # Check for heading
    if (
        lines[0].startswith("# ")
        or lines[0].startswith("## ")
        or lines[0].startswith("### ")
        or lines[0].startswith("#### ")
        or lines[0].startswith("##### ")
        or lines[0].startswith("###### ")
    ):
        # Ensure it's a heading by checking for the format
        if ' ' in lines[0]:
            return "heading"
    
    # Check for quote block
    if all(line.startswith('>') for line in lines):
        return "quote"

    # Check for unordered list
    if all(line.startswith(('* ', '- ')) for line in lines):
        return "ulist"

    # Check for ordered list
    if all(line[0].isdigit() and line[1] == '.' and line[2] == ' ' for line in lines):
        return "olist"

    # If none of the above, it's a paragraph
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_to_html_node(block)
    if block_type == "heading":
        return heading_to_html_node(block)
    if block_type == "code":
        return code_to_html_node(block)
    if block_type == "olist":
        return olist_to_html_node(block)
    if block_type == "ulist":
        return ulist_to_html_node(block)
    if block_type == "quote":
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_text_node(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('#') and not stripped_line.startswith('##'):
            return stripped_line[1:].strip()  # Remove the leading # and any trailing whitespace
    raise Exception("no title found")
