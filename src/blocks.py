from enum import Enum
from htmlnode import *
from splitter import *
from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    OLIST = "ordered_list"
    ULIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
    return [x for x in blocks if x]

def block_to_block_type(text):
    new_text = text.split("\n")

    if text.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if text.startswith(">"):
        for line in new_text:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if new_text[0] =="```" and new_text[-1] == "```" and len(new_text > 1):
        return BlockType.CODE
    
    if text.startswith("1. "):
        i = 1
        for line in new_text:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    
    if text.startswith("- "):
        for line in new_text:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        nodes.append(block_to_html(block))
    return ParentNode("div", nodes, None)

def block_to_html(block):
    block_type = block_to_block_type (block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html(block)
        case BlockType.CODE:
            return code_to_html(block)
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case BlockType.OLIST:
            return olist_to_html(block)
        case BlockType.ULIST:
            return ulist_to_html(block)
        case _:
            raise ValueError("invalid block")

def text_children(text):
    nodes = text_to_textnodes(text)
    print(nodes)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children


def paragraph_to_html(block):
    paragraph = " ".join(block.split("\n"))
    return ParentNode("p", text_children(paragraph))


def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalidi code block")
    
    text = TextNode(block[4:-3], TextType.TEXT)
    child = text_node_to_html_node(text)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def heading_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_children(text)
    return ParentNode(f"h{level}", children)


def olist_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_children(content)
    return ParentNode("blockquote", children)