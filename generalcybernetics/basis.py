
import uuid

class Element:
    """basically just for storing the meta information
    the payload should contain "deep" information about the function
    to be performed or the decision to be made.
    
    something that's a problem (eventually) is size. I would like 
    to keep things loaded that are relevant and discard other things
    and load them again from a known resource when I need them.
    
    weakref solves the unloading.
    but how do I get things back once they're gone?
    
    ok, so, I'm fusing stuff into one object.
    I think I want to be able to do several things with this...
    
    """
    def __init__(self,my_id=None,in_connections=None,out_connections=None,payload=None):
        
        if in_connections == None:
            self.in_connections = []
        else:
            self.in_connections = in_connections
            
        if out_connections == None:
            self.out_connections = []
        else:
            self.out_connections = out_connections
            
        self.payload = payload
        #specify color as {color: x11 color scheme color}
        #see https://renenyffenegger.ch/notes/tools/Graphviz/examples/index
        self.style = None
        self.elements = []
        self.same_rank_pairs = []
        if my_id == None:
            self.my_id = str(uuid.uuid4()) # should be... assigned by you.
        else:
            self.my_id = my_id
            
    def search_elements(self,exact_object=None,search_id=None,current_depth=0,max_depth=3,visited=None):
        """
        Search function to search elements, connections
        ids and payloads for the object or the id.
        will return
        dict_results, list_results
        in a shape of 
        {id:{id:[results]}}
        where possible.
        """
        
        # shit.
        # if I am searching, I either want to fetch the thing to get theobject
        # or I have an id from somewhere, possibly want to remove it from
        # my structure, but I have to remove it from the parent.
                
        dict_results = {}
        list_results = []
        if visited == None:
            visited = []
        
        if current_depth > max_depth:
            #print("max depth reached")
            return dict_results, list_results
        
        if exact_object == None and search_id == None:
            raise ValueError("provide either an exact object or a node id to search for")
    
        other_lists = [self.elements,self.in_connections,self.out_connections]
        
        for my_list in other_lists:
            for x in my_list:
                #print("my element",x,x.my_id)
                this_element_results = []
                if x in visited:
                    #print("visited,going back")
                    continue
                visited.append(x)
                
                object_match = ((x == exact_object) and (exact_object != None))
                payload_match = ((x.payload == exact_object) and (exact_object != None))
                id_match = (x.my_id == search_id)
                if object_match or payload_match or id_match:
                    #print('match')
                    this_element_results.append(x)
                    #print("...contains my result")
                    #print(object_match , payload_match , id_match)
                    
                else:
                    sub_dict, sub_list = x.search_elements(exact_object, search_id, current_depth+1, max_depth,visited = visited)
                    
                    if sub_dict == {} and sub_list != []:
                        dict_results[x.my_id] = sub_list
                    elif sub_dict != {} and sub_list == []:
                        dict_results[x.my_id] = sub_dict
                    elif sub_dict =={} and sub_list ==[]:
                        pass # do nothing
                    else:
                        #print(sub_dict,sub_list)
                        raise ValueError("something went wrong, I need either or both to be empty")
                
                if this_element_results!=[]:
                    list_results += this_element_results
            
        #results = list(set(results))
        return dict_results, list_results
        
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
        s=f"<generalcybernetics.Element id:{self.my_id}>"
        return s
        
    def connect_rl(self,other):
        other.out_connections.append(self)
        self.in_connections.append(other)
        
    def connect_lr(self,other):
        self.out_connections.append(other)
        other.in_connections.append(self)
        
    def serialize(self,visited=None):
        
        if visited == None:
            visited = []
        visited.append(self)
        
        if payload!=None:
            # some kind of serialization function?
            a=1
        in_ids = []
        for x in self.in_connections:
            in_ids.append(x.id)
        out_ids = []
        for x in out_ids:
            out_ids.append(x.id)
        elements = []
        for x in self.elements:
            if x in visited:
                continue
            elements.append((x.id,x.serialize(visited)))
        
        my_dict = {"my_id":self.id,"in_ids":in_ids,"out_ids":out_ids,"elements":elements}
        
        # put it into a string? idk.
        
        return my_dict
    
    @classmethod
    def deserialize(self,data):
        return 
       
    
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

#if __name__=="__main__":
    #this_test_main(
    
        
    
