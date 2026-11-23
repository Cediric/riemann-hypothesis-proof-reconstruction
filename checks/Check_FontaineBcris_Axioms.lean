import Development.AbelianVarietyTheory.Proofs.InertiaEigenvalues.FontaineBcrisBasicTheoremsProof

/-!
Copy this file into the root of the pinned upstream Lean project after its dependencies are available.
Run the following command from that upstream project root:
  lake env lean Check_FontaineBcris_Axioms.lean

This is a diagnostic script. It does not replace lake build Main or an independent
kernel replay. Preserve the exact Lean version and upstream commit with the output.
-/

#print axioms GlobalTheory.MemLoc.fontaineBcris
#print axioms GlobalTheory.MemLoc.fontaineBcris_of_tensorInj

#print axioms GlobalTheory.MemLoc.phiB_injective
#print axioms GlobalTheory.MemLoc.PhiInj.phiA_injective
#print axioms GlobalTheory.MemLoc.ULaws.iota_injective
#print axioms GlobalTheory.MemLoc.ULaws.u_laws
#print axioms GlobalTheory.MemLoc.crisP_injective
#print axioms GlobalTheory.MemLoc.exists_iota_cris_dR

#print axioms GlobalTheory.MemLoc.TensorInj.tensorInj
#print axioms GlobalTheory.MemLoc.fundamental_exact
#print axioms GlobalTheory.MemLoc.FundOnto.fundOnto
#print axioms GlobalTheory.MemLoc.one_sub_phi_onto
#print axioms GlobalTheory.MemLoc.core_regular
#print axioms GlobalTheory.MemLoc.regular_of_tensorInj

#print axioms GlobalTheory.Published.FontaineBcris.of_rest
