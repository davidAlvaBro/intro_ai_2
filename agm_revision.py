from main import *
import sympy

class TestAGMReveision:
    def test_closure(self):
        p,q,r = sympy.symbols('p q r')
        expressions = [(p), (q), (r)]

        BR = Belief_Revisor(expressions, 3)
        assert BR.entails(q) == True
        # B*φ = Cn(B*φ)
        phi = ~(q | r)
        BR.revision(phi)
        assert BR.entails(q) == False
    def test_success(self):
        p,q = sympy.symbols('p q')
        expressions = []
        BR = Belief_Revisor(expressions, 3)
        # φ ∈ B*φ
        phi = (p & q)
        assert BR.entails(phi) == False
        BR.revision(phi)
        assert BR.entails(phi) == True
    def test_inclusion(self):
        p,q = sympy.symbols('p q')
        expressions = [(~p), (q)]
        BR1 = Belief_Revisor(expressions, 3)
        BR2 = Belief_Revisor(expressions, 3)
        phi = p
        # B+φ
        assert BR1.entails(phi) == False
        BR1.expansion(phi)
        assert BR1.entails(p) == True
        assert BR1.entails(~p) == True

        # B*φ ⊆ B+φ
        assert BR2.entails(phi) == False
        BR2.revision(phi)
        assert BR2.entails(p) == True
        assert BR2.entails(~p) == False
    def test_vacuity(self):
        p,q = sympy.symbols('p q')
        expressions = [(q)]
        BR1 = Belief_Revisor(expressions, 3)
        BR2 = Belief_Revisor(expressions, 3)
        phi = p
        #  If ¬φ ∈/ B
        assert BR1.entails(~phi) == False
        assert BR2.entails(~phi) == False
        # Then B*φ = B+φ
        BR1.revision(phi)
        BR2.expansion(phi)
        assert BR1.entails(phi) == True
        assert BR2.entails(phi) == True
        assert BR1.entails(~phi) == False
        assert BR2.entails(~phi) == False
    def test_consistency(self):
        p,q = sympy.symbols('p q')
        expressions = []
        BR1 = Belief_Revisor(expressions, 3)
        assert BR1.entails(p | q) == False
        # if φ is consistent
        phi = (p | q)
        BR1.revision(phi)
        # B*φ is consistent
        assert BR1.entails(p | q) == True
        # Check if φ is inconsistent
        BR2 = Belief_Revisor(expressions, 3)
        assert BR2.entails(p) == False
        phi = (p & ~p)
        BR2.revision(phi)
        # B*φ is inconsistent
        assert BR2.entails(p & ~p) == False
    def test_extensionality(self):
        p,q = sympy.symbols('p q')
        expressions = []
        BR = Belief_Revisor(expressions, 3)
        # If (φ ↔ ψ) ∈ Cn(∅)
        phi1 = (p & q)
        phi2 = (q & p)
        BR.revision(phi1)
        BR.revision(phi2)
        # then B*φ = B*ψ
        assert len(BR.KB) == 1
        assert BR.entails(phi1) == True
        assert BR.entails(phi2) == True  
    def test_superexpansion(self):
        p,q = sympy.symbols('p q')
        expressions = []

        # (B*φ)+ψ
        BR = Belief_Revisor(expressions, 3)
        BR.revision(p)
        BR.expansion(q)

        # B*(φ∧ψ)⊆(B*φ)+ψ
        phi = p & q
        assert BR.entails(phi) == True
    def test_subexpansion(self):
        p,q = sympy.symbols('p q')
        expressions = []
        # If ¬ψ ∈/ B*φ
        BR1 = Belief_Revisor(expressions, 3)
        BR1.revision(p)
        assert BR1.entails(~q) == False

        # then (B*φ)+ψ ⊆ B*(φ∧ψ)
        BR2 = Belief_Revisor(expressions, 3)
        phi = p & q
        BR2.revision(phi)
        assert BR2.entails(p) == True
        assert BR2.entails(q) == True
        