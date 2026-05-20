from  src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import  TextType, TextNode, BlockType
import re

"""
    Create TextNode from raw markdown text. 
    Markdown parsers often support nested inline elements.
    Split Delimiters: ** for bold, * for italic, ` for code.
    Old_nodes: list  of nodes (TextNode),
    Delimiter: the markdown delimiter to split on, e.g. "**" for bold, "*" for italic, "`" for code, etc.
    Text_type: the TextType to use for the new nodes created from the split, e
"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            # if matching closing delimiter is not found, raise an exception
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f"Unmatched delimiter: {delimiter} in text: {node.text}")
            
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

"""
    Extract images
    Takes a raw markdown text and returns a list of tuples (text, url) for each image found in the text.
"""
def extract_markdown_images(text):
    pattern = r'!\[([^\[\]]*)\]\(([^\(\)]*)\)'
    return re.findall(pattern, text)

"""    
    Extract links
    Takes a raw markdown text and returns a list of tuples (text, url) for each link found in the text.
"""
def extract_markdown_links(text):
    pattern = r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)'
    return re.findall(pattern, text)


"""
    Split markdown  images into TextNodes.
"""
def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            matches = extract_markdown_images(node.text)
            if matches:
                last_index = 0
                for alt, url in matches:
                    match_str = f'![{alt}]({url})'
                    index = node.text.find(match_str, last_index)
                    if index != -1:
                        if index > last_index:
                            new_nodes.append(TextNode(node.text[last_index:index], TextType.TEXT))
                        new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                        last_index = index + len(match_str)
                if last_index < len(node.text):
                    new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


"""
    Split markdown links into TextNodes.
"""
def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.TEXT:
            matches = extract_markdown_links(node.text)
            if matches:
                last_index = 0
                for text, url in matches:
                    match_str = f'[{text}]({url})'
                    index = node.text.find(match_str, last_index)
                    if index != -1:
                        if index > last_index:
                            new_nodes.append(TextNode(node.text[last_index:index], TextType.TEXT))
                        new_nodes.append(TextNode(text, TextType.LINK, url))
                        last_index = index + len(match_str)
                if last_index < len(node.text):
                    new_nodes.append(TextNode(node.text[last_index:], TextType.TEXT))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes

"""
    Converts a TextNode to an HTMLNode, specifically a LeafNode.
    If it gets TextNode that is none of those types, it should raise an exception. 
    Otherwise return a new LeafNode with the appropriate tag and value.
"""
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception(f"Unsupported text type: {text_node.text_type}")


"""
    Converts a raw markdown text to a list of TextNodes objects
"""
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes

"""
    Separates blocks of text by double newlines and converts them to TextNodes.
    This is useful for handling block level elements in markdown, such as paragraphs, headers, lists
    removes whitespace between each newline.
"""
def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split('\n\n'):
        if block.strip() == '':
            continue
        blocks.append(re.sub(r'\n\s*', '\n', block.strip()))
        
    return blocks
"""    
    takes a single clock of markdown text and retuns a block type.
    - heading starts with 1-6 # followed by a space and then the text
    - multiline code blocks starts with ``` and a newline, then end with ```.
    - blockquotes start with > followed by a space and then the text
    - unordered list items start with - followed by a space and then the text
    - ordered list items start with 1. followed by a space and then the text
    - otherwise it's a paragraph
"""
def block_to_block_type(block):
    if re.match(r'#{1,6} ', block):
        return BlockType.HEADING
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    elif re.match(r'> ', block):
        return BlockType.QUOTE
    elif re.match(r'- ', block):
        return BlockType.UNORDERED_LIST
    elif re.match(r'\d+\. ', block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH  

"""
    Takes a string of text and returns a list of HTMLNode objects representing the inline markdown.
"""
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

"""
    Converts blocks of markdown text to a single HTMLNode. That one parent HTMLNode shoud contain many children HTMLNode
    objects representing nested elements.
    1. Split the markdown into blocks using markdown_to_blocks.
    2. For each block, determine its type using block_to_block_type.
       a. based on block type, create an new HTMLNode with proper data
       b. assign proper child HTMLNode objects to block node (TextNode --> HTMLNode)
"""
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = len(re.match(r'#{1,6}', block).group(0))
            children = text_to_children(block[level+1:])
            html_nodes.append(ParentNode(tag=f'h{level}', children=children))
        elif block_type == BlockType.CODE:
            code_text = block[3:-3]
            code_node = LeafNode(tag="code", value=code_text)
            html_nodes.append(ParentNode(tag="pre", children=[code_node]))
        elif block_type == BlockType.QUOTE:
            children = text_to_children(block[2:])
            html_nodes.append(ParentNode(tag='blockquote', children=children))
        elif block_type == BlockType.UNORDERED_LIST:
            items = [item[2:] for item in block.split('\n')]
            html_nodes.append(ParentNode(tag='ul',  children=[ParentNode(tag='li', children=text_to_children(item)) for item in items]))
        elif block_type == BlockType.ORDERED_LIST:
            items = [item[item.find('. ')+2:] for item in block.split('\n')]
            html_nodes.append(ParentNode(tag='ol', children=children))
            html_nodes.append(ParentNode(tag='ol', children=[ParentNode(tag='li', children=text_to_children(item)) for item in items]))
        else:
            children = text_to_children(block)
            html_nodes.append(ParentNode(tag='p', children=children))
    return ParentNode(tag='div', children=html_nodes)
 

