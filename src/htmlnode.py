class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or self.props == {}:
            return ""

        result = ""

        for key, value in self.props.items():
            result += " " + key + "=\"" + value + "\""
        return result


    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        else:
            return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"
        
    def __repr__(self):
        return (f"LeafNode({self.tag}, {self.value}, {self.props})")

class ParentNode(HTMLNode):
    def __init__(self, tag, children,  props=None):
            super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError
        else:
            childs_join = "".join(child.to_html() for child in self.children)
            return  "<" + self.tag + ">" + childs_join + "</" + self.tag + ">"
            
    
        
    
    
        