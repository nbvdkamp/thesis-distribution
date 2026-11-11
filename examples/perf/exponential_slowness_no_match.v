Definition x1 := 1.
Definition x2 := x1 + x1.
Definition x3 := x2 + x2.
Definition x4 := x3 + x3.
Definition x5 := x4 + x4.
Definition x6 := x5 + x5.
Definition x7 := x6 + x6.
Definition x8 := x7 + x7.
Definition x9 := x8 + x8.
Definition x10 := x9 + x9.
Definition x11 := x10 + x10.
Definition x12 := x11 + x11.
Definition x13 := x12 + x12.
Definition x14 := x13 + x13.
Definition x15 := x14 + x14.
Definition x16 := x15 + x15.
Definition x17 := x16 + x16.
Definition x18 := x17 + x17.
Definition x19 := x18 + x18.
Definition x20 := x19 + x19.

Theorem big : 1 < x20. Proof. Admitted.

(* Here we end up searching the whole unfold tree because we don't find a match.
Ideally we would remember that x1 doesn't subterm-match the pattern, so we can skip the second occurence,
then the same for x2 and so on so it's linear. *)
Search (_ * _) in exponential_slowness_no_match.