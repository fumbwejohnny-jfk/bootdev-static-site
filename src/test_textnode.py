import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_textnode_creation(self):
        node = TextNode("Hello, World!", TextType.TEXT)
        self.assertEqual(node.text, "Hello, World!")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_textnode_equality(self):
        node1 = TextNode("Hello, World!", TextType.TEXT)
        node2 = TextNode("Hello, World!", TextType.TEXT)
        node3 = TextNode("Hello, World!", TextType.BOLD)
        node4 = TextNode("Hello, World!", TextType.TEXT, "https://example.com")
        
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)

    
    
    def test_textnode_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node.text, "Click here")
        self.assertEqual(node.text_type, TextType.LINK)
        self.assertEqual(node.url, "https://example.com")
    
    def test_textnode_equality_with_url(self):
        node1 = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://example.com")
        node3 = TextNode("Click here", TextType.LINK, "https://different.com")
        
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
    
    def test_textnode_with_images(self):
        node = TextNode("Image description", TextType.IMAGE)
        self.assertEqual(node.text, "Image description")
        self.assertEqual(node.text_type, TextType.IMAGE)
        self.assertIsNone(node.url)
    
    
    
if __name__ == '__main__':
    unittest.main()