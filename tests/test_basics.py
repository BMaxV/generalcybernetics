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
    
    
        
    def test_calculation_setup_1(self):
        """correct order"""
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        
        
        N1.payload = {"this":[1,2,4,3]}
        N2.payload = basis.CyberCalculationPayload(basis.sort,"this")
        N3.payload = basis.CyberCalculationPayload(basis.myprint,"this")
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
        
    def test_calculation_setup_2(self):
        """bad order"""
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        
        
        N1.payload = {"this":[1,2,4,3]}
        N2.payload = basis.CyberCalculationPayload(basis.sort,"this")
        N3.payload = basis.CyberCalculationPayload(basis.myprint,"this")
        #N4.payload = # output?
        
        N1.connect_lr(N2)
        N2.connect_lr(N3)
        
        # so, I need to build... execution context and order of execution
        # before I can do something.
        
        goodlist = [N1,N2,N3]
        intentional_bad = [N3,N2,N1]
        mylist = intentional_bad
        #random.shuffle(mylist)
        #print("shuffled",mylist)
        
        fixed_list = basis.determine_execution_order(mylist)
        assert fixed_list == goodlist
        r = basis.execute_node_collection(fixed_list)
        
        assert N2.payload.last_result == [1,2,3,4]
        
    def test_calculation_setup_3(self):
        """multiple inputs"""
        N1 = basis.Element("1")
        N2 = basis.Element("2")
        N3 = basis.Element("3")
        N4 = basis.Element("4")
        N5 = basis.Element("5")
        
        N1.payload = {"this":1}
        N2.payload = {"this":2}
        N3.payload = {"this":3}
        N4.payload = basis.CyberCalculationPayload(basis.mysum,"this")
        N5.payload = basis.CyberCalculationPayload(basis.myprint,"this")
        
        
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
        print(loops)
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


def test_single():
    my_tests = TestMyCybernetics()
    my_tests.test_cycle_detection()


if __name__ == "__main__":
    unittest.main()
    #test_single()
