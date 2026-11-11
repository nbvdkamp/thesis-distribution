
Theorem H : 1 < let x := 1 in S(x).
Proof.
  simpl.
  apply le_n.
Qed.

(* We don't support zeta reduction so this doesn't find anything *)
Search 2 in local_binding_unfolding.