Definition x1 := 1.
Definition x2 := x1 + x1.

Definition y1 := 1.
Definition y2 := y1 + y1.

Theorem H : 1 < x2. Proof. unfold x2. unfold x1. apply le_n. Qed.

Search (y2) in double_unfold_both_sides. (* New: H *)
Search (S(_) + O) in double_unfold_both_sides. (* No new results *)
