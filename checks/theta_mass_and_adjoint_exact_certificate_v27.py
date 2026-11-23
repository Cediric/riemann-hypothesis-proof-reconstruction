"""V2.7 exact finite diagnostics for groupoid mass, minimal denominators,
weighted adjoints/composition/HS, and adjoint-invariance counterexample.
These tests do NOT prove general Theta/Rallis arithmetic hypotheses.
"""
from fractions import Fraction as Q
from itertools import permutations, product
from math import lcm
from sympy import Matrix, Rational, I, conjugate, simplify

H=list(permutations(range(3)))
e=(0,1,2)
def mul(x,y):return tuple(x[y[i]] for i in range(3))
assert all(mul(a,mul(b,c))==mul(mul(a,b),c) for a,b,c in product(H,repeat=3))
C2=[e,(1,0,2)]
C3=[e,(1,2,0),(2,0,1)]
for subgroup in (C2,C3,H):
    assert all(mul(a,b) in subgroup for a,b in product(subgroup,repeat=2))

def left_cosets(subgroup):
    return set(frozenset(mul(g,h) for h in subgroup) for g in H)
cs=[left_cosets(T) for T in (C2,C3,H)]
assert [len(X) for X in cs]==[3,2,1]
stabs=[2,3,6]
assert sum((Q(1,s) for s in stabs),Q())==Q(sum(map(len,cs)),len(H))==1
D=lcm(*stabs)
assert D==6 and D<2*3*6
count=0
for vals in product(range(-3,4),repeat=3):
    lhs=sum((Q(len(cs[i])*vals[i],len(H)) for i in range(3)),Q())
    rhs=sum((Q(vals[i],stabs[i]) for i in range(3)),Q())
    assert lhs==rhs and (D*rhs).denominator==1
    count+=1
for d in range(1,D):
    assert any((Q(d,s).denominator!=1 for s in stabs))

bden=[4,9,5]
Dstar=lcm(*(s*b for s,b in zip(stabs,bden)))
assert Dstar==1080
for v in range(3):
    assert (Dstar*Q(1,stabs[v]*bden[v])).denominator==1
for d in range(1,Dstar):
    assert any(Q(d,s*b).denominator!=1 for s,b in zip(stabs,bden))

# Complex example, with positive rational source/target weights.
a=[Rational(1,2),Rational(1,3),Rational(1,6)]
b=[Rational(1,3),Rational(2,3)]
K=Matrix([[1,I],[2,-1],[1+I,3]])
f=Matrix([1+I,2,-I]);g=Matrix([2-I,3+I])
A=Matrix.diag(*a);B=Matrix.diag(*b)
T=K.T*A
Tadj=K.conjugate()*B
inner=lambda x,y,w: (x.conjugate().T*w*y)[0]
assert simplify(inner(T*f,g,B)-inner(f,Tadj*g,A))==0
L=Matrix([[1,2],[I,3]])
assert (L.T*B*T-L.T*B*K.T*A).applyfunc(simplify)==Matrix.zeros(2,3)
assert (L.T*B*T-(K*B*L).T*A).applyfunc(simplify)==Matrix.zeros(2,3)
source=inner(f,f,A)
target=inner(T*f,T*f,B)
hs=sum(a[i]*b[j]*K[i,j]*conjugate(K[i,j]) for i in range(3) for j in range(2))
assert simplify(hs*source-target).is_nonnegative

# Orthogonal compression identity does not imply global scalar on S.
theta=Matrix([[1,1]])
e1=Matrix([1,0]);adj=theta.conjugate().T*theta
assert (theta*e1)[0]==1
assert adj*e1==Matrix([1,1]) and adj*e1 != e1
assert Matrix([[1,1],[1,1]]).rank()==1
print('orbit mass: 3 S3 homogeneous spaces, sizes',list(map(len,cs)),'stabilizers',stabs)
print('invariant functions checked:',count,'minimum universal stabilizer denominator:',D)
print('two-layer minimum universal denominator:',Dstar)
print('weighted adjoint, weighted kernel composition, HS bound: exact symbolic pass')
print('Rallis subspace adjoint non-invariance counterexample: exact pass')
print('NOTE: finite arithmetic is diagnostic only; no arithmetic Theta norm claims.')