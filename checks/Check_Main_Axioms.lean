import Main

/-!
Copy this file into the root of the pinned upstream Lean project after dependencies
and the complete Main target have built successfully.

Run:
  lake env lean Check_Main_Axioms.lean

Record the exact Lean toolchain, upstream commit, command output, and machine details.
A #print axioms result is a dependency audit, not a substitute for the successful
build or independent kernel replay.
-/

#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive

#print axioms allChi
#print axioms rhOfAll
#print axioms critAll
#print axioms claimAll

#print axioms UpperTheory.FinalTheorems.everyCharacter
#print axioms UpperTheory.FinalTheorems.riemannHypothesis
#print axioms Formalism.VW.rh_of_every
#print axioms Formalism.VW.critLine
