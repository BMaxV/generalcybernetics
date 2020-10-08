
class Element:
    """basically just for storing the meta information
    the payload should contain "deep" information about the function
    to be performed or the decision to be made.
    """
    def __init__(self,in_connections=None,out_connections=None,payload=None):
        
        if in_connections==None:
            self.in_connections=[]
        else:
            self.in_connections=in_connections
            
        if out_connections==None:
            self.out_connections=[]
        else:
            self.out_connections=out_connections
            
        self.payload=payload
        #specify color as {color: x11 color scheme color}
        #see https://renenyffenegger.ch/notes/tools/Graphviz/examples/index
        self.style=None
        
    
    def connect_rl(self,other):
        other.out_connections.append(self)
        self.in_connections.append(other)
        
    def connect_lr(self,other):
        self.out_connections.append(other)
        other.in_connections.append(self)
        
class System:
    def __init__(self):
        self.elements=[]
    #def make_graph_viz
    def copy(self):
        """creates a full copy of the graph,with idenical payload, but different nodes."""
        
        new_elements=[]
        for el in self.elements:
            new_elements.append(Element(payload=el.payload))
            
        for el in self.elements:
            for other in el.out_connections:
                if other not in new_elements:
                    continue
                i1=self.elements.index(el)
                i2=self.elements.index(other)
                new_el=new_elements[i1]
                new_other=new_elements[i2]
                new_el.connect_lr(new_other)
                
        S=System()
        S.elements=new_elements
        return S
                
def test():
    
    S=System()
    N1=Element()
    N2=Element()
    N3=Element()
    
    N1.connect_lr(N2)# -> this way
    N3.connect_rl(N2)# <- that way
    
    #you are now ready to do meta stuff with this.
    
#what about directionless stuff

if __name__=="__main__":
    test()
    
        
    
