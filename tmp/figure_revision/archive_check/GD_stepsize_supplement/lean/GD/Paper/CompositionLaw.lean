import GD.Balanced

/-!
The manuscript's abstract law is defined only on the nonnegative quadrant.
This interface imposes every law only there. Clamping inputs to zero supplies
an extension usable by the original implementation, with no assumption about
the original operation at negative inputs.
-/

namespace GD
noncomputable section

structure NonnegativeCompositionLaw where
  op : ℝ → ℝ → ℝ
  scale : ℝ
  scale_gt_one : 1 < scale
  nonneg : ∀ {x y}, 0 ≤ x → 0 ≤ y → 0 ≤ op x y
  comm : ∀ {x y}, 0 ≤ x → 0 ≤ y → op x y = op y x
  zero_left : ∀ {x}, 0 ≤ x → op 0 x = x
  diag : ∀ {x}, 0 ≤ x → op x x = scale * x
  hom : ∀ {t x y}, 0 ≤ t → 0 ≤ x → 0 ≤ y → op (t * x) (t * y) = t * op x y
  strict_left : ∀ {x x' y}, 0 ≤ x → 0 ≤ y → x < x' → op x y < op x' y
  rearr : ∀ {a b c d}, 0 ≤ a → a ≤ b → b ≤ c → c ≤ d →
    op (op a b) (op c d) ≤ op (op a c) (op b d) ∧
    op (op a c) (op b d) ≤ op (op a d) (op b c)

namespace NonnegativeCompositionLaw

def extend (C : NonnegativeCompositionLaw) : CompositionLaw where
  op x y := C.op (max 0 x) (max 0 y)
  scale := C.scale
  scale_gt_one := C.scale_gt_one
  nonneg := by
    intro x y hx hy
    exact C.nonneg (le_max_left _ _) (le_max_left _ _)
  comm := by
    intro x y
    exact C.comm (le_max_left _ _) (le_max_left _ _)
  zero_left := by
    intro x hx
    simpa only [max_self, max_eq_right hx] using C.zero_left hx
  diag := by
    intro x hx
    simpa only [max_eq_right hx] using C.diag hx
  hom := by
    intro t x y ht hx hy
    simpa only [max_eq_right (mul_nonneg ht hx), max_eq_right (mul_nonneg ht hy),
      max_eq_right hx, max_eq_right hy] using C.hom ht hx hy
  strict_left := by
    intro x x' y hx hy hxx
    simpa only [max_eq_right hx, max_eq_right hy, max_eq_right (hx.trans hxx.le)]
      using C.strict_left hx hy hxx
  rearr := by
    intro a b c d ha hab hbc hcd
    have hb := ha.trans hab
    have hc := hb.trans hbc
    have hd := hc.trans hcd
    simpa only [max_eq_right ha, max_eq_right hb, max_eq_right hc, max_eq_right hd,
      max_eq_right (C.nonneg ha hb), max_eq_right (C.nonneg hc hd),
      max_eq_right (C.nonneg ha hc), max_eq_right (C.nonneg hb hd),
      max_eq_right (C.nonneg ha hd), max_eq_right (C.nonneg hb hc)]
      using C.rearr ha hab hbc hcd

theorem extend_op_eq (C : NonnegativeCompositionLaw) {x y : ℝ}
    (hx : 0 ≤ x) (hy : 0 ≤ y) : C.extend.op x y = C.op x y := by
  change C.op (max 0 x) (max 0 y) = C.op x y
  rw [max_eq_right hx, max_eq_right hy]

def V (C : NonnegativeCompositionLaw) : ℕ → ℝ := C.extend.V

theorem V_nonneg (C : NonnegativeCompositionLaw) (n : ℕ) : 0 ≤ C.V n :=
  C.extend.V_nonneg n

@[simp] theorem V_zero (C : NonnegativeCompositionLaw) : C.V 0 = 0 :=
  C.extend.V_zero

@[simp] theorem V_one (C : NonnegativeCompositionLaw) : C.V 1 = 1 :=
  C.extend.V_one

theorem V_rec (C : NonnegativeCompositionLaw) {N : ℕ} (hN : 2 ≤ N) :
    C.V N = C.op (C.V (N / 2)) (C.V ((N + 1) / 2)) := by
  have h := C.extend.V_rec hN
  change C.V N = C.extend.op (C.V (N / 2)) (C.V ((N + 1) / 2)) at h
  rw [C.extend_op_eq (C.V_nonneg _) (C.V_nonneg _)] at h
  exact h

theorem bellman_nonneg (C : NonnegativeCompositionLaw) (W : ℕ → ℝ)
    (hW : BellmanSpec C.op W) (N : ℕ) (hN : 1 ≤ N) : 0 ≤ W N := by
  induction N using Nat.strong_induction_on with
  | h N ih =>
    by_cases hn : N = 1
    · subst N
      rw [hW.1]
      norm_num
    · obtain ⟨m, hm, hmN, he⟩ := hW.2.2 N (by omega)
      rw [he]
      exact C.nonneg (ih m hmN hm) (ih (N - m) (by omega) (by omega))

theorem balanced_optimality (C : NonnegativeCompositionLaw) :
    StrictMono C.V ∧
    (∀ m n : ℕ, C.op (C.V m) (C.V n) ≤ C.V (m + n)) ∧
    (∀ W : ℕ → ℝ, BellmanSpec C.op W → ∀ N : ℕ, 1 ≤ N → W N = C.V N) := by
  refine ⟨C.extend.V_strictMono, ?_, ?_⟩
  · intro m n
    have h := C.extend.supercomposition m n
    change C.extend.op (C.V m) (C.V n) ≤ C.V (m + n) at h
    rw [C.extend_op_eq (C.V_nonneg m) (C.V_nonneg n)] at h
    exact h
  · intro W hW N hN
    have hW' : BellmanSpec C.extend.op W := by
      refine ⟨hW.1, ?_, ?_⟩
      · intro j hj m hm hmj
        rw [C.extend_op_eq (C.bellman_nonneg W hW m hm)
          (C.bellman_nonneg W hW (j - m) (by omega))]
        exact hW.2.1 j hj m hm hmj
      · intro j hj
        obtain ⟨m, hm, hmj, he⟩ := hW.2.2 j hj
        refine ⟨m, hm, hmj, ?_⟩
        rw [C.extend_op_eq (C.bellman_nonneg W hW m hm)
          (C.bellman_nonneg W hW (j - m) (by omega))]
        exact he
    exact C.extend.bellman_unique W hW' N hN

end NonnegativeCompositionLaw
end
end GD
