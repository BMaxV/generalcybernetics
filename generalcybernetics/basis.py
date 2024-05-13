
class Element:
    """basically just for storing the meta information
    the payload should contain "deep" information about the function
    to be performed or the decision to be made.
    
    something that's a problem (eventually) is size. I would like 
    to keep things loaded that are relevant and discard other things
    and load them again from a known resource when I need them.
    
    weakref solves the unloading.
    but how do I get things back once they're gone?
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
    
    def __bt__(self,other):
        # to make things sortable.
        if type(other)!=type(self):
            raise TypeError
        if len(self.out_connections) < len(other.out_connections):
            return True
        elif len(self.out_connections) == len(other.out_connections) and len(self.in_connections) > len(other.in_connections):
            return True
        else:
            return False
        
    def __lt__(self,other):
        # to make things sortable.
        if type(other)!=type(self):
            raise TypeError
        if len(self.out_connections) > len(other.out_connections):
            return True
        elif len(self.out_connections) == len(other.out_connections) and len(self.in_connections) < len(other.in_connections):
            return True
        else:
            return False
            
    def __repr__(self):
        s="<Element id:"+str(id(self))[-5:]+"... in:"+str(len(self.in_connections))+" out:"+str(len(self.out_connections))+">"
        return s
        
    def connect_rl(self,other):
        other.out_connections.append(self)
        self.in_connections.append(other)
        
    def connect_lr(self,other):
        self.out_connections.append(other)
        other.in_connections.append(self)
        
    def serialize(self):
        a=1
    
    def deserialize(self,data):
        return 
       
class System:
    """
    system can be the payload of another node.
    
    nodes inside this system can point outside.
    """
    def __init__(self):
        self.elements=[]
        self.same_rank_pairs=[]
    #def make_graph_viz
    
    def dissolve(self,element):
        connections=[]
        for x in element.in_connections:
            for x2 in element.out_connections:
                x.connect_lr(x2)
                connections.append((x,x2))
                x2.in_connections.remove(element)
            x.out_connections.remove(element)
        self.elements.remove(element)
        return connections
    
    def subdivide_connection(self,e1,e2,verbose=False):
        
        # first of all, find out which way the connection goes
        
        lr = (e2 in e1.out_connections)
        rl = (e1 in e2.out_connections)
        new_e=Element()
        if lr:
            e1.out_connections.remove(e2)
            e2.in_connections.remove(e1)
            new_e.connect_lr(e2)
            new_e.connect_rl(e1)
            self.elements.append(new_e)
            connections=[[new_e,e2],[e1,new_e]]
        if rl:
            e1.in_connections.remove(e2)
            e2.out_connections.remove(e1)
            new_e.connect_lr(e1)
            new_e.connect_rl(e2)
            self.elements.append(new_e)
            connections=[[new_e,e1],[e2,new_e]]
        if verbose:
            print("cyber",new_e,connections)
        
        return new_e, connections
            
        
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
                
    if new_current_left!=[]:
        this_recursive_structure(new_current_left,current_x-1,x_ordering,done_nodes)
    if new_current_right!=[]:
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


#what about directionless stuff

if __name__=="__main__":
    test()
    test2()
    
        
    
