from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for n in old_nodes:
        if n.text_type == TextType.TEXT:
            split_node = n.text.split(delimiter)
            if(len(split_node) % 2 == 0):
                raise ValueError("invalid markdown, section isn't closed")
            for s in range(len(split_node)):
                if split_node[s] == "":
                    continue
                if s % 2 == 0:
                    new_nodes.append(TextNode(split_node[s], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_node[s], text_type))
        else:
            new_nodes.append(n)
            continue
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)",text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)


def split_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:
            seperate = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(seperate) != 2:
                raise ValueError("invalid, link not closed")
            if seperate[0] != "":
                new_nodes.append(TextNode(seperate[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = seperate[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes    


def split_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image in images:
            seperate = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(seperate) != 2:
                raise ValueError("invalid, image not closed")
            if seperate[0] != "":
                new_nodes.append(TextNode(seperate[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = seperate[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_images(nodes)
    nodes = split_links(nodes)
    return nodes


# images
# r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

# regular links
# r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"