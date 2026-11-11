Theorem negb_injective1 :
    forall x y,  negb x = negb y -> x = y.
Proof.
    intros x y H.
    destruct x.
    - destruct y.
      + reflexivity.
      + discriminate H.
    - destruct y.
      + discriminate H.
      + reflexivity.
Qed.

Theorem negb_injective2 :
    forall x y,  (fun x => negb x) x = (fun x => negb x) y -> x = y.
Proof.
    intros x y H.
    destruct x.
    - destruct y.
      + reflexivity.
      + discriminate H.
    - destruct y.
      + discriminate H.
      + reflexivity.
Qed.

Search (?f ?x = ?f ?y -> ?x = ?y). (* finds 1 & 2 *)