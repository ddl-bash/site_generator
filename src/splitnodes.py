from textnode import TextNode
from extract import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != 'text':
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], 'text'))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != 'text':
            new_nodes.append(old_node)
            continue
        text = old_node.text
        markdowns = extract_markdown_images(text)
        for markdown in markdowns:
            string = f"![{markdown[0]}]({markdown[1]})"    
            parts = text.split(string,1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if parts[0]:
                new_nodes.append(TextNode(parts[0], 'text'))
            new_nodes.append(TextNode(markdown[0], 'image', markdown[1]))
            text = parts[1]
        if text:
            new_nodes.append(TextNode(text, 'text'))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != 'text':
            new_nodes.append(old_node)
            continue
        text = old_node.text
        markdowns = extract_markdown_links(text)
        for markdown in markdowns:
            string = f"[{markdown[0]}]({markdown[1]})"     
            parts = text.split(string,1)
            if len(parts) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if parts[0]:
                new_nodes.append(TextNode(parts[0], 'text'))
            new_nodes.append(TextNode(markdown[0], 'link', markdown[1]))
            text = parts[1]
        if text:
            new_nodes.append(TextNode(text, 'text'))
    return new_nodes

def text_to_text_node(text):
    if not text:
        return []
    nodes = split_nodes_delimiter([TextNode(text, 'text')], '**', 'bold')
    nodes = split_nodes_delimiter(nodes, '*', 'italic')
    nodes = split_nodes_delimiter(nodes, '`', 'code')
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

