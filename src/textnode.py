
from enum import Enum


class TextType(Enum):
    """ Inline text types for a text node. """
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class BlockType(Enum):
    """ Block text types for a text node. """
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'
    
    
class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type.value == other.text_type.value and self.url == other.url
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'
    
    