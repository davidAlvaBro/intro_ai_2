from main import *
import sympy

class TestAGMReveision:
    def test_closure(self):
        p,q,r = sympy.symbols('p q r')
        expressions = {(p), (q), (r)}

        BR = Belief_Revisor(expressions)

        assert BR.entails(q) == True
        phi = ~(q | r)
        BR.revision(phi)
        assert BR.entails(q) == False
    def test_success(self):
        p,q = sympy.symbols('p q')
        expressions = {}

        BR = Belief_Revisor(expressions)

        assert BR.entails(p & q) == False
        phi = (p & q)
        BR.revision(phi)
        assert BR.entails(p & q) == True
    def test_inclusion(self):
        p,q = sympy.symbols('p q')
        expressions = {(~p), (q)}
        BR1 = Belief_Revisor(expressions)
        BR2 = Belief_Revisor(expressions)
        assert BR1.entails(p) == False
        assert BR2.entails(p) == False
        phi = p
        BR1.expansion(phi)
        BR2.revision(phi)
        print(BR1.KB)
        print(BR2.KB)
        assert BR1.entails(p) == True
        assert BR1.entails(~p) == True
        assert BR2.entails(p) == True
        assert BR2.entails(~p) == False
    def test_vacuity(self):
        p,q = sympy.symbols('p q')
        expressions = {(q)}
        BR1 = Belief_Revisor(expressions)
        BR2 = Belief_Revisor(expressions)
        phi = p
        assert BR1.entails(~phi) == False
        assert BR2.entails(~phi) == False
        BR1.revision(phi)
        BR2.expansion(phi)
        assert BR1.entails(phi) == True
        assert BR2.entails(phi) == True
        assert BR1.entails(~phi) == False
        assert BR2.entails(~phi) == False
    def test_consistency(self):
        p,q = sympy.symbols('p q')
        expressions = {}
        BR = Belief_Revisor(expressions)
        assert BR.entails(p) == False
        phi = (p | q)
        BR.revision(phi)
        assert BR.entails(p | q) == True
        

        #TODO Må vi godt have inconsistent ting i vores KB? entails siger at det ikke entailer, men det er i vores KB alligevel.
        BR = Belief_Revisor(expressions)
        assert BR.entails(p) == False
        phi = (p & ~p)
        BR.revision(phi)
        assert BR.entails(p & ~p) == False
        print(BR.KB)
        assert 1 == 2

        
    def test_extensionality(self):
        p,q = sympy.symbols('p q')
        expressions = {}
        BR = Belief_Revisor(expressions)
        phi1 = (p & q)
        phi2 = (q & p)
        BR.revision(phi1)
        BR.revision(phi2)
        print(BR.KB)
        assert len(BR.KB) == 1
        assert BR.entails(phi1)
        assert BR.entails(phi2)
        
    def test_superexpansion(self):
        p,q = sympy.symbols('p q')
        expressions = {}
        BR = Belief_Revisor(expressions)

        phi = p & q
        BR.revision(p)
        BR.expansion(q)

        assert BR.entails(phi) == True

    def test_subexpansion(self):
        pass
        # TODO IMPLEMENT
        '''
        p,q = sympy.symbols('p q')
        expressions = {}
        BR = Belief_Revisor(expressions)

        assert 
        phi 
        BR.revision(phi)
        assert 
        '''