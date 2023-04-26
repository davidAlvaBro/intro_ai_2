from main import *
import sympy

class TestAGMContration:
    def test_closure(self):
        p,q = sympy.symbols('p q')
        expressions = {(p & ~q)}
        BR = Belief_Revisor(expressions)
        assert BR.entails(~q) == True

        phi = ~q
        # B÷φ = Cn(B÷φ)
        BR.contract(phi)
        assert BR.entails(p & ~q) == False
    def test_success(self):
        p = sympy.symbols('p')
        expressions = {p}
        BR = Belief_Revisor(expressions)
        print(BR.KB)
        # TODO: Maybe change phi back to (p | ~p) and expr to {}, depending on the implementation of tautologies
        # If φ ∈/ Cn(∅) (phi isn't a tautology) 
        phi = (p)
        assert BR.entails(phi) == True
        # Then φ ∈/ Cn(B ÷ φ)
        BR.contract(phi)
        assert BR.entails(phi) == False
    def test_inclusion(self):
        p,q = sympy.symbols('p q')
        expressions = {(p), (q)}
        BR = Belief_Revisor(expressions)
        phi = p
        assert BR.entails(q) == True
        assert BR.entails(phi) == True
        # B÷φ ⊆ B
        BR.contract(phi)
        assert BR.entails(q) == True
        assert BR.entails(phi) == False
    def test_vacuity(self):
        p,q,r = sympy.symbols('p q r')
        # If φ ∈/ Cn(B)
        expressions = {(q & r)}
        BR = Belief_Revisor(expressions)
        assert BR.entails(q & r) == True
        # Then B ÷ φ = B
        phi = p
        BR.contract(phi)
        assert BR.entails(q & r) == True
    def test_extensionality(self):
        p,q,r  = sympy.symbols('p q r')
        expressions = {(p & q),(r)}
        BR1 = Belief_Revisor(expressions)
        BR2 = Belief_Revisor(expressions)
        # If (φ ↔ ψ) ∈ Cn(∅)
        phi1 = (p & q)
        phi2 = (q & p)
        BR1.contract(phi1)
        BR2.contract(phi2)
        # Then B÷φ = B÷ψ
        assert len(BR1.KB) == 1
        assert len(BR2.KB) == 1
        # Test with the opposite, to verify not entailed.
        assert BR1.entails(phi2) == False
        assert BR2.entails(phi1) == False
        assert BR1.entails(r) == True
        assert BR2.entails(r) == True
    def test_recovery(self):
        p,q,r = sympy.symbols('p q r')
        expressions = {(p & q), (q & r), (r | p)}

        BR = Belief_Revisor(expressions)
        assert BR.entails(p & q) == True
        assert BR.entails(q & r) == True
        assert BR.entails(r | p) == True
        phi = p
        #B ⊆ (B ÷φ)+φ
        BR.contract(phi)
        BR.expansion(phi)
        assert BR.entails(p & q) == True
        assert BR.entails(q & r) == True
        assert BR.entails(r | p) == True
    def test_conj_inclusion(self):
        p,q = sympy.symbols('p q')
        expressions = {(p): 1, (q):2 }
        BR1 = Belief_Revisor(expressions)
        BR2 = Belief_Revisor(expressions)

        phi = p
        psi = q
        expr = phi & psi
        # If φ ∈/ B÷(φ∧ψ)
        assert BR1.entails(phi) == True
        assert BR1.entails(psi) == True
        BR1.contract(expr)
        # TODO It does something weird, where it remove psi instead of phi
        assert BR1.entails(phi) == False
        assert BR1.entails(psi) == True
        # Then B÷(φ∧ψ) ⊆ B÷φ
        BR2.contract(phi)
        assert BR2.entails(phi) == False
        assert BR2.entails(psi) == True


    def test_conj_overlap(self):
        pass
        '''
        p,q,r = sympy.symbols('p q r')
        expressions = {(p), (q), (r)}

        BR = Belief_Revisor(expressions)
        assert BR.entails(q) == True
        # B*φ = Cn(B*φ)
        phi = ~(q | r)
        BR.revision(phi)
        assert BR.entails(q) == False
        '''