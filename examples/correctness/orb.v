
Inductive bool : Type :=
  | true
  | false.

Definition negb (b:bool) : bool :=
  match b with
  | true => false
  | false => true
  end.

Definition andb (b1 b2 : bool) : bool :=
  match b1 with
  | true => b2
  | false => false
  end.

Definition orb (b1 b2 : bool) : bool :=
  match b1 with
  | true => true
  | false => b2
  end.

Definition orb' (b1 b2 : bool) : bool :=
    negb (andb (negb b1) (negb b2)).

Definition norb' (b1 b2 : bool) : bool :=
    negb (orb' b1 b2).


Theorem orb_negb_nand_equivalent : forall b1 b2,
    orb b1 b2 = orb' b1 b2.
Proof.
    intros b1 b2.
    destruct b1.
    - destruct b2.
      + reflexivity.
      + reflexivity.
    - destruct b2.
      + reflexivity.
      + reflexivity.
Qed.

Theorem norb_norb'_equivalent : forall b1 b2,
    negb (orb b1 b2) = norb' b1 b2.
Proof.
    intros b1 b2.
    unfold norb'.
    f_equal.
    apply orb_negb_nand_equivalent.
Qed.

Theorem norb_unfolded_equivalent : forall b1 b2,
    negb (orb b1 b2) = negb(orb' b1 b2).
Proof.
    intros b1 b2.
    f_equal.
    apply orb_negb_nand_equivalent.
Qed.

Search (orb' ?a ?b). (* New: norb_norb'_equivalent *)
