from generalcybernetics import basis
import unittest

class TestMyCybernetics(unittest.TestCase):
        

    def test_basic_construction_connection(self):
        
        S = basis.System()
        
        N1=basis.Element()
        N2=basis.Element()
        N3=basis.Element()
        
        N1.connect_lr(N2)# -> this way
        N3.connect_rl(N2)# <- that way
        
        S.elements=[N1,N2,N3]
    
    def test_sort(self):
        S=basis.System()
        
        N1=basis.Element()
        N2=basis.Element()
        
        N1.connect_lr(N2)
        
        S.elements=[N2,N1]
        
        S.elements.sort()
                
        assert S.elements == [N1,N2]
        
    def test_dissolve(self):
        
        S=basis.System()
        
        N1=basis.Element()
        N2=basis.Element()
        N3=basis.Element()
        
        N1.connect_lr(N2)# -> this way
        N3.connect_rl(N2)# <- that way
        
        S.elements=[N1,N2,N3]
        
        S.dissolve(N2)
        
        assert S.elements[0]==N1
        assert S.elements[1]==N3
        assert N1.out_connections[0]==N3
        assert N3.in_connections[0]==N1

        
    def test_subdivide(self):
        S=basis.System()
        
        N1=basis.Element()
        N2=basis.Element()
        
        S.elements=[N1,N2]
        
        N1.connect_lr(N2)
        S.subdivide_connection(N1,N2)
        S.elements.sort()
                
        N11=S.elements[1]
        
        assert S.elements[0]==N1
        assert S.elements[2]==N2
        assert N1.out_connections[0]==N11
        assert N2.in_connections[0]==N11
        

if __name__ == "__main__":
    unittest.main()
