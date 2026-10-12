import GD.Conjugacy
import GD.KernelRatios
import GD.TreeCounts
import GD.Paper.CompositionLaw

/-!
# Composition results of `GD_stepsize_schedule.pdf`

Public statements follow the revised manuscript's numbering. The underlying
kernel and tree proofs are reused independently of their historical numbering.
The certificate interfaces quoted from other papers in Appendix A are external
to the scalar and recursive-tree model formalized here.
-/

namespace GD
noncomputable section

namespace PaperTargets

/-- Balanced recurrence, strict growth, supercomposition, and every equality case. -/
def theorem_3_1 : Prop :=
  (∀ N : ℕ, 2 ≤ N → U N = K (U (N / 2)) (U ((N + 1) / 2))) ∧
  StrictMono U ∧
  (∀ m n : ℕ, K (U m) (U n) ≤ U (m + n)) ∧
  (∀ m n : ℕ, 1 ≤ m → 1 ≤ n →
    (K (U m) (U n) = U (m + n) ↔ EqualityPattern m n))

def theorem_3_2 : Prop :=
  ∀ a b c d : ℝ, 0 ≤ a → a ≤ b → b ≤ c → c ≤ d →
    K (K a b) (K c d) ≤ K (K a c) (K b d) ∧
    K (K a c) (K b d) ≤ K (K a d) (K b c) ∧
    (K (K a b) (K c d) = K (K a c) (K b d) ↔ b = c ∨ a * d = b * c) ∧
    (K (K a c) (K b d) = K (K a d) (K b c) ↔ a = b ∨ c = d)

/-- Scalar optima are attained by actual trees. `BellmanSpec` is a maximum,
including attainment, rather than an upper-bound-only relaxation. -/
def proposition_A_5 : Prop :=
  BellmanSpec K U ∧
  (∀ N : ℕ, 1 ≤ N →
    (balancedTree N).leaves = N ∧
    (balancedTree N).primitiveSum + 1 = U N ∧
    1 / (balancedTree N).sRate = U N ∧
    (∀ t : Tree, t.leaves = N → t.primitiveSum ≤ U N - 1) ∧
    (∀ t : Tree, t.leaves = N → 1 / U N ≤ t.sRate) ∧
    1 / (2 * (balancedTree N).primitiveSum + 1) = 1 / (2 * U N - 1) ∧
    (balancedTree N).sRate / (2 - (balancedTree N).sRate) = 1 / (2 * U N - 1)) ∧
  (∀ t : Tree, t.primitiveSum + 1 = t.value ∧ t.sRate = 1 / t.value) ∧
  (∀ x y : ℝ, 0 ≤ x → 0 ≤ y → mu (1 / (x + 1)) (1 / (y + 1)) = phi x y)

def proposition_A_6 : Prop :=
  Continuous (fun xy : ℝ × ℝ => K xy.1 xy.2) ∧
  (∀ x y : ℝ, 0 ≤ x → 0 ≤ y → 0 ≤ K x y) ∧
  (∀ x y : ℝ, K x y = K y x) ∧
  (∀ t x y : ℝ, 0 ≤ t → 0 ≤ x → 0 ≤ y → K (t * x) (t * y) = t * K x y) ∧
  (∀ x x' y : ℝ, 0 ≤ x → 0 ≤ y → x < x' → K x y < K x' y) ∧
  (∀ x y y' : ℝ, 0 ≤ x → 0 ≤ y → y < y' → K x y < K x y') ∧
  (∀ x : ℝ, 0 ≤ x → K 0 x = x ∧ K x x = rho * x) ∧
  (∀ x y : ℝ, 0 < x → 0 < y → x + y < K x y ∧ max x y < x + y) ∧
  (∀ x y x' y' : ℝ, 0 < x → 0 < y → 0 < x' → 0 < y' →
    min (x' / x) (y' / y) ≤ K x' y' / K x y ∧
    K x' y' / K x y ≤ max (x' / x) (y' / y) ∧
    (x' / x ≠ y' / y → min (x' / x) (y' / y) < K x' y' / K x y ∧
      K x' y' / K x y < max (x' / x) (y' / y)))

/-- Equality of signs expressed by the three possible orders. -/
def lemma_B_1 : Prop :=
  ∀ a b c d z : ℝ, 0 ≤ a → 0 ≤ b → 0 ≤ c → 0 ≤ d →
    max (K a b) (K c d) < z →
    (pairedPoly a b c d z < 0 ↔ z < K (K a b) (K c d)) ∧
    (pairedPoly a b c d z = 0 ↔ z = K (K a b) (K c d)) ∧
    (0 < pairedPoly a b c d z ↔ K (K a b) (K c d) < z)

def lemma_B_2 : Prop :=
  ∀ a b c d z : ℝ, 0 ≤ a → 0 ≤ b → 0 ≤ c → 0 ≤ d →
    pairedPoly a c b d z - pairedPoly a b c d z =
      2 * z ^ 2 * (d - a) * (c - b) * quartic a b c d (a * d + b * c) z ∧
    pairedPoly a d b c z - pairedPoly a c b d z =
      2 * z ^ 2 * (b - a) * (d - c) * quartic a b c d (a * b + c * d) z

def lemma_B_3 : Prop :=
  ∀ a b c d E : ℝ, 0 ≤ a → 0 ≤ b → 0 ≤ c → 0 ≤ d →
    0 < K a b → 0 < K c d →
    quartic a b c d E (K (K a b) (K c d)) =
      2 * (a * b * (K c d) ^ 2 + c * d * (K a b) ^ 2 - E * K a b * K c d) *
        (K a b * K c d + K a b * K (K a b) (K c d) +
          K c d * K (K a b) (K c d)) / (K a b * K c d)

def theorem_B_4 : Prop :=
  ∀ C : NonnegativeCompositionLaw,
    StrictMono C.V ∧
    (∀ m n : ℕ, C.op (C.V m) (C.V n) ≤ C.V (m + n)) ∧
    (∀ W : ℕ → ℝ, BellmanSpec C.op W → ∀ N : ℕ, 1 ≤ N → W N = C.V N)

def corollary_B_5 : Prop :=
  StrictMono U ∧
  (∀ m n : ℕ, K (U m) (U n) ≤ U (m + n)) ∧
  (∀ N : ℕ, 2 ≤ N → U N = K (U (N / 2)) (U ((N + 1) / 2)))

def lemma_C_1 : Prop :=
  ∀ m n : ℕ, 1 ≤ m → 1 ≤ n →
    (K (U m) (U n) = U (m + n) ↔ EqualityPattern m n)

/-- The three finite optimizer sets. An odd number greater than one is written
`2*n+1` with `1 ≤ n`; a positive valuation is written `k+1`. -/
def corollary_C_2 : Prop :=
  (∀ k : ℕ, optimalSplitSet (2 ^ (k + 1)) = {2 ^ k}) ∧
  (∀ n : ℕ, 1 ≤ n → optimalSplitSet (2 * n + 1) = {n, n + 1}) ∧
  (∀ n k : ℕ, 1 ≤ n → optimalSplitSet ((2 * n + 1) * 2 ^ (k + 1)) =
    {2 ^ (k + 1) * n, 2 ^ k * (2 * n + 1), 2 ^ (k + 1) * (n + 1)})

/-- Balanced ConPP sums in step-count notation and the complete three-way tie
classification, stated for sums rather than only kernel values. -/
def theorem_C_3 : Prop :=
  (∀ n : ℕ, 1 ≤ n →
    U (n + 1) - 1 = (U ((n - 1) / 2 + 1) - 1) + (U ((n - 1 + 1) / 2 + 1) - 1) +
      phi (U ((n - 1) / 2 + 1) - 1) (U ((n - 1 + 1) / 2 + 1) - 1)) ∧
  (∀ nu k m : ℕ, nu % 2 = 1 → 1 < nu → 1 ≤ m → m < nu * 2 ^ (k + 1) →
    ((U m - 1) + (U (nu * 2 ^ (k + 1) - m) - 1) +
        phi (U m - 1) (U (nu * 2 ^ (k + 1) - m) - 1) = U (nu * 2 ^ (k + 1)) - 1 ↔
      m = (nu - 1) * 2 ^ k ∨ m = nu * 2 ^ k ∨ m = (nu + 1) * 2 ^ k))

def corollary_C_4 : Prop :=
  (∀ l r : Tree, (Tree.join l r).value = U (l.leaves + r.leaves) ↔
    l.value = U l.leaves ∧ r.value = U r.leaves ∧
      OptimalSplit (l.leaves + r.leaves) l.leaves) ∧
  (∀ t : Tree, t.value = U t.leaves ↔ t.AllSplitsOptimal) ∧
  (∀ t : Tree, t.value = U t.leaves ↔ t.AllEqualityPatterns)

def proposition_C_5 : Prop :=
  T 1 = 1 ∧
  (∀ N : ℕ, 2 ≤ N → T N = ∑ m ∈ optimalSplitSet N, T m * T (N - m)) ∧
  (∀ k : ℕ, T (2 ^ k) = 1) ∧
  (∀ n : ℕ, 1 ≤ n → T (2 * n + 1) = 2 * T n * T (n + 1)) ∧
  (∀ n k : ℕ, 1 ≤ n → T ((2 * n + 1) * 2 ^ (k + 1)) =
    2 * T (2 ^ (k + 1) * n) * T (2 ^ (k + 1) * (n + 1)) + (T (2 ^ k * (2 * n + 1))) ^ 2)

end PaperTargets

namespace Paper

theorem theorem_3_1 : PaperTargets.theorem_3_1 :=
  ⟨GD.corollary_4_2.2.2, U_strictMono, GD.corollary_4_2.2.1, GD.lemma_4_3⟩

theorem theorem_3_2 : PaperTargets.theorem_3_2 :=
  fun _ _ _ _ ha hab hbc hcd => GD.theorem_3_1 ha hab hbc hcd

theorem proposition_A_5 : PaperTargets.proposition_A_5 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · refine ⟨U_one, ?_, ?_⟩
    · intro N hN
      exact (GD.proposition_2_5 N (by omega)).2.2.2 hN |>.1
    · intro N hN
      exact (GD.proposition_2_5 N (by omega)).2.2.2 hN |>.2
  · intro N hN
    have hprim := primitive_tree_optimum N hN
    have hs := s_tree_optimum N hN
    have hU : 1 ≤ U N := by simpa using U_strictMono.monotone hN
    refine ⟨hprim.1, (GD.proposition_2_5 N hN).1,
      (GD.proposition_2_5 N hN).2.1, hprim.2.2, hs.2, ?_, ?_⟩
    · rw [hprim.2.1]
      congr 1
      ring
    · rw [hs.1]
      exact objective_reciprocal hU
  · intro t
    exact ⟨t.primitive_conjugacy, t.s_conjugacy⟩
  · intro x y hx hy
    exact join_step_conjugacy hx hy

theorem proposition_A_6 : PaperTargets.proposition_A_6 := by
  refine ⟨K_continuous, ?_, K_symm, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x y hx hy
    exact K_nonneg hx hy
  · intro t x y ht hx hy
    exact K_hom ht hx hy
  · intro x x' y hx hy hxx
    exact K_strict_left hx hy hxx
  · intro x y y' hx hy hyy
    exact K_strict_right hx hy hyy
  · intro x hx
    exact ⟨K_zero_left hx, K_diag hx⟩
  · intro x y hx hy
    exact ⟨K_gt_sum hx hy, max_lt (by linarith) (by linarith)⟩
  · intro x y x' y' hx hy hx' hy'
    exact K_ratio_bounds hx hy hx' hy'

theorem lemma_B_1 : PaperTargets.lemma_B_1 :=
  fun _ _ _ _ _ ha hb hc hd hz => GD.lemma_3_2 ha hb hc hd hz

theorem lemma_B_2 : PaperTargets.lemma_B_2 := by
  intro a b c d z ha hb hc hd
  exact ⟨GD.lemma_3_3_first ha hb hc hd z, GD.lemma_3_3_second ha hb hc hd z⟩

theorem lemma_B_3 : PaperTargets.lemma_B_3 :=
  fun _ _ _ _ E ha hb hc hd hu hv => GD.lemma_3_4 ha hb hc hd hu hv E

theorem theorem_B_4 : PaperTargets.theorem_B_4 := NonnegativeCompositionLaw.balanced_optimality

theorem corollary_B_5 : PaperTargets.corollary_B_5 := GD.corollary_4_2

theorem lemma_C_1 : PaperTargets.lemma_C_1 := GD.lemma_4_3

theorem corollary_C_2 : PaperTargets.corollary_C_2 :=
  ⟨optimalSplitSet_dyadic, optimalSplitSet_odd, optimalSplitSet_even_odd_part⟩

/-- Conjugacy turns the optimizer criterion into equality of ConPP sums. -/
theorem primitive_split_optimal_iff (N m : ℕ) (hm : 1 ≤ m) (hmN : m < N) :
    (U m - 1) + (U (N - m) - 1) + phi (U m - 1) (U (N - m) - 1) = U N - 1 ↔
      OptimalSplit N m := by
  have h := affine_conjugacy (U m - 1) (U (N - m) - 1)
  simp only [sub_add_cancel] at h
  simp only [OptimalSplit, hm, hmN, true_and]
  constructor <;> intro he <;> linarith

theorem theorem_C_3 : PaperTargets.theorem_C_3 := by
  refine ⟨GD.theorem_4_5_balanced, ?_⟩
  intro nu k m hodd hnu hm hmN
  exact (primitive_split_optimal_iff _ _ hm hmN).trans
    (GD.theorem_4_5_ties nu k m hodd hnu hm hmN)

theorem corollary_C_4 : PaperTargets.corollary_C_4 := by
  refine ⟨?_, GD.corollary_4_6, optimal_tree_iff_patterns⟩
  intro l r
  have hl : 1 ≤ l.leaves := l.leaves_pos
  have hmN : l.leaves < l.leaves + r.leaves := by have := r.leaves_pos; omega
  simpa only [OptimalSplit, hl, hmN, true_and, Nat.add_sub_cancel_left] using
    (Tree.root_optimal_iff l r)

theorem proposition_C_5 : PaperTargets.proposition_C_5 := GD.theorem_B_1

/-- Exact scalar correctness of Algorithm 1; arithmetic operation/bit costs are
not included in this mathematical statement. -/
theorem algorithm_1 (bits : List Bool) :
    (runBits bits (0, 1)).1 = U (readBits bits 0) := GD.algorithm_1 bits

end Paper
end
end GD
