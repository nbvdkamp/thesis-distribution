Definition one := S(O).
Definition two := S(one).
Lemma H : 2 = two. Proof. reflexivity. Qed.

Search one. (* New: H *)
