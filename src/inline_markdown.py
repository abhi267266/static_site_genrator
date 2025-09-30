from src.textnode import TextNode, TextType
import re


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    res = []

    for node in old_nodes:
        if node.text_type == TextType.LINK:
            # Already a link, keep as is
            res.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            res.append(node)
            continue

        last_index = 0
        for link_text, link_url in links:
            # Find where this link appears in the text
            start = text.find(f"[{link_text}]({link_url})", last_index)
            end = start + len(f"[{link_text}]({link_url})")

            # Add text before the link
            if start > last_index:
                res.append(TextNode(text[last_index:start], TextType.TEXT))

            # Add the link node
            res.append(TextNode(link_text, TextType.LINK, link_url))

            last_index = end

        # Add remaining text after the last link
        if last_index < len(text):
            res.append(TextNode(text[last_index:], TextType.TEXT))

    return res


def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type == TextType.IMAGE:
            # Already an image, keep as is
            res.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            res.append(node)
            continue

        last_index = 0
        for alt_text, url in images:
            # Find the exact position of this image in text
            img_markdown = f"![{alt_text}]({url})"
            match_start = text.find(img_markdown, last_index)

            # Add preceding text if any
            if match_start > last_index:
                res.append(TextNode(text[last_index:match_start], TextType.TEXT))

            # Add the image node
            res.append(TextNode(alt_text, TextType.IMAGE, url))

            # Move last_index past this image
            last_index = match_start + len(img_markdown)

        # Add any remaining text after the last image
        if last_index < len(text):
            res.append(TextNode(text[last_index:], TextType.TEXT))

    return res



def text_to_textnodes(text):
    # Start with the whole text as a single TEXT node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by code blocks first (highest precedence)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Then split by bold (**text**)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # Then split by italic (_text_)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # Then split by images
    nodes = split_nodes_image(nodes)
    
    # Finally split by links
    nodes = split_nodes_link(nodes)
    
    return nodes

