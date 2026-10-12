# Numerical details, reproducibility, and related work

This document accompanies the submitted paper and the numerical code. For
Lean 4, start with [LEAN_FORMALIZATION.md](LEAN_FORMALIZATION.md) and the
[statement correspondence](lean/docs/THEOREMS.md). The Lean scalar proofs,
Python interval calculations, and floating-point illustrations are distinct
forms of evidence. Historical run records are identified in
[checks/README.md](checks/README.md); they are not new measurements from this
packaging pass. This supplement does not contain the full manuscript TeX source.

The pinned environment and quick commands are in the root [README](README.md).
To rerun the interval computation while preserving inherited evidence, use
`python scripts/check_phase_certificate.py --output checks/current/reviewer/interval_checks.json`.
The symmetric minimum enclosure is discussed in Appendix **D.8** (a subsection),
with the grid theorem numbered **Proposition D.10**. These two identifiers must
not be confused with Proposition D.8 on integral density and regularity.

The numerical corner products in this document are separately recomputed by
Python. The Lean development also supplies an exact rational corner proof
for Corollary D.9; this does not turn the level-17 decimal phase-minimum
enclosure into a Lean-certified numerical result.

## 1. Reference implementations and numerical checks

The accompanying source project contains two implementations of the scalar recursions. The Python script `scripts/reference_checks.py` tabulates the symmetric recurrence, evaluates single horizons by Algorithm 1, and implements the asymmetric Bellman recursion by testing every ordered split. The C++ program `scripts/obsf_exhaustive.cpp` performs the same exhaustive asymmetric computation at larger horizons. Neither implementation prunes pivots or assumes that an asymmetric optimizer is balanced. The C++ loop can be vectorized, but the maximization still includes all $m=1,\ldots,N-1$.

Floating-point regression checks compare the binary evaluator with symmetric tabulation through $N=4096$ and compare the analytic maximizing-split sets with exhaustive symmetric maximization through $N=256$. They also check the reciprocal sandwich against exhaustive asymmetric values. These checks detect implementation errors; they are not substitutes for the proofs in Appendices B–E. Machine-readable results, compiler options, and measured runtimes are recorded in the accompanying `checks` directory.

For a maximum leaf count $M$, exhaustive asymmetric tabulation evaluates $M(M-1)/2$ candidate splits and stores $O(M)$ scalar values. Thus the computation through $M=2^{19}$ requires $137{,}438{,}691{,}328$ candidate evaluations. The reported timings refer to the reference implementation and its recorded environment, not to a subquadratic algorithm. The theorem on logarithmic evaluation concerns only the symmetric scalar value $U_N$. The reference run recorded in the supplied source archive used double-precision arithmetic in a single-threaded, SIMD-vectorized C++17 implementation, compiled with GCC 14.2.0 in a Linux x86-64 container reporting an AMD EPYC 9V74 processor. The exhaustive Bellman loop through $2^{19}$ took $81.51$ seconds, excluding CSV output. The recomputed extrema and successive-scale difference agree with the rounded annotations below; these floating-point results remain distinct from interval certification.

## 2. Phase plots and the distinction between samples and certificates

For the symmetric curve, the grid values are $U_N/N^p$ for $2^{22}\le N\le2^{23}$. The sampled minimum is approximately $0.99281933$ at phase $0.468212$. The separate interval certificate in Appendix D.8 gives $0.99281236<\phi_*<0.99281934$. The sampled extremizing phase is not certified to be unique or exact. The nonconstancy witness is the exact identity $\Phi(\log_2(3/2))=U_3/3^p<1$.

For the asymmetric curve, the nodes of $\Psi_{18}$ are $N^p/W_N$ for $2^{18}\le N\le2^{19}$. The values reported in the supplied figures are a sampled minimum of approximately $0.42139019$ near phase $0.495894$ and a sampled maximum of approximately $0.42311312$ near phase $0.007838$. These are extrema of the finite-scale interpolant, not certified extrema of $\Psi_F$. For piecewise-affine interpolants, the supremum of their difference is attained at a node of the union of their grids. The level-17 grid is contained in the level-18 grid, so the numerical value of $\|\Psi_{18}-\Psi_{17}\|_\infty$ can be obtained by evaluating both at the level-18 nodes. Its reported value, approximately $9.82\times10^{-7}$, is a successive-scale difference, not a bound on $\|\Psi_{18}-\Psi_F\|_\infty$.

For direct comparison of objective guarantees, the symmetric panel in Figure 1 displays the transformed leading-coefficient phase $C_{\mathrm S}(t)=1/(2\Phi(t))$, evaluated from the same dyadic-grid values by plotting $N^p/(2U_N)$ on $2^{22}\le N\le2^{23}$. The detailed symmetric figure linked below retains the underlying scalar phase $\Phi$, because the finite certificate of Appendix D.8 directly controls $\phi_*=\min\Phi$. The detailed asymmetric figure retains $\Psi_{18}$ together with its sampled extrema, support bounds, and successive-scale comparison. The compact-panel plotting sources and exported data are included with the project. The fully annotated figures are preserved as the supplied vector PDFs; their original generating scripts were not part of the source archive.

Detailed symmetric illustration: [vector PDF](figures/phi_phase_original.pdf).

Detailed symmetric scalar-phase illustration supplied with the source manuscript. The curve shows $\Phi$; the rigorous minimum enclosure comes from Appendix D.8, while the sampled minimum and its phase are numerical estimates. The symmetric objective-leading phase shown in Figure 1 is obtained by the monotone transformation $C_{\mathrm S}(t)=1/(2\Phi(t))$.

Detailed asymmetric illustration: [vector PDF](figures/psi_phase_original.pdf).

Detailed finite-scale asymmetric illustration supplied with the source manuscript. The curve is $\Psi_{18}$, and all annotated extrema belong to this interpolant. The dashed line is $c_*$; the dotted line is the conservative limiting-profile enclosure $c_*/0.99281236$. The successive-scale difference is not a certified limiting-profile error. The main-text panel suppresses these numerical annotations except for the structural barrier $c_*$.

## 3. Checking the finite certificates

The script `scripts/check_phase_certificate.py` encloses $U_N$ through $2^{18}$ by exact integer arithmetic and integer square roots on a fixed decimal grid. Monotonicity of $\mathcal{K}$ propagates lower and upper endpoint bounds through the balanced recurrence. Noninteger powers in the finite phase bounds are evaluated using outward interval arithmetic at 60 decimal digits. The script checks every candidate in the lower and upper grids against the reported enclosure endpoints and checks the two reported witness indices. It also checks that the six-factor products used for the dyadic corner lie inside their recorded enclosures and are strictly separated. The output records interval-arithmetic checks, not Lean kernel verification.

## 4. Further related work

For short steps, performance estimation gives tight bounds for fixed-step methods (Drori and Teboulle 2014), and schedules approaching the short-step threshold improve the leading constant without improving the $n^{-1}$ order (Teboulle and Vaisbourd 2023). Smooth convex interpolation provides the finite-dimensional representation of worst-case performance (Taylor, Hendrickx, and Glineur 2017); branch-and-bound performance estimation enables numerical optimization over stepsize schedules (Das Gupta, Van Parys, and Ryu 2024). Long-step patterns first gave constant-factor improvements (Grimmer 2024) and then polynomial acceleration (Grimmer, Shu, and Wang 2023; Altschuler and Parrilo 2025a, 2025b). These advances differ from acceleration using momentum or extrapolation (Y. E. Nesterov 1983; Y. Nesterov 2004).

The present paper studies finite-horizon optimization and phase laws within recursive classes. The global ConPD/OBS-F optimality conjectures of Zhang and Jiang (2026, sec. 6.1) and Grimmer, Shu, and Wang (2025, Conjecture 1) concern all predetermined schedules and are stronger. The lower bounds of Ye and Liu (2026) determine the best polynomial exponent, but do not determine an exact finite-horizon minimax coefficient. Anytime acceleration is a separate problem because a guarantee at the end of a long-step block need not control intermediate iterates (Kornowski and Shamir 2024; Zhang et al. 2025; Tsai et al. 2026). Extensions to proximal and composite optimization are also outside the present analysis (Bok and Altschuler 2025, 2026).

Periodic fluctuations are familiar in linear half-split recurrences (Hwang, Janson, and Tsai 2024), and the midpoint construction here is related in form to de Rham-type functional equations (Okamura 2016). Those connections provide context, but the proofs here use the specific nonlinear kernel and its rearrangement and ratio-contraction properties.

## References

Altschuler, J. M., and P. A. Parrilo. 2025a. “Acceleration by Stepsize Hedging: Multi-Step Descent and the Silver Stepsize Schedule.” *Journal of the ACM* 72 (2): Article 12. <https://doi.org/10.1145/3708502>.

———. 2025b. “Acceleration by Stepsize Hedging: Silver Stepsize Schedule for Smooth Convex Optimization.” *Mathematical Programming* 213: 1105–18. <https://doi.org/10.1007/s10107-024-02164-2>.

Bok, J., and J. M. Altschuler. 2025. “Accelerating Proximal Gradient Descent via Silver Stepsizes.” In *Proceedings of COLT 2025*, 291:421–53. Proceedings of Machine Learning Research. PMLR. <https://proceedings.mlr.press/v291/bok25a.html>.

———. 2026. “Optimized Methods for Composite Optimization: A Reduction Perspective.” *Mathematical Programming*. <https://doi.org/10.1007/s10107-026-02377-7>.

Das Gupta, S., B. P. G. Van Parys, and E. K. Ryu. 2024. “Branch-and-Bound Performance Estimation Programming: A Unified Methodology for Constructing Optimal Optimization Methods.” *Mathematical Programming* 204: 567–639. <https://doi.org/10.1007/s10107-023-01973-1>.

Drori, Y., and M. Teboulle. 2014. “Performance of First-Order Methods for Smooth Convex Minimization: A Novel Approach.” *Mathematical Programming* 145: 451–82. <https://doi.org/10.1007/s10107-013-0653-0>.

Grimmer, B. 2024. “Provably Faster Gradient Descent via Long Steps.” *SIAM Journal on Optimization* 34 (3): 2588–608. <https://doi.org/10.1137/23M1588408>.

Grimmer, B., K. Shu, and A. L. Wang. 2023. “Accelerated Gradient Descent via Long Steps.” <https://arxiv.org/abs/2309.09961>.

———. 2025. “Composing Optimized Stepsize Schedules for Gradient Descent.” *Mathematics of Operations Research*. <https://doi.org/10.1287/moor.2024.0764>.

Hwang, Hsien-Kuei, Svante Janson, and Tsung-Hsi Tsai. 2024. “Identities and Periodic Oscillations of Divide-and-Conquer Recurrences Splitting at Half.” *Advances in Applied Mathematics* 155: 102653. <https://doi.org/10.1016/j.aam.2023.102653>.

Kornowski, G., and O. Shamir. 2024. “Open Problem: Anytime Convergence Rate of Gradient Descent.” In *Proceedings of the 37th Conference on Learning Theory*, 247:5335–39. Proceedings of Machine Learning Research. PMLR. <https://proceedings.mlr.press/v247/kornowski24a.html>.

Nesterov, Y. E. 1983. “A Method of Solving a Convex Programming Problem with Convergence Rate $O(1/k^2)$.” *Soviet Mathematics Doklady* 27 (2): 372–76.

Nesterov, Yurii. 2004. *Introductory Lectures on Convex Optimization: A Basic Course*. Vol. 87. Applied Optimization. Boston: Kluwer Academic Publishers. <https://doi.org/10.1007/978-1-4419-8853-9>.

Okamura, Kazuki. 2016. “On Regularity for de Rham’s Functional Equations.” *Aequationes Mathematicae* 90 (6): 1071–85. <https://doi.org/10.1007/s00010-016-0439-6>.

Taylor, A. B., J. M. Hendrickx, and F. Glineur. 2017. “Smooth Strongly Convex Interpolation and Exact Worst-Case Performance of First-Order Methods.” *Mathematical Programming* 161: 307–45. <https://doi.org/10.1007/s10107-016-1009-3>.

Teboulle, M., and Y. Vaisbourd. 2023. “An Elementary Approach to Tight Worst Case Complexity Analysis of Gradient Based Methods.” *Mathematical Programming* 201: 63–96. <https://doi.org/10.1007/s10107-022-01899-0>.

Tsai, C.-E., I. Fatkhullin, L. Zhang, and N. He. 2026. “Lower Bounds for Anytime Acceleration of Gradient Descent.” <https://arxiv.org/abs/2607.02053>.

Ye, Yuhan, and Kaizhao Liu. 2026. “Silver Rate Is (Almost) Optimal for Gradient Descent Acceleration.” <https://arxiv.org/abs/2609.09152>.

Zhang, Z., and R. Jiang. 2026. “Accelerated Gradient Descent by Concatenation of Stepsize Schedules.” *SIAM Journal on Optimization* 36 (2): 1182–1210. <https://doi.org/10.1137/25M173898X>.

Zhang, Z., J. D. Lee, S. S. Du, and Y. Chen. 2025. “Anytime Acceleration of Gradient Descent.” In *Proceedings of COLT 2025*, 291:5991–6013. Proceedings of Machine Learning Research. PMLR. <https://proceedings.mlr.press/v291/zhang25a.html>.
