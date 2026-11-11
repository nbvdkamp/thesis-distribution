Definition one_plus_one := 1 + 1.
Eval cbv delta in one_plus_one.
Theorem two : one_plus_one = 2. Proof. reflexivity. Qed.
Search (_ + _) in unfold_too_far. (* if no unfolding is applied to the pattern `two` isn't found because + gets unfolded *) (* New: two *)