from enum import Enum
import re
import os

from src.htmlnode import ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = markdown.strip().split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")
    
    if re.match(r"^#{1,6} ", lines[0]):
        return BlockType.HEADING

    if lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(re.match(r"^\d+\. ", line) for line in lines):
        numbers = [int(re.match(r"^(\d+)\. ", line).group(1)) for line in lines]
        if numbers == list(range(1, len(numbers)+1)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Convert markdown text to a list of HTMLNode children.
    This function processes inline markdown (bold, italic, code, links, images).
    Assumes you have text_to_textnodes and text_node_to_html_node functions.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def heading_to_html_node(block):
    """Convert a heading block to an HTMLNode."""
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Convert a code block to an HTMLNode."""
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    
    # Extract the text between the ``` markers
    text = block[4:-3]
    
    # For code blocks, don't parse inline markdown
    # Create a simple TextNode and convert it
    code_node = TextNode(text, TextType.TEXT)
    code_child = text_node_to_html_node(code_node)
    
    code = ParentNode("code", [code_child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    """Convert a quote block to an HTMLNode."""
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to an HTMLNode."""
    items = block.split("\n")
    html_items = []
    
    for item in items:
        text = item[2:]  # Remove "- " prefix
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    
    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to an HTMLNode."""
    items = block.split("\n")
    html_items = []
    
    for item in items:
        # Remove the "1. ", "2. ", etc. prefix
        text = re.sub(r"^\d+\. ", "", item)
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    
    return ParentNode("ol", html_items)


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTMLNode."""
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Args:
        markdown: A string containing the full markdown document
        
    Returns:
        A ParentNode (div) containing all the block-level HTML nodes
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        else:
            raise ValueError(f"Invalid block type: {block_type}")
    
    return ParentNode("div", children)


def extract_title(markdown):
    """
    Extract the H1 header from the markdown content.

    Args:
        markdown (str): The markdown content as a string.

    Returns:
        str: The content of the H1 header, stripped of the leading '#' and whitespace.

    Raises:
        ValueError: If no H1 header is found in the markdown content.
    """
    lines = markdown.split("\n")
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("# "):
            return stripped_line[2:].strip()
    raise ValueError("No H1 header found in the markdown content.")


