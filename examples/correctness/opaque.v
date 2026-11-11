Definition double : forall n : nat, nat.
Proof.
  intros n.
  induction n as [ | n' IHn'].
  - exact O.
  - exact (S (S IHn')).
Defined.

Lemma n_le_double : forall n, n <= double n.
Proof. 
  induction n as [| n' IHn'].
  - apply le_0_n.
  - simpl.
    apply le_S.
    apply le_n_S.
    apply IHn'.
Qed.

Definition opaque_double : forall n : nat, nat.
Proof.
  intros n.
  induction n as [ | n' IHn'].
  - exact O.
  - exact (S (S IHn')).
Qed.

Lemma n_le_opaque_double : forall n, n <= opaque_double n.
Proof. Admitted.

Search (S(S _)) in opaque. (* New: n_le_double *)
