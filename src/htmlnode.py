class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        #child classes must override
        raise NotImplementedError()
    
    def props_to_html(self):
        return ''.join(f' {k}="{v}"' for k, v in self.props.items()) if self.props else ''
    
    def __repr__(self):
        return f"{self.__class__.__name__}\nTag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props}"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.children

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag is None:
            return self.value
        prop_string = self.props_to_html()
        return f"<{self.tag}{prop_string}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: Parent tag is None")
        if not self.children:
            raise ValueError("Error: Parent children is None")
        return f"<{self.tag}{self.props_to_html()}>"+''.join(child.to_html() for child in self.children)+f"</{self.tag}>"