Definition injective {A B : Type} (f : A -> B) := forall x y, f x = f y -> x = y.

Theorem negb_injective :
    injective negb.
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

Search injective. (* finds negb_injective *)
Search "injective". (* finds both because their names contain "injective" *)

Search (?f ?x = ?f ?y -> ?x = ?y). (* finds neither *) (* New: negb_injective *)
Search (negb ?x = negb ?y -> ?x = ?y). (* finds neither *)