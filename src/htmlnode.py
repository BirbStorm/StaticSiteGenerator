class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props != None:
            for i in self.props:
                result += f" {i}=\"{self.props[i]}\""
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes MUST have a value")
        if not self.tag:
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def __repr__(self):
        return f"Parent({self.tag}, {self.children}, {self.props})"
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Missing a tag")
        if not self.children:
            raise ValueError("Missing children")
        result = f"<{self.tag}{self.props_to_html()}>"
        for i in self.children:
            result += i.to_html()
        return result + f"</{self.tag}>"