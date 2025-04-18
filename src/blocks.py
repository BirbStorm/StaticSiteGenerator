from enum import Enum
from htmlnode import LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()
    return [x for x in blocks if x]

