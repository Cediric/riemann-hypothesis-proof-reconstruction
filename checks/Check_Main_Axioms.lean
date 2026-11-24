import Statements
import Supplements.Kernels.MainTheorems

/-!
Targeted audit of the actual RH/GRH theorem module.

This deliberately imports Supplements.Kernels.MainTheorems rather than Main:
Main additionally imports unrelated small-class-number modules. The theorem
chain under audit is the one used to derive RH and Dirichlet L-function
nonvanishing/critical-line results.

Run from the pinned upstream source root:
  lake build Supplements.Kernels.MainTheorems
  lake env lean Check_Main_Axioms.lean

A successful result is a Lean kernel dependency audit, not an independent
mathematical verification of every upstream theorem.
-/

#print axioms allChi
#print axioms rhOfAll
#print axioms critAll
#print axioms claimAll

#print axioms UpperTheory.FinalTheorems.everyCharacter_of_row
#print axioms UpperTheory.FinalTheorems.everyCharacter
#print axioms UpperTheory.FinalTheorems.riemannHypothesis

#print axioms Formalism.VW.rh_of_every
#print axioms Formalism.VW.critLine
