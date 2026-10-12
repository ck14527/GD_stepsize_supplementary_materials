import GD.Proposition62
import GD.DiscreteModulus
import GD.OBSInterpolation
import GD.ContactPhase
import Mathlib.Analysis.Asymptotics.Lemmas

/-! # The asymmetric phase results of the current manuscript

The public statements follow Theorem 5.1 and Appendix E of
`GD_stepsize_schedule.pdf`. The underlying Bellman sequences are the actual
`GD.U`, `GD.W`, and `GD.etaF`, and the canonical profile is `GD.Psi`.
Functions on the phase circle are represented by one-periodic real functions.
The scalar coefficient asymptotics are proved here; the smooth-convex
gradient-descent certificate invoked in the discussion after E.4 is external.
-/

namespace GD
noncomputable section
open Set Filter
open scoped Topology

namespace PaperTargets

def lemma_E_1 : Prop :=
  (∀ x y : ℝ, 0 < x → 0 < y → A x (rho*y) ≤ rho*K x y) ∧
  (∀ x y : ℝ, 1 ≤ x → 1 ≤ y → 2*K x y-1 ≤ A x (2*y-1))

def proposition_E_2 : Prop :=
  (∀ N : ℕ, 1 ≤ N → 2*U N-1 ≤ W N ∧ W N ≤ rho*U N) ∧
  (∀ m : ℕ, 1 ≤ m →
    Tendsto (fun k : ℕ => C (m*2^k)) atTop (𝓝 (Psi (phase m)))) ∧
  (∀ m : ℕ, 1 ≤ m →
    1/(rho*Phi (phase m)) ≤ Psi (phase m) ∧
    Psi (phase m) ≤ 1/(2*Phi (phase m)))

def lemma_E_3 : Prop := ∀ LF : ℝ,
  (∀ x y : ℝ, x ∈ Icc (1:ℝ) 2 → y ∈ Icc (1:ℝ) 2 → |F x-F y| ≤ LF*|x-y|) →
  let LU := max 1 LF
  (∀ m : ℕ, 1 ≤ m → 0 < U m-U (m-1) ∧ U m-U (m-1) ≤ LU*(m:ℝ)^(p-1)) ∧
  (∀ N : ℕ, 1 ≤ N → 0 < W (N+1)-W N ∧ W (N+1)-W N ≤ 4*LU*(N:ℝ)^(p-1)) ∧
  (∀ N : ℕ, 1 ≤ N → |C (N+1)-C N| ≤ (4*LU+rho*p)/(phiMin^2*(N:ℝ)))

/-- Includes the exact logarithmic interpolants, their uniform limit and
uniqueness, block uniformity, the explicit Lipschitz constant, and little-o. -/
def theorem_E_4 : Prop :=
  Targets.theorem_6_3 ∧
  Clust C = Psi '' Icc (0:ℝ) 1 ∧
  Asymptotics.IsLittleO atTop
    (fun N : ℕ => etaF N-(N:ℝ)^(-p)*Psi (phase N))
    (fun N : ℕ => (N:ℝ)^(-p))

def lemma_E_5 : Prop :=
  xi ∈ Ioo (0:ℝ) 1 ∧ xi^(2*q-1)*(2-xi)=1 ∧
  (∀ x : ℝ, x ∈ Ioo (0:ℝ) 1 → x^(2*q-1)*(2-x)=1 → x=xi) ∧
  (2:ℝ)^q < Bsup ∧
  (∀ u w : ℝ, 0 ≤ u → 0 ≤ w → (A u w)^q ≤ Bsup*u^q+w^q) ∧
  (∀ u w : ℝ, 0 < u → 0 < w → ((A u w)^q=Bsup*u^q+w^q ↔ u/w=tau)) ∧
  (∀ w : ℝ, 0 ≤ w → (A 0 w)^q=w^q) ∧
  (∀ u : ℝ, 0 < u → (A u 0)^q < Bsup*u^q)

def proposition_E_6 : Prop :=
  (∀ N : ℕ, 1 ≤ N → (W N)^q ≤ Bsup*(N:ℝ) ∧ cstar ≤ C N) ∧
  (∀ N m : ℕ, 1 ≤ m → m < N → W N=A (U m) (W (N-m)) →
    deficit N=Bsup*((m:ℝ)-(U m)^q)+deficit (N-m)+sigma (U m) (W (N-m)) ∧
    0 ≤ Bsup*((m:ℝ)-(U m)^q) ∧ 0 ≤ deficit (N-m) ∧ 0 ≤ sigma (U m) (W (N-m)))

def lemma_E_7 : Prop :=
  (∀ x ∈ Ioo (1:ℝ) 2, F x < x^p) ∧
  (∀ t ∈ Ioo (0:ℝ) 1, Phi t < 1)

def lemma_E_8 : Prop :=
  alpha=1-xi^(2*q) ∧ 1-alpha=xi^(2*q) ∧
  1/4 < 1-alpha ∧ 1-alpha < 1/2 ∧ 1/2 < alpha ∧ alpha < 1 ∧
  2*alpha ∈ Ioo (1:ℝ) 2

def lemma_E_9 : Prop :=
  Tendsto (fun k : ℕ => C (2^k)) atTop (𝓝 (Psi 0)) ∧ cstar < Psi 0

def lemma_E_10 : Prop := ∀ c : ℝ, (∀ t : ℝ, Psi t=c) → c=cstar

def lemma_E_11 : Prop :=
  (∀ t : ℝ, cstar < Psi t) ∧ cstar < sInf (Psi '' Icc (0:ℝ) 1)

def proposition_E_12 : Prop :=
  (∀ t : ℝ, Psi t ≤ cstar/phiMin) ∧
  (∀ t : ℝ, Bsup^p*phiMin ≤ 1/Psi t)

def theorem_E_13 : Prop :=
  (¬ ∃ c : ℝ, ∀ t : ℝ, Psi t=c) ∧
  cstar < sInf (Psi '' Icc (0:ℝ) 1) ∧
  sInf (Psi '' Icc (0:ℝ) 1) < sSup (Psi '' Icc (0:ℝ) 1) ∧
  sSup (Psi '' Icc (0:ℝ) 1) ≤ cstar/phiMin

/-- Theorem 5.1 joins phase existence/convergence and strict support separation. -/
def theorem_5_1 : Prop := theorem_E_4 ∧ theorem_E_13

end PaperTargets

namespace Paper

theorem lemma_E_1 : PaperTargets.lemma_E_1 :=
  ⟨fun _ _ hx hy => GD.lemma_D_1_upper hx hy,
    fun _ _ hx hy => GD.lemma_D_1_lower hx hy⟩

theorem proposition_E_2 : PaperTargets.proposition_E_2 := by
  refine ⟨W_sandwich, fun m hm => OBSPhase_ray Psi Psi_OBSPhase m hm, ?_⟩
  intro m hm
  obtain ⟨c,hc,hlo,hhi⟩ := GD.proposition_6_2.2 m hm
  have he : c=Psi (phase m) := tendsto_nhds_unique hc (OBSPhase_ray Psi Psi_OBSPhase m hm)
  exact he ▸ ⟨hlo,hhi⟩

theorem lemma_E_3 : PaperTargets.lemma_E_3 := GD.lemma_D_2

/-- The scaled error of the actual coefficient tends to zero. -/
theorem etaF_phase_littleO : Asymptotics.IsLittleO atTop
    (fun N : ℕ => etaF N-(N:ℝ)^(-p)*Psi (phase N))
    (fun N : ℕ => (N:ℝ)^(-p)) := by
  apply (Asymptotics.isLittleO_iff_tendsto' ?_).mpr
  · apply (OBSPhase_error Psi Psi_OBSPhase).congr'
    filter_upwards [eventually_ge_atTop 1] with N hN
    have hn : (0:ℝ) < N := by exact_mod_cast (show 0 < N by omega)
    have hp := Real.rpow_pos_of_pos hn p
    rw [Real.rpow_neg hn.le]
    dsimp only [C]
    field_simp [hp.ne']
    ring
  · filter_upwards [eventually_ge_atTop 1] with N hN hz
    have hn : (0:ℝ) < N := by exact_mod_cast (show 0 < N by omega)
    exact False.elim ((Real.rpow_pos_of_pos hn (-p)).ne' hz)

theorem theorem_E_4 : PaperTargets.theorem_E_4 :=
  ⟨GD.theorem_6_3, C_Clust.trans Psi_range.symm, etaF_phase_littleO⟩

theorem lemma_E_5 : PaperTargets.lemma_E_5 := GD.lemma_6_4

/-- The closed-form coefficient is the supremum used in Section 5.2. -/
theorem Bsup_eq_support_supremum :
    Bsup=sSup {z : ℝ | ∃ u : ℝ, 0 < u ∧ z=((A u 1)^q-1)/u^q} := by
  let S := {z : ℝ | ∃ u : ℝ, 0 < u ∧ z=((A u 1)^q-1)/u^q}
  have hub : ∀ z ∈ S, z ≤ Bsup := by
    rintro z ⟨u,hu,rfl⟩
    apply (div_le_iff₀ (Real.rpow_pos_of_pos hu q)).mpr
    linarith [(support_one u hu).1]
  have hmem : Bsup ∈ S := by
    refine ⟨tau,tau_positive,?_⟩
    have he := (support_one tau tau_positive).2.mpr rfl
    apply (eq_div_iff (Real.rpow_pos_of_pos tau_positive q).ne').mpr
    linarith
  exact le_antisymm (le_csSup ⟨Bsup,hub⟩ hmem) (csSup_le ⟨Bsup,hmem⟩ hub)

theorem proposition_E_6 : PaperTargets.proposition_E_6 := GD.proposition_D_3

theorem lemma_E_7 : PaperTargets.lemma_E_7 := GD.lemma_D_4

theorem lemma_E_8 : PaperTargets.lemma_E_8 := by
  obtain ⟨h1,h2,h3,h4,h5,h6⟩ := GD.lemma_D_5
  exact ⟨h1,h2,h3,h4,h5,h6,by constructor <;> linarith⟩

theorem lemma_E_9 : PaperTargets.lemma_E_9 := by
  refine ⟨?_,GD.theorem_D_8.1 0⟩
  simpa [phase] using OBSPhase_ray Psi Psi_OBSPhase 1 (by norm_num)

theorem lemma_E_10 : PaperTargets.lemma_E_10 := GD.lemma_D_7

theorem lemma_E_11 : PaperTargets.lemma_E_11 := GD.theorem_D_8

theorem proposition_E_12 : PaperTargets.proposition_E_12 := by
  refine ⟨GD.proposition_D_9,?_⟩
  intro t
  have h := GD.proposition_D_9 t
  rw [cstar,Real.rpow_neg Bsup_pos.le,← one_div,div_div] at h
  have hprod := (le_div_iff₀ (mul_pos (Real.rpow_pos_of_pos Bsup_pos p) phiMin_bounds.1)).mp h
  apply (le_div_iff₀ (Psi_pos t)).mpr
  simpa only [mul_comm] using hprod

theorem theorem_E_13 : PaperTargets.theorem_E_13 := by
  refine ⟨?_,GD.theorem_6_5⟩
  rintro ⟨c,hc⟩
  have he := lemma_E_10 c hc
  have hs := lemma_E_11.1 0
  rw [hc 0,he] at hs
  exact (lt_irrefl _ hs)

theorem theorem_5_1 : PaperTargets.theorem_5_1 := ⟨theorem_E_4,theorem_E_13⟩

end Paper
end
end GD
