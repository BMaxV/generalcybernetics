from generalcybernetics import basis
import unittest


class TestMyCybernetics(unittest.TestCase):

    def test_search(self):

        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")
        N5 = basis.Element("5")

        N1.elements = [N2]
        N2.elements = [N3]
        N3.elements = [N4]
        N4.elements = [N5]

        r = N1.search_elements(N5)
        assert str(
            r) == "({'2': {'3': {'4': [<generalcybernetics.Element id:5>]}}}, [])"

        r = N1.search_elements(search_id=N5.my_id)
        assert str(
            r) == "({'2': {'3': {'4': [<generalcybernetics.Element id:5>]}}}, [])"

        # this will not return a path, because it's the first level
        r = N1.search_elements(N2)
        assert str(r) == "({}, [<generalcybernetics.Element id:2>])"
        r = N1.search_elements(search_id=N2.my_id)
        assert str(r) == "({}, [<generalcybernetics.Element id:2>])"

        # max depth test
        r = N1.search_elements(N5, max_depth=2)
        assert r == ({}, [])

    def test_search_payload(self):
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")
        N5 = basis.Element("5")

        N5.payload = 3.141

        N1.elements = [N2]
        N2.elements = [N3]
        N3.elements = [N4]
        N4.elements = [N5]

        r = N1.search_elements(3.141, max_depth=10)
        comp = "({'2': {'3': {'4': [<generalcybernetics.Element id:5>]}}}, [])"
        assert str(r) == comp
    
    def test_sort_order_connection_based(self):
        # never mind doing anything with it,
        # does it work based on connections?
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        
        N1.connect_lr(N2)
        N2.connect_lr(N3)
        
        mylist = [N3,N1,N2]
        fixed_list = basis.determine_execution_order(mylist)
        #print('fixed',fixed_list)
        assert fixed_list == [N1,N2,N3]
        
    def test_sort_correct_order(self):
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        
        
        N1.payload = {"this":[1,2,4,3]}
        N2.payload = basis.CyberCalculationPayload(basis.sort,"this")
        N3.payload = basis.CyberCalculationPayload(basis.mypass,"this")
        #N4.payload = # output?
        
        N1.connect_lr(N2)
        N2.connect_lr(N3)
        
        # so, I need to build... execution context and order of execution
        # before I can do something.
        
        mylist = [N1,N2,N3]

        fixed_list = basis.determine_execution_order(mylist)
        r = basis.execute_node_collection(fixed_list)
                
        assert N2.payload.last_result == [1,2,3,4]
        # assert something? 
        #raise NotImplementedError
    
    def test_sort_good_input(self):
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        
        # do nothing.
        N1.payload = None
        N2.payload = None
        N3.payload = None
        
        N1.connect_lr(N2)
        N2.connect_lr(N3)
        
        goodlist = [N1,N2,N3]
        out = basis.determine_execution_order(goodlist)
        
        assert goodlist == out
        
    def test_sort_bad_node_order(self):
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        
        
        N1.payload = {"this":[1,2,4,3]}
        N2.payload = basis.CyberCalculationPayload(basis.sort,"this")
        N3.payload = basis.CyberCalculationPayload(basis.mypass,"this")
        #N4.payload = # output?
        
        N1.connect_lr(N2)
        N2.connect_lr(N3)
        
        # so, I need to build... execution context and order of execution
        # before I can do something.
        
        goodlist = [N1,N2,N3]
        intentional_bad = [N3,N2,N1]
        mylist = intentional_bad
        #random.shuffle(mylist)
        
        fixed_list = basis.determine_execution_order(mylist)
        assert fixed_list == goodlist
        r = basis.execute_node_collection(fixed_list)
        
        assert N2.payload.last_result == [1,2,3,4]
        
    def test_calculation_multiple_inputs(self):
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")
        N5 = basis.Element("5")
        
        N1.payload = {"this":1}
        N2.payload = {"this":2}
        N3.payload = {"this":3}
        N4.payload = basis.CyberCalculationPayload(basis.mysum,"this")
        N5.payload = basis.CyberCalculationPayload(basis.mypass,"this")
        
        
        N1.connect_lr(N4)
        N2.connect_lr(N4)
        N3.connect_lr(N4)
        N4.connect_lr(N5)
        
        # so, I need to build... execution context and order of execution
        # before I can do something.
        
        goodlist = [N1,N2,N3,N4,N5]
        intentional_bad = [N5,N1,N2,N4,N3]
        mylist = intentional_bad
                
        fixed_list = basis.determine_execution_order(mylist)
        assert fixed_list == goodlist
        r = basis.execute_node_collection(fixed_list)
        
        assert N4.payload.last_result == 6
    
    
    def test_cycle_detection(self):
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")

        N1.connect_lr(N2)
        N2.connect_lr(N3)
        N3.connect_lr(N4)

        loops , loop_nodes = basis.cycle_detection ([N1,N2,N3,N4])
        
        assert len(loops)==0
        
        
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")

        N1.connect_lr(N2)
        N2.connect_lr(N3)
        N3.connect_lr(N4)
        N4.connect_lr(N1)
        
        loops , loop_nodes = basis.cycle_detection ([N1,N2,N3,N4])
        assert len(loops) > 0
        assert loops == [("4","1")]            
    
    def test_search_sideways_lr(self):
        # test side ways
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")

        N1.connect_lr(N2)
        N2.connect_lr(N3)
        N3.connect_lr(N4)

        # this will not return a path, because it's the first level
        r = N1.search_elements(N3)
        assert str(r) == "({'2': [<generalcybernetics.Element id:3>]}, [])"
        
        r = N1.search_elements(search_id=N3.my_id)
        assert str(r) == "({'2': [<generalcybernetics.Element id:3>]}, [])"

    def test_search_sideways_rl(self):
        # test side ways
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")

        N1.connect_rl(N2)
        N2.connect_rl(N3)
        N3.connect_rl(N4)

        # this will not return a path, because it's the first level
        r = N1.search_elements(N3)
        assert str(r) == "({'2': [<generalcybernetics.Element id:3>]}, [])"

        r = N1.search_elements(search_id=N3.my_id)
        assert str(r) == "({'2': [<generalcybernetics.Element id:3>]}, [])"

    def test_basic_construction_connection(self):

        S = basis.Element()

        N1 = basis.Element()
        N2 = basis.Element()
        N3 = basis.Element()

        N1.connect_lr(N2)  # -> this way
        N3.connect_rl(N2)  # <- that way

        S.elements = [N1, N2, N3]

    def test_sort(self):
        S = basis.Element()

        N1 = basis.Element()
        N2 = basis.Element()

        N1.connect_lr(N2)

        S.elements = [N2, N1]

        S.elements.sort()

        assert S.elements == [N1, N2]

    def test_dissolve(self):

        S = basis.Element()

        N1 = basis.Element()
        N2 = basis.Element()
        N3 = basis.Element()

        N1.connect_lr(N2)  # -> this way
        N3.connect_rl(N2)  # <- that way

        S.elements = [N1, N2, N3]

        S.dissolve(N2)

        assert S.elements[0] == N1
        assert S.elements[1] == N3
        assert N1.out_connections[0] == N3
        assert N3.in_connections[0] == N1

    def test_subdivide(self):
        S = basis.Element()

        N1 = basis.Element()
        N2 = basis.Element()

        S.elements = [N1, N2]

        N1.connect_lr(N2)
        S.subdivide_connection(N1, N2)
        S.elements.sort()

        N11 = S.elements[1]

        assert S.elements[0] == N1
        assert S.elements[2] == N2
        assert N1.out_connections[0] == N11
        assert N2.in_connections[0] == N11

    
    def test_simple_loop(self):
        # a cybernetic feedback loop example
        
        # disclaimer, if you just want the functionality, this is a very
        # bad way to do it, you can just roll everything into 1) python
        # and 2) a regular program, you don't need these layers of abstraction.
        # I'm putting the layers there, specifically because this case
        # represents an example for a collection of problems
        # that mostly work in a similar way and specifically
        # what action is required isn't important. and can be user defined.
        
        # TODO: build examples with 
        # errors in action, detection, comparison.
        # slow reaction speed (and then bad outcomes)
        
        # this is what I'm going to do today.
        # * input can just not work
        # * time delay ()
        # * message delay (that would be better with a connection object HMMMM)
        # * input can be wrong and varying, offset, scaled wrong, 
        # random (let's call this "scalar error") 
        # (and also, let's say it's correct when it's working within
        # some 5?% of some expected value or range? Hmmmmmm.
        
        # action 
        # * can just not work
        # * can have a scalar error as well
        # * also, time delay... not really message delay, since it's not messaging
        
        # compare
        # * can just not work
        # * scalar error
        # * message delay
        
        # feedback
        # * can also just not work
        # * scalar error in action magnitude(?) effect(?)
        # * error in calculation if an action is necessary or not.
        # (more of a binary logic / evaluation error)
        
        # If I get no input, what happens?
        # I may want some fault tolerance for HOW MUCH "packet loss" I have
        # 1) I can continue to use old values
        # 2) I can stop doing stuff
        # 3) random behavior (make things up)
        # 4) purposefully create something that looks correct but is made up.
        
        # execution behavior:
        # * squential (must wait for input or expects input "events")
        # * permanent, ongoing, (physical) -> any block, blocks the whole thing, -> gets "stuck" on a value.
        
        # test fault detection
        # would be, isolate the parts into a controlled environment
        # and see if they behave correctly in that environment
        # or create / procure a seperate "verified functioning"
        # system that creates "master output" to calibrate with.
        
        # input can take external input,
        # action applies a specific offset
        # compare compares whether action is necessary
        # feedback decides how much but also sets action? Hmm.. overlap.
            
        N1 = basis.Element("input")
        N2 = basis.Element("action")
        N3 = basis.Element("compare")
        N4 = basis.Element("feedback")
        
        # there was a way to bake inputs into functions.
        value_dict = {"value":0,"action":False,"target":-0.3,"reduce_amount":0.1,"compare_result":False}
        
        N1.payload = basis.InputObject(value_dict)
        N2.payload = basis.CyberCalculationPayload(basis.myaction,datakeywords = ["action","value","reduce_amount"])
        N3.payload = basis.CyberCalculationPayload(basis.compare,datakeywords = ["value","target"])
        N4.payload = basis.CyberCalculationPayload(basis.myfeedback,datakeywords = ["value","compare_result","action"])
        
        N1.connect_lr(N2)
        N2.connect_lr(N3)
        N3.connect_lr(N4)
        N4.connect_lr(N1)
            
        container = basis.Element("System")
        container.payload = basis.CyberContainer()
        container.elements = [N1,N2,N3,N4]
        
        basis.test_execute_container(container,graphical_output=False)
        
    def test_sensor_malfunction_off(self):
        
        N1 = basis.Element("input")
        N2 = basis.Element("action")
        N3 = basis.Element("compare")
        N4 = basis.Element("feedback")
        
        # there was a way to bake inputs into functions.
        value_dict = {"value":0,"action":False,"target":-0.3,"reduce_amount":0.1,"compare_result":False}
        
        # I guess my sensor is my input
        N1.payload = basis.InputObject(value_dict)
        N2.payload = basis.CyberCalculationPayload(basis.myaction)
        N3.payload = basis.CyberCalculationPayload(basis.compare)
        N4.payload = basis.CyberCalculationPayload(basis.myfeedback)
        
        N1.connect_lr(N2)
        N2.connect_lr(N3)
        N3.connect_lr(N4)
        N4.connect_lr(N1)
            
        container = basis.Element("System")
        container.payload = basis.CyberContainer()
        container.elements = [N1,N2,N3,N4]
        
        import math
        
        x = 0
        xs = [0]
        ys = [0]
        ys_controlled = [0]
        
        delta_t = 0.05 # how often do I do this, sine is continous.
        m = 2 * math.pi * 2 # run for two periods of sine curves
        
        running_data_dict = {"value":0,"action":False,"target":-0.3,"reduce_amount":0.2}
        
        exec_order = container.elements
        
        while x < m:
            xs.append(x)
            ys.append(math.sin(x)) # this is the completely undisturbed curve.
            
            # the controlled curve will not be built like this,
            # it will be "assembled by hand" via the derivative,
            # which we happen to know:
            diff = math.cos(x)
            running_data_dict["value"] += diff*delta_t
            
            # and then the effect of the system is built inside of the
            # system. Could be interesting to track the effect and output
            # but not for now.
            
            sub_loops, sub_loop_nodes = cycle_detection(exec_order)
    
            # hmmm.
            if optional_input != None:
                for node in exec_order:
                    if type(node.payload) == InputObject:
                        node.payload.overwrite_passed_value(optional_input)
                    
            error = None
            for focus_node in exec_order:
                if optional_input != None:
                    if type(focus_node.payload) == InputObject:
                        focus_node.payload.overwrite_passed_value(optional_input)
                
                print(focus_node,focus_node.payload)
                
                # this kind of explicit calling is interesting if
                # there is time delay between steps.
                step_result = execution_step(focus_node)
            
            # I'm copying the internal result to my external variable.
            running_data_dict = container.payload.last_result
            
            # record it for plotting (or logging)
            ys_controlled.append(running_data_dict["value"])
            
            assert ys_controlled[-1] > -0.5 
            # I guess this is good enough
            # for testing?
            
            # "natural cooling" where the state of the system
            # will "naturally" approach the undisturbed state
            
            # get the values
            last_controlled = ys_controlled[-1]
            last = ys[-1]
            
            # set the speed / mixing rate 
            cooling_rate = 5 * delta_t
            
            # this works out to be e.g. 80% of controlled system 20% of outside,
            
            # or different values, 20% of controlled system, 80% outside,
            # would mean in the very next time step 80% of the control 
            # effect is already gone, very fast cooling.
            
            running_data_dict["value"] = (1-cooling_rate) * last_controlled + cooling_rate * last
            
            # advance time.
            x += delta_t
        
        if graphical_output: #plot this?
            
            from matplotlib import pyplot as plt
            plt.plot(xs,ys_controlled ) #,marker="o"
            plt.plot(xs,ys)
        
            plt.plot([xs[0],xs[-1]],[-0.3,-0.3],color="red")
        
            #plt.show()
            plt.savefig("simple_control.png")
            
        
    # def test_sensor_malfunction_offset(self):
        # a=1
    # def test_sensor_malfunction_variation(self):
        # a=1
    # def test_sensor_malfunction_delayed(self):
        # a=1
        
        


def test_single():
    my_tests = TestMyCybernetics()
    #my_tests.test_sort_good_input()
    my_tests.test_simple_loop()


if __name__ == "__main__":
    #unittest.main()
    test_single()
