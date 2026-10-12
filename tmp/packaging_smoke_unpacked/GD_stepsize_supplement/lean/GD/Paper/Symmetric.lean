import GD.AdjacentRatios
import GD.ObjectivePhase
import GD.DerivativeTheorem
import GD.CornerTheorem
import GD.GridAlgorithm

/-! Public statements for Section 4 and Appendix D of GD_stepsize_schedule.pdf
(2026-09-24). The existing analytic development supplies the supporting proofs.
Periodic real functions represent functions on the phase circle ℝ/ℤ. -/
namespace GD
noncomputable section
open Set Filter MeasureTheory
open scoped Topology

namespace PaperTargets

/-- The exact positive, unique, nonconstant phase profile, including its extrema. -/
def theorem_4_1 : Prop :=
  PeriodicLipschitzPositive Phi ∧
  (∀ N : ℕ, 1 ≤ N → U N = (N:ℝ)^p * Phi (phase N)) ∧
  (∀ G : ℝ → ℝ, Continuous G → (∀ t, G (t+1)=G t) →
    (∀ N : ℕ, 1 ≤ N → U N=(N:ℝ)^p*G (phase N)) → G=Phi) ∧
  (¬∃ c : ℝ, ∀ t : ℝ, Phi t=c) ∧
  0 < phiMin ∧ phiMin < 1 ∧ sSup (Phi '' Icc 0 1)=1 ∧ Phi 0=1

/-- Explicit phase-uniform remainder bound, cluster interval and nonconvergence. -/
def corollary_4_2 : Prop :=
  (∀ N : ℕ, 1 ≤ N → B N=1/(2*(N:ℝ)^p*Phi (phase N)-1)) ∧
  (∀ N : ℕ, 1 ≤ N → 0 < B N-(N:ℝ)^(-p)/(2*Phi (phase N)) ∧
    B N-(N:ℝ)^(-p)/(2*Phi (phase N)) ≤ (N:ℝ)^(-2*p)/(2*phiMin^2)) ∧
  Clust (fun N : ℕ => (N:ℝ)^p*B N)=Icc (1/2) (1/(2*phiMin)) ∧
  ¬∃ l : ℝ, Tendsto (fun N : ℕ => (N:ℝ)^p*B N) atTop (𝓝 l)

def lemma_D_1 : Prop := ∀ x y : ℝ, 0 ≤ x → 0 ≤ y →
  K x y ≤ (x^q+y^q)^(1/q) ∧ (K x y=(x^q+y^q)^(1/q) ↔ x=y ∨ x*y=0)

/-- The value and reciprocal-rate formulations, with both equality cases. -/
def proposition_D_2 : Prop := ∀ N : ℕ, 1 ≤ N →
  U N ≤ (N:ℝ)^p ∧ (N:ℝ)^(-p) ≤ s N ∧
  (U N=(N:ℝ)^p ↔ ∃ k : ℕ, N=2^k) ∧
  (s N=(N:ℝ)^(-p) ↔ ∃ k : ℕ, N=2^k)

def lemma_D_3 : Prop := ∀ N : ℕ, 1 ≤ N →
  R (2*N)=T0 (R N) ∧ R (2*N+1)=T1 (R N) ∧
  1 < R N ∧ R N ≤ rho ∧ 0 < R N-1 ∧
  R N-1 ≤ (rho-1)/(2:ℝ)^(N.log2) ∧
  (rho-1)/(2:ℝ)^(N.log2) ≤ 2*(rho-1)/(N:ℝ)

def lemma_D_4 : Prop :=
  Targets.theorem_5_4 ∧ StrictMonoOn F (Icc (1:ℝ) 2) ∧
  LipschitzOnWith ⟨cplus,cplus_pos.le⟩ F (Icc (1:ℝ) 2)

def theorem_D_5 : Prop := theorem_4_1 ∧
  (∀ t ∈ Icc (0:ℝ) 1, Phi t=rho^(-t)*F ((2:ℝ)^t)) ∧
  (∀ x y : ℝ, |Phi x-Phi y| ≤ (2*Real.log 2*cplus+rho*Real.log rho)*|x-y|)

def corollary_D_6 : Prop :=
  Clust (fun N : ℕ => U N/(N:ℝ)^p)=Icc phiMin 1 ∧
  Clust (fun N : ℕ => (N:ℝ)^p*s N)=Icc 1 (1/phiMin) ∧
  ¬(∃ l, Tendsto (fun N : ℕ => U N/(N:ℝ)^p) atTop (𝓝 l)) ∧
  ¬(∃ l, Tendsto (fun N : ℕ => (N:ℝ)^p*s N) atTop (𝓝 l))

def corollary_D_7 : Prop := corollary_4_2

/-- Integral representation, regularity, uniform binary products, the exact log
tail and both binary expansions at a dyadic point. The bounds and regularity are
stated for the same canonical `derivativeProfile` used by the integral and path
products, rather than only for a separately existentially quantified function. -/
def proposition_D_8 : Prop := Targets.theorem_C_1 ∧
  (∀ x ∈ Icc (1:ℝ) 2, cminus ≤ derivativeProfile x ∧ derivativeProfile x ≤ cplus) ∧
  (∀ x ∈ Ioo (1:ℝ) 2, ¬IsDyadic x →
    ContinuousAt derivativeProfile x ∧ HasDerivAt F (derivativeProfile x) x)

def corollary_D_9 : Prop :=
  (∃ dl dr : ℝ, HasDerivWithinAt F dl (Iic (3/2)) (3/2) ∧
    HasDerivWithinAt F dr (Ici (3/2)) (3/2) ∧ dr < dl ∧
    ¬DifferentiableAt ℝ F (3/2)) ∧
  ¬ContDiffOn ℝ 1 F (Icc (1:ℝ) 2)

/-- Nested bounds, convergence and a certified evaluation algorithm. Summing the
work of every level through `k` still has order `2^k` in the stated scalar
operation model, where real powers are primitive operations. -/
def proposition_D_10 : Prop := Targets.theorem_C_3 ∧
  (∀ k : ℕ, (∑ j ∈ Finset.range (k+1), gridWork j) ≤ 60*2^k)

end PaperTargets

namespace Paper

theorem symmetric_phase_nonconstant : ¬∃ c : ℝ, ∀ t : ℝ, Phi t=c := by
  rintro ⟨c,hc⟩
  have hzero := hc 0
  rw [Phi_zero] at hzero
  have hlt := Phi_lt_one (1/2) (by norm_num)
  rw [hc (1/2), ← hzero] at hlt
  exact (lt_irrefl (1:ℝ)) hlt

theorem theorem_4_1 : PaperTargets.theorem_4_1 :=
  ⟨Phi_positive_periodic_lipschitz, U_phase_exact, Phi_unique,
    symmetric_phase_nonconstant, phiMin_bounds.1, phiMin_bounds.2, Phi_sSup, Phi_zero⟩

theorem objective_phase_nonconvergent :
    ¬∃ l : ℝ, Tendsto (fun N : ℕ => (N:ℝ)^p*B N) atTop (𝓝 l) := by
  have hmin : 0 < phiMin := phiMin_bounds.1
  have hlt : (1/2:ℝ) < 1/(2*phiMin) := by
    apply (lt_div_iff₀ (by positivity : (0:ℝ) < 2*phiMin)).mpr
    nlinarith [phiMin_bounds.2]
  apply no_limit_of_two_clusters (x:=(1/2:ℝ)) (y:=1/(2*phiMin))
  · rw [B_scaled_Clust]; exact ⟨le_rfl,hlt.le⟩
  · rw [B_scaled_Clust]; exact ⟨hlt.le,le_rfl⟩
  · exact hlt.ne

theorem corollary_4_2 : PaperTargets.corollary_4_2 :=
  ⟨B_phase_exact, B_remainder_bound, B_scaled_Clust, objective_phase_nonconvergent⟩

theorem lemma_D_1 : PaperTargets.lemma_D_1 := GD.lemma_5_1

theorem proposition_D_2 : PaperTargets.proposition_D_2 := by
  intro N hN
  have hn : (0:ℝ) < N := by exact_mod_cast (show 0 < N by omega)
  have hu : 0 < U N := U_pos (by omega)
  have hU := GD.proposition_5_2 N hN
  have hs : (N:ℝ)^(-p)=1/(N:ℝ)^p := by rw [Real.rpow_neg hn.le, one_div]
  refine ⟨hU.1, ?_, hU.2, ?_⟩
  · rw [hs, s]
    exact one_div_le_one_div_of_le hu hU.1
  · rw [hs, s]
    constructor
    · intro h
      apply hU.2.mp
      have he := congrArg (fun x : ℝ => 1/x) h
      simpa only [one_div_one_div] using he
    · intro h
      rw [hU.2.mpr h]

theorem lemma_D_3 : PaperTargets.lemma_D_3 := by
  intro N hN
  obtain ⟨h0,h1,hr,hrho,hlo,hhi⟩ := GD.lemma_5_3 N hN
  exact ⟨h0,h1,hr,hrho,sub_pos.mpr hr,hlo,hhi⟩

theorem lemma_D_4 : PaperTargets.lemma_D_4 :=
  ⟨GD.theorem_5_4,F_strictMonoOn,F_lipschitzOn⟩

theorem theorem_D_5 : PaperTargets.theorem_D_5 := by
  refine ⟨theorem_4_1, ?_, Phi_lipschitz⟩
  intro t ht
  exact Phi_eq_profile t ht

theorem corollary_D_6 : PaperTargets.corollary_D_6 := GD.corollary_5_7

theorem corollary_D_7 : PaperTargets.corollary_D_7 := corollary_4_2

theorem proposition_D_8 : PaperTargets.proposition_D_8 := by
  refine ⟨GD.theorem_C_1, derivativeProfile_bounds, ?_⟩
  intro x hx hnd
  exact ⟨derivativeProfile_continuousAt_nondyadic x hx hnd, F_hasDeriv_nondyadic x hx hnd⟩

theorem corollary_D_9 : PaperTargets.corollary_D_9 := by
  refine ⟨GD.corollary_C_2, ?_⟩
  intro hc
  obtain ⟨dl,dr,hl,hr,hlt,hnd⟩ := GD.corollary_C_2
  exact hnd (((hc.differentiableOn (by norm_num)) (3/2) (by norm_num)).differentiableAt
    (Icc_mem_nhds (by norm_num) (by norm_num)))

/-- Running all certified grid evaluations from level zero through level `k`
uses at most `60*2^k` scalar operations. -/
theorem gridWork_through_level_bound (k : ℕ) :
    (∑ j ∈ Finset.range (k+1), gridWork j) ≤ 60*2^k := by
  induction k with
  | zero =>
    simpa using (gridWork_bound 0).trans (by norm_num : 30*2^0 ≤ 60*2^0)
  | succ k ih =>
    change (∑ j ∈ Finset.range (k+1+1), gridWork j) ≤ 60*2^(k+1)
    rw [Finset.sum_range_succ, pow_succ]
    have hk := gridWork_bound (k+1)
    rw [pow_succ] at hk
    omega

theorem proposition_D_10 : PaperTargets.proposition_D_10 :=
  ⟨GD.theorem_C_3, gridWork_through_level_bound⟩

end Paper
end
end GD
