# Statement-by-statement correspondence

Each "Recorded checked" entry summarizes the inherited Lean audit of the precise real-number, recursion, or combinatorial statement listed below. It does not certify every sentence of the manuscript or reprove external optimization certificates. The supplementary revision rechecked source/export consistency, but did not run a fresh Lean build.

**Version boundary:** the registry names PDF SHA-256 `db3137a4cc77fcebf4f7956f4afdccd5ed51dd006e32dec69657f84843898fc9`; the locally reviewed PDF has SHA-256 `e38f43f82aca4cf4e26d3f58d202a853aedee2bfd4be0d6c9f1fb1a5d6374003`. The following is the registered correspondence, pending final semantic review against the exact submitted PDF. This table does not assert byte-identical provenance.

[Scope and trust boundary](VERIFICATION.md) · [Machine-readable coverage](../audit/coverage.json) · [CSV table](THEOREMS.csv)

| Paper result | Description | Status | Proof declaration(s) and source |
|---|---|---|---|
| Theorem 3.1 | Balanced optimality and complete equality classification | Recorded checked | [`GD.Paper.theorem_3_1`](../GD/Paper/Composition.lean) |
| Theorem 3.2 | Four-point rearrangement and both equality cases | Recorded checked | [`GD.Paper.theorem_3_2`](../GD/Paper/Composition.lean) |
| Theorem 4.1 | Exact symmetric dyadic phase law | Recorded checked | [`GD.Paper.theorem_4_1`](../GD/Paper/Symmetric.lean) |
| Corollary 4.2 | Exact objective phase law and uniform expansion | Recorded checked | [`GD.Paper.corollary_4_2`](../GD/Paper/Symmetric.lean) |
| Theorem 5.1 | Asymmetric uniform phase law and strict support separation | Recorded checked | [`GD.Paper.theorem_5_1`](../GD/Paper/Asymmetric.lean) |
| Proposition A.5 | Treewise conjugacy and common Bellman optimum | Recorded checked (scalar interface) | [`GD.Paper.proposition_A_5`](../GD/Paper/Composition.lean) |
| Proposition A.6 | Composition-kernel properties and strict ratio bounds | Recorded checked | [`GD.Paper.proposition_A_6`](../GD/Paper/Composition.lean) |
| Lemma B.1 | Sign beyond the inner roots | Recorded checked | [`GD.Paper.lemma_B_1`](../GD/Paper/Composition.lean) |
| Lemma B.2 | Pairing-difference identities | Recorded checked | [`GD.Paper.lemma_B_2`](../GD/Paper/Composition.lean) |
| Lemma B.3 | Quartic evaluation at the composed root | Recorded checked | [`GD.Paper.lemma_B_3`](../GD/Paper/Composition.lean) |
| Theorem B.4 | Abstract balanced-composition principle | Recorded checked | [`GD.Paper.theorem_B_4`](../GD/Paper/Composition.lean) |
| Corollary B.5 | Balanced recurrence and symmetric supercomposition | Recorded checked | [`GD.Paper.corollary_B_5`](../GD/Paper/Composition.lean) |
| Lemma C.1 | Complete equality patterns in supercomposition | Recorded checked | [`GD.Paper.lemma_C_1`](../GD/Paper/Composition.lean) |
| Corollary C.2 | All maximizing root splits | Recorded checked | [`GD.Paper.corollary_C_2`](../GD/Paper/Composition.lean) |
| Theorem C.3 | Conjecture 4.17 of Zhang and Jiang: balanced ConPP and all ties | Recorded checked | [`GD.Paper.theorem_C_3`](../GD/Paper/Composition.lean) |
| Corollary C.4 | Optimal composition trees | Recorded checked | [`GD.Paper.corollary_C_4`](../GD/Paper/Composition.lean) |
| Proposition C.5 | Exact counts of optimal ordered composition trees | Recorded checked | [`GD.Paper.proposition_C_5`](../GD/Paper/Composition.lean) |
| Lemma D.1 | Sharp power-mean kernel bound | Recorded checked | [`GD.Paper.lemma_D_1`](../GD/Paper/Symmetric.lean) |
| Proposition D.2 | Sharp power envelope and all equality cases | Recorded checked | [`GD.Paper.proposition_D_2`](../GD/Paper/Symmetric.lean) |
| Lemma D.3 | Adjacent-ratio recursion and contraction | Recorded checked | [`GD.Paper.lemma_D_3`](../GD/Paper/Symmetric.lean) |
| Lemma D.4 | Unique strictly increasing bi-Lipschitz interpolation | Recorded checked | [`GD.Paper.lemma_D_4`](../GD/Paper/Symmetric.lean) |
| Theorem D.5 | Positive nonconstant symmetric phase profile | Recorded checked | [`GD.Paper.theorem_D_5`](../GD/Paper/Symmetric.lean) |
| Corollary D.6 | Symmetric value and reciprocal-rate cluster intervals | Recorded checked | [`GD.Paper.corollary_D_6`](../GD/Paper/Symmetric.lean) |
| Corollary D.7 | Objective coefficient, uniform remainder and clusters | Recorded checked | [`GD.Paper.corollary_D_7`](../GD/Paper/Symmetric.lean) |
| Proposition D.8 | Integral density and nondyadic regularity | Recorded checked | [`GD.Paper.proposition_D_8`](../GD/Paper/Symmetric.lean) |
| Corollary D.9 | Certified dyadic corner | Recorded checked | [`GD.Paper.corollary_D_9`](../GD/Paper/Symmetric.lean) |
| Proposition D.10 | Nested certified grids and linear work | Recorded checked | [`GD.Paper.proposition_D_10`](../GD/Paper/Symmetric.lean) |
| Lemma E.1 | Local reciprocal comparisons | Recorded checked | [`GD.Paper.lemma_E_1`](../GD/Paper/Asymmetric.lean) |
| Proposition E.2 | Reciprocal sandwich and fixed-ray limits | Recorded checked | [`GD.Paper.proposition_E_2`](../GD/Paper/Asymmetric.lean) |
| Lemma E.3 | Discrete modulus | Recorded checked | [`GD.Paper.lemma_E_3`](../GD/Paper/Asymmetric.lean) |
| Theorem E.4 | Uniform asymmetric phase convergence | Recorded checked | [`GD.Paper.theorem_E_4`](../GD/Paper/Asymmetric.lean) |
| Lemma E.5 | Sharp homogeneous support | Recorded checked | [`GD.Paper.lemma_E_5`](../GD/Paper/Asymmetric.lean) |
| Proposition E.6 | Support barrier and nonnegative deficit decomposition | Recorded checked | [`GD.Paper.proposition_E_6`](../GD/Paper/Asymmetric.lean) |
| Lemma E.7 | Strict symmetric power envelope | Recorded checked | [`GD.Paper.lemma_E_7`](../GD/Paper/Asymmetric.lean) |
| Lemma E.8 | Contact fraction geometry | Recorded checked | [`GD.Paper.lemma_E_8`](../GD/Paper/Asymmetric.lean) |
| Lemma E.9 | Strict dyadic-ray separation | Recorded checked | [`GD.Paper.lemma_E_9`](../GD/Paper/Asymmetric.lean) |
| Lemma E.10 | Constant-phase rigidity | Recorded checked | [`GD.Paper.lemma_E_10`](../GD/Paper/Asymmetric.lean) |
| Lemma E.11 | Global strict support separation | Recorded checked | [`GD.Paper.lemma_E_11`](../GD/Paper/Asymmetric.lean) |
| Proposition E.12 | Uniform upper phase enclosure | Recorded checked | [`GD.Paper.proposition_E_12`](../GD/Paper/Asymmetric.lean) |
| Theorem E.13 | Nonconstant phase and final support bounds | Recorded checked | [`GD.Paper.theorem_E_13`](../GD/Paper/Asymmetric.lean) |

## Registered scope notes

These notes describe the registered mathematical targets and their intended correspondence; "complete" below refers to that specified scalar/combinatorial scope, not all GD certificates or all manuscript prose.

| Result | Mathematical correspondence / limitation |
|---|---|
| 3.1 | Complete numbered scalar statement. EqualityPattern unfolds to the exact two arithmetic alternatives. |
| 3.2 | Complete numbered statement. |
| 4.1 | Complete statement. Periodic real functions represent the phase circle; uniqueness is proved among all continuous periodic functions. |
| 4.2 | Complete scalar coefficient statement. The O(N^(-2*p)) assertion is certified by the stronger explicit positive remainder bound N^(-2*p)/(2*phiMin^2). The interpretation as a tight GD objective coefficient uses external certificates. |
| 5.1 | Complete scalar statement of the numbered theorem; etaF is the concrete Bellman coefficient, with the external GD certificate boundary described above. |
| A.5 | Complete scalar/treewise statement, with Bellman maximum encoded by upper bounds and an attaining split. The correspondence to smooth-convex trajectories uses externally cited certificate interfaces; no such imported certificate is asserted as a Lean theorem. |
| A.6 | Complete numbered statement; continuity is proved globally, stronger than continuity restricted to the quadrant. |
| B.1 | Complete statement in equivalent three-way form: negativity, zero and positivity iff the corresponding strict order or equality with the outer root. P is the product of all four actual conjugate-root factors. |
| B.2 | Complete two-identity statement using the actual conjugate-root polynomials. |
| B.3 | Complete statement, with precisely the positive-inner-root hypotheses required by the manuscript. |
| B.4 | Complete abstract theorem. NonnegativeCompositionLaw contains exactly the manuscript's nonnegative-domain operator assumptions, not the desired conclusion. Its V satisfies the original balanced recurrence by V_rec; BellmanSpec includes attainment. |
| B.5 | Complete numbered statement. |
| C.1 | Complete equivalence, with both unordered orientations represented explicitly by ScaledConsecutive. |
| C.2 | Complete three-case statement, parameterized by nu=2*n+1 (n>=1) and ell=k+1 in the third case. |
| C.3 | Complete recursive-family scalar/stepsize-sum statement. Positive valuation ell is encoded as k+1. Optimized recursive primitive sums are U_N-1, justified constructively by Proposition A.5. External trajectory-certificate closure is outside the scalar model. |
| C.4 | Complete treewise equivalences; no assumption that every optimal tree represents a different numerical schedule. |
| C.5 | Complete numbered recurrence and three cases for actual finite sets of trees. The subsequent unnumbered asymptotic paragraph and sample table are not included in this target. |
| D.1 | Complete numbered scalar statement, with all displayed domain assumptions and equality cases retained. |
| D.2 | Complete numbered scalar statement, with all displayed domain assumptions and equality cases retained. |
| D.3 | Complete numbered scalar statement, with all displayed domain assumptions and equality cases retained. |
| D.4 | Complete numbered scalar statement, with all displayed domain assumptions and equality cases retained. |
| D.5 | Complete statement. Periodic real functions represent the phase circle; uniqueness is proved among all continuous periodic functions. |
| D.6 | Complete numbered scalar statement, with all displayed domain assumptions and equality cases retained. |
| D.7 | Complete scalar coefficient statement. The O(N^(-2*p)) assertion is certified by the stronger explicit positive remainder bound N^(-2*p)/(2*phiMin^2). The interpretation as a tight GD objective coefficient uses external certificates. |
| D.8 | Complete regularity statement and the stronger binary-product formulas in its proof. The same canonical derivativeProfile used in the integral explicitly satisfies the bounds, nondyadic continuity and derivative identity. The supporting target is GD.Targets.theorem_C_1. |
| D.9 | Complete one-sided derivative separation, nondifferentiability and not-C^1 conclusions. The finite rational corner certificate is checked by the Lean kernel. |
| D.10 | Complete exact grid bounds and limits, a 30*2^k single-level work bound, and a 60*2^k cumulative bound for all levels through k, in the documented real-RAM model (real powers are primitive). Optional level-17 printed decimals are not a Lean interval certificate. |
| E.1 | Complete statement, both inequalities with exactly their stated domains. |
| E.2 | Complete scalar statement including existence, explicit bounds and identification of the fixed-ray limit. |
| E.3 | Complete statement, parametrized by any valid Lipschitz constant LF. |
| E.4 | Complete scalar phase assertion. The discussion's equation (71) uses an external smooth-convex GD certificate; no claim that the certificate is formalized. |
| E.5 | Complete statement, unique interior root and all boundary/interior equality cases. |
| E.6 | Complete scalar statement. |
| E.7 | Complete statement. |
| E.8 | Complete statement including all identities and strict interval bounds. |
| E.9 | Complete statement; no circular proof dependency. |
| E.10 | Complete statement. |
| E.11 | Complete pointwise and strict-minimum statement. |
| E.12 | Complete pair of equivalent enclosures. |
| E.13 | Complete scalar statement. Its interpretation as tight objective-gap leading constants invokes the external GD certificate described above. |

Every numbered entry has a `GD.PaperTargets` definition and a checked `GD.Paper` theorem whose entire elaborated type is that exact target. A proposition definition or a theorem merely assuming the target is never counted as its proof. Historical names in the supporting library are internal proof identifiers, not current manuscript numbers.

Numbering is recorded in `docs/statement_inventory.json` and `audit/coverage.json` under the inherited manuscript hash stated above. Review and update the registry and correspondence if the final paper is renumbered; preserve the history of the existing audit.
