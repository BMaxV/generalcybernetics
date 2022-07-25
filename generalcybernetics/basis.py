
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
        self.same_rank_pairs=[]
    #def make_graph_viz
    def copy(self):
        """creates a full copy of the graph,with idenical payload, but different nodes."""
        
        new_elements=[]
        for el in self.elements:
            new_elements.append(Element(payload=el.payload))
            
        for el in self.elements:
            for other in el.out_connections:
                if other not in self.elements:
                    continue
                i1=self.elements.index(el)
                i2=self.elements.index(other)
                new_el=new_elements[i1]
                new_other=new_elements[i2]
                new_el.connect_lr(new_other)
        
        new_pairs=[]
        for pair in self.same_rank_pairs:
            i1=self.elements.index(pair[0])
            i2=self.elements.index(pair[1])
            new_pairs.append([new_elements[i1],new_elements[i2]])
        
        S=System()
        S.elements=new_elements
        S.same_rank_pairs=new_pairs
        
        return S


def this_recursive_structure(current_nodes,current_x,x_ordering,done_nodes):
    new_current_left=[]
    new_current_right=[]
    for n in current_nodes:
        for x in n.in_connections:
            new_x=current_x-1
            if new_x not in x_ordering:
                x_ordering[new_x]=[x]
            else:
                if x not in x_ordering[new_x]:
                    x_ordering[new_x].append(x)
            if x not in done_nodes and x not in new_current_left:
                new_current_left.append(x)
        
        for x in n.out_connections:
            new_x=current_x+1
            if new_x not in x_ordering:
                x_ordering[new_x]=[x]
            else:
                if x not in x_ordering[new_x]:
                    x_ordering[new_x].append(x)
            if x not in done_nodes and x not in new_current_right:
                new_current_right.append(x)
        
        done_nodes.append(n)
                
    #print(new_current_left,new_current_right)
    if new_current_left!=[]:
        print(new_current_left)
        this_recursive_structure(new_current_left,current_x-1,x_ordering,done_nodes)
    if new_current_right!=[]:
        print(new_current_right)
        this_recursive_structure(new_current_right,current_x+1,x_ordering,done_nodes)

def get_geometric_arrangement(x_ordering):
    
    positions={}
    key_list=list(x_ordering.keys())
    key_list.sort()
    currentx=0
    
    diff_y=1
    diff_x=1
    for x in key_list:
        currenty=0
        y_base=len(x_ordering[x])/2
        for element in x_ordering[x]:
            positions[element]=(currentx,y_base+currenty,0)
            currenty-=diff_y
        currentx+=diff_x
    return positions

def start_finding(my_nodes):
    start=None
    
    for x in my_nodes:
        if x.in_connections==[]:
            start=x
            break
        if x.out_connections==[]:
            start=x
            break
    
    if start==None:
        # it's circular, start with any, might as well be element 0
        start=my_nodes[0]
        
    return start
    
def this_test_main(my_nodes):
    
    start=start_finding(my_nodes)
    done_nodes=[]
    current_nodes=[start]
    x_ordering={0:[start]}
    current_x=0
    
    this_recursive_structure(current_nodes,current_x,x_ordering,done_nodes)
    positions=get_geometric_arrangement(x_ordering)
    return positions


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
    
        
    
