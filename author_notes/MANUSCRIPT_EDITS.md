# 当前论文需要同步修改的位置

对应原始 `GD_stepsize_schedule.pdf`（45 页）。这里只给出源稿修改建议；主 PDF
未被重写。正文 LaTeX 未随文件夹提供。数学定理和摘要不需要仅因加入 Lean
说明而改变结论。

## 第 8 页 Figure 1：保留曲线数值和原来的下方子图标题

原右图的曲线数据、极值和坐标范围是正确的，本次没有更改。旧脚本的支撑
参考线参数落在纵轴范围外；按论文 Lemma E.5 求得 `0.420809352823451` 后更新
`figures/psi_phase_compact.tex` 与 `figures/psi_phase_compact.pdf`。
新 PDF 已移除我此前添加的顶部标题，与原图一样不内嵌子图标题。
主稿中保留原来的图下方 `(b) Asymmetric: finite-scale interpolant`，不要移动它。
如使用带可见支撑参考线的新 PDF，在主稿中重新导入后编译即可。

图注中的 “The dashed line marks the sharp support barrier c_*” 可以保留。
末句（约行427–428）建议替换为：

> Numerical methods, reproduction commands, and the distinction between finite-scale plots, interval certificates, and Lean verification are documented in the supplementary NUMERICAL_REPRODUCIBILITY.md.

## 应修改：第 10 页 Reproducibility Statement（约行497–503）

当前最后一句：

> We also provide Lean 4 formalization of the mathematical results in supplementary materials.

推荐将整个段落整理为：

> The appendix proof roadmap locates the complete mathematical proofs, and Appendix A states the imported certificate interfaces and prior results. The supplement provides the scalar evaluator, reference Bellman recursions, figure data, and reproduction commands. NUMERICAL_REPRODUCIBILITY.md distinguishes floating-point computations from interval certificates. The phase-minimum and dyadic-corner certificates are specified in Appendices D.8 and D.7, respectively. The supplement also includes Lean 4 proofs of the scalar and combinatorial results identified in lean/docs/THEOREMS.md. LEAN_FORMALIZATION.md documents the pinned environment, verification commands, and scope. The external smooth-convex GD certificates and their tightness interpretation remain outside the formalization; the level-17 decimal minimum enclosure is checked separately by interval arithmetic.

注意 D.8/D.7 此处是附录**小节**，不是 Proposition D.8 和 Corollary D.7。
可用小节标签作 `\ref`，不必改正确的现有小节引用。此声明不计正文页数，
但应重新检查参考文献/附录的分页。

此版本特意不声称当前 PDF 已完成整篇认证。待最终稿与 inventory 逐项复核
并在固定工具链成功构建后，可以加入准确的 40-result 覆盖描述；不要把历史
源码 hash 核对称为新的 Lean build。

## 应说明：第 36 页，Appendix D.8，式(65)后（约行1898–1901）

在现有 certificate 解释后增加：

> Proposition D.10 is formalized in Lean. The displayed level-17 decimal enclosure is obtained separately by the interval-arithmetic procedure in scripts/check_phase_certificate.py; these particular decimal endpoints are not part of the Lean certificate.

式(65)已有严格区间计算支持，可以保留 “certified enclosure”；本次已重跑
相应 Python 全级别检查。这里需要澄清的是验证方式，而非将其降格为普通采样。

## 建议：第 11 页，proof roadmap 后（约行553–571）

> A statement-by-statement correspondence between the scalar and combinatorial results and their Lean declarations is provided in lean/docs/THEOREMS.md; LEAN_FORMALIZATION.md documents the verification commands and scope limitations.

无需为此给现有 roadmap 表增加一列；一句话足够。

## 建议：第 11 页，Appendix A 引言（约行575–579）

> The Lean development verifies the scalar and tree-based statements derived from these interfaces. The smooth-convex function classes, gradient-descent trajectories, and imported composition and tightness certificates recalled in this appendix remain outside the formalization.

这能使读者在接触 Proposition A.5 前理解标量形式化与优化解释的边界。若
第 10 页已经说得足够清楚，可缩短此处以避免重复。

## 可小改：第 10 页 AI USE STATEMENT（约行486–493）

该声明已经存在，且已披露 proof development 和 Lean scripts，不应再新建
重复章节。可把 “ChatGPT, including interactions through Codex and Cursor”
调整为 “AI assistants, including ChatGPT, Codex, and Cursor”，以准确区分工具。
把 “supplementary numerical README” 改成具体文件名
`NUMERICAL_REPRODUCIBILITY.md`。作者按真实使用情况核对正文和 OpenReview
表单即可；无需补写未经确认的模型版本或人工核验过程。

## 无需改动的内容

* 主体 9 页已经符合本次初投稿上限。
* Appendix A–E 不应因添加 Lean 项目而删去；纸面证明仍是主阅读路径。
* 数学核心结论、理论支撑常数定义、已有采样极值均不因本次绘图修复而改变。
* 参考文献与附录当前同在第 11 页；另起附录页是排版建议，不是本次查到的硬性违规。
