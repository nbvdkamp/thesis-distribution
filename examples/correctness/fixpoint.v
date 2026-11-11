Fixpoint add (n : nat) (m : nat) :=
match n with
| O => m
| S n' => S(add n' m)
end.

Theorem H : forall x, S x = add x 1.
Proof.
  intros x.
  induction x as [| x' IHx'].
  - reflexivity.
  - simpl.
    rewrite IHx'.
    reflexivity.
Qed.
    

Search (fix add (n m : nat) {struct n} : nat := match n with 0 => m | S n' => S (add n' m) end) in fixpoint. (* New: H *)
