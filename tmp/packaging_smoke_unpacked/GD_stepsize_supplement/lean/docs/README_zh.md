# Lean 4 形式化说明

本目录提供论文中**标量递推、组合树和相位规律**的 Lean 4 证明。请先阅读根目录的 [英文审稿人指南](../../LEAN_FORMALIZATION.md)、[逐条定理映射](THEOREMS.md)和[验证范围说明](VERIFICATION.md)。

形式化从实数核 `K`、`A`，实际递推 `U`、`W` 和有限组合树开始。外部光滑凸梯度下降证书、轨迹有效性以及最坏情况紧致性的证明不在本项目内。不能把“40 项登记的标量／组合结论”表述成“整篇论文完全形式化”。

工具链固定为 Lean 4.19.0；mathlib 固定为 `c44e0c8ee63ca166450922a373c7409c5d26b00b`，其余依赖版本见 `lake-manifest.json`。论文入口为 `GD.Paper.*`，对应目标为 `GD.PaperTargets.*`；支持模块中的历史编号不是当前论文编号。

## 本次实际核验的结果

2026-09-24 的只读检查确认：74 个证明输入文件和 elaborated export 的哈希与随附的历史构建记录一致；623 个源定理均存在于导出记录中，40 个登记结果均有类型恰好为相应目标的定理。定理的公理依赖仅含标准基础公理 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx` 或额外数学公理；其导出项目证明／类型闭包中没有 `unsafe` 或 `partial` 定义。

**本次没有重新完成 Lean 全量编译。** 本机没有安装所需的 Lean 4.19.0 和 mathlib 缓存。`audit/` 中是此前构建和导出的记录，不能当成本次新运行报告；其中约两秒的构建耗时是增量构建，不是首次安装编译耗时。

当前 PDF 的 SHA-256 为 `e38f43f82aca4cf4e26d3f58d202a853aedee2bfd4be0d6c9f1fb1a5d6374003`，历史映射记录的 PDF 哈希为 `db3137a4cc77fcebf4f7956f4afdccd5ed51dd006e32dec69657f84843898fc9`。字节不同不自动意味着数学内容改变，但最终投稿前仍需逐条确认论文陈述与 Lean 类型的语义对应。不能直接改写旧哈希来宣称已经核验新版论文。

## 可用复现命令

在 `lean/` 目录运行：

```bash
python tools/check_snapshot.py --manuscript ../GD_stepsize_schedule.pdf
```

该脚本只需 Python 标准库，不联网、不修改旧审计数据。预期 `snapshot_consistent` 为 true，而 `manuscript_hash_matches` 为 false；退出码 0 仅表示历史证明证据内部一致。加上 `--require-manuscript-match` 后，当前 PDF 的版本不一致会返回退出码 2。该脚本不是 Lean 内核验证器。

安装 elan 和固定版本工具链后，重新编译证明：

```bash
lake exe cache get
lake build GD
```

初次下载工具链和依赖需要网络，无需 GPU、数据集或私有凭据。若要重新导出公理和类型信息，应在单独工作副本运行 `lake env lean GD/Audit.lean`；它会覆盖该副本的 `audit/lean_declarations.json`，不会自动更新其余来源、覆盖率或图数据。

旧文档中提到的完整 audit runner、文档生成器和 CI workflow 的匹配版本不在本补充包中，因此已撤下这些不可执行的复现指令。依赖图是随附的导航材料，不代表本次重新生成。

## 数值结果与形式证明

Corollary D.9 的有限有理数角点证书属于 Lean 证明。Proposition D.10 形式化的是精确网格界、极限和指定 real-RAM 模型下的运算次数。level-17 小数区间由独立 Python 区间程序检查，不是 Lean 内核认证的区间计算。绘图和浮点 Bellman 计算也不属于 Lean 形式化的实现验证；相关方法和运行结果见 [数值复现说明](../../NUMERICAL_REPRODUCIBILITY.md)。
