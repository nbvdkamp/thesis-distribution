Definition one := 1.
Definition two := one + one.
Lemma three : two + one = 3. Proof. reflexivity. Qed.
Search (one + one) in more_unfolding. (* New: three *)
