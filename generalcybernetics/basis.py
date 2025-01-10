
import uuid
import random
import copy


# it's not that complicated, I'm either passing
# *args
# or **kwargs
# or both.

# for *args
# I need to either copy it directly
# or treat a source I as already prepared *args
# or I need to treat it as  asource that I need
# to perform steps to generate a correctly
# ordered *args from.

# for **kwargs
# same deal, either it's already prepared and a good
# fit
# or I need to build it.

# the functions or calc nodes need to contain
# the info on what they want and how that's called.

# in blender / node systems, this is solved by
# directly connecting the input / output sockets
# of a compatible type.

# ...and the point with multiple inputs
# would be that I can assemble my inputs from
# multiple sources.

# and then the functions need to be able to 
# handle arbitrary length inputs, not single
# values, so "sum" not "add".

class CyberCalculationPayload:
    """
    ok so what do I want to do with this?
    
    I want to build automatic chains of calculations
    that aren't directly and purely in (my) code.
    
    I can chain stuff now, containerization is also possible/done.
    
    But what do I want to *actually* do here?
    
    I want to automate things that are automatable, but I want to allow
    players to take over when that's necessary or desirable.
    
    so, e.g. a "decision node" that, if control over that plan step
    is given to NP/AI, will have some value function to decide that.
    and if given to a player, is left to the player to decide which
    ones is superior.
    
    I also want to be able to model a feedback loop.
    Do calculations with that and be able to determine if something
    is stuck in a certain kind of spiral or not.
    
    which is probably done by variation of variables?
    
    cybernetic loops usually have some "feedback time" 
    and I know there is some differential math that can decide
    whether the reaction speed of the loop is fast enough to
    balance out the problem or not.
    Which is actually a different problem case than the "pure"
    downward spiral.
    
    also, if the purpose is control, or "directing" I need them to
    be able to... act?
    
    or do I just treat it as a data layer that provides information
    and then something other does the actuation?
    
    regarding input parsing, let's enforce dicts and kwargs first.
    since at least that's named.
    
    """
    def __init__(self,function, datakeyword=None):
        
        # let's change the logic here that the datakeyword is
        # only used and required if the input that's expected
        # for the function is NOT a dict, and I just want a single value.
        
        # otherwise, it's assumed to be a dict, and the 
        # which values and keywords are being used is supposed to be written
        # inside of the function.
        
        # I'm sure some... static typing ethusiasts would point
        # out the difficulty of having that work reliably
        # and I'm probably going to encounter a sort of...
        # venn diagram problem, where I can't really group
        # things of shared concern with regular coding practices.
        
        self.function = function
        
        self.datakeyword = datakeyword
        self.last_result = None
        self.last_attempt_successful = None
           
    def execute(self,data):
        sub_d = {}
        for x in self.datakeywords:
            if x in data:
                sub_d[x] = copy.deepcopy(data[x])
        
        self.last_result = function(**sub_d)


def sort(*args):
    # do i assert, that things have to be numbers or strings?
    # probably not. if it causes a problem I should just report it.
    full_list = []
    for arg in args:
        if type(arg) == list:
            full_list += arg
        else:
            full_list.append(arg)
            
    mylist = list(full_list)
    mylist.sort()
    return mylist
    
def myprint(anything):
    print("my anything",[anything])
    return anything
    
def mypass(anything):
    return anything
    
def mysum(*args):
    num = 0
    for x in args:
        num += x
    return num
    
def myproduct(*args):
    num = 1
    for x in args:
        num *= x
    return num
    
def mybiggerthancompare(*args):
    if len(args) != 2:
        raise ValueError("wrong number of inputs, can only compare two values")
    
    return args[0] > args[1]

def mysmallerthancompare(*args):
    if len(args) != 2:
        raise ValueError("wrong number of inputs, can only compare two values")
    
    return args[0] > args[1]

def my_write_feedback():
    """this is a bit tricky, because I need to give this function
    and the node it is in write access to data.
    
    that's very bad.
    
    how about instead...
    """
    
    return 1
    
def my_feedback_loop_start():
    """
    I set up something to fetch the value from the feedback node,
    if available?
    """
    
    
    return 1 



def main():
    # ok, these cover basic steps.
    # they show how to set something up,
    # that it works, normally, shuffled,
    # and that it can combined multiple nodes into one
    # calculation.
    a = 1

def myinput(anything):
    return anything

def myreturn(anything):
    return anything

class InputObject:
    def __init__(self,value,copy_value=True):
        if copy_value:
            value = copy.deepcopy(value)
        self.passed_value = value
    
    def overwrite_passed_value(self,value):
        # this is assuming I'm using a dict again.
        value = copy.deepcopy(value)
        self.passed_value.update(value)
    
    def __getitem__(self,key):
        # it's probably the passed value, right?
        return self.passed_value
    
    def get_node_value(self,node):
        if node.last_result != None:
            # actually more specifically if it's a dictionary?
            # hmm...
            node_val = node.last_result
            self.passed_value.update(node_val)
        
def test_InputObject():
    # that works, just be a bit carefulback about access stuff.
    mylist= [1,2,3,(4,5)]
    I = InputObject(mylist)
    new = I["ololol"]
    assert new==mylist
    assert id(new)!=id(mylist)
    
def example_container():
    
    N1 = Element("1")
    
    n1 = Element("1.1")
    n2 = Element("1.2")
    n3 = Element("1.3")
    n4 = Element("1.4")
    n5 = Element("1.5")
    
    # normally inputs are either passed by reference, passed
    # by value and copied internally or not.
    # the more problematic part is that I have to insert
    # whatever I'm passing into the input object's dictionary.
    
    n1.payload = {"this":1}
    n2.payload = {"this":2}
    n3.payload = {"this":3}
    n4.payload = CyberCalculationPayload(mysum,"this")
    n5.payload = CyberCalculationPayload(myreturn,"this")
    
    # but it serves as a marker for other parts of the code
    # to extract the information.
    # contained 
    
    # do I just take this as a marker?
    # to use 
    
    
    n1.connect_lr(n4)
    n2.connect_lr(n4)
    n3.connect_lr(n4)
    n4.connect_lr(n5)
    
    N1.elements = [n1,n2,n3,n4,n5]
    
    main_list = [N1]
    mylist = main_list
    # so the main point is that if I have contents inside of a cell,
    # I should not allow other payloads?
    # and then instead of executing the payload, I want to execute the sub_list.
    # how about 'returns'
    
    fixed_list = determine_execution_order(mylist)
    execute_node_collection(fixed_list)
    
    N1.last_result
    
def determine_execution_order(node_list):
    
    # do a loop detection first.
    this_run_uid = str(uuid.uuid4())
    
    exec_order = []
    function_nodes = []
    # basically the inverted
    checked_dict = {}
    for x in node_list:
        if type(x.payload) == CyberCalculationPayload:
            function_nodes.append(x)
                    
        elif type(x.payload) == InputObject:
            exec_order.append(x)
            
        elif type(x.payload) == dict:
            # do nothing
            exec_order.append(x)
            checked_dict[x.my_id] = this_run_uid
        
        elif type(x.payload)==type(None) and len(x.elements)!=0:
            exec_order.append(x)
            
        else:
            # it's a complex object... that should somehow
            # expose it's data as input?
            # hm... shit.
            function_nodes.append(x.payload.data_snapshot())
    
    exec_order = exec_order + function_nodes
    
    
    while True:
        done = False
        move = None
        realbreak = False
        
        for node in exec_order:
            base_index = exec_order.index(node)
            
            for in_node in node.in_connections:
                in_node.loop_starts
                
                adjust=True
                
                for x in in_node.loop_starts:
                    if (in_node.my_id, node.my_id) == x:
                        # don't worry about this node "fixing"
                        adjust = False
                        
                if adjust:
                    in_index = exec_order.index(in_node)
                    if base_index < in_index:
                        move = node
                        new_index = in_index + 1
                        realbreak=True
                        break
                        
            if realbreak:
                break
                
        if move != None:
            exec_order.remove(node)
            exec_order.insert(new_index, node)
            
        if realbreak:
            continue
            
        break
                    
    return exec_order

def single_execution(focus_node):
    data = focus_node.in_connections[0].payload
    
    if type(data)==dict:
        # this is fine, do nothing.
        data = data[focus_node.payload.datakeyword]
    
    elif type(data) == CyberCalculationPayload:
        # only do this when the calculation has finished,
        # but the execution order should take
        # care of that.
        data = data.last_result
        
    elif type(data) == InputObject:
        data = data.passed_value
    else:
        # expose object data somehow
        raise NotImplementedError
        
    focus_node.payload.last_result = focus_node.payload.function(data)
    
def execute_node_collection(exec_order,optional_input=None):
    # this detects my loops
    sub_loops, sub_loop_nodes = cycle_detection(exec_order)
    
    
    # ok, so how do I...
    
    # hmmm.
    if optional_input!=None:
        for node in exec_order:
            if type(node.payload)==InputObject:
                node.payload.overwrite_passed_value(optional_input)
    
    error = None
    for focus_node in exec_order:
        if type(focus_node.payload) == dict:
            continue
        
        elif type(focus_node.payload) == InputObject:
            for in_node in focus_node.in_connections:
                node_val = in_node.payload.last_result
                # if it's the first iteration there will be nothing here.    
                if node_val!=None:
                    focus_node.payload.passed_value.update(node_val)
            
            focus_node.payload.last_result = focus_node.payload.passed_value
        
        elif type(focus_node.payload)==CyberCalculationPayload:
            try:
                # ok, veeeery constructed case of only one specific thing
                
                # I guess I can meta it, by looking at how many
                # arguments the function I have set takes, and then check
                # if the inputs match that.
                
                if len(focus_node.in_connections) == 1:
                    single_execution(focus_node)
                
                elif len(focus_node.in_connections) > 1:
                    
                    #... 
                    
                    # I can just assume *args in most cases.
                    
                    # ok, so do I sum it up?
                    # what's my function like?
                    # if it's a sorting function
                    # I want to create a list from individual values and sort that.
                    # if it's multiple lists, I want to merge them and then sort them.
                    
                    # if it's a math function, there are specific 
                    # inputs. e.g. add only takes two.
                    
                    # compare should take two and return the bigger one.
                    # or produce a boolean?
                    
                    # for a decision system I... should have something like
                    # "evaluate plans" and this is also the step I want to mess with.
                    
                    my_args = []
                    for in_node in focus_node.in_connections:
                        if type(in_node.payload) == dict:
                            my_args.append(in_node.payload[focus_node.payload.datakeyword])
                        elif type(in_node.payload) == CyberCalculationPayload:
                            my_args.append(in_node.payload.last_result)
                    
                    focus_node.payload.last_result = focus_node.payload.function(*my_args)
            except:
                error = "that didn't work"
                
                #break -> fail gracefully, give UI feedback.
                raise
        
        
        elif type(focus_node.payload)==type(None) or type(focus_node.payload)==CyberContainer:
            if len(focus_node.elements)!=0:
                sub_loops = cycle_detection(focus_node.elements)
                sub_nodes = determine_execution_order(focus_node.elements)
                execute_node_collection(sub_nodes,optional_input)
                focus_node.payload.last_result = sub_nodes[-1].payload.last_result
    
class CyberContainer:
    """
    this is a bit dumb. I need this... for like... homomorphism.
    I'm accessing last_result sometimes, so some object having
    this variable needs to exist, even if it doesn't make "explicit" sense.
    but
    """
    def __init__(self):
        self.last_result = None

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
        self.loop_starts = [] # if this node is the start of a loop, 
        # the elements that would form the loop go here. by id.
        
        if my_id == None:
            self.my_id = str(uuid.uuid4()) # should be... assigned by you.
        else:
            self.my_id = my_id
    
    @property
    def last_result(self):
        if len(self.elements)==0:
            
            return None
        
        internal_return_values = []
        for x in self.elements:
            if type(x.payload)==CyberCalculationPayload:
                if x.payload.function == myreturn:
                    internal_return_values.append(x.payload.last_result)
        
        if len(internal_return_values)==1:
            internal_return_values=internal_return_values[0]
            
        return internal_return_values
                    
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
            return dict_results, list_results
        
        if exact_object == None and search_id == None:
            raise ValueError("provide either an exact object or a node id to search for")
    
        other_lists = [self.elements,self.in_connections,self.out_connections]
        
        for my_list in other_lists:
            for x in my_list:
                this_element_results = []
                if x in visited:
                    continue
                visited.append(x)
                
                object_match = ((x == exact_object) and (exact_object != None))
                payload_match = ((x.payload == exact_object) and (exact_object != None))
                id_match = (x.my_id == search_id)
                if object_match or payload_match or id_match:
                    this_element_results.append(x)
                
                if this_element_results!=[]:
                    list_results += this_element_results
                    
        for my_list in other_lists:
            for x in my_list:
                sub_dict, sub_list = x.search_elements(exact_object, search_id, current_depth+1, max_depth,visited = list(visited+self.elements))
                
                if sub_dict == {} and sub_list != []:
                    dict_results[x.my_id] = sub_list
                elif sub_dict != {} and sub_list == []:
                    dict_results[x.my_id] = sub_dict
                elif sub_dict =={} and sub_list ==[]:
                    pass # do nothing
                else:
                    raise ValueError("something went wrong, I need either or both to be empty")
                
                
            
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

def cycle_detection(nodes,visited=None):
    """this assumes some kind of forward thing. it's not omnidirectional, and I'm only detect the problematic pairs, not the full loops."""
    detected_loops = []
    detected_loop_nodes = []
    if visited == None:
        visited = []
    
    for node in nodes:
        if node.my_id in visited:
            continue
        
        visited.append(node.my_id)
        new_nodes = node.out_connections
        for x in new_nodes:
            if x.my_id in visited:
                detected_loop_nodes.append(x.my_id)
                detected_loops.append((node.my_id,x.my_id))
                node.loop_starts.append((node.my_id,x.my_id))
                
        sub_loops, sub_loop_nodes = cycle_detection(new_nodes,visited)
        detected_loops += sub_loops
        
    return detected_loops, detected_loop_nodes

def test_loop_detection():
    
    N1 = Element("1")
    N2 = Element("2")
    N3 = Element("3")
    N4 = Element("4")

    N1.connect_lr(N2)
    N2.connect_lr(N3)
    N3.connect_lr(N4)

    loops , loop_nodes = cycle_detection ([N1,N2,N3,N4])
    
    assert len(loops)==0
    
    
    N1 = Element("1")
    N2 = Element("2")
    N3 = Element("3")
    N4 = Element("4")

    N1.connect_lr(N2)
    N2.connect_lr(N3)
    N3.connect_lr(N4)
    N4.connect_lr(N1)
    
    loops , loop_nodes = cycle_detection ([N1,N2,N3,N4])
    assert len(loops) > 0
    assert loops == [("4","1")]

def start_finding(my_nodes):
    start = None
    all_start = []
    for x in my_nodes:
        if x.in_connections == []:
            start = x
            all_starts.append(x)
    
    if start == None:
        # it's circular, start with any, might as well be element 0
        start = my_nodes[0]
        
    return start,all_starts
    
def this_test_main(my_nodes):
    
    start, all_starts =start_finding(my_nodes)
    done_nodes=[]
    current_nodes=[start]
    x_ordering={0:[start]}
    current_x=0
    
    this_recursive_structure(current_nodes,current_x,x_ordering,done_nodes)
    positions=get_geometric_arrangement(x_ordering)
    return positions


#what about directionless stuff

if __name__=="__main__":
    main()
    
