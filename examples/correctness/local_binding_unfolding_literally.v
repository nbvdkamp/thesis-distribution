Eval cbv zeta in let x := 1 in S(x).
Eval cbv delta beta in 1 < let x := 1 in S(x).

Theorem H : 1 < let x := 1 in S(x).
Proof.
  simpl.
  apply le_n.
Qed.

Search (let x := 1 in S(x)) in local_binding_unfolding_literally.