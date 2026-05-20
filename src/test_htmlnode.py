import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from src.helpers import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_images, split_nodes_links, split_nodes_links
from textnode import BlockType, TextNode, TextType
from helpers import markdown_to_blocks, text_node_to_html_node, text_to_textnodes

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_creation(self):
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.props, {"class": "greeting"})
    
    def test_htmlnode_props_to_html(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')
    
    def test_htmlnode_repr(self):
        node = HTMLNode(tag="p", value="This is a paragraph.", props={"style": "color: red;"})
        expected_repr = 'HTMLNode(tag=p, value=This is a paragraph., children=[], props={\'style\': \'color: red;\'})'
        self.assertEqual(repr(node), expected_repr)
    
    def test_htmlnode_with_children(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.children, [child1, child2])
    
    def test_leaf_to_html(self):
        leaf = LeafNode(tag="p", value="This is a paragraph.")
        self.assertEqual(leaf.to_html(), '<p>This is a paragraph.</p>')
        
    def test_leaf_to_html_with_props(self):
        leaf = LeafNode(tag="a", value="Click me!", props={"href": "https://example.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://example.com">Click me!</a>')
    
    def test_leaf_to_html_without_value(self):
        leaf = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            leaf.to_html()
    def test_leaf_without_tag(self):
        leaf = LeafNode(tag=None, value="Just text")
        self.assertEqual(leaf.to_html(), 'Just text')
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(tag="span", value="grandchild")
        child1 = LeafNode(tag="b", value="Child 1 - Bold")
        child2 = LeafNode(tag="i", value="Child 2 - Italic")
        parent = ParentNode(tag="div", children=[child1, child2])
        grand_parent_node= ParentNode(tag="div", children=[parent])
        
        expected_parent_html = '<div><b>Child 1 - Bold</b><i>Child 2 - Italic</i></div>'
        self.assertEqual(parent.to_html(), expected_parent_html)
        
        expected_html = '<div><div><b>Child 1 - Bold</b><i>Child 2 - Italic</i></div></div>'
        self.assertEqual(grand_parent_node.to_html(), expected_html)
    
    def test_text_node_html_node(self): 
        text_node = TextNode("This is some bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is some bold text")
        self.assertEqual(html_node.props, {})
    
    def test_code_delimiter(self):
        text_node = TextNode("This is some `code` in between", TextType.TEXT)
        html_node = split_nodes_delimiter([text_node], "`", TextType.CODE)
        
        self.assertEqual(html_node, [TextNode("This is some ", TextType.TEXT), TextNode("code", TextType.CODE), TextNode(" in between", TextType.TEXT)])
    
    
    def test_bold_delimiter(self):
        text_node = TextNode("This is **bold** text", TextType.TEXT)
        html_node = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        
        self.assertEqual(html_node, [TextNode("This is ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.TEXT)])
    
    def test_italic_delimiter(self):
        text_node = TextNode("This is _italic_ text", TextType.TEXT)
        html_node = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        
        self.assertEqual(html_node, [TextNode("This is ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" text", TextType.TEXT)])
    
    def test_unmatched_delimiter(self):
        text_node = TextNode("This is **bold text with unmatched delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertTrue("Unmatched delimiter" in str(context.exception))
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
        
        
    def test_split_images(self):
        text_node = TextNode("This is some **bold** text with a ![first image](https://example.com/image.png) and an image ![alt text](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_images([text_node])
        self.assertEqual(new_nodes, [TextNode("This is some **bold** text with a ", TextType.TEXT), TextNode("first image", TextType.IMAGE, "https://example.com/image.png"), TextNode(" and an image ", TextType.TEXT), TextNode("alt text", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")])
    
    def test_split_links(self):
        text_node = TextNode("This is some **bold** text with a [first link](https://example.com) and an image [second link](https://jw.org)", TextType.TEXT)
        new_nodes = split_nodes_links([text_node])
        self.assertEqual(new_nodes, [TextNode("This is some **bold** text with a ", TextType.TEXT), TextNode("first link", TextType.LINK, "https://example.com"), TextNode(" and an image ", TextType.TEXT), TextNode("second link", TextType.LINK, "https://jw.org")]) 
    
    def test_text_to_textnodes(self):
        text = "This is **bold** text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ]
        self.assertEqual(text_nodes, expected_nodes)
    
    def test_markdown_to_blocks(self):
        markdown = """
        This is a paragraph.

        This is another paragraph with a line break
        and more text.

        - This is a list item
        - This is another list item
        """
        blocks = markdown_to_blocks(markdown)
        expected_blocks = [
            "This is a paragraph.",
            "This is another paragraph with a line break\nand more text.",
            "- This is a list item\n- This is another list item"
        ]
        self.assertEqual(blocks, expected_blocks)
    
    def test_block_to_block_type(self):
        from helpers import block_to_block_type
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```code block```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. Ordered item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("This is a paragraph with a line break\nand more text."), BlockType.PARAGRAPH)
    
    
    def test_markdown_to_html_node(self):
        from helpers import markdown_to_html_node
        markdown = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """
        html_node = markdown_to_html_node(markdown)
        expected_html = '<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><pre><code>\nThis is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>'
        self.assertEqual(html_node.to_html(), expected_html)