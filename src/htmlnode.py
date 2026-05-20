"""
    TextNode represents the various types of inline that can exist in HTML an Mardown.
    HTMLNode represents a 'node' in a HTML document tree (like a div, span, p and  its content). 
    It can be block level or inline, and is designed to only output HTML.
"""

class HTMLNode:
    """
        HTLM node without a tag will just render a raw text
        HTML node without a value will be assumed to have children
        HTML node without children will be assumed to have a value
        HTML node without props simply won't have any attributes
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")
    
    """ Formatted string representation of the HTML attributes of the node """
    def props_to_html(self):
        if not self.props:
            return ''
        return " " + ' '.join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'
    

"""
    LeafNode is a type of HTMLNode that represents a single HTML tag with no children.
"""
class LeafNode(HTMLNode):
    """
        Should not allow any chilren
        both tag and value are required for a leaf node, but props are optional
    """
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    """
        if leaf noe has no value, it should raise a ValueError
        if leaf node has no tag, it should just return the value as raw text
        otherwise it should return an HTML tag.
    """
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode(tag={self.tag}, value={self.value}, props={self.props})'
    
    
"""
    Parent node represents a HTML node that can have children. It can be a block level or inline element.
    It should not have a value, but it can have props and children.
"""
class ParentNode(HTMLNode):
    """
        tag and children arguments are required for a parent node,
        doesn't take a value argument
    """
    
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.children:
            raise ValueError("ParentNode must have children")
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
    
    def __repr__(self):
        return f'ParentNode(tag={self.tag}, children={self.children}, props={self.props})'
    
    