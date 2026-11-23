# 黎曼猜想 Lean 证明的人类可读重构与精简审计稿

> V2.7 · Theta 轨道质量、最小共同分母与 Rallis 非退化性边界 · 2026-11-23
>
> 本文件由工作稿 DOCX 的可检索文本层导出。原稿中的部分公式/版式对象可能未被文本抽取完整保留；数学公式以相邻定义、源码链接及正文解释为准。尚非最终验收版。

---


黎曼猜想 Lean 证明的人类可读重构与精简审计稿
               V2.7｜Theta 轨道质量、最小共同分母与 Rallis 非退化性边界｜2026-11-23

                         目标：从形式化依赖恢复可检查的传统数学论证


阅读前说明
这份稿件的任务不是复述“Lean 已经证明 RH”这一新闻，而是从公开 Lean 项目的最终定理反向追踪依赖，

并把其中可以恢复的数学论证改写成传统数学语言。

重要区分：机器可检查的形式证明、完整的人类可读证明、以及数学共同体对证明的独立审查，是三个不同层

次。本稿只报告已经核对的源码结构与公开工作稿内容，不把尚未理解的环节包装成已经完成的自然语言推

导。 原作者在 4 页说明中使用的是“I believe I have ... discovered a proof”的措辞，并同时说明自己尚未掌

握证明周围的大量数学；因此本稿不把作者声明、Lean 可检查性与外部数学审查混为一谈。

本稿目前达到“结构可审计、关键接口可定位、解析主线可讲清”的程度；尚未达到“每个算术几何关键引理

均已独立展开”的最终验收标准。

源码链接统一固定到仓库快照 commit 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4，避免 main 分支后

续变化造成行文与代码不一致。

-   原始作者 Levent Alpöge 的 4 页说明：https://alpo.ge/remark.pdf

-   Slijepčević 的证明纲要（94 页）：https://hexagonmath.org/pdf/2611.00812v1

-   Lean 源码仓库：https://github.com/CocoSgt/riemann-hypothesis-lean

-   解析部分的 10 页简化稿（2026-11-21）：https://hexagonmath.org/pdf/2611.00828v1（该稿自述为 Codex

    辅助整理，故只作为解析简化参考，不视为独立同行审查）

2026-11-23 核查更新：Michael Rubinstein 的 164 页工作稿（2026-11-21）已系统整理从主不等式 (M) 推出 RH 的解析部

分，但 (M) 的完整自然语言证明仍未写成。Rubinstein 与 Andrew Sutherland 报告了完整 Lean 编译、标准公理审计和独

立 kernel 校验通过；此处严格区分形式系统的独立检查与可供数学家逐步阅读的算术证明。资

料：https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/；https://math.mit.edu/~drew/grh/。


                                   

---


一、最终定理究竟是什么
Lean 中的核心目标先是所有 Dirichlet L 函数的零点排除，而不只是 Riemann zeta 函数。源码定义的

EveryCharacter 可写为：

    对任意模数 N、Dirichlet 特征 χ 及复数 s，

     Re(s) > 1/2 且 (χ ≠ 1 或 s ≠ 1)

     ⇒ L(s, χ) ≠ 0。


-     其中 χ=1、s=1 的例外对应 ζ(s) 在 s=1 的极点。

-     对所有 Dirichlet 特征得到右半平面的零点排除后，再结合函数方程处理临界带左半边，得到 Dirichlet GRH；

      Riemann zeta 函数的 RH 是其特例。

-     本项目最终定理链位于 src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean；

      最后一步调用 riemannHypothesis_of_everyCharacter。


二、五个真正的核心依赖
Slijepčević 的纲要明确指出：在窗口版 Landau 零点排除之后，整个论证被归约为以下五个结果。它们不是任

意挑选的章节标题，而是从辅助域、格数据到素数和上界的实际接口。

    核心结果                             作用                                 输出

    命题 4.11                          单个辅助域 + core-tied 格数据              G_L(x) ≤ x^(1/2+(e_D+e_L+7)ε)

    命题 3.5                           由 Sha 窗口界供应辅助域                     在包含 3/2-窗口的尺度集合上构造合格

                                                                        hosts

    引理 6.14                          把 chain-tied 家族落实到单个成员             从链式绑定抽取 core-tied host

    命题 6.20                          由 host 供应与 Sha 界构造 tied families   得到与 ε 无关的 e_D、e_L

    定理 9.1                           统一 Tate–Shafarevich 群窗口估计          每个 primitive ψ 满足指数 401 的 window

                                                                        Sha bound


三、五个结果如何拼接
固定一个 primitive Dirichlet 特征 ψ，记其阶为 o。首先由定理 9.1 得到指数 401 的窗口 Sha 界；再由命题

3.5，在一批含有 3/2-窗口的尺度上供应具有所需 Galois 群、Artin 映射、局部条件和 Sha 界的 host。

命题 6.20 将这些 host 组织成 tied family，并给出不随 ε 改变的误差指数 e_D、e_L。对任意足够大的窗口尺

度，家族的 chain-tied 性质由引理 6.14 变成某个成员的 core-tied 性质。最后命题 4.11 给出加权 Chebyshev

函数的窗口上界。

这正是证明中最重要的量词结构：e_D、e_L 必须先固定，再让 ε 任意趋近于 0。否则指数无法逼近 1/2。
                                      

---


精确的 ε 选择如下。给定目标点 s，令 m=min(Re(s)−1/2,1/2)>0；选 ε 使 (e_D+e_L+7)ε≤m/2，置

θ=1/2+m/2。命题 2.4 给出 G_{Lψ}(x)≤x^{1/2+(e_D+e_L+7)ε}≤x^θ；命题 2.2 排除 Re(ρ)>θ 的零点，而

θ<Re(s)，故 L(s,ψ)≠0。

    Theorem 9.1

      ↓

    Proposition 3.5: hosts on 3/2-windows

      ↓

    Proposition 6.20: tied host families (e_D,e_L independent of ε)

      ↓

    Lemma 6.14: chain-tied family → one core-tied member

      ↓

    Proposition 4.11: G_L(x) ≤ x^(1/2+(e_D+e_L+7)ε)

      ↓

    Proposition 2.2: window Landau zero-free criterion

      ↓

    EveryCharacter → Dirichlet GRH → RH


四、解析部分：把零点问题转成一个单边素数和上界
记 Λ(n) 为 von Mangoldt 函数，并令 u_+=max(u,0)。对 ζ 函数定义 Riesz 平滑的素数和：

    G_1(x) = Σ_{n≥1} Λ(n) (x/n - 1)_+

          - x log x + (1+γ)x。


    对非主 primitive 特征 ξ，定义

    G_ξ(x) = Σ_{n≥1} Λ(n) ξ(n) (x/n - 1)_+

          + x · L'(1,ξ)/L(1,ξ)。


-      对 primitive ψ，令 F_ψ 为 ψ 的各次幂所诱导出的 primitive 特征代表，包含主特征。若 o=ord(ψ)，则权重取

       κ_1=1，κ_ξ=1/(3o+1)（ξ≠1）。

-      定义 G_ψ(x)=Σ_{ξ∈F_ψ} κ_ξ Re G_ξ(x)。正权重的设计使得不同 L 函数若在同一点有共同零点，其对数导数的

       留数不会相互抵消。


五、Mellin 变换与零点留数
关键积分可以直接计算：

逐项积分并使用 Euler 乘积，可得加权函数的 Mellin 变换：


---


    ∫_1^∞ (x/n - 1)_+ x^(-s-1) dx

     = n^(-s) / (s(s-1))，Re(s)>1。


    M_{Gψ}(s)

    = - 1/[s(s-1)] · Σ_{ξ∈Fψ} κ_ξ L'(s,ξ)/L(s,ξ)

     - 1/(s-1)^2

     + [1+γ+Σ_{ξ≠1} κ_ξ ℓ_ξ]/(s-1)，

    ℓ_ξ=L'(1,ξ)/L(1,ξ)。


-      在 s=1 处，中心化项与 ζ 的 Laurent 展开抵消相应极点。

-      若 ρ 是家族中某个 L(s,ξ) 的零点，m_ξ(ρ) 表示其重数，则 Mellin 变换在 ρ 处的留数为 Σ_ξ κ_ξ m_ξ(ρ) / [ρ(1-

       ρ)]。

-      当 ρ=β∈(0,1) 为实零点时，分母 β(1-β)>0，因此留数为正；对非实零点，分子仍是正权重重数之和，多个特征

       共享零点时不会在分子中抵消。


六、窗口版 Landau 原理
若存在零点 ρ 且 Re(ρ)>θ，那么相应 Mellin 变换在 θ 右侧有极点。Landau 型论证说明，单边上界

G_ψ(x)≤Kx^θ 不可能在任意靠后的整段乘法窗口中持续成立。

本证明需要的窗口形状是 [Y,Y^(3/2)]，其中 Y 可以任意大。于是，只要对每个足够小的 ε，都能在这些窗口上

证明 G_ψ(x)≤x^(1/2+Cε)，就可任取 θ>1/2 并选择 ε 使 1/2+Cε<θ，从而排除 Re(ρ)>θ 的零点。让 θ 下降到

1/2，即得到右半平面的零点排除。

-      原 Lean 证明的 landauWindow.lean 走的是高阶导数、Cauchy 估计和最近极点分析路线；lemmaL.lean 将其

       用于特征族。

-      2026-11-21 的补充稿给出另一种较短的证明：利用 Kaczorowski–Pintz 的符号变化定理。它把可能的实极点通

       过减去 r_β x^β(1−cos(u log x)) 转化为同实部的非实极点，再与好窗口上的负性矛盾。

-      这份补充稿是解析部分的独立简化，不应冒充 Lean 原证明实际采用的步骤；它也不负责构造 Theta Lift 或证明

       Sha 界。

-      Landau 判据需要的是组合中各特征的权重为正，并不要求带特征扭曲的 Dirichlet 级数系数本身非负；这一区

       分是本方法能处理复杂特征的关键。


七、辅助域 host 与 window Sha bound
一个 host 是嵌入某个分圆域的阿贝尔 CM 数域，连同其 Galois 群与 Artin 映射的显式描述。其抽象 frame 包

含有限阿贝尔群 A 和循环子群 A₀；在本问题中 [A:A₀]=o，因而在对 A₀ 平凡的字符中可以编码 ψ 的各次幂。


---


窗口素数对由 q、d 构成，典型条件包括 q≡3 (mod 8)、d≡7 (mod 16)、q | d+1，以及所有足够小的奇素数

p 都整除 d+1。其大小满足 log q≈Y^(ε/5)，log d≈Y^(ε/5)log²Y。这些条件为 Q(√−d) 中小素数的分裂和

host 的局部构造提供算术控制。

更精确地，纲要把相关群记为 Sha^1_ℓ(E, Q_ℓ/Z_ℓ(−k))；它通过 Poitou–Tate 对偶与 H²(E,Z_ℓ(k+1)) 联系，

并由 Soulé 型结果与 K 理论输入控制。Lean 的 VVle 以 shaLen 的长度函数编码这些群。

    VVle(E,t,B) 的数学含义：


    对所有相关的 ℓ-adic Galois 上同调数据：

    1. 每个素数 ℓ、每个 1≤e<t 的 Sha 长度均有限；

    2. 对任意有限素数集 S，

      Σ_{ℓ∈S} log(ℓ) · Σ_{1≤e<t} len_ℓ(E,e) ≤ B。


    VWinAt(ψ,401)：

    对任意小 ε、任意允许的 page function，

    对每个足够大的 X 和窗口素数对 (q,d)，

    存在 Y，使 X^(1/J)≤Y、Y²≤X，

    并且所有 x∈[Y,Y²] 上的相关数域 E 满足

      VVle(E, floor(x^401), exp(x^ε/2))。


-     这里的指数 401 是 rank 上界的幂指数；B=√exp(x^ε)=exp(x^ε/2) 是总加权 Sha 长度的上界。

-     定理 9.1 的路线包括：将 Sha 约化为严格 Tate–Shafarevich 群；利用 Poitou–Tate 对偶、局部 Tate 对偶、

      Soulé 型 H² 界和 Ferrero–Washington 处理坏素数；主情形使用 U(3) Eisenstein congruences；其他情形使用

      GSp₄、酉群提升及相应消失结论。

-     命题 3.5 再把这些窗口 Sha 界与二次特征扭曲的均方估计、分圆域类域论结合，构造具有所需 host 条件的辅助

      域。

-     401 的来源可在 PageFix.lean 直接核算：eP=12，cTO=28·12+41=377，Ct=cTO+24=401；PageWin 同时固

      定 host 的 n、m、k 三个尺度区间。VWinAt 中的指数 401 正是这套 page 参数的 Ct。


八、Theta Lift 链、格与 tied families
证明的算术几何部分把每个 host 配上一组 Hermitian 格、自动形式空间及 Theta Lift 链。作者的说明把这一

机制与 Stepanov 方法作类比：在函数域证明中，函数的高重数可以由导数/重数直接制造；在整数环上没有

同样方便的“对整数求导”，于是通过迭代 Theta Lift 来模拟重数。作者说明链长与素数和长度 X 的关系约为

√X。


                                             

---


Section 7 的 Theta agreement 与局部匹配把 Theta 常数沿塔的变化联系到临界 Hecke L 值的乘积，形状类

似酉群 Rallis 内积公式。Section 8 则通过酉 Shimura 簇整模型上的算术高度下界、塔上的算术比例关系和格

协体积估计，提供所需的 covolume 控制。

这些格数据被打包成 master data。chain-tied 表示同一有限群 A 上一族成员在不同平移处共享 rank、top、

权重、局部数据、算术数据和误差参数；core-tied 则是某一个 host 已经具备 Proposition 4.11 所需的完整单

点数据。

-      Lean 中 TieGlobal.lean 的 TieGlobal、TieLocal、TieArith 分别要求不同成员的全局数值、局部格量和

       Artin/字符数据彼此兼容；ChainTied 将它们连同 SizeData、ErrWindows、BNBounds、

       GrowthInequalityRemainingHyps、CostWindows 等条件整体打包。

-      LevelGmLeOnFamilyScales.lean 中 tiedCore_of_chainTied 把 ChainTied 转换成

       FamCoreConstantBounds；这正是把“家族级结构”变成“某个 host 的单点核心数据”的程序化接口。

-      引理 6.14 的数学内容很朴素：若一个参数化 host 家族在 x 处 chain-tied，那么至少有一个成员在同一 x 处

       core-tied。难点不在这一步的概念，而在 chain-tied 的定义包含大量精确的跨成员兼容条件。


九、Sha 界如何进入格的局部缺陷
命题 6.20 是 Sha 与 Theta Lift 格数据相接的关键。它的输入是：host 在含 λ-窗口的尺度上供应充分；并且每

个成员的数域 E 满足 V(E;t,√b)。输出是：存在 e_D、e_L 和 ε₀，使每个足够小 ε 都能构造相应的 tied

family，且 e_D、e_L 不随 ε 改变。

纲要说明，Sha 界通过 linking inequality 控制格的局部缺陷 η_j。其关键项可概括为：

    Σ_ℓ log(ℓ) · Σ_{k<t} len_ℓ(E,k) ≤ √b

               ↓

            局部格缺陷受控

               ↓

          slope / divisor / cost 条件

               ↓

            tied family 存在


-      命题 6.18 的 definite-side family structure、Green 对有限域 cuspidal characters 的参数化，以及一个

       closure statement 被组合起来构造 tied families。

-      Section 11 明确承认：纲要作者没有展开 closure statement，也没有完全理解 Sha 界如何进入 slope

       conditions 的参数。


                                           

---


十、单个 host 如何给出素数和上界（命题 4.11）
这是整套方法最重要的桥。host 的 Galois 群写成 Γ_H=(Z/2Z)^2×H。对每个平移 u，定义惯性素数和 S_u；

它是对 top t 与 Theta Lift 链层 j 求和的惯性素数贡献。

格数据在每个惯性素数 p 上产生一个净局部增益。把这些增益乘以 log p 并求和，得到 Θ_u。损失条件（S3）

要求 S_u−Θ_u 不超过一个小的统一损失。随后，斜率转移不等式、对偶斜率界和除子界把 Θ_u 控制在主项之

下，从而得到 S_u≤Main(u)+Err(u)。

本轮继续追踪后，已经恢复 S3 的形式化来源：LinkG_at 给出逐素数的格增益覆盖与轨道残差界；

ChosenBadp 控制坏轨道总质量；ChW_at 控制大局部份额的加权质量；

LossRequirementsOfSmallShares.loss_setting_family 将三者转成 PrimeClassLossHypotheses，再由

Losses5OfLossHypD 汇总为 LossBounds。仍未完全恢复的是这些 LinkG / 小份额条件如何由底层 Theta Lift

几何输入证明。

    第一半（算术/几何）：

    S_u ≤ Θ_u + Loss

    Θ_u ≤ Main(u) + slope/divisor errors

    ---------------------------------------

    S_u ≤ Main(u) + Err(u)


    第二半（解析）：

    对 u∈A₀ 平均

     ↓

    有限阿贝尔群字符正交

     ↓

    隔离与 ψ 的幂相关的 primitive 特征

     ↓

    控制其他辅助特征

     ↓

    G_L(x) ≤ x^(1/2+(e_D+e_L+7)ε)


-    Proposition 4.8 是字符平均部分；Proposition 4.5 是斜率与格增益部分；Proposition 4.9 吸收误差；

     Proposition 4.11 将它们合并。

-    Lean 的 CoreAtH 定义明确列出 host-character compatibility、IdentU、SizeData₂、ErrWindows、

     BNBoundsU、SizesA、ThinScales、CostWindows 和 RestSize 等条件。

-    CoreGm.lean 中 core_gm 的证明实际调用 Deduction.ch_core、Deduction.ch_top、gmA_eq 和 sigA_le。

     它不是简单的 `linarith`：ch_core 负责字符正交与 Chebyshev 函数比较，ch_top 负责把格斜率数据转换成惯

     性素数和上界。


---


-         真正未被自然语言纲要解释清楚的核心是：Theta Lift 格在经典术语下的“局部增益”究竟是什么，以及为什么

          这些局部增益能逐素数控制惯性素数贡献，且总损失满足 (S3)。


十-A、S3 的源码级重构：从局部轨道到统一损失界
这一轮已经把 S3 从抽象条件追到具体 Lean 数据结构。核心不是一句“格增益覆盖素数和”，而是把每个

inert prime p 的 Frobenius 轨道分成 good/served、bad/unserved 和高份额等类别，再分别估计。

先看 Frobenius 轨道。对 inert p，h_P(p) 是 host Galois 群中的 Frobenius 元素；topsOn(X,p,t₀) 是 top 标

签 TT 中落在同一轨道代表 t₀ 下的元素，Nv(X,p,t₀) 是该轨道内 top 标签数。Good(X,p,t₀) 表示这些标签在循

环轨道上的位置满足一个均匀分布条件；goodReps 收集所有 Good 的轨道代表。

定义 Sig(p)=m·Σ_{t₀∈goodReps(p)} kapv(p,t₀)。VV(p) 只在 p 是候选素数且 Sig(p)≤x^(−ε) 时保留

goodReps；因此 VV 是“份额小且轨道良好”的可服务轨道集合。badTops(p) 则是 TT 中落在非 Good 轨道

的标签。

    Sig(p) = m · Σ_{t₀∈goodReps(p)} kapv(p,t₀)


    VV(p) =

     goodReps(p), if p is a candidate and Sig(p) ≤ x^(−ε);

     ∅,          otherwise.


    Sv(p,t₀) =

     ceil Σ_{j=1}^m max(0, gU(p,j,t₀) − Pr(p,j,t₀)

                   − max(g0(p,j,t₀),0)).


    ioP(p) =

     2 · Sig(p) · max_{t₀∈VV(p)} Sv(p,t₀), if VV(p) ≠ ∅;

     0,                       otherwise.


-         g0 与 gU 是两种对同一 Frobenius 轨道局部素数幂贡献的估计表达式；它们由 top 权重 a、局部截断 capU、奇

          数幂求和及离散化误差 dl 组成。Pr 是对非 V 型标签和小素数区间的修正项。Sv 统计实际贡献超过这两种估计

          所覆盖部分的剩余量。

-         gainP(p,j) 对 VV 中的轨道累加 max(gU−Pr, max(g0,0))，对 VV 外的轨道累加 max(g0,0)；tauP(p) 则在 VV 非

          空时加入 ep(p) 及每个被服务轨道的阈值成本。它们是把轨道级局部估计压成逐素数“收益—成本”数据的对

          象。

-         LinkG_at 的第三组条件给出真正的格覆盖不等式。对 inert p≤X''，每层 j 的局部增益满足 0≤gain(j,w)≤4|TT|

          a/p；同时，served top 标签的 von Mangoldt 类和减去局部误差 lo、fl 后，不超过 Σ_j gain(j,w)−tau(w)。这

          就是局部格增益支配惯性素数贡献的精确形式。


---


-        LinkG_at 的第二组条件进一步要求每个被保留轨道满足 Sv(p,t₀)≤2m·Nv(p,t₀)·a/p。因此

         ioP(p)≤2·Sig(p)·2m·Nv·a/p，恰好能接入后面的 IoD 估计。

-        坏轨道由 ChBadp_at 控制：Σ_{p∈largeOrderResiduePrimes}(log p/p)|badTops(p)|≤|TT|x^(−2+ε)。小份额

         由 ChW_at 控制：Σ_{p∈cands}(log p/p)(2·1_{x^(−ε)<Sig(p)}+4Sig(p))≤x^(−9)。前者控制 served 集合外的

         未匹配标签，后者控制大 Sig 素数及 ioP 残差。

-        PrimeClassLossHypothesesSatisfiable.lean 将误差拆成 OutD、SecondD、IoD：OutD 用

         badPrimeLogWeightedCount 控制 served 类中未服务的标签；SecondD 用 lhsW 控制第二类高 Sig 素数；

         IoD 用 io≤4mT a Sig/p 控制局部 io 项。三者分别给出显式上界。

-        PrimeClassLossHypotheses 还记录 prime class cl、served 标签集 TTp、局部误差 lo/fl、gainP/tauP 及候选

         集之间的兼容关系。显式大小估计把其余边界项（floors、CP bucket、低/高素数、order、band、

         discriminant 等）逐项吸收，最终得到系数 (2 log 4 · C + 13·sg(P,K))·unitU。

-        LossRequirementsOfSmallShares.loss_setting_family 的实际输入是 PtH、LinkG_at、ParTie、

         ChBadp_at、ChW_at 及非空 TT；输出 PrimeClassLossHypotheses。随后 losses_of_small_share_weight

         将其变成 LossesSmallShares，再由 lossF_of_7W 和 ChosenW 得到 LossF。

-        最终 Loss_at 同时控制两项：IOsum，以及任意可读入同一 host 数据的算术数据中 ASK−Ga。抽象层的

         LossBounds 正是 ∀u₀，ASK(u₀)−Ga(u₀)≤LoP 且 IO(u₀)≤LoP。


十-B、LinkG 的上游：RecTAlt 如何把 Theta 数据变成局部格控制
现在可以把 S3 的上游再向前追一层。Lean 并不是直接假设 LinkG；它从一个随尺度 x 和索引 i 变化的

RecTAlt 结构出发。TwistSelectionFunctions 要求存在 x₀，使得对所有 x≥x₀、所有 i，都能选出一个

RecTAlt(Fm.ex x i)。这是一项统一的家族存在性，而不是单个数域上的偶然选择。

RecTAlt 的字段揭示了它的数学内容：T 是 TiedDataSKAlt；另有 RowPinMinAlt、JointsSAlt、

HostDatumSelfDual 和 Theta.WeilCompatibleEquivariance。TiedDataSAlt 内部包含 host/level、

Hermitian columns、完整列空间、额外列兼容性、Theta.AllTied、twist/character 数据、行兼容、几何数

据以及 GroupCompatibilityAll。TiedDataSKAlt 再加入 kernel、每层坐标矩阵、Gram 恒等式、自对偶格坐

标刻画和核形式恒等式。

因此，RecTAlt 可以理解为：在一个 host 上，把 Theta/Weil 数据、自动形式列、Hermitian 格、局部

Hida/表示数据和递归链的 Gram/核结构同时绑定起来的完整记录。它是从 Theta Lift 构造走向局部格增益的

实际载体。

    TwistSelectionFunctions

    ⇒ 对所有充分大的 x、每个 i，选出 RecTAlt(Fm.ex x i)


    RecTAlt

    ={


---


         TiedDataSKAlt,

         RowPinMinAlt,

         JointsSAlt,

         HostDatumSelfDual,

         Theta.WeilCompatibleEquivariance

     }


    TiedDataSKAlt

    = TiedDataSAlt

     + kernel / coordinate matrices / Gram identities

     + self-dual lattice-coordinate equivalence

     + kernel-form identity


    TiedDataSAlt

    = host + level + Hermitian columns + Theta.AllTied

     + twist/character/row/geometry data

     + GroupCompatibilityAll


-        GroupCompatibilityAll 本身包含 Herm0、每个 word 的 Forms0、CmpTied、RingCompatibleAt 和 GatIs。

         它把抽象的 Theta/automorphic package 变成可在每个局部 place 上使用的 Hermitian 与环结构。

-        Duty 的精确组成是 PageFix、PageWin、SmallFirstModulusBelowScale、TameDistinctF、ChosenWall、

         TupUsedF 和 TwAllF。PageFix 固定 Cp=1、eP=12、cTO=28eP+41=377、Ct=cTO+24=401 等常数；PageWin

         规定 n≈x^(2+8ε)、m≈√(xδ₁)、k≈x^(9/2+10ε)。因此 Sha 窗口指数 401 与 PageFix 的 Ct 是同一常数，并非

         任意挑选。

-        class_duties_of_choice 将被选中的 RecT 记录和 Duty 变成 LinkedFamiliesAligned；

         layerTwoFamilyClass_of_linked_aligned 再得到 SecondLayerFamilyClass；

         group_compatibility_of_second_layer_family 将其变成 GroupCompatibilityFamily。

-        GlobalTheory.Top.closed_linkG_of_duty 的证明正是这条链：Raw selection 给出 RecT 选择，Duty 保证跨

         尺度对齐；由此获得 SecondLayerFamilyClass，再调用 linkG_concrete5。后者从

         GroupCompatibilityFamily 与 Adm2F 推出 LinkG。

-        linkG_concrete5 的内部进一步使用 GroupCompatibilityAll 推出的 TrivialStabiliserFiniteClasses、StdSubAt

         和 NPDescF，以及两套 LocalDataSystem（lowU 与 lowFE）和 Loc 中的局部数值/群论结果。换言之，LinkG

         的局部格控制不是纯形式包装，而是依赖一整套局部环、格比较和群兼容性定理。

-        在顶层，HypsAlt 保存 raw selection、hduty、definite-side row/column data、spectral ties、Theta/Weil

         inputs、counting constants、mass/volume estimates、period inputs 等大量条件。published literature

         inputs 与 ThetaIntegralsAgree、LocalMatching、CovolumeBoundOfX、RecTExists 一起先构造 Nonempty

         HypsAlt；TopPlug 再将 Green、VWin 和 HypsAlt 合成为 ZeroFreeAll。


---


十-C、Theta Lift 如何产生 Galois 表示（最终定理的另一条主干）
最终证明并非直接把一个现成的 Galois 表示塞进窗口估计。RowSrc.lean 中的

galoisLocalGlobalStrong_recParameter 是从一个完整的 Theta Lift 存在定理 TLiftK 构造出来的。

TLiftK 的数学内容是：给定 CM 数域 E、满足良好条件的基 B、一个正定 Hermitian 数据 X 和足够大的目标维

数 d，对任意满足标量条件的 skew-Hermitian 数据 W、兼容的 Hecke 字符与指数数据，以及满足相应无穷处

权重不等式的酉群自守表示 U，存在目标酉群上的自守表示 U'，使 U' 与 U 之间存在指定的 theta lift 关系，并

满足预定的权重转移和分裂有限处的局部配对条件。

TLiftK 在源码中不是一个空白公理。TPGHolds.lean 构造 Tools_k；TPGTop.lean 将这些工具代入

tLift_of_tools_k；其关键非消失部分又组合 Rallis 内积公式、表示分解、Bump 型非消失、datum/tail 控制

和 SchurStep。最终得到 tLift_holds_k，再得到 TLiftK。

Row0b 的输出是强局部—整体相容性：对每个正则代数 cuspidal 自守表示 π 及相应的 polarized character，

存在连续半单 Galois 表示 r:G_E→GL_a(\overline{Q}_ℓ)；几乎处处的特征多项式与局部 Weil–Deligne 参数

匹配；无穷处 Hodge–Tate 权重与自守权重相符并满足共轭对称；ℓ-adic 处满足 crystalline/de

Rham/potentially semistable 及 monodromy-jump 条件。

tools_holds_k

 ├─ Siegel–Weil / Eisenstein continuation

 ├─ finite-level & compactness / stabilizer

 ├─ theta basic / polynomial Schur

 ├─ unfolding / Weil pair existence / split model

 ├─ vacuum fixing / operator actions / Lie algebra

 └─ local theta-kernel identities

   ↓

tLift_of_tools_k

 ├─ branching & height bounds

 ├─ real-pair compatibility

 ├─ Rallis + decomposition + nonvanishing

 ├─ SchurStep

 ├─ automorphy of lift

 └─ projection / read-lift

   ↓

TLiftK


TLiftK + GeoOne

 ├─ GeoOne → SeedFinOdd

 ├─ WtLacEx → CongFinOdd


                                              

---


     ├─ SeedFinOdd + CongFinOdd → LimFinOdd

     └─ TLiftK + ClosedPhi + DescOffT + LimFinOdd → Core

                    ↓

                 Core + Inputs

                    ↓

                   CoreAll

                    ↓

            unlinked support + Iwahori compatibility

                    ↓

                   Row0

                    ↓

                  Row0b


-     TLiftK 的输出不是单纯的“存在另一个表示”：IsLift 还携带目标表示的自守性、权重转移以及分裂有限处的局

      部 Weil 配对。它为后续的 Galois 表示构造提供可追踪的 automorphic input。

-     另一条输入是 GeoOne。WeightOneGeometricRealization.lean 将 holomorphic Lefschetz formula 应用于有

      限 étale correspondence，得到 geometric_realization_of_weight_one，再得到 GeoOne。GeoOne 的结论

      是在特定 CM 场、非分裂素数集、酉群自守形式及局部 Satake/权重条件下，构造满足 VBase、局部

      crystalline、monodromy jumps 和 PhiKilled 条件的 Galois 表示。

-     SeedFinOdd 由 GeoOne 与除子整除、复共轭、饱和性、局部特征和 gap 条件组合得到；CongFinOdd 由

      WtLacEx（p-adic weight-lattice congruence）得到；limFinOdd_of 将两者合并。

-     Development.lean 中的核心组合为：TLiftK + ClosedPhi + DescOffT + LimFinOdd → Core；再由 Core 与额

      外 Inputs 得到 CoreAll；最后利用 unlinked support 和 Iwahori-fixed 局部—整体相容性得到 Row0，再强化为

      Row0b。


十-E、Row0b 如何导出定理 9.1 的 VWin（窗口 Sha 界）
VWinAt(ψ,401) 是定理 9.1 的精确形式化接口。它要求：对任意足够小 ε、任意符合 PageN 的 page

function、每个足够大的 X 及每个允许的窗口素数对 (q,d)，都能找到 Y，使 X^(1/J)≤Y、Y²≤X，并且对所有

x∈[Y,Y²]，相应数域 E 的前 floor(x^401) 层 Sha 长度总和受 exp(x^ε/2) 控制。

实际 Lean 路线为 Row0b → OpenImageCondition → automorphic_window_of_inputs →

v_window_of_literal_automorphy_n → VWin。这里还需要 BaseChangeIsobaricN，以及一整组局部表示

论、自守形式、CM 几何和 Galois 上同调输入；所以不能把定理 9.1 简化成“Galois 表示一旦存在就自动有

Sha 界”。

    Row0b + BaseChangeIsobaricN + OpenImageCondition

     ↓


---


    LiteratureRankNHypothesis

     = LitLocAlt + LiteratureAutomorphyHypothesis

      + LitCoh + LiteratureCMHypothesis

     ↓

    published_hypotheses_from_patching_alt

     ↓

    HypothesesH'

     ├─ Kato / automorphy → Count I

     ├─ SP4 image / adjoint lift → Count II & III

     ├─ reduced unitary lift → Count V

     └─ end/vanishing inputs → Count Z and auxiliary bounds

     ↓

    vwin_of_hypotheses_H_E_alt

     ↓

    VWin = ∀ primitive ψ, VWinAt(ψ,401)


-      LitLocAlt 包含 Bernstein–Zelevinsky 有限性、几何引理、Langlands 多重段、Jacquet 等局部表示论输入；

       LiteratureAutomorphyHypothesis 包含 cusp rapid decay、Harish-Chandra 有限性、GL 自守形式有限性、

       Jacquet–Shalika、cuspidal spectrum、base change、Gelfand–Kazhdan、Clozel purity/cohomological、

       global Artin reciprocity、ray class field、Hecke L-adic character 和 de Rham/potentially semistable 输

       入。

-      LiteratureCMHypothesis 包含 Grothendieck deformation、abelian de Rham、dual crystal、period

       comparison、Gauss–Manin periods、Serre–Tate good reduction、elliptic CM、Hilbert class field j、

       Siegel–Klingen–Deligne–Ribet、partial zeta 与 Hecke–Tate functional equations。

-      published_hypotheses_from_patching_alt 将上述输入转成 HypothesesH'。随后

       vwin_of_hypotheses_H_E_alt 先取得 K 与端点估计，再用 Kato/automorphy 计数、SP4 image、adjoint lift

       和 reduced unitary lift 建立 Count I、II、III、V 等项，最后由 Core.of_four_alt 得到 VWin。

-      这也解释了为什么定理 9.1 在 Lean 中是一个极大的依赖节点：它同时调用 Galois 表示、base change、CM 几

       何、局部—整体自守理论和一组精细的 congruence/counting 估计。


十-D、TLiftK 的非消失证明：Rallis 内积公式如何真正发挥作用
把 TLiftK 再拆开，核心不是一句“theta lift 非零”。Lean 将其分成：构造测试向量、证明 theta 积分收敛、

用 Rallis 内积公式识别内积、证明内积非零、提取自守表示、读取局部类型六步。

在一个 theta pair (X,W,M,χX,χW,ω) 上，先选取输入自守表示 U 中的非零向量 φ，以及多项式/Schwartz 数据

f₀。RealPair_k 保证可选到与 U 同型、具有所需无穷处权重的输入向量；BumpAny_k 与 Datum_k 在有限多

个指定 place 构造局部 bump 函数，在其余 place 使用标准 vacuum，从而得到一个全局有限数据 Φ。
                                                

---


Decomp_k 给出酉群的 adelic 分解与紧性/开闭性信息；HgtFst_k 给出矩阵系数的高次可积性；Tail_k 选择

足够大的有限 place 集，使 off 部分的积分尾项小于主项。Rallis_k 则把 theta lift 的内积写成一个显式的双积

分/轨道和表达式。

NonVan_k 将 Rallis 恒等式、Decomp、BumpAny、Datum、Tail、绝对非零性 AbsNe 和 SchurStep 组合，

证明存在有限数据 φ_f，使 theta lift lift(M,ω,Φ,φ) 不为零。LiftAut_k 再证明由 theta 积分得到的函数确实属

于目标酉群的自守表示；ProjEx 取出目标表示中的非零不可约投影；ReadLift_k 最后读取其无穷处权重和分

裂有限处的 LocPair 条件。

    RealPair_k

    → choose nonzero input vector φ and polynomial datum f₀


    BumpAny_k + Datum_k

    → local bump functions at S + standard vacuum outside S

    → global finite Schwartz datum Φ


    HgtFst_k + Decomp_k + Tail_k

    → convergence and control of adelic tails


    Rallis_k

    → theta inner product = explicit global/local integral


    NonVan_k

    → Rallis + nonzero local datum + tail control + SchurStep

    → theta lift is nonzero


    LiftAut_k + ProjEx

    → extract a nonzero automorphic representation U'


    ReadLift_k

    → prescribed infinity weights + split-place LocPair

    → IsLift, hence TLiftK


-      Rallis_k 的形式化陈述给出：对适当的 theta kernel 系数与 cusp forms，相关积分可积，并且提升为零会迫使

       一个明确的积分恒等式为零；NonVan_k 反向利用非零积分排除提升为零。

-      Decomp_k 不只是群的形式分解；它把 adelic 群拆成无穷处、有限多个指定处和其余处，并控制各部分的拓扑

       性质，使全局积分可以分解为局部数据与可控尾项。

-      BumpAny_k 保证在单位元任意小邻域内存在具有规定局部支持的 bump 函数；Datum_k 进一步保证由这些局

       部 bump 与 vacuum 拼成的全局 theta 系数在单位元处非零，并对相应局部群满足规定变换关系。


---


-   Tail_k 使用高次矩可积性，扩大有限集合 S，使 off 部分非整数/非全整点的尾积分严格小于整数部分的贡献；

    这一步是把局部非零信息提升为全局非零信息的关键。

-   SchurStep_k 给出非零常数 κ，使一个平均后的矩阵系数积分等于 κ 乘以原矩阵系数。这是从 theta 积分非零

    到不可约表示分量非零的表示论步骤。

-   这条链是标准 theta correspondence 证明模式的形式化版本：Rallis 内积公式负责把非消失转成积分，局部测

    试函数保证积分不为零，Schur/投影抽取不可约目标表示，最后再读取权重与局部配对。


十一、11 月 21 日补充简化稿的价值与边界
补充稿《Three simplifications in the Alpöge–Claude argument for Dirichlet GRH》对解析桥进行了三项改

进。第一，把低斜率输入空间的秩损失按阈值积分，得到 UH/(U+H) 型界，避免点态包络积分带来的对数损

失。第二，把不同权重 w 下的 G_χ(a_t/w) 统一移动到共同尺度 x，保留真实的权重 a_t/x，再通过平移平均和

字符正交提取固定 Dirichlet 特征族。第三，用 Kaczorowski–Pintz 的符号变化定理给出更短的窗口零点排

除。

这份稿件最有价值的是它让“斜率比较 → 固定尺度素数和 → L 函数零点”这一段更易读。但作者明确把

Theta Lift 的构造和产生窗口估计的算术输入作为前提。因此它没有解决 Section 4 最深处的局部增益/损失来

源，也没有替代 Section 6–10 的算术几何证明。


十二、Lean 源码地图（可逐项核查）
以下链接对应本轮实际追踪到的声明与证明入口。它们是后续逐条重构的索引，不代表每个文件已经被本稿完

整翻译。

-   最终定理组合：MainConclusion.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/CharacterBoxes/MainConclusion.lean

-   Galois 表示构造：Development.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/

    Development.lean

-   从 Galois row 得到窗口 Sha 界：VwinOfRow.lean — https://github.com/CocoSgt/riemann-hypothesis-

    lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/

    AutomorphicVarieties/ModularityArgument/ThresholdArguments/DenseThresholdCases/

    VwinOfRow.lean


                                   

---


-   Sha 界定义：ExistsPageN.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean

-   Sha 界转成除子/局部界：DivinNOfHypV.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean

-   host 供应：SupplyChi.lean / HostOfField.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/CharacterBoxes

-   core-tied 条件：CoreAtH.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/PrimitiveCosets/CoreAtH.lean

-   单 host Chebyshev 上界：CoreGm.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/PrimitiveCosets/CoreGm.lean

-   chain-tied 定义：TieGlobal.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Formalism/SharpRestriction/GlobalSchurBounds/TieGlobal.lean

-   chain-tied 转成窗口估计：LevelGmLeOnFamilyScales.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/

    AutomorphicArithmetic/PrimitiveCosets/LevelGmLeOnFamilyScales.lean

-   窗口 Chebyshev 估计：WindowInequalityOfArtinInputs.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/

    AutomorphicArithmetic/PrimitiveCosets/WindowInequalityOfArtinInputs.lean

-   Landau 窗口引理：landauWindow.lean / lemmaL.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/

    AutomorphicArithmetic/DedekindLFunctions/LandauTheorems

-   从所有 Dirichlet L 函数推出 RH：RiemannHypothesisOfEveryCharacter.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/CharacterBoxes/

    RiemannHypothesisOfEveryCharacter.lean

-   LinkG_at 的精确定义：GlobalTheoremInputs.lean — https://github.com/CocoSgt/riemann-hypothesis-

    lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/

    GlobalTheoremInputs.lean


                                   

---


-   局部轨道、Sig、VV、Sv、ioP、gainP：IsResidueClassZero.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/

    GrowthBounds/IsResidueClassZero.lean

-   坏轨道与小份额权重：WeightVectorSmallSharesSeven.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/

    GlobalSchurBounds/WeightVectorSmallSharesSeven.lean

-   坏轨道计数与二阶矩结构：TopDensityNGeSixteen.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/SharpRestriction/

    GlobalSchurBounds/TopDensityNGeSixteen.lean

-   小份额转成损失界：LossRequirementsOfSmallShares.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/

    GlobalTheory/LossRequirementsOfSmallShares.lean

-   PrimeClassLossHypotheses 的三类估计：PrimeClassLossHypothesesSatisfiable.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Formalism/SizeWindowBrackets/PrimeClassLossHypothesesSatisfiable.lean

-   LossHypD 转成 LossBounds：Losses5OfLossHypD.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/

    SizeWindowBrackets/Losses5OfLossHypD.lean

-   ASK−Ga 与 IO 的最终损失定义：QuotientSlopeBoundsWith.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/

    SizeWindowBrackets/QuotientSlopeBoundsWith.lean

-   LinkG 从家族几何条件导出：AdmissibleFamilyNoKernel.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/

    GroupLattices/AdmissibleFamilyNoKernel.lean

-   RecTAlt 与 SecondLayerFamilyClass：LayerTwoFamilyClass.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/

    LayerTwoFamilyClass.lean

-   Theta/automorphic 数据包 TiedDataSAlt：LinkedFamiliesFixedValues.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/

    LinkedFamiliesFixedValues.lean


                                     

---


-   自对偶格与 Gram 数据：LinkedFamiliesKernelFrame.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/

    AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/

    LinkedFamiliesKernelFrame.lean

-   RecT 选择：TSelF.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/

    TSelF.lean

-   Duty 与 family alignment：ClassOfRecordOfChoice.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/

    ClassOfRecordOfChoice.lean

-   PageFix / PageWin 与指数 401：PageFix.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Formalism/SharpRestriction/PageFix.lean

-   GroupCompatibilityAll 与局部环兼容：StdSubAtOfRing.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/

    GroupLattices/StdSubAtOfRing.lean

-   GroupCompatibility → LinkG：LinkGConcreteNoKer.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/

    GroupLattices/LinkGConcreteNoKer.lean

-   Duty + RecT selection → LinkG：ThirdPlaceSeries/LinkG.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/

    AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LinkG.lean

-   顶层 HypsAlt 记录：Hyps.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/

    Hyps.lean

-   顶层 Green + VWin → ZeroFreeAll：TopPlug.lean — https://github.com/CocoSgt/riemann-hypothesis-

    lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/

    ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/TopPlug.lean

-   公开输入如何构造 HypsAlt 并推出 EveryCharacter：EveryCharacterOfLiteratureOfVWin.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/

    EveryCharacterOfLiteratureOfVWin.lean


                                     

---


-   TLiftK 的数学定义：HalfIndexLattices/TLiftK.lean — https://github.com/CocoSgt/riemann-hypothesis-

    lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/

    Foundations/GaloisRepresentations/ThetaParseval/HalfIndexLattices/TLiftK.lean

-   Theta Lift 工具包构造：TPGHolds.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGHolds.lean

-   工具包推出 Theta Lift：TPGTop.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGTop.lean

-   GeoOne 的有限 étale Lefschetz 实现：WeightOneGeometricRealization.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/

    GeometricFlagBases/WeightOneGeometricRealization.lean

-   GeoOne → SeedFinOdd：MainFin.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/

    ZetaCharacterDivisibility/MainFin.lean

-   Core 构造：ToCoreK.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/IntegralStructures/

    CrystallineDescent/ToCoreK.lean

-   CoreAll / Row0 / Row0b 的组合：Development.lean — https://github.com/CocoSgt/riemann-hypothesis-

    lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/

    Foundations/GaloisRepresentations/IntegralStructures/Development.lean

-   Row0b 的精确性质：WeightsConjBis.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/TypeConditions/

    WeightsConjBis.lean

-   Row0b → VWin：VwinOfRow.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/

    ThresholdArguments/DenseThresholdCases/VwinOfRow.lean


                                      

---


-   VWin 的自守输入组合：TopMainZj.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/

    ThresholdArguments/DenseThresholdCases/TopMainZj.lean

-   Sha 窗口计数链：WindowBoundOfLiteratureLevel.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/

    AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/

    DenseThresholdCases/WindowBoundOfLiteratureLevel.lean

-   LiteratureRankNHypothesis 的四类输入：LitAut.lean — https://github.com/CocoSgt/riemann-

    hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/

    AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/ThresholdArguments/

    DenseThresholdCases/LitAut.lean

-   公开输入 → HypothesesH'：PublishedHypothesesFromPatching.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/

    ThresholdArguments/DenseThresholdCases/PublishedHypothesesFromPatching.lean

-   SP4 image 输入：Sp4In0.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/

    ThresholdArguments/DenseThresholdCases/Sp4In0.lean

-   端点与 ThmS6Core 输入：DnEndsTop.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/AutomorphicVarieties/ModularityArgument/

    ThresholdArguments/DenseThresholdCases/DnEndsTop.lean

-   BaseChangeIsobaricN：DefiniteNHolds.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/BaseChangeIdentities/DefiniteNHolds.lean

-   Rallis 内积恒等式：TPGRallis.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGRallis.lean

-   adelic 分解：TPGDecomp.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGDecomp.lean


                                      

---


-   局部 bump 函数：TPGBumpAny.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGBumpAny.lean

-   全局 theta datum：TPGDatum.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGDatum.lean

-   adelic 尾项控制：TPGTail.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGTail.lean

-   Schur/不可约分量步骤：TPGSchurStep.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGSchurStep.lean

-   非零 theta lift：TPGNonVan.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGNonVan.lean

-   目标表示自守性：TPGLiftAut.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGLiftAut.lean

-   读取权重与局部配对：TPGReadLift.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/TPGReadLift.lean

-   TLiftK 所需工具的完整类型：GalTPDefs.lean —

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b03
    b4/src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/ThetaParseval/

    ThetaKernels/GalTPDefs.lean


                                     

---


十三、目前不能宣称已经重构完成的部分
这里必须把“形式化已通过检查”与“我们已写出完整的人类证明”分开。Slijepčević 的纲要在结尾明确说

明：其作者只读了主要结果的陈述和顶层证明，底层约有 15,000–25,000 条中间声明没有逐条阅读。Section

11 还列出多个没有理解或没有展开的机制。

-       Section 4 的 S3 已追到局部轨道、Sig/Sv、gainP/tauP、PrimeClassLossHypotheses 和 LossBounds；上游

        也已追到 RecTAlt → GroupCompatibilityFamily → LinkG。尚未独立展开的是 RecTAlt 的实际构造、

        GroupCompatibilityAll/LocalDataSystem 的局部数学内容，以及 LinkG 的每个几何输入如何由 Theta Lift 定

        理证明。

-       Section 6：definite-side family structure 中约四十项条件；ON、LOW 等行条件；Green 参数化、closure

        statement 如何具体产生 tied families。

-       Section 7：Theta agreement 的常数如何从常数项恒等式推出；Theorem 7.6 中多项估计的完整证明；关键

        Hecke L 值的精确估值。

-       Section 8：协体积界中的算术比例关系、根判别式依赖、L'/L(1,χ_{−d}) 依赖，以及 Zhang successive

        minima 不等式在塔论证中的具体位置。

-       Section 9：Sha 与 congruence module 的变形论比较；部分 case IV/V 的最终处理；Bernoulli bound 的具体

        算术输入。

-       Section 10：Galois 表示 seed step 的几何机制、两种 Theta Lift 的相减步骤、Frobenius 数据的密度及局部—

        整体相容性的升级。

-       最终 Galois/VWin 链已经追到 TLiftK、GeoOne、CoreAll、Row0b、LiteratureRankNHypothesis 与 Count

        I/II/III/V；但 TLiftK 的 Rallis/Schur/nonvanishing 子证明、GeoOne 的几何实现、以及 theorem 9.1 各

        counting case 尚未逐项改写为可独立阅读的传统证明。

-       TLiftK 的非消失路线已拆为 Rallis、Decomp、BumpAny、Datum、Tail、AbsNe、SchurStep、LiftAut、

        ProjEx、ReadLift；但各模块内部的积分估计、局部模型和自守性证明尚未逐条改写。


十四、后续验收标准与施工顺序
我建议不再追求把全部 Lean 代码按文件顺序翻译，而是按数学依赖和风险排序，逐个消灭黑箱。

    阶段                             交付内容                           验收条件

    A                              解析主线与 Landau 窗口引理              给出完整定义、Mellin 变换、留数和窗口

                                                                  矛盾证明；标清原 Lean 路线与替代简化路

                                                                  线

    B                              命题 4.11 的完整自然证明                解释 S3 的局部增益来源；逐项证明斜率、

                                                                  除子、误差和字符平均；常数指数可复算

    C                              定理 9.1 + 命题 3.5                把 Sha 各 case、坏素数、窗口素数对、

                                                                  host 构造及所有均匀量词写全


---


D                             命题 6.20 + Section 7–8        完整展开 Theta agreement、

                                                           covolume、definite-side family

                                                           structure 与 linking inequality

E                             Section 10 + 最终拼接            把 Galois 表示构造和最终

                                                           EveryCharacter→RH 的所有依赖逐项对

                                                           应到源码


十五、本版结论
本轮已经完成：确认最终定理类型；核对 Lean 最终调用链；校正五个核心依赖；恢复 Riesz 加权 Chebyshev

函数、Mellin 变换和窗口 Landau 的解析骨架；追踪 host、Sha、chain-tied、core-tied 与单 host

Chebyshev 上界之间的源码接口。

进一步完成：将 S3 展开为 Frobenius good/bad 轨道、Sig/Sv、gainP/tauP、OutD/SecondD/IoD 三类估

计，并核对其如何汇总成 LossBounds；把 LinkG 上游追到 TwistSelection、RecTAlt、TiedDataSKAlt、

GroupCompatibilityAll、Duty 和 SecondLayerFamilyClass；把 TLiftK、GeoOne、CoreAll、Row0b、

LiteratureRankNHypothesis、HypothesesH'、Count I/II/III/V 与 VWin 串成一条源码可追溯链。

解析部分已可形成较短的传统证明骨架；Theta Lift 的非零性也已拆成 Rallis、Decomp、BumpAny、

Datum、Tail、AbsNe、SchurStep、LiftAut、ProjEx、ReadLift 等明确步骤。源码链接已固定到 commit

7cbf7a0c32fca1badf05931879a37c3f8a2b03b4。

尚未达到最终验收：Rallis 局部积分的具体计算、SchurStep 的表示论细节、GeoOne 的所有局部结论、

LinkG 的上游几何输入、VWin 计数链各 case 的定量证明，以及 Section 7–8 的 period/covolume 技术细节

尚未逐项改写并核验。

下一轮将优先把 Rallis_k 与 NonVan_k 中的关键积分恒等式改写成传统证明，并核对其与公开 Rallis inner

product formula 的归一化、收敛域和非零条件；随后逐项拆开 VWin 的 Count I/II/III/V。


                              

---


第二编：RH 自然语言证明——解析核心（V0.8 新增）
本编直接写数学推导，区别于第一编的源码地图。已独立展开的等式逐步写出；引用外部已证定理时标明出处；当

前未完成证明的算术输入一律以【待展开输入】标识。特别注意：本编不把条件证明冒充为完整 RH 证明。


A. 500 页硬上限与章节预算
最终提交时严格少于 500 页，内部排版上限设为 480 页，预留至多 19 页用于最后校订。篇幅优先给出全部新的数

学思想及其必需的定量引理；普通标准定理可给出精确版本并引用可靠出处，不能因为页数限制省略关键假设。主

稿以 Riemann ζ 的 RH 为目标，Dirichlet GRH 的推广只收录与主稿不重复的部分。

 模块                              页数上限                                  写作原则

 零点归约、Mellin、窗口 Landau           35                                    直接证明，摒弃 Lean 类型/实例细节

 辅助特征、零点密度、B/C                   45                                    文献定理精确陈述，重要界独立推导

 辅助 CM 域、host 与字符正交              45                                    写出大小条件、所有量词与傅里叶系

                                                                       数

 Theta 核、非消失、局部整除性               85                                    保留新技术和所有必要的局部引理

 格、斜率、S3、损失与局部—整体                65                                    对 (M) 每个误差项进行数字核对

 周期、协体积、迹、秩、一般位置                 75                                    定量估计和归一化不能略

 Galois 表示、Sha、数值窗口界             95                                    分支按 Case 列证明，统一常数

 最终拼接、来源审计与索引                    35                                    完整量词核查、编号与 Lean 回指

 合计                              480                                   目标 < 500；超过预算时优化重复，

                                                                       不隐去数学义务


B. 核心加权素数和与完全准确的中心化
记 Λ(n) 为 von Mangoldt 函数，γ 为 Euler 常数，t₊:=max(t,0)。对 x≥1 定义

                            G(x) = ∑ₙ Λ(n)(x/n − 1)₊ − x log x + (1+γ)x.

令 χ 为非主 primitive Dirichlet 特征，置 cχ=L′(1,χ)/L(1,χ)，定义

                               Gχ(x) = ∑ₙ Λ(n)χ(n)(x/n − 1)₊ + cχ x.

再取奇素数 q,d，令 χq、χd 为对应二次特征，η=χqχd。定义非负选择权重对应的和

                          S(q,d;x)=∑ₙ Λ(n)(1+χq(n))(1−χd(n))(x/n−1)₊.

把中心化的四项恰好组合成

                         R(q,d;x) = S(q,d;x) − x log x + (1+γ+cq−cd−cη)x.


---


**引理 B.1（逐项恒等式）。** 对所有 x≥1，

                             R(q,d;x)=G(x)+Gχq(x)−Gχd(x)−Gη(x).

证明：将 (1+χq)(1−χd)=1+χq−χd−χqχd 代入 S，得到四个 Riesz 和。第一个的中心化常数为 −xlogx+(1+γ)x；后三

个分别加 cq x、减 cd x、减 cη x。四项相加正好产生定义中的 R，故等式逐项成立。注意此处为精确恒等式，不涉

及 x→∞ 的误差项。∎

因此只要在同一窗口同时满足 R(q,d;x)≤x^(1/2+α) 与 |Gχ(x)|≤x^(1/2+β)（χ∈{χq,χd,η}），就直接有

                                G(x) ≤ x^(1/2+α)+3x^(1/2+β).


C. 主不等式 (M)：从 lattice 损失恢复四种误差
本节把尚未展开的深层算术输入缩成唯一的定量黑箱，而不是含糊说“theta lift 给出 RH”。令 H 为 n 元的列群，T

为 h 元的标签集，T₂ 为 h₂ 元的 distinguished 标签集，δ:=h₂/n，m 为 lift 链长，k 为 rank 参数，b 为局部

weight。令 a_t 是第 t 个标签的微分阶数。P(u,t,j) 是一格的惯性素数和，M(u,t,j) 是相应主项。

【待展开输入 M】对每个足够小 ε 和每个被选定的区间 [Y,Y^(3/2)]，存在同一对辅助素数 q,d；对每个 x 在该区间

内，构造上述数据且满足

                  (1/n)∑_{u∈H}∑_{t∈T}∑_{j=1}^m (P(u,t,j)−M(u,t,j)) ≤ E,

                      E / B ≤ x^(Cε) [x/m + xm/k + m + k/n²], B=hmbδ/2,

其中 C 为统一的常数，且 δ≥x^(−ε)，h/n≥(1/2)x^(−ε/8)。算术研究的主体目标正是把 M 从 Lean 深层定理展开为

无黑箱的自然语言证明。


C.1 误差归一化逐项核算
源码的一个平行形式给出上界（a_E≤2xb 且 h₂=nδ）：

               E ≤ x^(Cε){ h a_E(1+m²/k) + m[2nmb x^ε + h₂kb x^ε/(n²x^(−ε))] }.

令 B=hmbδ/2。将右侧三项分别除以 B，精确得到以下上界，不使用任何局部几何理论。

                                    I₁ ≤ (4/δ)(x/m+xm/k),

                                     I₂ = (4n/(hδ)) m x^ε,

                                    I₃ = 2(n/h)(k/n²)x^(2ε).

证明：第一项等于 2a_E(1+m²/k)/(mbδ)，利用 a_E≤2xb 得结论。第二项约去 hmb/2 后为 4nm x^ε/(hδ)。第三项

利用 h₂=nδ，将 2h₂kx^(2ε)/(hδn²) 化为 2kx^(2ε)/(hn)，即所示。∎

再由 1/δ≤x^ε、n/h≤2x^(ε/8)，得


---


                                     I₁ ≤ 4x^ε(x/m+xm/k),

                            I₂ ≤ 8x^(17ε/8)m, I₃ ≤ 4x^(17ε/8) k/n².

这说明所有归一化误差都可由 [x/m+xm/k+m+k/n²] 乘一个 x^(C′ε) 吸收。此处尤其能看出 sqrt(x) 指数的来源：

x/m 与 m 互相牵制，m 取约 sqrt(x) 时才可达到平方根级。


C.2 四项尺度的代数核验
取 m=x^(1/2+O(ε))，k=x^(9/2+O(ε))，n=x^(2+O(ε))。逐项指数为

                           x/m = x^(1/2+O(ε));    xm/k = x^(−3+O(ε));

                            m = x^(1/2+O(ε));     k/n² = x^(1/2+O(ε)).

因此，若 M 及其到 R(q,d;x) 的字符平均和变尺度转换均成立，则在整个 [Y,Y^(3/2)] 上有 R(q,d;x)≤Cε

x^(1/2+C″ε)。这就是 RH 归约所需的 Estimate A。


D. 辅助素数估计 B 与大尺度估计 C：统一量词
对固定 ε∈(0,1/52) 和所有足够大的 Y，要挑一对 q,d，而不是针对窗口内每个 x 分别重新挑选。准确要求为：q≡3

(mod 8)，d≡7 (mod 16)，q|d+1，且所有奇素数 p≤Y^(ε/5) 均整除 d+1。并且

                                 (1/2)Y^(ε/5)< log q ≤ Y^(ε/5),

                          (1/2)Y^(ε/5)(log Y)² < log d ≤ Y^(ε/5)(log Y)².

B 的 zeta 特化形式要求对 χq、χd、χqχd，同时对所有 x∈[Y,Y^(3/2)] 成立 |Gχ(x)|≤x^(1/2+ε/2)。证明不是来自

GRH 这种循环假设，而是在所选 q,d 的平均上结合零点密度、排除 Siegel 异常零和进阶算术级数素数分布得出。现

有 Rubinstein 工作稿将其还原为四类可核对的传统数论定理；Lean 顶层对应 QH.pairEx。

C 的精确大尺度范围从 y≥(1/3)exp(x^(ε/3)) 开始，目标是对导体 N|Qqd（Q 的奇数部分有界）的所有 primitive χ

满足

                                   |Gχ(y)| ≤ y exp(−c x^(ε/8)).

一个短而严密的推导路径是：在导体增长 log N≲x^(ε/5)(log x)² 下，对 real characters 排除靠近 1 的异常零，应用

标准零点无关区域和局部零点计数；取显式公式截断高度 T=exp(sqrt(log y)) 得

                |Ψχ(y)−δχ y| ≤ Cy(log y+log N)² exp[−c log y/(log N+sqrt(log y))].

其中 δχ=1 对平凡特征，其余为 0。对 u≥y，积分变换 Gχ(y)=−y∫_y^∞ (Ψχ(u)−δχ u)/u² du，再用 log

y≥(1/2)x^(ε/3) 和 log N≲x^(ε/5)(log x)²，指数可吸收为 exp(−c′x^(ε/8))。


                                 

---


严格的关键点是 1/3−1/5=2/15>1/8，因此导体的增长速度仍不足以破坏大尺度上的指数节省。这个证明逻辑无需把

整个零点密度论证再写一次：只要在正文精确列出三个标准定理、标明适用范围和异常零排除即可。


E. 窗口版 Landau：为什么零点不能躲过好窗口
窗口估计比全体 x 的估计弱得多；仅仅有无限多个局部好点不够。关键在于每次好区间必须完整覆盖 [Y,Y^(3/2)]，

并允许 Y 任意趋于无穷。

设 F(s)=∫₁^∞G(x)x^(−s−1)dx（初始 Re(s)>1）。由逐项积分与 −ζ′/ζ 的 Dirichlet 级数，可得

                         F(s)=−ζ′(s)/[s(s−1)ζ(s)]−1/(s−1)²+(1+γ)/(s−1).

ζ(s) 在 s=1 的 Laurent 展开说明右边在 1 的两阶极点相互抵消；在临界带的 ζ 零点 ρ 处，F 有一阶极点，留数为

ν/[ρ(1−ρ)]，ν 为零点重数。

在 Re(s)>2 处微分 j 次，并令 u=log x、g(u)=G(e^u)，得

                                 A_j(σ+it)= (−1)^jF^(j)(σ+it)/j!

                               = ∫₀^∞ g(u)e^(−itu)u^j e^(−σu) du/j!.

取好窗口 U=logY，j≈(5/4)(σ−2)U。核 u^j exp[−(σ−2)u] 的最大值所在位置是 u≈(5/4)U，处在 [U,3U/2] 中部。由

归一化 Gamma 核的大偏差估计，区间外的核质量相对于总质量指数下降。

令 K_j(u)=u^j e^(−σu)/j!≥0，使用 |z|+Re(z)≤2max(Re(z),0) 的实值版本，得

                      |A_j(σ+it)| + A_j(σ) ≤ 2 ∫₀^∞ max(g(u),0)K_j(u)du.

窗口内 G(e^u)≤e^(θu)，窗口外由普通 Chebyshev 界控制 G(e^u)≪e^(2u)，所以选足够大的固定 σ 后，可得沿上

述 j→∞ 序列

                               |A_j(σ+it)| + A_j(σ) ≪ (σ−θ)^(−j).

如果 Re(ρ)>θ 存在 ζ 零点，则 F 有距离某一中心 σ+it 为 d<σ−θ 的极点。通过选 t 使此点成为唯一最近极点，在

d<r<σ−θ 的圆盘中减去其主部，再用 Cauchy 估计，可得到 |A_j(σ+it)|≥c d^(−j)−O(r^(−j))。另一方面 A_j(σ) 的增长

至多是 O(r^(−j))。由于 d<r<σ−θ，这与先前的统一上界矛盾。

以上给出了证明的实际分析结构；最后一步“最近极点唯一化”与 Gamma 核尾项的定量常数需在终稿写成独立引

理。本轮源码参考：landauWindow.lean（原证明）；Rubinstein 工作稿 II.1（可读重构）。


F. 条件定理：M + B + C 严格推出 RH
**定理 F.1。** 假设存在对所有充分小 ε 统一成立的主不等式 M，且其产生的 R(q,d;x) 上界、同一对辅助素数对应的

B 与 C 可在整段 [Y,Y^(3/2)] 对任意大的 Y 同时成立。再假设上节的窗口 Landau 引理。则 Riemann 假设成立。


                                

---


证明：任给 θ∈(1/2,1)。先选择足够小的 ε>0，使得 (1/2)+C₁ε<θ，其中 C₁ 是由 M 的误差吸收以及 B 的 exponent

得到、与 ε、Y、q、d 无关的常数。对每个足够大的 Y，选 q,d 及每个 x 的构造。M+C 给出

R(q,d;x)≤Cεx^(1/2+C₁ε)；B 给出三个 twist 的绝对值上界。由引理 B.1，在整个窗口上 G(x)≤C′εx^(1/2+C₁ε)。增

大 Y 后，固定常数 C′ε 可被 x 的剩余正指数吸收，故 G(x)≤x^θ。Landau 窗口引理推出 ζ(s) 在 Re(s)>θ 无零点。

θ↓1/2，故 ζ 的临界带内无零点位于 Re(s)>1/2；由 ζ 的函数方程，亦无零点位于 Re(s)<1/2。因此全部非平凡零点

均在临界线上。∎

此定理的证明在逻辑上闭合，唯一尚未被本稿独立证明的是标记为【待展开输入 M】的深层算术不等式，以及 B/C

和窗口 Landau 所引用的传统数论引理的最终逐条核验。把 M 写成明确、量词统一、常数可追踪的形式，是本稿与

普通介绍性文章的区别。


G. 一项不能忽略的来源审计：η_j(w) 的身份
Rubinstein 的 164 页工作稿在最后一节特别指出一项未确认的自然语言识别：某些局部缺陷 η_j(w) 是否确实等于前

文以格的局部商长度定义的对象。在 Lean 中名为 TieEta、etaN_eq_etaJ 的声明并未显示为最终定理的实际依赖，

因此自然语言作者不能直接把这些名称当作已在最终链中用到的证明。

这是自然语言重构的“对象同一性”问题，不等于 Lean 证明有逻辑漏洞：形式化证明可能使用另一套记录字段或不

同的归约路径。终稿必须直接追踪最终使用的 LinkN/linkN_of_twGood_galoisPreconditions、相关的 etaJ 与

etaW/locLen，并给出同一性定理的明确公式及源代码位置，或者改写论证使其完全避免该未经确认的同一性。

这一点被列为最高优先级的验收阻断项。若不能闭合，就不能把现有 164 页工作稿简单扩写成“完整自然语言证

明”，即使总页数低于 500。


H. 本轮审计状态与下一条推导链
项目                         现有状态                        进入终稿的条件

S=G+三个扭曲项                  完全展开的代数恒等式                  固定归一化与特殊素数的约定

M 中 4 项误差的归一化              逐项推导完成                      把实际最终 Lean 依赖与平行式区别

                                                       开

m,k,n 幂次与 √x               代数核验完成                      所有 O(ε) 常数一致

Estimate B                 依据现有自然语言论文与源码接口             单对 q,d 在整个窗口成立，核查零点

                                                       密度/例外零

Estimate C                 从显式公式与尾积分恢复主要证明             精确展开常数和异常零分支

Landau 窗口准则                变换、Gamma 核与极点矛盾机制已          补齐尾界与最近极点选择的定量引理

                           恢复

主算术不等式 M                   仅获得输入/输出与部分格侧来源             完整证明 theta kernel、局部整除、

                                                       S3、格/协体积、trace 和 Sha


                           

---


    局部缺陷 η_j(w) 同一性                已确认是外部重构的未解决接口                   在最终 Lean 依赖链中给出同一性公

                                                                    式


I. 本轮新用的一手资料与定位
-     Michael Rubinstein 主持的 164 页自然语言工作稿（2026-11-

      21）：https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf

-     Rubinstein 验证及论文导航：https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/

-     Rubinstein Part II, §1：窗口 Landau；§3–5：M、辅助二次特征与误差转换；Part III, §III.1：Estimate B；

      §III.2：Estimate C；§III.9：Sha 及 η_j(w) 审计。

-     原 Lean 项目快

      照：https://github.com/CocoSgt/riemann-hypothesis-lean/tree/7cbf7a0c32fca1badf05931879a37c3f8a2

      b03b4

-     分析收尾核心：Formalism/SharpRestriction/RamificationFrobenius/TotientGaloisClasses/TopWin.lean；

      Development/AutomorphicArithmetic/PrimitiveCosets/CoreGm.lean；Development/

      AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean

-     外部三项分析简化稿：https://hexagonmath.org/pdf/2611.00828v1

V0.8 评定：明确达到了「500 页硬上限已落实、解析条件证明可逐项检查、M 的定量规模和来源问题得到核验」；

尚未达到「无需引用未展开的原创算术核心即可独立验收」的最终标准。


                                    

---


第三编：可独立检查的引理重构（V0.9 新增）
本编不是路线图，而是把原始 Lean 的三个实际证明节点改写成自足的数学引理。假设被明确列出，证明中每
一步代数、级数比较和常数吸收都可直接验算。所涉及的 Sha 估计本身仍来自深层算术几何；本编完整证明
的是“该估计如何传递到除子误差”的中间桥梁，不能将二者混同。


J. 统一符号与 Sha 长度上界
设 E 为数域，t 为正整数，ℓ 遍历素数。对每个 1≤e<t，记 h_{ℓ,e} 为某一与 E 关联的 ℓ-primary Tate–
Shafarevich 型 Galois 上同调群的长度（即 Lean 中的 shaLen）。本节只需其非负整数性与下述上界，不需
要假设这些群都与理想类群相同。

                        V(E;t,B): h_{ℓ,e}<∞，且对任意有限素数集 S，

                          ∑_{ℓ∈S} (log ℓ) ∑_{1≤e<t} h_{ℓ,e} ≤ B。

这个陈述包含两个独立要求：所有有关长度有限，以及整个加权总量的有限子和一致有界。其逻辑量词是先固
定 E、t、B，再对任意有限 S 验证，而不是只对某一个事先选定的素数集有效。

引理 J.1：有限子和上界自动给出整个总和收敛
假设 V(E;t,B)。定义对自然数 n 的非负序列 aₙ：n 是素数时，aₙ=(log n)∑_{1≤e<t}h_{n,e}，其余时候
aₙ=0。则 ∑_{n≥0} aₙ 收敛，且总和不超过 B。
证明。首先，由 h_{ℓ,e}≥0 且 log ℓ≥0，知所有 aₙ≥0。任取有限自然数集 F，删去 F 中的非素数不会改变
∑_{n∈F}aₙ；剩下的素数集合 S 有限。于是

                   0 ≤ ∑_{n∈F}aₙ = ∑_{ℓ∈S}(log ℓ)∑_{1≤e<t}h_{ℓ,e} ≤ B。

特别地，部分和 s_N=∑_{n≤N}aₙ 单调不减且统一有上界 B，因此收敛到某个 s≤B。这正是非负级数的单调收
敛判别。结合 V(E;t,B) 的有限长度要求，结论成立。□
此处的证明对应 Lean 中 vvRecord 的核心逻辑：先逐素数匹配形式化 shaLen 与记录中的 shaLen；再将自
然数求和化为素数求和；最后调用“非负且有限子和统一有界 ⇒ Summable”，并将总和界传给后续步骤。

引理 J.2：V(E;t,B) 的单调性
若 V(E;t,B) 成立、t′≤t 且 B≤B′，则 V(E;t′,B′) 成立。
证明。1≤e<t′ 的每个 e 也满足 1≤e<t，因此每一长度仍然有限。另一方面，对于任意有限素数集 S，由每个
h_{ℓ,e}≥0，

                             ∑_{ℓ∈S}(log ℓ)∑_{1≤e<t′} h_{ℓ,e}

                       ≤ ∑_{ℓ∈S}(log ℓ)∑_{1≤e<t} h_{ℓ,e} ≤ B ≤ B′。

此即结论。□
这一引理仅使用区间包含和非负性；它允许把较强、较长的 Sha 窗口结论缩短成某个具体格构造所需的有限
层级结论。


K. LinkN 如何把 Sha 上界转成格的局部除子误差
以下将从 Lean 中抽取的常数统一记为实数，而将格的局部缺陷记为 η_j。固定 x>1、ε>0、b≥1、f,m≥1、
N_c≥0，以及 D₀≥0。设 y=x^ε，则 y≥1。定义

                          B₀ = f m b y，   L = y，   T = (log x)²。


---


记 η_j≥0 为诸局部缺陷的加权总和。LinkN 的准确形状是：在相关非负级数可求和时，

                             η_j ≤ D_j { C [f m b L² + T N_c] + V }，

其中 V=∑_ℓ a_ℓ 为 J.1 中的 Sha 长度加权总和，C 是不预先假设非负的实常数，D_j 是当前格层的非负整数度
数。
目标是将其改写为 DIVinN 使用的统一形式

                                 η_j ≤ D₀ (|C|+1) y (B₀+N_c)。

引理 K.1：完全明确的常数吸收
假设 (i) LinkN 上式；(ii) D_j=D₀≥0；(iii) V≤√b；(iv) T≤y；(v) x>1、ε>0、b≥1、f,m≥1、N_c≥0。那么
DIVinN 的上述上界成立。
证明。由 B₀=fmby 和 L=y，立即有

                           f m b L² = f m b y² = y B₀。               (1)

由于 T≤y 且 N_c≥0，

                             T N_c ≤ y N_c。                        (2)

由于 b≥1，√b≤b。又 f,m,y≥1，所以 b≤fmby=B₀，故

                          0≤V≤√b≤b≤B₀≤y(B₀+N_c)。                         (3)

将 (1)、(2) 代入 LinkN。记 U=yB₀+TN_c，则 U≥0 且 U≤y(B₀+N_c)。对于任意 C∈ℝ，有 C·U≤|C|·U≤|C|
y(B₀+N_c)。结合 (3)，

                           C·U+V ≤ (|C|+1)y(B₀+N_c)。                 (4)

最后乘以 D₀≥0，保持不等号方向；再利用 D_j=D₀，得到要求的统一上界。□
这个结果与 Lean divinN_at 的结论一致，特别保留了容易遗漏的两个细节：一是 C 可以为负，所以统一常数
要取 |C|+1；二是 D_j 的替换需要单独的 SmallLevelRankEq 输入。

引理 K.2：log²x 与 x^ε 的吸收不需要额外数论
给定任意 ε>0，存在 X_ε，使对所有 x≥X_ε，(log x)²≤x^ε。
证明。令 u=log x，则要求 u²≤e^{εu}。因 e^{εu}/u²→∞（u→∞），存在 U_ε，使 u≥U_ε 时成立。取
X_ε=e^{U_ε} 即得。更定量地，写 e^{εu}≥(εu)^3/6；当 u≥6/ε³ 且 u>0，就有 e^{εu}≥u²。故可直接取
X_ε=exp(max{1,6/ε³})。□
这一步可用常微积分直接完成；Lean 的 log_sq_le_rpow 使用 log x = o(x^{ε/2}) 的标准极限再平方，实质相
同。

定理 K.3：HypV + LinkN + SmallLevelRankEq ⇒ DIVinN
设 F_ε 为一族随尺度 x 变化的格数据。假设 ε>0，并且存在充分大的 X₁、X₂、X₃，令所有 x≥max{X₁,X₂,X₃}
和任意家族成员 i 都满足如下条件：
-   HypV：对应数域 E 的 Sha 长度界 V(E;t,√b)，即 J.1 的输入。
-   LinkN：对每个允许的 lift 层 j 都有 K.1 所用的 η_j 不等式，常数 C 在 x、i、j 之间统一。
-   SmallLevelRankEq：每个 j 都满足 D_j=D₀。
-   标准尺度条件：b≥1、f,m≥1、N_c≥0 且 B₀=fmby；并取 x 再大一些使 (log x)²≤x^ε。

则存在统一常数 C_DIV=|C|+1 与阈值 X₀，使对所有 x≥X₀、所有 i 及所有允许的 j，

                         η_j(x,i) ≤ D₀(x,i) C_DIV x^ε [B₀(x,i)+N_c(x,i)]。


---


证明。固定 x、i、j。由 HypV 及 J.1，相关非负级数可求和，且 V≤√b，故 LinkN 的可求和前提成立。由指
数吸收引理，在共同阈值以外有 (log x)²≤x^ε。再由 SmallLevelRankEq 替换 D_j。此时满足 K.1 全部假
设，故取得结论。所选常数 C_DIV 不依赖 x、i、j，取最大阈值即可使全部结论同时有效。□
这完成了一个非平凡的“数论输入→格的统一误差”自然语言接口。它没有证明窗口 Sha 界本身，也没有擅自把
η_j 定义为某个特定格的商长度；后一对象同一性在更深一层仍需单独核查。


L. PageN 与 401 的参数如何严格衔接

引理 L.1：选择 page exponent 的显式构造
对 ε>0、x≥1，令 A=x^{2+8ε}≥1。取整数 e(x)=⌈log₂ A⌉。则

                             x^{2+8ε} ≤ 2^{e(x)} ≤ 2x^{2+8ε}。

证明。由 e−1<log₂A≤e 得 2^{e−1}<A≤2^e，故 A≤2^e<2A；当 e=0 时直接是 A=1。特别地，较弱的 ≤2A
成立。这个构造比“存在某个 e”更明确，并与 Lean 中 exists_pageN 的选择引理等价。□

引理 L.2：为什么出现 401
PageFix 的固定常量满足 e_P=12、c_TO=28e_P+41、C_t=c_TO+24。因此 C_t=28·12+41+24=401。随后
VWinAt(ψ,401) 中 t=floor(x^{401})。这个数字不是 Riemann 零点的数学常数，而是构造中为了同时吸收若
干 rank 和 cohomology 阈值所选的技术参数。
注意：由 401 的来源推算出它的整数值，并不意味着已经证明 401 足够大。该充分性的证明依赖 PageFix、
PageWin、各层 rank 与 Sha 条件的联合兼容性，属于尚须展开的几何/算术部分。


M. Riesz–Chebyshev 函数的 Mellin 变换与尾积分（完整证明）
本节从定义重新证明解析部分的两个基本恒等式，同时纠正把中心化常数或 χ 主非主情况混在一起可能造成的
符号错误。

引理 M.1：Riesz 核的 Mellin 恒等式
若 n≥1，且 Re s>1，则

                       ∫₁^∞ (x/n−1)₊ x^{−s−1} dx = n^{−s}/[s(s−1)]。

证明。核在 x<n 时为零，因此积分从 n 开始。对于 Re s>1，

                                 ∫_n^∞ (x/n−1)x^{−s−1}dx

                         = (1/n) ∫_n^∞x^{−s}dx −∫_n^∞x^{−s−1}dx

                       = n^{−s}/(s−1) −n^{−s}/s = n^{−s}/[s(s−1)]。□

引理 M.2：ζ 的中心化为什么恰好是 1+γ
设 Ψ(x)=∑_{n≤x}Λ(n)，E(x)=Ψ(x)−x。记

                         G₀(x)=∑_{n≤x}Λ(n)(x/n−1)−xlogx+(1+γ)x。

由 Stieltjes 分部积分，对 x≥1 有

                         ∑_{n≤x}Λ(n)(x/n−1)=x∫₁^x Ψ(t)t^{−2}dt。

因此 G₀(x)=x∫₁^x E(t)t^{−2}dt+(1+γ)x。


---


接下来证明 ∫₁^∞ E(t)t^{−2}dt=−(1+γ)。对实 s>1，利用 Euler 乘积和积分表示，

                           ∫₁^∞ Ψ(t)t^{−s−1}dt=−ζ′(s)/[sζ(s)]，

                               ∫₁^∞ t·t^{−s−1}dt=1/(s−1)。

于是 ∫₁^∞ E(t)t^{−s−1}dt=−ζ′(s)/[sζ(s)]−1/(s−1)。若使用素数定理的有效余项保证 s↓1 时可按支配收敛取
极限，再由 ζ(1+h)=h^{−1}+γ+O(h) 得

                         −ζ′(1+h)/[(1+h)ζ(1+h)] = 1/h−(1+γ)+O(h)。

相减后极限就是 −(1+γ)。代回 G₀ 的定义，即得精确的尾积分公式

                           G₀(x)=−x∫_x^∞ [Ψ(t)−t]t^{−2}dt。□

引理 M.3：非主 primitive Dirichlet 特征的尾积分
设 χ 为非主 primitive Dirichlet 特征，Ψχ(x)=∑_{n≤x}Λ(n)χ(n)，且 ℓ χ=L′(1,χ)/L(1,χ)。定义

                           Gχ(x)=∑_{n≤x}Λ(n)χ(n)(x/n−1)+xℓχ。

由相同的分部积分与 −L′/L 在 s=1 处的极限，并利用 Dirichlet 素数定理的有效误差保证尾积分收敛，

                         ∫₁^∞ Ψχ(t)t^{−2}dt=−L′(1,χ)/L(1,χ)=−ℓχ。

因此

                            Gχ(x)=−x∫_x^∞ Ψχ(t)t^{−2}dt。□

重要：主特征的中心化不是把 ℓ χ 简单代成某个有限数；它需要 ζ 的极点 Laurent 展开，因而要单独写成
M.2。

推论 M.4：ζ 误差与三个二次扭曲的精确组合
若 q,d 为不同的奇素数，χq、χd 为相应非主二次特征，η=χqχd 为非主乘积特征，则

                           R(q,d;x)=G₀(x)+Gχq(x)−Gχd(x)−Gη(x)

                     =−x∫_x^∞ {E(t)+Ψχq(t)−Ψχd(t)−Ψη(t)}t^{−2}dt。

这不是渐近式，而是函数恒等式。其首行可以通过 (1+χq)(1−χd)=1+χq−χd−η 直接检验；第二行来自 M.2
与 M.3。它清楚说明估计 B/C 的作用：控制三个辅助扭曲的尾积分，并将 M 的一个单边上界传给 ζ 的单边误
差。□

引理 M.5：从有效素数定理余项得到 Gχ 的指数节省
令 Eχ(t) 代表上述主特征的 Ψ(t)−t 或非主特征的 Ψχ(t)。假设某个固定 c>0、A>0 对所有 t≥x≥e 有

                              |Eχ(t)| ≤ A t exp(−c√(log t))。

则存在仅依赖 A、c 的常数 A′>0，使

                         |Gχ(x)| ≤ A′x(1+√log x) exp(−c√log x)。

证明。由 M.2 或 M.3，

                          |Gχ(x)| ≤ Ax∫_x^∞ exp(−c√log t)dt/t。

令 u=√log t，则 dt/t=2u du，因此积分恰为

                                2∫_{√log x}^∞u e^{−cu}du

                             =2e^{−c√log x}(√log x/c+1/c²)。


---


代回即得。特别地，对任意 0<c′<c，充分大的 x 上 (1+√log x)exp(−c√log x)≤Cexp(−c′√log x)。□
这条引理把有效素数定理与 Riesz 平滑和之间的转换独立证明了出来。它不能替代整个 Estimate B/C（其模
数 q,d 随 Y 快速增长，常数必须对模数统一），但能避免在证明中错误地使用固定模数版本的 PNT。


N. 错误敏感性审计：哪些地方不能靠熟悉的标准引理略过
对象/接口                        已闭合内容                          仍需外部证明
V(E;t,B) → 可求和               J.1–J.2 完全证明                   VWin 本身
Sha 总量 → η_j 上界              K.1–K.3 完全证明                   LinkN、SmallLevelRankEq 的来源
PageN 和常数 401                L.1 构造、L.2 算术核算                PageFix/PageWin 联合可行性
Mellin 与尾积分                  M.1–M.5 完全证明（所用 PNT 有效         辅助模数一致的 B/C
                             余项作为标准输入）
单 host (M)                   仅有 CoreAtH→Chebyshev 的 Lean    theta 积分、局部整性、损失 S3、
                             证明接口                           迹、协体积、上同调
η_j 和格商长度                    记号已区分，避免冒充已识别                  最终 Lean 依赖链中 etaJ/etaW 的精
                                                            确同一性


对“证明完全完成”的验收特别关注最后一行。Rubinstein 的工作稿明说，η_j(w) 与以商格长度定义的局部缺
陷的同一性尚未确证；本编刻意只使用记录中 η_j 的定义，不擅自用未核对的格长度替换。这保证 K 部分独立
有效，也清楚地展示下一步必须核验的数学对象。
参考并逐句核对过的 Lean 文件：src/Formalism/SharpRestriction/GlobalTheoremInputs.lean
（vvTerm、etaSum、LinkN_at、DIVinN_at），src/Development/AutomorphicArithmetic/
CharacterBoxes/DivinNOfHypV.lean（vvRecord、log_sq_le_rpow、divinN_at、divinN_of_hypV），
src/Development/AutomorphicArithmetic/CharacterBoxes/ExistsPageN.lean（VVle、VWinAt、
exists_pageN）。快照 commit：7cbf7a0c32fca1badf05931879a37c3f8a2b03b4。
V0.9 结论：新增的 J–M 部分都可独立按定义逐项检验；整套 RH 的完整人类证明仍未完成，特别是 M 的深层
算术几何输入。总篇幅坚持 <500 页硬上限，下一步应优先使 LinkN 的 η_j 定义与实际 theta-lattice 的 local
index 严格对接。


                              

---


第四编：局部 Fourier 正交与窗口 Gamma 核（V1.0 新增）
这一编围绕最后的解析零点排除继续深入。它给出两个在 Lean 中分散于众多技术引理的自足数学论证：有限
阿贝尔群的平移平均如何留下目标特征族，以及窗口加权上界如何通过 Gamma 型导数核控制 Mellin 变换的
高阶导数。两者均可独立验算，不依赖未公开的 Theta Lift 构造。


O. 有限阿贝尔群字符正交——为何只剩指定的特征

引理 O.1：子群上的字符正交
设 A 为有限阿贝尔群，H≤A 为子群，χ:A→C× 为复乘法特征。则

                  ∑_{h∈H}χ(h) = |H|，当 χ 在 H 上恒等于 1；否则等于 0。

证明。当 χ|H=1，显然总和为 |H|。否则选 h₀∈H，χ(h₀)≠1，令 S=∑_{h∈H}χ(h)。由 H 在加法 h↦h+h₀ 下
是置换，

                                S=∑_{h∈H}χ(h+h₀)=χ(h₀)S。

因 χ(h₀)−1≠0，故 S=0。□

引理 O.2：平移平均是投影算子
定义 (P_H f)(a)=|H|⁻¹∑_{h∈H}f(a+h)。若 f 在有限群 A 上作 Fourier 展开 f(a)=∑_{χ∈Â} f̂(χ)χ(a)，则

                            (P_H f)(a)=∑_{χ∈Â, χ|H=1} f̂(χ)χ(a)。

证明。把展开代入平均并交换两个有限求和，得到 f̂(χ)χ(a)·|H|⁻¹∑_{h∈H}χ(h)。最后一项由 O.1 恰是 χ|H=1
的指示函数。□
如果 A/H 为阶 o 的循环群，那么满足 χ|H=1 的特征恰有 o 个，与商群 A/H 的全部特征一一对应；若取商群
生成元 ā，并记其上的基本特征为 ψ，则这些特征正是 1,ψ,ψ²,…,ψ^{o−1}。将非本原幂次替换为其诱导的
primitive 特征，就得到核心 Dirichlet L 函数族。

引理 O.3：正的二次特征选择器
对不同的奇素数 q,d，令 χ_q、χ_d 为模 q、d 的实二次 Dirichlet 特征。对于任意正整数 n，

                             w(n)=(1+χ_q(n))(1−χ_d(n)) ≥ 0。

证明。每个实二次特征的取值属于 {−1,0,1}，因此两个因子都非负。若素数 p 不整除 qd，则
χ_q(p),χ_d(p)∈{±1}；此时 w(p)=4 当且仅当 χ_q(p)=1、χ_d(p)=−1，其余情形 w(p)=0。□
由此可见，平移平均做的是频率投影，二次特征乘积做的是非负的素数类别筛选。二者的组合并不神秘：先用
arithmetic/geometry 约束非负筛选权重下的惯性素数，再用有限 Fourier 正交抽出 ζ 和若干次级 L 函数。

引理 O.4：不同特征共享零点时正权重不会抵消极点
设 P(s)=∏_{j=1}^r L_j(s)^{α_j}，其中 α_j>0 可以是实数，仅在零点附近考虑形式对数导数 ∑α_j L′_j/L_j。若
ρ 是某些 L_j 的零点，重数为 m_j≥0，则

                 Res_{s=ρ} ∑_{j=1}^r α_j L′_j(s)/L_j(s)=∑_{j=1}^r α_j m_j>0。

证明。逐个展开 L_j(s)=(s−ρ)^{m_j}h_j(s)，其中 h_j(ρ)≠0。于是 L′_j/L_j=m_j/(s−ρ)+h′_j/h_j，后项全纯。乘
以 α_j 求和即得。注意这只证明极点重数的正性，不能单独代替窗口 Landau 的极点排除论证。□


                               

---


P. Gamma 核的定量集中：窗口版 Landau 的解析发动机

引理 P.1：归一化 Gamma 密度和指数矩
设 α>0，k 为非负整数，定义

                  dμ_{k,α}(u) = [α^{k+1}/k!] u^k e^{−αu}du，u≥0。

则 μ_{k,α} 是概率测度，且对 −α<λ<α，

                       ∫₀^∞ e^{λu}dμ_{k,α}(u)=(α/(α−λ))^{k+1}。

证明。根据 Gamma 积分 ∫₀^∞u^k e^{−βu}du=k!/β^{k+1}（β>0），取 β=α 和 β=α−λ 依次得到总质量 1
与指数矩公式。□

引理 P.2：左右两侧的 Chernoff 界
对于任意 a∈(0,1)、v>0，有

                      μ_{k,α}([v,∞)) ≤ e^{−aαv}(1−a)^{−(k+1)}；

                       μ_{k,α}([0,v]) ≤ e^{ aαv}(1+a)^{−(k+1)}。

证明。第一个不等式在事件 {u≥v} 上使用 e^{aαu}≥e^{aαv}，然后由 P.1 积分；第二个在 {u≤v} 上使用
e^{−aαu}≥e^{−aαv} 并再次调用 P.1。□

引理 P.3：Gamma 核集中于任意固定比例的乘法窗口
给定 δ>0，取 m₀=1+δ/2。对 U>0 和 α>0，令 k(U)=⌊m₀ α U⌋。则存在 c_δ>0 和 U_δ>0，使对所有 U≥U_δ，

                     μ_{k(U),α}([0,U]∪[(1+δ)U,∞)) ≤ 2e^{−c_δ αU}，

其中若 α≥1，U_δ 可以只依赖 δ，不需要随 α 变化。
证明。选一个只依赖 δ 的小数 a∈(0,1/4)，以后固定。对于左尾，由 P.2 和 k+1>m₀αU，

                           log μ([0,U]) ≤ aαU − (k+1)log(1+a)

                                 ≤ αU [a −m₀(a−a²/2)]

                               =−αU[(δ/2)a−(m₀/2)a²]。

选 a≤δ/(2m₀)，上式 ≤−(δa/4)αU。对于右尾，k+1≤m₀αU+1；利用 −log(1−a)≤a+a²（a≤1/4 时成立），

                     log μ([(1+δ)U,∞)) ≤ −aα(1+δ)U −(k+1)log(1−a)

                            ≤ αU[−a(1+δ)+m₀(a+a²)]+(a+a²)

                             =−αU[(δ/2)a−m₀a²]+(a+a²)。

再选 a≤δ/(4m₀)，使方括号至少为 δa/4。若 U≥8(1+a)/(δα)，最后常数可吸收，得到 ≤−(δa/8)αU。于是可取
c_δ=δa/8，并将两个尾部概率相加。□

引理 P.4：一个完整窗口上的 G 上界如何控制 Mellin 高阶导数
固定 0<θ<1、δ>0。设 g:[0,∞)→R 可测，并满足 |g(u)|≤C e^{2u}（C≥1）。对任意大的 U，假设在整段 [U,
(1+δ)U] 上另有单边上界 g(u)≤e^{θu}。令

                         Φ(s)=∫₀^∞g(u)e^{−su}du，Re(s)>2，

                             A_k(s)=(-1)^k Φ^{(k)}(s)/k!。


                             

---


则可选择仅依赖 θ、δ 的实数 σ>2 和仅依赖 C、θ、δ 的常数 K，使对上面每一个足够大的好窗口 U，存在整数
k=k(U)→∞，对全部实数 t 同时有

                          |A_k(σ+it)|+A_k(σ) ≤ K(σ−θ)^{−(k+1)}。

证明。由支配收敛在 Re(s)>2 处逐项微分，

                      A_k(σ+it)= ∫₀^∞ g(u)e^{−itu}u^k e^{−σu}du/k!。

令 W_k(u)=u^k e^{−σu}/k!≥0。将 g=g₊−g₋，应用三角不等式，有

                            |A_k(σ+it)| ≤∫₀^∞ (g₊+g₋)W_k du；

                               A_k(σ)=∫₀^∞(g₊−g₋)W_k du，

二者相加，负部严格相消，因此

                      |A_k(σ+it)|+A_k(σ) ≤ 2∫₀^∞g₊(u)W_k(u)du。 (∗)

记 α=σ−2，并取 k=⌊(1+δ/2)αU⌋。窗口内 g₊≤e^{θu}，窗口外 g₊≤Ce^{2u}。把 (∗) 的积分分成窗口内外，得

                                    |A_k(σ+it)|+A_k(σ)

               ≤2∫_{U}^{(1+δ)U}e^{θu}W_k du +2C∫_{outside}e^{2u}W_k du

                    ≤ 2(σ−θ)^{−(k+1)} + 2C α^{−(k+1)}·μ_{k,α}(outside)。

由 P.3，外部概率 ≤2e^{−c_δαU}。故把外部误差与 (σ−θ)^{−(k+1)} 比较，其比值最多为

                            4C·exp[−c_δαU +(k+1)log((σ−θ)/α)]。

注意 (σ−θ)/α=1+(2−θ)/α。由 log(1+z)≤z 以及 k+1≤(1+δ/2)αU+1，

                                     (k+1)log((σ−θ)/α)

                                ≤ (1+δ/2)(2−θ)U+(2−θ)/α。

因此选择 α=σ−2 充分大，满足 c_δα>2(1+δ/2)(2−θ)，并令 U 再足够大，上述比值就一致有界（事实上趋于
0）。于是整体右侧不超过 K(σ−θ)^{−(k+1)}，K 可取 2+4C（增大阈值即可）。该估计对 t 完全一致，结论
成立。□
P.4 是窗口版 Landau 的核心分析估计：它明确解释为什么“整个窗口上的单边界”能转成高阶导数的统一上
界，以及为什么只需要对任意大的某些窗口成立，而不需要对全部 x 成立。

还未闭合的最后一跳：由极点产生的导数下界
若 Φ 在 Re s>θ 存在极点，下一步必须选取垂直直线上的中心，使一个最近极点在某个圆盘中被隔离，用
Laurent 主部给出 c·d^{−k} 的高阶导数下界；与此同时，P.4 给出至多 K(σ−θ)^{−k} 的上界，因 d<σ−θ 而
矛盾。
本编已严格证明高阶导数上界，但没有把最近极点的存在、唯一隔离、余项 Cauchy 估计等几何解析细节伪装
成已证明。它们在原 Lean 中由 landau_dichotomy、landau_nearest、landau_pole_asym 与
landau_cauchy 处理。


Q. 斜率—整除—体积：一个完整的可检查模型

引理 Q.1：满秩格映射的整除性与范数界
设 L,M 是同维 r 的 Euclidean lattice，T:R^r→R^r 可逆线性映射，且 T(L)⊂p^e M，其中 p 是素数，e≥0。
设 covol(L)、covol(M) 分别为协体积，||T|| 为算子范数。则


---


                 e log p ≤ log ||T|| + (1/r)log covol(L) −(1/r)log covol(M)。

证明。因 T(L) 是 p^eM 的子格，有 covol(TL)≥covol(p^eM)=p^{er}covol(M)。另一方面，covol(TL)=|
detT|covol(L)≤||T||^r covol(L)。连乘即得 p^{er}covol(M)≤||T||^r covol(L)；取对数并除以 r，得要
求的不等式。□
若采用 Arakelov 格平均斜率 μ(L)=−r⁻¹ log covol(L)，则同一不等式是

                             e log p ≤ log||T|| + μ(M) −μ(L)。

原证明中格映射一般并非两侧同秩，还需要最大斜率、子格饱和、亏格/索引及跨层高阶矩；Q.1 不足以替代这
些深层步骤，但完整展示了整除性与解析大小界为何可以联合控制素数和。

引理 Q.2：平方根尺度的最基本最优化理由
对任何 x>0 与 m>0，

                           m + x/m ≥ 2√x，等号当且仅当 m=√x。

证明。由 (√m−√(x/m))²≥0 即得。它证明了若同一估计不可避免地同时含 m 和 x/m，则最优的链长标度必为
√x。实际证明还有 xm/k 和 k/n² 两项；若 n≈x²，k≈x^{9/2}，则 k/n²≈√x，而 xm/k≈x^{-3}，于是四项可
同时处于至多 √x 级别。□
原始 Lean 的 CoreGm.lean 在更复杂的 rank/window 假设下实现了这种指数收支，其最终指数为 1/2+
(e_D+e_L+7)ε。Q.2 不是 CoreGm 的证明，但为该尺度选择提供了一个数学上完全明确、能独立检查的优化
理由。


R. V1.0 审计结果：四个可闭合模块与三个不能略去的关口
-   闭合模块一：V(E;t,B) 到非负加权级数收敛，以及 LinkN 与 DIVinN 之间的数值常数传递（J–K）。
-   闭合模块二：PageN 指数的显式构造；ζ 和非主 Dirichlet 特征的 Riesz/Mellin/尾积分公式（L–M）。
-   闭合模块三：有限阿贝尔群的平移平均与目标字符族投影，以及二次特征素数选择器的非负性（O）。
-   闭合模块四：窗口 Gamma 核的 Chernoff 集中界与 Mellin 变换高阶导数的单边上界（P）；满秩格整除体积
    模型（Q）。
-   仍待完成：窗口 Landau 的最近极点隔离与主部下界、长链 θ 提升的真实整性与局部损失恒等式、Galois 上同
    调窗口界及向实际格的对象同一性传递。

源码依据：Formalism/SharpRestriction/GlobalTheoremInputs.lean；Development/
AutomorphicArithmetic/CharacterBoxes/DivinNOfHypV.lean；Development/
AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/landauWindow.lean；
Development/AutomorphicArithmetic/DedekindLFunctions/LandauTheorems/ChCore.lean；
Development/AutomorphicArithmetic/PrimitiveCosets/CoreGm.lean。外部人类化主稿：Michael O.
Rubinstein 主持的 164 页工作稿（2026-11-21）。
V1.0 仍不是完整 RH 的独立自然语言证明。当前版新增的若干引理已达到可逐条验算程度，下一步的最高优
先级是把这些闭合模块与原 Lean 中真实的 LinkG/LinkN/RecT 数据构造在同一符号系统下对接，同时明确证
明每一个新的几何输入。目标篇幅继续严格少于 500 页。


                               

---


第五编：从 Sha 长度到真实 Theta 格的整除缺陷（V1.1 新增）
本编解决了前版中最容易被“已经证明了 DIVinN”一语掩盖的对象同一性问题：原先算术侧的 etaSum 只是
D7 记录里的一组有理数，几何侧真正需要的是 Theta 提升格的局部商模长度。这里沿着 Lean 中实际使用的
SumLeEtaSumNum、InpAtOf、LinkNOfGd 三条证明链，把归一化、权重、支集、秩和分母损失逐个写
清。


S. 真正的局部格长度与记录 etaJ 的归一化

引理 S.1：局部长度与归一化长度
设 K 为数域，v 为 O_K 的有限素位，e_v 为 v 在相应有理素数 p 下的分歧指数。设 T_j、C_j 是同一 K-向量空
间中的满秩 O_K-格，C_j⊆T_j，且其在 v 处的局部商长度有限。定义：

                         ℓ_j(v)=length_{(O_K)_v}((T_j)_v/(C_j)_v)∈ℕ，

                               η_j^{geom}(v)=ℓ_j(v)/e_v∈ℚ。

则 e_v η_j^{geom}(v)=ℓ_j(v)。这是定义的直接等式，但必须注意分母的意义：在代码中 etaW 是整数局部商
长度，etaU=Col.lenUW 是除以 eW 后的有理长度。`eta_units`、`etaJ_units` 和 `etaJ_ramw` 才让这两个对
象真正对应。

证明。因 e_v≥1，数有理除法得到 e_v(ℓ_j(v)/e_v)=ℓ_j(v)。注意若原始格不是嵌入链或局部商无穷，本定义
不可直接使用；Lean 另有格的存在性、有限长度与同层嵌入证明。□

引理 S.2：有理素数上的局部权重恒等式
记 n=[K:ℚ]。每个 v|p 的惯性度为 f_v、分歧指数为 e_v。令

                      λ_v=(f_v/n)log p， a_v=λ_v e_v=(e_v f_v/n)log p。

若 S_p 是位于 p 上方的任意一批素位，则

                                 0≤∑_{v∈S_p} a_v≤log p。

证明。所有权重非负。数域中素数分解的基本恒等式 ∑_{v|p}e_v f_v=n，故 ∑_{v∈S_p}e_v f_v≤n，乘以
log p/n 得所需结论。

这个等式在 Lean 的 `TwistedPlaces.admissibleMeanCondition_holds` 中实际由 ramification-inertia
degree formula 证明；`SizeData₂.lwP·ramIdx` 等于上面的 a_v。局部长度归一化中的 e_v 因而恰好与这个
权重的 e_v 配对：

                              a_v η_j^{geom}(v)=λ_v ℓ_j(v)。□

引理 S.3：加权素因子损失不会超过 log N
设 N≥1 为整数，令 ν_p(N) 为 p-adic 赋值。对任意有限的素位集合 S，

                              ∑_{v∈S} a_v ν_{p(v)}(N)≤log N。

证明。按下方有理素数 p 重新分组，由 S.2，左边不超过

                               ∑_{p|N} ν_p(N)log p = log N。

最后一式是整数 N=∏p^{ν_p(N)} 取对数。N=1 时，两边都为 0。□


                               

---


数学意义：当我们把某些 Hecke/Galois 行裁剪成较小的 good 子空间时，每个素位至多产生 ν_{p(v)}(N) 倍
的格商损失；所有素位的加权损失可由一个全局整数 N 的 log 控制。


T. 真实 Theta 格长度受记录界控制：对象对接定理

引理 T.1：从 NumTie 与 twisted-place 支集得出项对项等式
设 D 是 Lean 中一条 host/Theta 记录，L 为相应 SizeData₂。设 Tw⊆Pl(K) 是 twist 所用的有限素位集，
ι(y)=D.plEq.symm(y) 将真实 K-素位嵌入/对应到 D 的抽象素位标号。假设：

-   （i）NumTie 的 etaJ 字段成立：对 y∈Tw，记录 η_{j+1}(ιy) 恰等于具体 DefFam 上的 η_j^{geom}(y)；
-   （ii）D 的 ramification field `ramIdx(ιy)` 等于 e_y，记录权重 `lwP(ιy)` 等于 λ_y；
-   （iii）TieTwRec：每个 y∈Tw 都进入 L.supp，且其扭曲参数 μ_y≠μ_0。

那么对每个链层 j，以及 y∈Tw，

                           λ_y ℓ_j(y) = lwP(ιy)·ramIdx(ιy)·η_{j+1}(ιy)。

证明。由 S.1，ℓ_j(y)=e_yη_j^{geom}(y)。再逐一代入（i）、（ii）即可。注意右边的 etaJ 是 D7 的记录字
段，左边的 ℓ_j 则是具体 Hermitian 格的局部 quotient length。两者之间需要（i），不能因为名字相同就省
略此条件。□

定理 T.2：从 etaSum 到真实格长度总和
仍作 T.1 的假设，再假设 etaJ≥0，权重非负。令

                   E_j=∑_{w∈L.supp, μ_w≠μ_0}lwP(w)·ramIdx(w)·η_{j+1}(w)。

则

                                  ∑_{y∈Tw} λ_y ℓ_j(y) ≤ E_j。

证明。T.1 给出每个 y 的等式。由于 ι 是素位标号的双射/单射，Tw 上的有限求和等于其像 ι(Tw) 上对应项的
求和。由 TieTwRec，ι(Tw)⊆{w∈L.supp: μ_w≠μ_0}。集合补集上的每个求和项均为非负数，所以把求和域
扩大到后者不会减小和。这证明了所需不等式。□

这个“部分和≤总和”看似基本，却完成了极重要的事实：`DIVinN` 控制的记录缺陷，确实可以控制实际与
twist 相关的 Theta 提升格商缺陷。其 Lean 实现是 `SumLeEtaSumNum.lean` 中的
`sum_le_etaSum_num`。

定理 T.3：DIVinN → InEta 的完整数学证明
假设链长 m 与记录的 R.m 一致，每个 1≤j≤m 都满足

                                   E_j≤d_j C_e x^ε(B₀+N_c)，

其中 d_j=D.what₂.D0。再假设 d_j 等于真实基础自守空间的维数 d_geom，并且 T.1 的所有数据兼容条件成
立。则对每个 j，

                         ∑_{y∈Tw} λ_y ℓ_j(y) ≤d_geom C_e x^ε(B₀+N_c)。

证明。由 T.2，真实局部商长度加权和≤E_j；由 DIVinN，E_j≤d_j C_e x^ε(B₀+N_c)。再使用秩匹配
d_j=d_geom 合并两式。这个不等式恰是 Divisibility 模块中 `InEta` 的定义，取 `bd(j)=divSize(L,C_e)`。□

Lean 的 `inEta3_num` 是三层 family 数据上的同一论证：先下行到 `FamIn`，应用 `inEta_num`，再把结果
提升回三层 family。这一步并非单纯“重命名变量”，它要同时保持 rank、twist membership 和具体层 j 的
索引一致。
                                 

---


核对调用链：这不是仓库中一条闲置的理论路线
我核实到具体工程入口：`ThirdPlaceSeries/InpAtOf.lean` 中的 `inpAt_of_alt` 直接调用 `inEta3_num`，将
结果命名为 hN，并把它传进 `DivisionInputsWithoutNorm.ofRows ... .toDef hN`。因此，真实局部商长度
与记录 etaJ 的桥梁确实进入最终使用的 Theta/Divisibility 数据构造。

                   DIVinN + NumTie + TieTwRec + rank agreement ⇒ InEta

             InEta → DivInputsDefN.toDef → DivInputs0R → theta/divisor estimates

这比前版“数值型 Sha 界传入 DIVinN”的结论更强：它明确排除了在错误的空间、错误的归一化或错误的层级
上使用 etaJ 的可能。


U. good-cut 稳定性：为什么剪裁不会破坏 LinkN

引理 U.1：逐素位缺陷比较的积分形式
设旧缺陷 η_j(w)，剪裁后的 good 缺陷 η_j^c(w)。假设 N≥1，a_w≥0，d_j≥0，且

                    η_j(w) ≤η_j^c(w)+d_j ν_{p(w)}(N)，对所有相关 w 成立。

那么

                        ∑_w a_wη_j(w) ≤∑_w a_wη_j^c(w)+d_j log N。

证明。将逐点不等式乘以非负权重 a_w 并求和，再用 S.3 给出的 ∑a_wν_{p(w)}(N)≤log N。□

原 Lean 并不直接假定单点系数就是 d_j。`etaJ_le` 先得到更精细的乘数 M_j(w)=∑_{i∈locs(j,w)}
∑_{π∈Zgood(i)}mult(i,π)；随后 `MultLe` 在实际 twisted places 上证明
M_j(w)≤zeroSpaceRankAtPlace(j,w)，并由 `TwistedPlaces.adm3`/rank 对齐将其改写为适用的 d_j。
`etaSum_le_add` 则恰是上面加权和结论。

引理 U.2：把 log N 吸收进原有的几何误差规模
设 x→∞，ε>0，L=x^ε，b=exp(L)，f,m≥1，N=N(x) 满足

                                 log N≤C₁ x^{C₁}L，C₁≥0。

则对足够大的 x，

                                     log N≤C₁ f m b L²。

证明。因为 x^{C₁}=exp(C₁log x)，而 ε>0 保证 C₁log x=o(x^ε)=o(L)，所以最终 x^{C₁}≤exp(L)=b。另外
L≥1，f m≥1，于是 x^{C₁}L≤fmbL²。乘以 C₁≥0 即得。□

定理 U.3：剪裁后的 LinkN 可以传回原 family
设剪裁后的 family F^c 满足 LinkN，具有常数 C；设旧缺陷和剪裁后缺陷满足 U.1，且 rank/size、twisted
support 与新旧数据兼容；再设 N 的大小满足 U.2。写

                   Z=fmbL²+(log x)²N_c， S=∑_p(log p)∑_e len Sha_{p,e}。

剪裁后 LinkN 给出 E_j^c≤d_j(CZ+S)。由 U.1 与 U.2：

                                    E_j ≤ E_j^c+d_j log N

                           ≤ d_j[CZ+S+C₁fmbL²] ≤d_j[(C+C₁)Z+S]。

最后一步使用 Z≥fmbL²，而这来自 N_c≥0。因此原 family 也满足 LinkN，统一常数变为 C+C₁。□
                               

---


这是 `LinkNOfGd.lean` 的 `linkN_of_gd` 的数学内容。它解释了为什么为获得 Galois/local compatibility 而
剪裁好子表示，并不会让关键除子估计的误差失控。

上游：LinkN 真正来自什么数学输入
在 `ThirdPlaceSeries/LinkNFam.lean` 中，`linkN_of_twGood_galoisPreconditions` 首先由
GaloisPreconditions 与 Tie4 取得 good cut，再对剪裁 family 调用
`linkN_along_family_of_localBounds`，最后用 U.3 把 LinkN 传回原 family。剪裁 family 的 LinkN 又经
`GlobalTheory.LinkFam.main` 归结于 `N.linkN_of`；这里需要 `ConclF` 和 `TwistedPlaces.AdmF`，而
ConclF 由 `Hypotheses₂`、局部 Facts 和 BoundAtTwoThreeFamily 等深层输入构造。

                              GaloisPreconditions + Tie4 → good cut

                      Hypotheses₂ + local Facts + BoundAtTwoThree → ConclF

                                   ConclF → LinkN(cut family)

                     LinkN(cut family) + log N bound → LinkN(original family)

注意这里的结论仅是精确恢复了这一条推导链。`Hypotheses₂` 内部的 Galois cohomology、local
Tate/Hecke integral 等深层证明尚待在完整人类证明中逐项展开。


V. V1.1 的实质进展与剩余验证关口
-   已完整写出证明：归一化局部格商长度、按 ramification-inertia 公式归一的局部权重、log N 的素因子吸收、
    NumTie/TieTwRec 下从记录 etaJ 到真实局部长度的项对项恒等式、DIVinN→InEta，以及 good-cut 对
    LinkN 的稳定性。
-   已落实到实际调用：inpAt_of_alt 直接使用 inEta3_num；linkN_of_twGood_galoisPreconditions 确实经
    linkN_along_family_of_localBounds 和 linkN_of_gd。
-   尚未完成：从具体 Theta/Weil 构造证明所有 NumTie、TieTwRec、GaloisPreconditions、ConclF、
    Hypotheses₂ 和 Rallis 局部积分条件；不能把它们作为不需说明的“数学公理”。
-   下一步应沿 `InpAtOf` 的 `DivTied3` 与 `RowsU` 继续，把从真实局部格商长度到斜率—整除不等式的线性代数
    细节彻底展开；然后返回主不等式 M。

本编源码索引（全部固定为 commit 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4）：

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/LiftLat.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/
LiftLatLemmas.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/
SumLeEtaSumNum.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/
LinkDefN.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/TupUsed.lean


---


https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/InpAtOf.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/
ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/InpAtOf.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/
ResidueCharacters/TwistedPlaces.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/
Foundations/GaloisRepresentations/HeckeGaloisCriteria/EvPowLeExp.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/
Foundations/GaloisRepresentations/HeckeGaloisCriteria/IsHeckeGaloisIff.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/
Foundations/GaloisRepresentations/HeckeGaloisCriteria/LinkNOfGd.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AbelianVarietyTheory/Proofs/
InertiaEigenvalues/LinkNAlongFamilyOfLocalBounds.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Development/AutomorphicArithmetic/
ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/LinkNFam.lean

状态声明：V1.1 较 V1.0 新增的是能够逐行验证、具有实质对象意义的数学桥梁，不是把同一份纲要改版。整
套 RH 的自然语言证明仍未完成；只要仍依赖尚未展开的新数学输入，就绝不将当前稿标记为“完整证明”。最
终篇幅仍必须严格小于 500 页。


                                  

---


第六编：主算术不等式的斜率—求和—误差压缩（V1.2 新增）
本编延续第五编中 DIVinN→InEta 的对象对接，继续沿着源代码的真实逻辑次序：InEta 进入
DivInputsDefN.toDef，形成 DivInputsR；由格的积分性、链算子范数和斜率控制产生 DivClausesR；再通
过一个纯粹的有限求和恒等式 DivAssembly 和一个纯粹的常数吸收定理 AbsorbE，得到精确的 divisor
inequality。与只引用 Lean 定理名称不同，本文把 DivAssembly 与 AbsorbE 的主体不等式逐项证明。


W. 三类输入和一条格斜率链

引理 W.1：有限算子链的高度估计
设一组有限维复 Hermitian 空间 V₀,…,V_M 和连续线性映射 T_i:V_i→V_{i+1}，以及终端配对 P:V_M→W。
若对固定无穷素位 v 有 ∥T_i∥_v²≤exp(h_i(v))，∥P∥_v²≤exp(H(v))，则对复合映射 B=P∘T_{M−1}∘⋯∘T₀
有：

                        log ∥B∥_v² ≤ H(v)+Σ_{i=0}^{M−1}h_i(v) （B≠0）。

证明。算子范数的次乘性给出 ∥B∥≤∥P∥∏∥T_i∥；平方并取对数。每个右端的局部上界均为正。若 B=0，则不
取 log(0)，在 DivClausesR 中由单独的零映射分支处理。□

实际 Theta 格的配对不是直接用链始端的度量计算，而是经过一个 Hermitian 商空间和若干尺度 λ_j(v,p) 比
较。若该商空间的度量满足已记录的 scalar-on 分解，把 V₀ 度量送到目标空间时产生的归一化系数记为
κ(v)∏_j λ_j(v,p)，则可将上述一般估计加强为：

                  log ∥B∥_v² ≤ H(v)+Σ_j h_j(v) −log κ(v) −min_p Σ_j log λ_j(v,p)。

其中最小值来自在给定商空间指标 p 中选择对 B 最有利的正定比较界。注意：这一步的标量商度量公式并非
一般的算子链结论；它是源码 `height_chain_atR` 所调用的 `complex_height_cast_at` 的明确几何输入，还
不能被忽略。

引理 W.2：无穷素位平均与最小特征值界
记 A 为无穷素位个数，A>0。对 W.1 第二式取各无穷素位的平均，使用有限和换序，以及每个 v 上 ∑_j
ℓ₆(j)≤min_p Σ_j log λ_j(v,p)，得到

                      (1/A)Σ_v log∥B∥_v² ≤ H̄ +Σ_j h̄ _j−Σ_jℓ₆(j)−meanLog κ。

证明。逐 v 相加，再除以 A；Σ_vΣ_j h_j(v)=Σ_jΣ_vh_j(v)。由于 ℓ₆(j) 与 v 无关，平均后的 Σ_jℓ₆(j) 不变。□

Lean 中 `height_chain_atR` 的前半步是逐 v 上界，后半步完全由上述有限求和恒等式和
`log_eigenvalue_sum_le_min` 完成；`HtNums.le_hu` 再将其送入数字记录 R.hu。最终得到 `DivClausesR`
的第二个字段：非零列映射的平均高度不超过 R.hu−meanLogκ。


X. 核心斜率传递：28 常数的准确用法

定理 X.1：从基础 Hermitian 斜率到列空间斜率
写 μ_B 为基础 Hermitian 格的对偶斜率，μ_C 为所取列空间格的对偶斜率；κ 是相应无穷处归一化。置
m₀=μ_B−meanLogκ。定义有限处误差：

                               F=Σ_jΣ_{y∈Tw} lw(y)·ram(y)·F₀(y,j)，

                                  E=E_{ℓ3}+L_G+Σ_j(E₁(j)+E₂(j))+E₃。


---


设已由基础 Hermitian 格的除子估计及格数据的两个误差约束证明：

                       m₀≤Σ_jℓ₃(j)+2F+L_G+Σ_j(E₁(j)+E₂(j))+E₃，

                   Σ_jℓ₃(j)≤T+E_{ℓ3}，其中 T=Σ_{j,ρ}p_j w_{jρ} log Ω。

则 m₀≤T+2F+E。这是两条不等式直接合并，不涉及新的分析估计。

另外假设列空间与基础格之间的 passage lemma 给出

                  μ_C−meanLogκ ≤ m₀+3d_e(m₀+h_h+28ℓ_a)+28ℓ_a。

在数值记录中 Q≥1，d_e≥0，3d_e Q≤1，m₀+h_h+28ℓ_a≤Q，ℓ_a≤λ₀，m≥1，λ₀≥0，C₀≥28。于是：

                              3d_e(m₀+h_h+28ℓ_a)+28ℓ_a

                              ≤3d_e Q+28λ₀≤1+C₀mλ₀。

这就证明了明确的斜率 passage 上界

                   μ_C−meanLogκ ≤m₀+L_pass， L_pass≤1+C₀mλ₀。

最后设 E≤E_B（误差预算）。把三条不等式输入下一节的纯数值 divisor inequality，可得到

                         μ_C−meanLogκ+R.hu−2F ≤ R.rhs。

说明。这里基础斜率上界来自 `boundsMu`、`latticeGlue` 和相关分母/格商输入；passage lemma 来自
`P.extra.passage`。本定理完整展开了这两项几何结果被调用之后的代数传递，但仍需把二者本身在自然语言
版本中另行证明。□


Y. 从斜率到主项：DivAssembly 的完整有限求和证明

定理 Y.1：分层 factorial/weight 数据的合并恒等式
设 J、Π 为有限集合，T₀⊆Π 为 top 集合，m=|J|，令 A_ρ 为 top 权重，w_{jρ} 为非负辅助权重，p_j、k、
δ_{jρ} 为实数。记 Φ(A)=ph(A)，它在本引理中只需被视为给定的实值函数。设：

                        ν_{jρ}=1_{ρ∈T₀}A_ρ+k w_{jρ}+δ_{jρ}，

                     Φ(ν)_{jρ}−fa_{jρ}≤1_{ρ∈T₀}Φ(A_ρ)+e^E_{jρ}。

再设 U_C≤U_B+L_pass，U_B≤logκ+Σ_{jρ}p_jw_{jρ}logΩ+2F+E_B，并假设以下高度/谱量满足：

                           h_u=h_P+Σ_j h_K(j)−M_λ−logκ；

                      h_K(j)≤Σ_ρ[Φ(ν)_{jρ}−ν_{jρ}logΩ]+e^K_j；

                M_λ≥Σ_{jρ}fa_{jρ}−e₆； h_P≤−Σ_{ρ∈T₀}A_ρ log T+e_P。

则可以精确推出：

             U_C+h_u−2F ≤Σ_{ρ∈T₀}[m(Φ(A_ρ)−A_ρ logΩ)−A_ρ log T]+R_all，

其中 R_all 是误差项

                   R_all=L_pass+E_B+Σ_j e^K_j+e₆+e_P+Σ_{jρ}e^E_{jρ}

                   +Σ_{jρ}|p_j−k||w_{jρ}||logΩ|+Σ_{jρ}|δ_{jρ}||logΩ|。

证明。先把 U_C≤U_B+L_pass、U_B 的上界和 h_u 表达式相加，并减去 2F，得到

           U_C+h_u−2F≤L_pass+E_B+Σ_{jρ}p_jw_{jρ}logΩ+h_P+Σ_jh_K(j)−M_λ。


---


使用对 h_K、M_λ、h_P 的三个估计，右端转化为

                         −Σ_{T₀}A_ρ log T+L_pass+E_B+Σ_j e^K_j+e₆+e_P

                      +Σ_{jρ}[p_jw_{jρ}logΩ+Φ(ν)_{jρ}−fa_{jρ}−ν_{jρ}logΩ]。

由 ν 的精确分解，方括号内等于

                             (Φ(ν)_{jρ}−fa_{jρ})−1_{ρ∈T₀}A_ρ logΩ

                                +(p_j−k)w_{jρ}logΩ−δ_{jρ}logΩ。

前两项由假设≤1_{ρ∈T₀}[Φ(A_ρ)−A_ρlogΩ]+e^E_{jρ}；后两项分别用 t≤|t| 与 −t≤|t| 控制。对 j、ρ 求和
后，1_{ρ∈T₀} 的部分重复 m=|J| 次，便得到所证。□

重要：这里既不使用 θ-lift 的非零性，也不要求 Φ 是特殊光滑函数。本节是一个真正可独立复算的有限求和代
数定理；它对应 `DivAssembly.lean` 中 `divisor_inequality_assembly` 的完整数学内容。


Z. 所有误差如何吸收到一个统一常数：AbsorbE

引理 Z.1：基础尺度预算
设 x≥1、ε>0，记 L=x^ε，b=exp(L)，a=xb，rd≥1，La=log(a·rd)，并假定 log x≤L、log rd≤L。则

                             1≤L，1≤b，0≤La=log x+L+log rd≤3L。

记 B₀=fmbL，N_c≥0，xe≥L，m,f≥1。定义 U=m·xe·(B₀+N_c)，T=|T₀|aLa。那么
U≥mB₀≥B₀≥fb≥b≥1，且 U≥fm²bL。这些不等式均由 m,f,L,xe≥1 和 N_c≥0 推出。□

引理 Z.2：小参数在 b 下统一吸收
另设参数 N≥1、k≥1、S≥0、t,η≥0、C₀≥0、d_C≥1、wʺ≥0，满足

                           N²d_C≤b； m³N²L≤b； mηNL≤b； kN≤b；

                       kS≤wʺ； m(t+1)η≤wʺ； Nwʺ≤b； bʹN≤a； mkbʹ≤a。

那么 N²≤b，S≤wʺ≤b，SN≤b，k(N+S)≤2b。此外，对 0≤w_{jρ}≤2b 有

                                  w_{jρ}+S+N²+m(t+1)η≤5b，

                                 w_{jρ}+k(N+S)+m(t+1)η≤5b。

证明。因为 d_C,N,k≥1，由 N²d_C≤b 推出 N²≤b；由 kS≤wʺ 得 S≤wʺ；由 Nwʺ≤b 得 wʺ≤b。再逐项代入
即可。注意这些上界对所有 j、ρ 统一成立。□

定理 Z.3：精确的八类误差吸收
继续假设 Z.1、Z.2。若各误差函数还满足以下逐点或总量上界：

-   L_pass≤1+C₀λ₀ 且 λ₀≤b； E_B≤C₀U。
-   e^K_j≤C₀[fN²(La+d_C)+fm³N²L]，e₆≤C₀mfN²La。
-   e_P≤C₀[|T₀|bʹN+f(mη+S)N+fN²]La。
-   e^E_{jρ}≤C₀(w_{jρ}+S+N²+m(t+1)η)La。
-   |p_j−k|≤m，|logΩ|≤La，|δ_{jρ}|≤C₀[w_{jρ}+k(N+S)+m(t+1)η+1_{ρ∈T₀}kbʹ]。

则定理 Y.1 中的每项误差均可按下表逐项估计。

误差项                                             来自尺度假设的统一上界


---


L_pass                                          (1+C₀)U
E_B                                             C₀U
Σ_j e^K_j                                       5C₀U
e₆                                              3C₀U
e_P                                             C₀T+9C₀U
Σ_{j,ρ}e^E_{jρ}                                 15C₀U
Σ_{j,ρ}|p_j−k||w_{jρ}||logΩ|                    6U
Σ_{j,ρ}|δ_{jρ}||logΩ|                           C₀T+15C₀U


现逐行证明。第一行由 U≥b≥1，L_pass≤1+C₀b≤(1+C₀)U；第二行是给定预算。

第三行：用 N²La≤3bL、N²d_C≤b、m³N²L≤b，可得每层 e^K_j≤C₀f(3bL+2b)≤5C₀fbL；再按 m 层求和并
使用 mf bL=B₀≤U，得到≤5C₀U。

第四行：e₆≤C₀mfN²La≤3C₀mfbL≤3C₀U。

第五行：|T₀|bʹNLa≤|T₀|aLa=T；由 mηNLa≤3b、SNLa≤3bL 和 N²La≤3bL，剩余项
≤C₀f(3b+6bL)≤9C₀fbL≤9C₀U。

第六行：由 Z.2，每个 e^E_{jρ}≤C₀·5b·3L=15C₀bL。J 恰有 m 个元素、Π 至多有 f 个元素，因此双重和
≤15C₀mfbL≤15C₀U。

第七行：|p_j−k||w_{jρ}||logΩ|≤m·2b·3L=6mbL；在 m 层、至多 f 个位置上求和，≤6fm²bL≤6U。

第八行：Z.2 给出 |δ_{jρ}||logΩ|≤C₀[5b+1_{ρ∈T₀}kbʹ]La≤15C₀bL+1_{ρ∈T₀}C₀kbʹLa 。双重求和的第一项
≤15C₀U；第二项=m|T₀|C₀kbʹLa≤C₀|T₀|aLa=C₀T。

合并全部八行，得到了比源码最终目标还略强的显式上界：

                                     R_all≤(7+49C₀)U+2C₀T。

由于 T,U,C₀≥0，(7+49C₀)≤(10+50C₀)，而 2C₀≤10+50C₀，故

                                    R_all≤(50C₀+10)(T+U)。□

这完整恢复了 `AbsorbE.lean` 中 `error_absorption` 的数值论证；并解释了源码常数 50C₀+10 为什么是一个
可统一吸收的安全余量，而非一个不可说明的“足够大常数”。


AA. Divisor inequality 与实际格侧结论拼接

定理 AA.1：数值型 divisor inequality 的完整合并
在 Y.1 的结构假设和 Z.3 的尺度假设下：

                        U_C+h_u−2F≤Σ_{t∈T₀}[m(Φ(A_t)−A_t logΩ)−A_t log T]

                                    +(50C₀+10)(|T₀|aLa+m xe(B₀+N_c))。

证明。定理 Y.1 的右端恰为所示主项加 R_all，再代入定理 Z.3 的统一误差界。□

在实际 Theta 格构造中，U_C=μ_C−meanLogκ，h_u=R.hu，F=FoOf；而源码 `RecNums.rhs` 的误差项为
(50C₀+10)|T₀|aLa+60c_e m x^ε(B₀+N_c)，比上述公式使用的 U=mxe(B₀+N_c) 有一个归一化版本差异。
Lean 通过 NcF=(x^εN_c)/(log x)² 和 `NcF_spec` 精确核对这两个记号，并利用 C₀≤c_e 与系数冗余吸收后一
项；不能未核对便把这两种 U 直接当作同一量。


---


因此，上述完整证明直接覆盖 `DivAssembly → AbsorbE → TheoremDivIneq` 这一条纯数值链。要进一步得
到实际 `DivClausesR`，仍须使用 X.1 的 Hermitian 斜率、正定格、投影/规范化与商格积分条件。它们既是
深层的数学问题，也是剩余 (M) 尚未完全重构的原因。

定理 AA.2：在几何输入下的 DivClausesR 四个输出
从 `DivInputsR` 的定义出发，`divClausesR_of` 产生如下四项：

-   （i）整性：被有限素位理想 shift 后的初始格在列映射 B 下进入目标格的对偶；使用 DivIntoDualShift 与局部
    val2。
-   （ii）高度：若 B≠0，则链式范数控制与 W.2 的无穷处平均给出 htMap(B)≤R.hu−meanLogκ；B=0 时另行处
    理。
-   （iii）斜率：X.1 提供基础与列格的 passage 上界，Y.1、Z.3 给出数值型 divisor inequality，最终
    μ_C−meanLogκ+R.hu−2F≤R.rhs。
-   （iv）理想 shift 的平均斜率：μ(shiftLat Nu sg)=μ(Nu)+2Σ_w lw(w)⌊sg(w)⌋。该等式来自局部体积/格指数的
    product formula，具体形式是 `shiftMu`。

四项同时成立才是 `DivClausesR`，并非只要证明了（iii）就可推出全部局部—整体比较。随后
`RecBridge.lean` 将它们转成 `WordFacts`，再汇总为 `LinkDIV`；最终 `LinkDIVt` 说明 LinkEta 与 DIVinN
足以触发这条路径。这是 (M) 的格侧主要输入之一。


AB. V1.2 审计报告：完成了什么，尚未完成什么
-   完成且可独立检查：引理 W.1 的算子范数乘法、W.2 的无穷素位有限和变换；定理 X.1 中 28 常数和斜率
    passage 的完整代数传递；定理 Y.1 的纯有限求和证明；Z.1/Z.2 的尺度约束；Z.3 中八项误差的逐项严格吸收
    及常数 50C₀+10。
-   已确认源码直接使用：DivAssembly.lean 与 AbsorbE.lean 被 TheoremDivIneq.lean 联合调用；
    RecNums.divIneq 在 DivisionHeightBoundStatement.lean 中调用 divIneqRecord；
    ConstantGeTwentyEight.lean 的 divClausesR_of 将最终数值界和几何输入合并。
-   仍需证明的原创数学输入：Theta 列映射的实际积分性与先验范数控制、complex_height_cast_at 的商度量比
    较、base.boundsMu 的格协体积/斜率估计、passage lemma 的几何来源、局部算术 val2 与 shiftMu 的具体
    数域格论前提，以及后续 prime-balance 的复杂字符平均。
-   边界说明：这仍不是完整的 RH 自然语言证明。虽然 (M) 的数值压缩已经完成，但 (M) 的原创几何与算术估计
    尚待展开；任何将现稿称为“完整”或“已验收”的说法都不成立。

本轮新增源码索引（均为固定 commit）：

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/StatementJ.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/
StatementE.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/
HermitianTwistDivisors/DivAssembly.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/
HermitianTwistDivisors/AbsorbE.lean


                                  

---


https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/
HermitianTwistDivisors/TheoremDivIneq.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/Inputs.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/
DivisionHeightBoundStatement.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/
ConstantGeTwentyEight.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/LocalToGlobal/Divisibility/
RecBridge.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/
DivIntoDualShift.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/
ScalarLiftLowerBoundFull.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/
7cbf7a0c32fca1badf05931879a37c3f8a2b03b4/src/Formalism/QuotientMetricDivisors/
TheoremDivIneqRows.lean

版本纪律：全稿总页数继续遵守严格 <500 页。当前新增的是有限求和、严格不等式和完整的常数吸收，不是
借鉴结构写出的文字提纲。真正需要大量篇幅的是进一步证明组成 (M) 的几何、上同调和自守表示论引理。


                                  

---


第七编：Theta 格平移、对偶整性与协体积变化（V1.3 新增）
第六编已把 DivClausesR 的斜率字段化成了可复算的有限求和与误差吸收。DivClausesR 还有另外两个必须
解释的几何字段：理想格平移后配对取整，以及平移引起的平均斜率变化。本编直接从数域局部 DVR 的基本
性质出发，逐项重建对应的 `ShiftPairing`、`DivIntoDualShift`、`ShiftIndex` 和 `ShiftMu`。它们是传统代
数数论和格论可以独立检查的推导，而不是另一个原始 Theta Lift 假设。


AC. 局部格的理想平移与双线性配对取整

定义 AC.1：一个按有限素位指定的格平移
设 K 为数域，O_K 为整数环，V 是 K 上 d 维空间，N⊂V 是满秩 O_K-格。对每个有限素位 v，记 v:K×→ℤ 为
标准离散赋值，且设 τ_v∈ℤ 只有有限个非零。定义分式理想

                          I_τ=∏_v 𝔭_v^{−τ_v}，并定义 N_τ=I_τ·N。

在 DVR O_{K,v} 中，分式理想 I_τ 的局部化是 π_v^{−τ_v}O_{K,v}；因此

                                 (N_τ)_v=π_v^{−τ_v}N_v。

这里使用的是局部化与有限分式理想乘法的相容性，并不要求 π_v 在 K 中全局同时统一选择。恰恰因为各素
位可以选择不同局部 uniformizer，必须使用分式理想而不是一个全局数。

引理 AC.2：有限处取整阈值
设 f:V→K 是 K-线性泛函，固定素位 v，实数 s_v 和整数 τ_v 满足 τ_v≤⌈s_v⌉。若对任意 ψ∈N_v 都有 f(ψ)=0
或 v(fψ)≥s_v，则对任意 φ∈(N_τ)_v 都有 f(φ)∈O_{K,v}。

证明。由 AC.1，φ=π_v^{−τ_v}ψ，其中 ψ∈N_v。若 fψ=0，结论显然。否则 v(fφ)=v(fψ)
−τ_v≥s_v−τ_v≥s_v−⌈s_v⌉>−1。因 v(fφ) 是整数，它必须≥0。因此 f(φ)是局部整数。□

注意重要细节：结论只需 τ_v≤⌈s_v⌉，不必要求 τ_v≤s_v。这正是源码 `shift_pairing_formula` 中
`Int.ceil_le` 和整数赋值共同作用的原因。我们的实际应用取 τ_v=⌊s_v⌋，显然满足这一要求。

定理 AC.3：从局部取整推出对偶格整性
设 W 是 K-向量空间，R⊂W 是满秩 O_K-格，B:V×W→K 为 K-双线性配对。设每个 v 都存在局部的标量
ζ_v、投影矩阵 π_v 和基变换 ι_v，使局部配对 P_v 满足

                           P_v(ψ,F)=ζ_v·B(ψ,ι_vπ_vF)， v(ζ_v)=0。

并假设 R_v=ι_vπ_v(M_v)，其中 M_v 是用于定义 P_v 的局部格。再假定对任意 ψ∈N_v、F∈M_v 都有
P_v(ψ,F)=0 或 v(P_v(ψ,F))≥s_v。若 τ_v≤⌈s_v⌉，则

                            B(N_τ,R)⊆O_K，亦即 B(N_τ)⊆R^∨。

证明。固定 v。由于 ζ_v 是局部单位，v(P_v(ψ,F))与 v(B(ψ,ι_vπ_vF))相等。由 AC.2，平移后的所有
ψ∈(N_τ)_v 对 M_v 的配对均为局部整数。借助 R_v=ι_vπ_v(M_v)，得到 B((N_τ)_v,R_v)⊆O_{K,v}。对每个
有限素位 v 都成立，利用数域整数环等于所有有限 DVR 的交 O_K=⋂_v O_{K,v}，推出 B(N_τ,R)⊆O_K。□

这与 `DivIntoDualShift` 中的全部数学假设逐项一致：局部 ζ 的赋值为零；P_v 与 B 的矩阵转换公式；经
ι_vπ_v 的目标格局部化；逐点 val2 下界；最后的 shift。因而 `divClausesR_of` 的第一个输出可用上述三步
独立解释。


                              

---


AD. 格平移与局部指数：−dτ_v 的来源

引理 AD.1：局部指数改变
在 O_{K,v} 这个 DVR 上，选 N_v 的基 e₁,…,e_d。则 (N_τ)_v 的基是 π_v^{−τ_v}e₁,…,π_v^{−τ_v}e_d。基变
换矩阵为 π_v^{−τ_v}I_d，其行列式为 π_v^{−dτ_v}。若 idx_v(N,N_τ) 按基行列式赋值定义（允许为负），
那么

                                    idx_v(N,N_τ)=−dτ_v。

证明。v(det(π^{-τ_v}I_d))=v(π^{-dτ_v})=−dτ_v，且指数在更换 O_{K,v} 基时不变，因为两组基的行列式比
是单位。□

注意这个公式在 τ_v<0 时同样成立；此时 N_τ 在 v 处变小，指数变成正数。源码 `shift_index_formula` 的核
心就是该对角基变换计算。

引理 AD.2：有限素位权重的规范化
设 n=[K:ℚ]，在有限素位 v 上令 𝒩v=|O_K/𝔭_v|，并定义

                                    lw(v)=log 𝒩v / n >0。

若 v 位于有理素数 p 上方，惯性度 f_v、分歧指数 e_v，则 𝒩v=p^{f_v}、v(p)=e_v，因而

                          lw(v)=(f_v/n)log p；Σ_{v|p}lw(v)v(p)=log p。

证明。Σ_{v|p}lw(v)v(p)=Σ_{v|p}(f_v e_v/n)log p=log p，因为 Σ_{v|p}e_vf_v=n。又 v(p)≥1，且所有权重
非负，得到

                                  0≤Σ_{v|p}lw(v)≤log p。□

这一公式与第五编的局部素位权重相同；本编再次从范数与局部度数定义出发，是为了确保在协体积论证里不
会误用 ramification index。


AE. 协体积和平均斜率的精确变化公式

引理 AE.1：局部指数导致的协体积改变
设 K 为全复数域，N 和 N_τ 为同一 d 维 K-空间内的满秩 Hermitian O_K-格，配备相同的无穷处正定度量。
令 lcv(N) 表示本项目按复嵌入归一的对数协体积。对于任意满足局部指数有限支集的格变化，有相对协体积
公式：

                           lcv(N_τ)−lcv(N)=2Σ_v lw(v)·idx_v(N,N_τ)。

证明梗概可直接回到 Dedekind 环的行列式理想：局部格变化的行列式指数为 idx_v，所对应的指数理想范数
是 ∏_v(𝒩v)^{idx_v}。取对数得到 Σ_v idx_v log𝒩v；全复数域上 Hermitian 度量将每个复嵌入计为两个
实维度，因此相对平方范数/协体积的项目归一化带来因子 2/n。最终得到 2Σ_v(lw(v)idx_v)。这一步依赖对
lcv 的具体归一化，不能任意删掉因子 2。

将 AD.1 代入，便有：

                               lcv(N_τ)=lcv(N)−2dΣ_v lw(v)τ_v。

这一式在 Lean 中由 `idxLcv_of`、`covolume_via_basis` 和 `shift_index_formula` 依次给出。


                                

---


定理 AE.2：平均斜率的平移公式
设 d>0。项目使用的平均斜率是 μ(N)=−lcv(N)/d。于是

                                    μ(N_τ)=μ(N)+2Σ_v lw(v)τ_v。

证明。由 AE.1：μ(N_τ)=−[lcv(N)−2dΣ_vlw(v)τ_v]/d=μ(N)+2Σ_vlw(v)τ_v。□

这准确对应 `ShiftMu`，也就是前版 `DivClausesR` 第四字段。它并非额外假设，而是局部指数 + 协体积乘法
性 + 平均斜率定义的直接结果。


AF. 取整误差的精确控制（不遗漏零件）

定理 AF.1：对 floor 平移的双边斜率估计
设 s_v∈ℝ 只有有限个非零。取 τ_v=⌊s_v⌋，且所有非整数 s_v 所在的素位都位于一个有限有理素数集 S 的上
方。则

                             0≤2Σ_v lw(v)(s_v−⌊s_v⌋)≤2Σ_{p∈S}log p。

证明。任意实数 u 满足 0≤u−⌊u⌋<1。乘以正权重 lw(v) 后在有关素位求和，并按其下方有理素数分组，由
AD.2 的 Σ_{v|p}lw(v)≤log p，即得所需双边上界。□

AE.2 因而给出完整的取整损失：

                                 μ(N)+2Σ_vlw(v)s_v−2Σ_{p∈S}log p

                                       ≤μ(N_τ)≤μ(N)+2Σ_vlw(v)s_v。

这个误差是由整数边界产生的真实有限处成本，不是默认可以忽略的 O(1)。当 S 包含所有 p≤Y 的有理素数
时，可再调用经典 Chebyshev 型上界压缩为 O(Y)；对于本段核心结论，不需要假定任何新素数分布结果。

定理 AF.2：DivClausesR 中从积分性到平均斜率的最终闭合
令 s_v=sg(v)，τ_v=⌊sg(v)⌋。由 AC.3，若所有 v 上的 Theta 配对估值至少为 s_v，且局部目标格兼容，则双线
性列映射 B 将 N_τ 送入 R 的对偶。由 AE.2，其源格平均斜率满足

                          B(N_τ)⊆R^∨， μ(N_τ)=μ(N)+2Σ_vlw(v)⌊sg(v)⌋。

若还需要把 floor 的平移转换为真实的 s_v，那么直接使用 AF.1 的双边估计。这两条就是 `divClausesR_of`
的第一和第四字段，连同第六编的高度与数值斜率结果，构成该定理的四项数学输出。□


AG. 本轮新增部分的源码交叉索引与剩余缺口
本轮逐项核查了 `TwistedLatticeNaturality` 中的 `shift_pairing_formula`、`shift_index_formula`、
`shift_slope_mu`，以及 `DivIntoDualShift` 中的 `ShiftPairing`、`ShiftMu`、`RoundingCost` 的精确定义。

-   DivIntoDualShift.lean · QuotientMetricDivisors

-   TwistedLatticeNaturality.lean · HermitianTwistDivisors

-   FinalW.lean · QuotientMetricDivisors

-   ProdFormula.lean · QuotientMetricDivisors

-   DivisionHeightBoundStatement.lean · Divisibility

-   ConstantGeTwentyEight.lean · Divisibility


---


-   本编已实质完成：DVR 中 floor/ceil 格平移的局部整性；所有有限处整数性交汇给出的对偶格包含；局部指数
    −dτ；数域绝对范数及按 p 分组权重；平均斜率的 exact shift formula；取整误差受 Σ_{p∈S}2log p 控制。
-   核心前提仍需另行从 Theta/Weil 几何证明：实际局部配对 P_v 与列映射 B 的 unit-factor 相容性；选取的
    Hermitian 子格确实对应所有相关局部 M_v；全复数域上的正定度量和 lcv 与原始自守列空间的同一性。
-   这些格论引理的证明不能替代复杂的 Rallis、Galois 上同调和 Theta 非零性；主算术不等式 (M) 仍未完整自然
    语言展开。本稿仍未达到最终验收条件。

下一步的真实数学目标：直接反向追踪 `IntoDualShift` 中的局部 P_v      ↔B 相容性如何由 Theta kernel、Weil
representation 和 Hecke/period pairing 的事实得到，同时把 `base.boundsMu` 的协体积项逐项还原。

长度约束保持不变：整套自然语言证明必须严格少于 500 页；当前每次新增都必须可独立检查和有源码对
应，不能重复把仍未完成的算术几何定理写成“由理论可知”。


                          

---


第八编：从商 Hermitian 度量到核心格斜率上界（V1.4 新增）
本编继续回溯第六编 `divClausesR_of` 中的 `P.base.boundsMu`。这不是某个可以随手引用的“斜率有界”公
理：Lean 先证明正定商度量的行列式约束，再将该约束经数域乘积公式与局部格指数转成对数协体积上界，
最后只用有限求和将局部误差吸收。现在将这条链按数学顺序独立写出。对最深层的 determinant/covolume
原始引理，明确划定可核查的已证明部分与依赖部分。


AH. 行列式版 Cauchy–Schwarz 不等式

引理 AH.1：两个满列秩矩阵的 Gram 行列式比较
设 A,B∈ℂ^{n×D} 均满列秩（n≥D），则

                            |det(A*B)|²≤det(A*A)det(B*B)。

证明。令 G_A=A*A、G_B=B*B。两者均正定，故存在正定平方根及其逆。定义 U=A G_A^{−1/2}，V=B
G_B^{−1/2}，从而 U*U=V*V=I_D。矩阵 U*V 是两个正交列等距嵌入间的压缩，故其算子范数至多为 1；所
有奇异值都不超过 1。因此 |det(U*V)|≤1。将 A*B=G_A^{1/2}(U*V)G_B^{1/2} 取行列式并取绝对值平方，
就得到结论。□

注意该不等式无需 A 和 B 的列空间相等；正是跨两个复嵌入时可能不同的行空间导致证明里出现两个 Gram
行列式，而不是同一个行列式的平方。

引理 AH.2：在互换的 CM 嵌入上比较正定商度量
设 K 为 CM 数域，K₀ 为其全实子域。令 H∈M_n(K₀) 在每个复嵌入下正定，P∈M_{D×n}(K) 为满秩商矩阵；
写 Q=P H^{-1}P*。对复嵌入 σ:K→ℂ，定义其 CM 伴随嵌入 σᵗ(z)=overline{σ(star z)}，并设

                 G_σ=σ(P)σ(H)^{−1}σ(P)*， G_{σᵗ}=σᵗ(P)σ(H)^{−1}σᵗ(P)*。

这里 σ(H)=σᵗ(H) 正是 H 的系数来自 K₀ 的结果。取 H_σ^{−1/2} 为正定平方根的逆，令 A=H_σ^{−1/2}
σ(P)*、B=H_σ^{−1/2}σᵗ(P)*。应用 AH.1，得到

                           |det(A*B)|²≤det(G_σ)det(G_{σᵗ})。

另一方面 A*B=σ(P)σ(H)^{−1}σᵗ(P)*=σ(P H^{-1}P*)，右端的 P* 必须使用 K 上的 star，而不仅是对 σ(P) 取
复共轭转置。假设 Q 的行列式非零，则

                            |σ(det Q)|²≤det(G_σ)det(G_{σᵗ})。

如果 X_Q(σ) 是由正定商度量定义的 Hermitian frame，按项目的约定其 metric matrix 等于 G_σ^{-1}。于
是将不等式两端取逆，

                   det(met X_Q(σ))·det(met X_Q(σᵗ))≤|σ(det Q)|^{−2}。

这一步对应 `ReductionLemmaSecond.lean` 的 `place_ineq`，也是后续用乘积公式把无穷处上界搬到有限处
的唯一非平凡矩阵不等式。□


AI. CM 嵌入配对、乘积公式与商格的基准协体积

引理 AI.1：对所有无穷处求和
定义 g=(det Q)^{−1}∈K×。AH.2 的两侧为正，逐个无穷处取自然对数，得到

                   log det met X_Q(σ)+log det met X_Q(σᵗ)≤2 log|σ(g)|。


---


在所有无限位 v 求和。CM 伴随操作 σ↦σᵗ 诱导一一对应 v↦vᵗ；因此左端两项之和恰好是 2∑_{v|∞}log det
met X_Q(v)。消去 2，

                       Σ_{v|∞}log det met X_Q(v)≤Σ_{v|∞}log|v(g)|。

记 [K:ℚ]=n；由于 K 全复，复无限位数为 n/2。数域乘积公式在这一归一化下给出

                         (2/n)Σ_{v|∞}log|v(g)|=Σ_{v∤∞}lw(v)ν_v(g)，

其中 lw(v)=log Norm(v)/n。结合项目把 Gram 行列式写入 lcv 的定义，得到商格基准项的上界：

                              lcv(X_Q,A)≤Σ_{v∤∞}lw(v)ν_v(g)，

这里 A 是正定商空间的基准满秩格，并要求商度量 X_Q 与 Gram 行列式规范匹配。这正是 `lemmaRb` 在把
局部基变换引入前的基准版本。□

引理 AI.2：局部改基导致两个指数项
令 e_v=γ_v e_std 是商格 A 在有限位 v 的局部基，γ_v∈GL_D(K_v)；若 G 的 Gram 行列式按该基计算，

                            G(e_v)=star(det γ_v)·det γ_v·G(e_std)。

对 v 取赋值，

                   ν_v(G(e_v))=ν_v(G(e_std))+ν_v(detγ_v)+ν_v(star detγ_v)。

由复共轭对有限位的作用，ν_v(star a)=ν_{conj(v)}(a)。把 `ν_v(detγ_v)` 解释为基准格到 A 的局部指数，就
得到

                       ν_v(G(e_v))=ν_v(G(e_std))+idx_v+idx_{conj(v)}。

再乘以 lw(v) 求和，由 lw(v)=lw(conj(v)) 和 conjugation 只是有限位集合的置换，两个指数项都合并为 lcv
的相对改变量。这解释了 `lemmaRb_of` 中为何同时出现 idx(v) 与 idx(conj(v))，并且两者都不能忽略。□


AJ. 从基准协体积到多层 Theta 链的分解式

命题 AJ.1：StepBR 型商格比较的准确数学形式
设 X_E 为目标商 Hermitian 度量，R 为与其配套的目标格；对链的第 j 层，设 X_{W,j}、M_j 是正定
Hermitian 格。设 κ(v)>0 为无穷处标量，w 遍历有限位，T_j(μ(w)) 为局部扭曲格；记 A_w 为有限位总校
正：

         A_w=ν_w(G_w)+Σ_j[idx_w(M_j,T_j)+idx_{conj(w)}(M_j,T_j)+jw_w(HT_j,T_j)]。

如果已建立商度量行列式分解 `detRatio(X_Q,X_E)=κ(v)^D∏_j detRatio(X_{T,j},X_{W,j})`、其在基点/扭曲参
数处的一致性，以及局部格指数/Gram 比较的相容性，则

               lcv(X_E,R)≤D·meanLogκ+Σ_j lcv(X_{W,j},M_j)+Σ_w lw(w)A_w。

证明。基准商格部分由 AI.1–AI.2 结合 CM 共轭控制。然后对行列式分解取对数，并对全部无穷处取归一化平
均；乘积成为和，κ(v)^D 贡献 D·meanLogκ，各层 detRatio 对应 lcv(X_{W,j},M_j) 与局部指数、jw 项之
和。有限位的相容性允许把基点与扭曲参数的局部数据放到同一求和中。该过程精确地组成 `weak_form_b` /
`second_step_refined_weak`，而非仅凭三角不等式得到。□

审计标记：AJ.1 的行列式分解及局部 twisted/covolume 相容性是实质性几何前提；本编证明的是在这些前提
下的推导。其原始来源在 `ConjugateWeightLatticeOfGeneral.lean` 以及更下游的
`ProdFormula`/`IdxChange`/`RatHermLcvTwist` 等模块。不得把这些前提称为本稿已经独立证明。


---


AK. 从有限处和到全局斜率：BoundsMu 的完整有限求和证明

定理 AK.1：有限位错误项的双层吸收
沿用 AJ.1。取有限素位集 S 和其子集 T⊆S（T 为 Tw，S 为 Sy）。假设 A_w=0 对所有 w∉S 成立。置

                           A_w=V_w+Σ_j(I_{w,j}+Iᶜ_{w,j}+J_{w,j})。

这里 V_w=ν_w(G_w)，I_{w,j}、Iᶜ_{w,j} 分别为原有限位与共轭位的格指数，J_{w,j} 是 Hermitian 格的 jw
项。令每个 lw(w)≥0，D>0。以下对各部分逐项估计。

条件 1（全局 Gram 部分）。对 w∈S，有 V_w≤D·g_w，且 Σ_{w∈S}lw(w)g_w≤L_G。故

                               (1/D)Σ_{w∈S}lw(w)V_w≤L_G。

条件 2（格指数部分）。对 w∈T，有

                  Σ_j(I_{w,j}+Iᶜ_{w,j})≤D[Σ_j(2F_{w,j}+e_{w,j})+2/ell_w²]。

乘 lw(w)求和并除以 D，交换有限求和次序：

                           (1/D)Σ_{w∈T}lw(w)Σ_j(I_{w,j}+Iᶜ_{w,j})

          ≤2Σ_jΣ_{w∈T}lw(w)F_{w,j}+Σ_jΣ_{w∈T}lw(w)e_{w,j}+Σ_{w∈T}lw(w)2/ell_w²。

条件 3（局部 jw）。对 w∈T、任意 j，J_{w,j}≤D J^0_{w,j}+η_{w,j}。因此

                  (1/D)Σ_{w∈T}lw(w)Σ_jJ_{w,j}≤Σ_jΣ_{w∈T}lw(w)J^0_{w,j}

                                        +Σ_jΣ_{w∈T}lw(w)η_{w,j}/D。

条件 4（预算）。已知对每层 j，

                        Σ_{w∈T}lw(w)(e_{w,j}+J^0_{w,j})≤E_{1,j}，

                             Σ_{w∈T}lw(w)η_{w,j}/D≤E_{2,j}，

                               Σ_{w∈S}lw(w)2/ell_w²≤E_3。

将条件 1–4 的估计相加并使用 T⊆S，得到

                   (1/D)Σ_{w∈S}lw(w)A_w≤L_G+2Σ_jΣ_{w∈T}lw(w)F_{w,j}

                                         +Σ_j(E_{1,j}+E_{2,j})+E_3。

这个公式包含了全部四种局部误差来源，完全由有限求和、非负权重和已陈述的逐点不等式证明，对各个格本
身的构造毫无额外假设。对应 Lean 的 `divisor_bounds_sum`。□

引理 AK.2：如何统一处理 T 之外的素位
在原始 `BoundsMu` 中，S\T 内的素位不必逐层等于零。可以通过一个完全可验证的重参数化把这些项纳入条
件 2 与条件 3：

                     e′_{w,j}=e_{w,j} (w∈T)，否则 (I_{w,j}+Iᶜ_{w,j})/D；

                           J′_{w,j}=J⁰_{w,j} (w∈T)，否则 J_{w,j}/D；

                              η′_{w,j}=η_{w,j} (w∈T)，否则 0。

再规定 F_{w,j}=0 于 S\T。此时对每个 w∈S\T，第 2、3 条不等式都变为等号（额外 2/ell² 非负，故允许放
宽）；而对 w∈T，所有定义不变。由此所有 E₁、E₂、F 的预算仍只在 T 上计算，不增加原有边界。这正是
`untwisted_choice` 的内容。□


---


定理 AK.3：Hermitian 对偶格的全局斜率上界 BoundsMu
设目标格 R 的对偶格平均斜率定义与对数协体积匹配：μ(R^∨)=lcv(X_E,R)/D。第 j 层满足
lcv(X_{W,j},M_j)/D=−μ(M_j)。那么以 AJ.1 的比较式除以 D，再代入 AK.1，得到

                     μ(R^∨)≤meanLogκ−Σ_j μ(M_j)+2Σ_jΣ_{w∈T}lw(w)F_{w,j}

                                      +L_G+Σ_j(E_{1,j}+E_{2,j})+E_3。

证明。由 AJ.1，lcv(X_E,R)/D≤meanLogκ+Σ_j lcv(X_{W,j},M_j)/D+(1/D)Σ_wlw(w)A_w。使用上文的两个斜
率—协体积恒等式并代入 AK.1，立得所写不等式。若 S\T 的素位需要过渡，先应用 AK.2，无须改变预算。□

源码将这个结论写作 `BoundsMu`，并在 `slope_bounds` 中依次调用 `untwisted_choice`、
`divisor_bounds_chain_weak` 和 `dual_lattice_measure`。进入具体的 IndefSide 数据时，`N.l3(j)` 为第 j
层的协体积替代上界；`ramw(w)N.F0(w,j)` 与 F_{w,j} 对应。于是得到项目实际使用的

               μ(R^∨)≤meanLogκ+Σ_j N.l3(j)+2Σ_jΣ_{w∈Tw}lw(w)ramw(w)N.F0(w,j)

                                       +L_G+Σ_j[N.E1(j)+E2(j)]+E3。

这就是第六编中 `divClausesR_of` 为了构造 `hM` 而调用的 `P.base.boundsMu`。本节将这一可复算的定量结
构完全展开了；格数据的各个先验输入则保留在对应的独立几何引理中。


AL. 到主算术不等式 (M) 还有哪些真实工作
本文现已覆盖四个闭合片段：① Sha 界到 DivinN 的常数吸收；② 从局部配对整性到平移格的对偶性与平均
斜率公式；③ 自守列空间的 divisor inequality 有限求和和 50C₀+10 误差吸收；④ 商 Hermitian 度量的
Gram 基准比较，以及 StepBR 输入下的 BoundsMu 有限求和估计。它们都可以定位到具体 Lean 证明。

尚有三种不可消除的几何依赖：第一，Theta/Weil/period 构造出的实际列空间、矩阵和 Hermitian 格必须
满足 AJ.1 所需的行列式比较与局部索引对应；第二，局部格增益 `LinkG_at` 必须对数论要求的每个惯性素数
给出足够强的覆盖；第三，CM 辅助域、Tate–Shafarevich 群与 Galois 表示的构造必须确保这些条件在全部
所需窗口统一成立。任何一个被跳过，都不能称为 (M) 已完整证明。

还应继续核查 determinant comparison 中的 `IsCMSub`、`IsQuotMetric` 和 embedding twist 的前提是否
恰好由实际 Theta Lift 数据提供；这些是用人类证明取代形式化记录时最容易发生逻辑错位的地方。

本编 Lean 源码核查点
-   StatementObj.lean · DivisorInequality

-   BaseLevelBoundsWithCovolumeHolds.lean · DivisorInequalityProofs

-   BoundsSum.lean · HermitianTwistDivisors

-   PlaceSumSquares.lean · HermitianTwistDivisors

-   ReductionLemmaSecond.lean · HermitianTwistDivisors

-   ConjugateWeightLatticeOfGeneral.lean · HermitianTwistDivisors

-   DualMu.lean · HermitianTwistDivisors

-   IndefUse.lean · IndefiniteForms

-   DivisionHeightBoundStatement.lean · Divisibility


                                  

---


-   可独立审核：AH.1 的 Gram 行列式 Cauchy–Schwarz；AH.2 的正定商度量不等式；AI.1–AI.2 的 CM 成对嵌
    入、乘积公式、局部基指数；AK.1 的所有误差项按有限集合逐项吸收；AK.2 的重参数化；AK.3 的协体积—平
    均斜率转换。
-   依赖特定原始构造：行列式分解 detRatio、局部 Gram/指数对应、Weil 表示下配对兼容，以及 uniform host
    上的 LinkG / Sha / Theta Lift。仍未完成完备自然语言证明，不能发布为最终 RH 证明。

本项目页数约束仍为“严格少于 500 页”；本编不依赖逐行翻译数百万行 Lean 代码，而是把数学主体与可引用
的成熟定理合并为论文式引理。


                          

---


第九编：分支秩误差、均值传递与核估计的对数平均（V1.5 新增）
这部分是把前两编的 Hermitian 格斜率上界最终转换成数论中的单边 Chebyshev 上界所需的代数枢纽。抽象
表示论产生的分支重数 n_s 并非完全常数；它们只与共同的参考重数 n̄ 相差 δ 的相对误差。本编从精确的有
限维加权和直接导出平均斜率传递不等式，然后恢复 `PassageAssembly` 以及复嵌入平均的核估计。


AM. 分支重数偏差下的加权均值传递

定理 AM.1：从非负缺额到平均斜率
令 S 为有限集合，对每个 s∈S 取 rk_s≥0、n_s≥0、dg_s∈ℝ。设 R=Σ_s rk_s>0，W=Σ_s n_s rk_s；假设
n̄ >0、0≤δ≤1/3、λ≥0、κ≥0，并有

                         (1−δ)n̄ ≤n_s≤(1+δ)n̄ ， dg_s≤rk_s(H₀+κλ)。

再设三个平均斜率参数 μP₀、μPs、μR₀、μRs 满足

                                   μP₀ R≤Σ_s dg_s+2λR，

                              μPs W≥Σ_s n_s dg_s−(17/2)λW，

                            |μR₀−μP₀|≤κλ， |μRs−μPs|≤κλ。

定义顶端高度上界 H=H₀+κλ 与“平均斜率缺额” Δ=H+2λ−μP₀。则

                                       Δ≥0， 0<W，

                       −μRs≤−μR₀+3δ[−μR₀+H₀+(2κ+2)λ]+(2κ+21/2)λ。

证明。首先 Σ_s dg_s≤HR，故 μP₀ R≤Σ_s dg_s+2λR≤(H+2λ)R；除以 R>0，得 Δ≥0。记非负数
d_s=H·rk_s−dg_s≥0。于是

                         Σ_s d_s=HR−Σ_s dg_s≤(H+2λ−μP₀)R=ΔR。

由于 n_s≥(1−δ)n̄ ，

                               W=Σ_s n_s rk_s≥(1−δ)n̄ R>0。

再因 n_s≤(1+δ)n̄ ，

                           Σ_s n_s d_s≤(1+δ)n̄ Σ_s d_s≤(1+δ)n̄ ΔR。

以 Σ_s n_s dg_s=H W−Σ_s n_s d_s 代入 μPs 的下界，

                             μPs≥H−[(1+δ)/(1−δ)]Δ−(17/2)λ。

关键是对 0≤δ≤1/3，有 (1+δ)/(1−δ)=1+2δ/(1−δ)≤1+3δ。因此

                                  μPs≥H−(1+3δ)Δ−(17/2)λ

                                    =μP₀−3δΔ−(21/2)λ。

用两条 |μR−μP|≤κλ 转移到 R 参数：

                          −μRs≤−μPs+κλ≤−μR₀+3δΔ+(2κ+21/2)λ。

最后，Δ=H₀+κλ+2λ−μP₀≤−μR₀+H₀+(2κ+2)λ，因为 μP₀≥μR₀−κλ。所求得证。□

这条证明清楚表明：δ 的作用不是任意扰动，而是通过非负缺额 Δ 的放大系数 (1+δ)/(1−δ) 进入；它是
`meanTransferBound` 里最值得保留的人类数学思想。


---


引理 AM.2：度数偏差的 17/2 界
假设每个 s 的两个分支度数 dgA_s、dgB_s 满足 |dgB_s−n_s dgA_s|≤(13/2)λ n_s rk_s，并且全局投影度数
degP 位于

                            Σ_s dgB_s≤degP≤Σ_s dgB_s+2λ W。

有限和的三角不等式给出

                          |Σ_s dgB_s−Σ_s n_s dgA_s|≤(13/2)λ W。

加上投影度数相对 Σ dgB 的区间偏差最多 2λW，立即得到

                           |degP−Σ_s n_s dgA_s|≤(17/2)λW。□

这一步就是 `degreeTransferBound`；它解释 AM.1 中数字 17/2 的来源，而不是在平均斜率传递中凭空插入
误差常数。


AN. 可用于主证明的 PassageAssembly 常数

定理 AN.1：小分支误差最终被 1+C₀λ 吸收
将 AM.1 应用于 κ=1，μR₀=−μ₀，μRs=−μC，并取 δ=8fr/g。要求 f,r≥0、g>0，且存在 Q≥1 满足

                                μ₀+H₀+4λ≤Q， 24fr Q≤g。

由 24fr Q≤g 得到 3δQ≤1，从 Q≥1 可知 δ≤1/3，故 AM.1 可应用。然后直接推出

                              μC≤μ₀+3δ(μ₀+H₀+4λ)+(25/2)λ。

但 3δ(μ₀+H₀+4λ)≤3δQ≤1。因此只要 C₀≥25/2，

                                      μC≤μ₀+1+C₀λ。

这是 `meanShiftAssembly` / `PassageAssembly` 的核心。若论文只为最终上界服务，可将中间系数 25/2 保
留在一个引理里，此后不再重做 13/2、17/2、21/2 的常数吸收。□


AO. 复嵌入平均怎样把局部 Theta 核变成统一算术权重

定理 AO.1：嵌入平均的基本恒等式
令 E 是非空有限嵌入集合、T 是有限标签集合、J 是层指标。假设对每层 j、每个 σ∈E，核的对数满足

                         log K(j,σ)≤Σ_{τ∈T}[A(j,τ)−n(j,τ)log Ω(τ,σ)]

                                      +|T|g₀(j) log Θ(σ)+R_j(σ)。

设 R_j(σ)≤R_j 与 σ 无关；令 hK_j=|E|^{-1}Σ_{σ∈E} log K(j,σ)。再假设

                              |E|^{-1}Σ_σ log Ω(τ,σ)=log Ω，

                               |E|^{-1}Σ_σ log Θ(σ)≤C₃ L。

那么

                       hK_j≤Σ_τ[A(j,τ)−n(j,τ)log Ω]+|T|g₀(j)C₃L+R_j。


                              

---


证明。将逐嵌入不等式对 σ 求和、除以 |E|，并交换两个有限和。A(j,τ) 与 σ 无关，因此原样保留；标签对应
的 log Ω(τ,σ) 被统一替换为 log Ω；Θ 项用给定平均上界估计。这一步没有使用均值定理或解析延拓，完全是
有限求和与正权重平均。□

命题 AO.2：将复杂核误差统一成 Ch·fN²(La+m³L)
若 |T|≤f、0≤g₀(j)≤N²，且逐嵌入的余项由下列四部分组成：

                                 R_j=|T|g₀(j)log(8+32|T|g₀(j)v)

                              +2[C₂fm²N²(log g+log T)+C_e fN² log g]

                           +Σ_τ[1+2g₀(j)log(2n(j,τ)+2)]+log h_j+log h′_j。

再设 log(8+32|T|g₀v)≤c₅La；log(2n+2)≤c₆La；log h_j、log h′_j 均不超过 C₄ fN²(L+log T+log g)；log
T≤C₇mL、log g≤C₈L；1≤m,N、0≤L≤La。则将右端按 La 与 m³L 两类分组，可得

                        hK_j≤Σ_τ[A(j,τ)−n(j,τ)log Ω]+Ch·fN²(La+m³L)，

其中只需选取 Ch 同时满足

                                Ch≥C₃+c₅+2c₆+1+2C₄+2C_e C₈，

                                     Ch≥2(C₂+C₄)(C₇+C₈)。

证明。常数项 1 可被 N²La 吸收，m²L、mL 和 L 因 m≥1 都被 m³L 控制；指数性大因子 |T|g₀ ≤fN²。项 |
T|g₀ C₃L、c₅La、2c₆La 及两个 log h 贡献并入第一类，带有 log T 和 log g 的项并入第二类。按上述两条 Ch
的下界分别吸收，得到结论。其算术本质是误差预算分组，不需要新的特殊函数恒等式。□

`AO.1` 对应 `UniformCovolumeTail.stepDiSharp` 中的 hX 有限求和恒等式；`AO.2` 对应随后对 K0、hZ 和
hscal 的逐项估计。若需要更简明的人类论文版本，可把这些预算系数集中放在一个技术引理中，正文只保留
其量纲为何是 fN²(La+m³L)。


AP. Theta 核对数界的来源和剩余数学依赖

引理 AP.1：乘积核界取对数的无损转换
设 K²、κ、M²、Θ²、h 都为正，且对每个标签 τ 有 Ω_τ>0、整数 n_τ≥0、实数 g₀≥0。若

               K²≤h·κ²·M²·Θ²·∏_τ[Ω_τ^{−nτ}·e·(2nτ+2)^{2g₀}·exp(Σ_i ph(ν_{τi}))]，

那么取自然对数，按乘法到加法展开，得

                             log K²≤Σ_τ[Σ_i ph(ν_{τi})−nτ logΩ_τ]

                         +logΘ²+log M²+2logκ+Σ_τ[1+2g₀log(2nτ+2)]+log h。

证明。由所有因子为正，可对不等式取 log；使用 log 乘积=log 之和、log exp(u)=u 和 log Ω^{-n}=−nlog
Ω。该步骤就是 `size_at_embedding`，没有近似损失。□

原始 Theta supremum/Schwartz 核输入负责提供 AP.1 左侧的乘积上界；AO.1 再把不同复嵌入的 Ω_τ 统一
为同一个 logΩ；AO.2 则把核、矩阵系数与高度误差吸收为 fN²(La+m³L)。这一链已经能写成简洁的人类论文
证明；但是第一行乘积上界为何对原始 Theta 核成立，仍要单独证明，不能在本篇中仅以“由显然的核估计”带
过。


                                

---


AQ. 本轮的证明压缩成果、准确边界与源码
第八编解决了从商 Hermitian 度量到 `BoundsMu` 的局部—整体估计。本编进一步把原来散落于分支表示、
核平均、秩扰动三条路线的步骤整合为两个成熟可引用的技术命题：AM.1 是“非负缺额与加权平均”引理，
AO.1 是“有限嵌入平均与共同权重”引理。两者在其他数论应用中也可直接复用。

-   完整展开：分支度数 13/2→17/2 的误差传递；重数相对偏差 δ 下的均值/斜率传递及 3δ 常数；
    PassageAssembly 的 25/2 系数与 1+C₀λ 吸收；Theta 核乘积对数恒等式；嵌入平均与主项消去；C_h 两条预
    算条件的由来。
-   尚需上游证明：实际不可约分支重数 n_s 落在 (1±δ)n̄ 内；原始自守形式空间的 dg_s、μP 与 μR 符合
    degreeTransferBound 前提；原始 Theta 核乘积上界成立；所有 logΩ(τ,σ) 平均确实为统一 logΩ。现阶段这
    些是 Lean 更深层定理的输入。

-   StatementR.lean · BranchSandwichDivisors

-   TransferMean.lean · BranchIsometryProofs

-   StepDiii.lean · BranchIsometryProofs

-   StatementC.lean · ThetaSupremumBounds

-   Assembly.lean · GaussianShiftBounds

-   EvenDegreeWeightBounds.lean · DivisorInequalityProofs

-   StatementObj.lean · DivisorInequality

当前版本仍是未完成的自然语言证明重构稿。严格少于 500 页仍是最后验收的必要而非充分条件；根本条件
依旧是主算术不等式 (M) 的全部自守表示论和 Galois 上同调输入逐个闭合。


                                  

---


第十编：格斜率预算中的统一素数级数界（V1.6 新增）
第八编的全局斜率上界留下一个 E₃ 型低层误差：Σ_v lw(v)·2/ell_v²。Lean 证明这一项≤1，其数值基础是一
个非常接近临界值的严格不等式 2Σ_p(log p)/p²<1。这里把被机械化的无穷素数级数估计改写为一个完全有
限、有理数可复核的传统证明，并给出其应用于数域有限位时正确的 ramification 权重。


AR. 统一素数级数上界

引理 AR.1：把所有大素数压缩到两条模 6 数列
令 f(t)=log t/t²，t≥8。其导数 f′(t)=(1−2log t)/t³<0，因此 f 在 [8,∞) 严格递减。对任何素数 p≥240，p 与 6
互素，故 p=6k+1 或 6k+5，其中 k≥40。即便 6k+1、6k+5 不是素数，把它们也纳入求和只会扩大右端。于
是

                       Σ_{p≥240} f(p) ≤ Σ_{k≥40}[f(6k+1)+f(6k+5)]。

因为 f 递减，f(6k+1)+f(6k+5)≤2f(6k)；而 [6k−6,6k] 长度为 6，其中 f(t)≥f(6k)，故

                             2f(6k)≤(1/3)∫_{6k−6}^{6k}f(t)dt。

取原函数 F(t)=(log t+1)/t，有 F′(t)=−f(t)。把 k≥40 的不等式求和，积分区间恰好衔接，得到

                       Σ_{p≥240}log p/p² ≤(1/3)∫_{234}^∞ (log t)/t² dt

                                       =(log234+1)/(3·234)。□

引理 AR.2：对数的显式有理数上界
对整数 n≥1，取唯一 k≥0 满足 2^k≤n<2^{k+1}，令 z=(n−2^k)/(n+2^k)，则 0≤z≤1/3。对 0≤u<1，反双
曲正切的幂级数是

                       log((1+u)/(1−u))=2Σ_{j=0}^∞ u^{2j+1}/(2j+1)。

将第 N 项之后的尾项用分母 2j+1≥2N+1 与几何级数估计，即有严格的有理数上界

                     0≤log((1+u)/(1−u))−2Σ_{j=0}^{N−1}u^{2j+1}/(2j+1)

                                ≤2u^{2N+1}/[(2N+1)(1−u²)]。

取 N=8。令 R₈(u) 表示右边的有限和加尾项上界，并定义

                                   U(n)=k·R₈(1/3)+R₈(z)。

因为 log n=k log2+log(n/2^k)，而 log2=log((1+1/3)/(1−1/3))，故 log n≤U(n)，且 U(n) 是完全显式的有理
数。这就把验证有限素数和中的所有自然对数，改成了整数乘法、分数幂与有理数比较。□

引理 AR.3：严格的 1/2 上界（含可复核数值证书）
对以下八组整数范围，只保留其中的素数 p，计算 Σ U(p)/p²。利用 AR.2 的显式有理数公式，逐组得到下表中
的严格有理数上界；所有数字以 10⁻⁶ 为单位。

素数区间                                           Σ_{p} U(p)/p² 的严格上界

2—29                                           462331/1000000

30—59                                          14783/1000000

60—89                                          5601/1000000


---


    90—119                                          2549/1000000

    120—149                                         1328/1000000

    150—179                                         1135/1000000

    180—209                                         714/1000000

    210—239                                         635/1000000

同样代入 n=234 的有理数上界，得到 (U(234)+1)/(3·234)<9196/1000000。合并所有区间，

                                Σ_{p<240}log p/p² + (log234+1)/(3·234)

                      <(462331+14783+5601+2549+1328+1135+714+635+9196)/10⁶

                                           =498272/10⁶<1/2。

由 AR.1，大素数的整个尾和不超过上述积分项。因此

                           2Σ_{p prime} (log p)/p² < 996544/1000000 <1。□

这不是浮点计算：各组上界都是由 U(n) 的有理数加法直接比较得出，独立核算程序只使用 Python 标准库
Fraction 的精确整数分数。该程序随本稿一并交付，作为可独立重算的数学计算证书。


AS. 数域每个有限位的局部误差均有统一预算

定理 AS.1：每个有限素位的 ramification 权重如何归并
设 K/ℚ 是 n 次数域。对 K 的有限素位 v，记其下方有理素数为 p(v)，分歧指数 e_v=ν_v(p(v))≥1，惯性度
f_v，残差域范数 Norm(v)=p(v)^{f_v}。按照项目定义

                                lw(v)=log Norm(v)/n=f_v log p(v)/n，

                              ramw(v)=e_v， ellw(v)=p(v)/sqrt(e_v)。

于是每一项直接化为

                            lw(v)·2/ellw(v)²=(f_v e_v/n)·(2log p(v)/p(v)²)。

对任意有限素位集 S，按有理素数分组；由于 ∑_{v|p}f_v e_v=n，

                                       Σ_{v∈S} lw(v)·2/ellw(v)²

                                  ≤Σ_p (2log p/p²)·[Σ_{v|p}f_v e_v/n]

                                         =2Σ_p log p/p²<1。□

不等式没有使用 GRH，也不依赖素数定理；它来自两个基本事实：数域中每个 p 上方的局部度数和为 n，以
及 AR.3 的显式初等素数级数上界。这就为第八编 `BoundsMu` 的 E₃ 项提供了完全可独立检验的绝对常数。

本编的源码与检验材料
-     BaseLevelBoundsWithCovolumeHolds.lean · DivisorInequalityProofs

-     PlaceSumSquares.lean · HermitianTwistDivisors

-     StatementT.lean · MirabolicMackeyTheory

-     RamBasic.lean · MirabolicMackeyProofs


---


本编独立解决的是一个数值和局部度数成本；它虽然发生在高度复杂的 Theta Lift/自守格证明中，却完全不需
要这两者。将来的人类论文可以把本编压缩为“数域有限位权重引理”，并把有理数分块表放在技术附录，正文
只需引用 AS.1。

整套 RH 自然语言证明仍未完成；主算术不等式 (M) 的深层 Theta Lift、Galois 上同调和统一 host 构造还必
须继续展开。严格少于 500 页仍是最终的必要要求。


                       

---


第十一编：Capelli 分支选择子、整数系数与伴随范数（V1.7 新增）


AT. 本编解决的具体问题
在 V1.6 中，格斜率估计已将协体积、有限位指数以及若干定量误差汇总，但这些结论的上游仍需要解释“从

分支表示中只留下指定分量”所带来的整性成本。本编从 Lean 的 BranchSandwichDivisors 与

LastMapNorm 代码恢复一个完全明确的代数构造：用 Capelli 算子的整数特征值构造消去算子，证明它只保

留目标最高权成分，同时计算其归一化时可能出现的整数分母。

本编与 V1.5 的平均斜率传递不同：这里处理的是表示论中“分支选择”和“构造出的整数系数非零”这一前

置步骤。相关的主要 Lean 声明是 InterlaceIdent、ConstituentRange、CapConst、CapLog、

WeylDimBound，以及下游的 cBr_ne、rCap_kill、br_tr 和 norm_le。


AU. 交错最高权与可允许的整数区间

定义 AU.1（交错权、缺额与截断缺额）
设 n≥1，λ=(λ₀,…,λ_n)∈ℤⁿ⁺¹ 和 σ=(σ₀,…,σ_{n−1})∈ℤⁿ 满足交错条件

   λ_i ≥ σ_i ≥ λ_{i+1}，0≤i<n。

这立即蕴含 λ₀≥λ₁≥⋯≥λ_n，即 λ 是弱降序整数列。记

   D₀ = ∑_{i=0}^{n−1}(σ_i−λ_{i+1}) ≥ 0，

   g_i = λ_i−λ_{i+1} ≥ 0，

   D₁ = ∑_{i=0}^{n−1} min(g_i,D₀) ≥ 0。

对每个 0≤i<n，定义可允许区间和它的平移：

   R_i = { v∈ℤ : λ_{i+1}≤v≤min(λ_i,λ_{i+1}+D₀) }，

   I_i = {v−i:v∈R_i}。

以上 R_i、D₀、D₁ 分别对应源码中的 rset、d0、d1。注意 R_i 不是全部交错权的取值区间，而是又受总缺额

D₀ 截断的较短区间。这个截断保证稍后的消去算子有可控的次数。


引理 AU.2（目标坐标的归属与区间大小）
对所有 i，有 σ_i∈R_i；且 |R_i\{σ_i}|=min(g_i,D₀)。特别地，

   ∑_{i=0}^{n−1}|R_i\{σ_i}|=D₁。

证明：由交错关系得 λ_{i+1}≤σ_i≤λ_i。同时，D₀ 是 n 个非负数 σ_j−λ_{j+1} 的总和，所以 σ_i−λ_{i+1}

≤D₀。因此 σ_i≤min(λ_i,λ_{i+1}+D₀)，即 σ_i∈R_i。


---


R_i 是端点均取到的整数区间，其总元素数为 min(λ_i,λ_{i+1}+D₀)−λ_{i+1}+1=min(g_i,D₀)+1。去掉其中的

σ_i，恰好剩 min(g_i,D₀) 个元素。求和即得结论。证毕。


引理 AU.3（相同缺额的其他分支也必落在同一区间）
若 μ=(μ₀,…,μ_{n−1}) 同样与 λ 交错且满足 ∑_i(μ_i−λ_{i+1})=D₀，则每个 μ_i∈R_i。

证明：每个 μ_i−λ_{i+1}≥0，故它不超过这些非负数的总和 D₀；再结合 μ_i≤λ_i 即得 λ_{i+1}

≤μ_i≤min(λ_i,λ_{i+1}+D₀)。证毕。

核对说明：这是 `MemBranchRangeOfDefectEq.lean` 的 `memBranchRangeOfDefectEq` 所表达的数学

事实。后续的消去性可以先对任意 μ_i∈R_i 证明，再用本引理恢复同缺额交错分支这一实际场景。


AV. 区间分离与 Capelli 整数多项式

引理 AV.1（移位区间两两不交）
定义 I_i=R_i−i。若 i<j，则 I_j 中每个整数严格小于 I_i 中每个整数。

证明：λ 单调不增，因此对 j≥i+1 有 λ_j≤λ_{i+1}。任意 x∈I_j 满足 x≤λ_j−j≤λ_{i+1}−j；任意 y∈I_i 满足

y≥λ_{i+1}−i。由于 j>i，有 λ_{i+1}−j<λ_{i+1}−i，故 x<y。证毕。

这一步是消去性的关键，并非一般的整数根多项式都具有这一性质。下标 i 的平移让相邻区间之间至少留出一

个严格的整数间隔，所以不会出现“目标分支的第 j 个特征值与其他区间的根撞车”。


定义 AV.2（Capelli 特征多项式与选择系数）
对任意 μ∈ℤⁿ，定义一元多项式的数值函数 C_μ(u)：

   C_μ(u) = ∏_{j=0}^{n−1} [u−(μ_j−j)] = ∏_j(u+j−μ_j)。

固定目标 σ 后，定义整数选择系数

   P_{λ,σ}(μ) = ∏_{i=0}^{n−1} ∏_{v∈R_i, v≠σ_i} C_μ(v−i)

          = ∏_i∏_{v∈R_i\{σ_i}}∏_j[(v−i)−(μ_j−j)]。

这正是 Lean 中 `capEig lam sg mu` 所使用的三重乘积。目标点的常数记为 c_{λ,σ}=P_{λ,σ}(σ)，对应

`cCap lam sg`。它是整数，因为每个乘积因子都是整数。


定理 AV.3（有限分支谱的精确消去）
若 μ_i∈R_i 对所有 i 成立，且 μ≠σ，则 P_{λ,σ}(μ)=0。

证明：选取某个 i 使 μ_i≠σ_i。因 μ_i∈R_i，整数 v=μ_i 就是外层第 i 个区间的合法取值，且未被删去。将

v=μ_i 代入内层乘积中 j=i 的因子，得到 (v−i)−(μ_i−i)=0。故整个乘积为零。证毕。


                               

---


特别地，由 AU.3，同一个 λ 下任何与 σ 缺额相同但不同的交错分支 μ 都被消去。这解释了为什么“同总缺

额”是最终分支问题中重要但在消去等式本身并非必需的限制。


定理 AV.4（目标系数非零与精确大小上界）
设 n≥1，令 B=λ₀−λ_n+n−1。则 c_{λ,σ} 为非零整数，并满足

   0 < |c_{λ,σ}| ≤ B^{nD₁}。

若 nD₁=0，右侧按 B⁰=1 解释；此时乘积为空，c_{λ,σ}=1。

证明：对任意 i、v∈R_i\{σ_i} 和任意 j，考虑因子 a=(v−i)−(σ_j−j)。若 a=0，说明 v−i=σ_j−j。由于 v−i∈I_i 且

σ_j−j∈I_j，由 AV.1 必有 i=j；于是 v=σ_i，与 v 被排除矛盾。因此所有因子均是非零整数，故它们的乘积

c_{λ,σ}≠0。

再看绝对值。交错关系与 λ 的单调性给出 λ_n≤v,σ_j≤λ₀，同时 0≤i,j≤n−1，故

   λ_n−(n−1) ≤ v−i, σ_j−j ≤ λ₀。

两者之差的绝对值因此至多 λ₀−λ_n+n−1=B。由 AU.2，被选择的整数 v 总数恰为 D₁，而每个 v 对应 n 个 j 因

子，故全部因子数为 nD₁。逐因子乘积即得 |c_{λ,σ}|≤B^{nD₁}。证毕。

核对说明：上面严格恢复了 `Numeric.lean` 的 `cap_factor` 与 `capacity_constant_bound`。这里的指

数 nD₁ 不是“某个常数乘维数”的粗糙猜测，而来自外层 D₁ 个备选根，每个根有 n 个特征值因子。

推论 AV.5（归一化的对数成本）
若 a>0 且 B≤2a，则 c_{λ,σ} 是非零整数，且

   log |c_{λ,σ}| ≤ nD₁ log(2a)。

证明：由非零性，|c_{λ,σ}|≥1；由 AV.4，|c_{λ,σ}|≤B^{nD₁}≤(2a)^{nD₁}。由于 B≤2a 且 B≥1（在 nD₁>0

情形），可取自然对数得到结论。若 nD₁=0，左侧为 0，结论也成立。证毕。

请注意这一界的实际意义：在特征零的数域中可以除以 c_{λ,σ} 得到归一化选择子；在整数格上却可能引入以

c_{λ,σ} 为分母的有理系数。因此需要把 log|c_{λ,σ}| 记入后面的有限位整性或高度预算，而不能简单把投影算

子视为整系数的。


AW. Capelli 算子怎样在表示空间中实现选择

引理 AW.1（Capelli 行列式的最高权特征值）
设 V 为特征零域上的 gl_n 表示，E_{ab} 为矩阵单位对应的算子。设线性泛函 ψ:V→K 满足：当 a>b 时，

ψ(E_{ab}x)=0；以及 ψ(E_{jj}x)=μ_j ψ(x)。定义具有固定因子顺序的 Capelli 行列式算子 Cap(u)，即将

[(u+k)δ_{a,k}−E_{a,k}] 按列指标 k 依次相乘并按置换符号求和。则


---

                                                            
   ψ(Cap(u)x) = C_μ(u)ψ(x)

         = [∏_{j=0}^{n−1}(u+j−μ_j)] ψ(x)。

证明：按照定义将 Cap(u) 展开为所有置换 α∈S_n 的和。对恒等置换，每个因子都是对角的 (u+k)−E_{kk}；

由 ψ 的权重性质，逐个作用后留下 ∏_k(u+k−μ_k)ψ(x)。

若 α≠id，设 k 为最小的非不动点。因为所有 0,…,k−1 都已被 α 固定，置换的单射性排除 α(k)<k；故

α(k)>k。该项中前 k 个因子为对角因子，到了第 k 个因子时，因 α(k)≠k，只剩下 −E_{α(k),k}。由于 α(k)>k，

ψ 在这一严格下三角算子上为零。故每个非恒等置换项均被 ψ 消去。余下恰是恒等置换项。证毕。

核对说明：此推导对应 `BranchingAdmissibleFacts.lean` 中的 `capDet_dual`；它需要明确规定非交换行

列式的乘法顺序。若随意把因子当作可交换，证明会出现逻辑跳步。

定理 AW.2（在半单分支谱上的代数选择子）
假设一个有限维表示空间 V 分解为若干最高权分量 V_μ 的直和，且每个 Cap(u) 在 V_μ 上按 C_μ(u) 作标量作

用，并且所有出现的 μ 都满足 μ_i∈R_i。定义算子

   Q_{λ,σ} = ∏_{i=0}^{n−1} ∏_{v∈R_i\{σ_i}} Cap(v−i)。

此处各 Cap(u) 在上述分量上同时按标量作用，因而乘积在该表示空间内是明确的。

对目标分量 V_σ，由定义及 AW.1，Q_{λ,σ}|_{V_σ}=c_{λ,σ}·id；对其他任何 V_μ，AV.3 给出 Q_{λ,σ}|_{V_μ}

=0。因此

   Π_{λ,σ} = c_{λ,σ}^{−1}Q_{λ,σ}

就是 V 上投影到 V_σ 的代数投影。因为 c_{λ,σ}≠0，这个算子在特征零域上定义良好，且 Π²=Π。证毕。

重要限定：实际形式化对象未必在每一步都已被拆成显式的半单直和。`rCap_kill` 还通过最高权过滤、首个

非零主项及归纳法处理非半单的中间数据。因此 AW.2 是清晰的“谱上结论”，不是对整个原 Lean 高度复杂

的过滤归纳的偷换。


AX. 从选择子到分支映射及伴随范数

命题 AX.1（分支映射复合中的整数因子）
设 Br:V_λ→V_σ 为分支映射，Tr:V_σ→V_λ 为相应配对意义下的伴随传递映射，并假定两者与目标群作用相

容。假设存在非零目标向量 e_σ、向量 ξ_λ 以及标量 b，使

   Tr(e_σ)=c_{λ,σ} ξ_λ，

   Br(ξ_λ)=b e_σ。

若 V_σ 为不可约表示，则 Br∘Tr 是 V_σ 的自同态，按 Schur 引理是某个标量算子；把上式应用于 e_σ，得到

标量恰为 c_{λ,σ}b。因此


---


   Br ∘ Tr = (c_{λ,σ}b)·id_{V_σ}。

如果 b≠0，则 Br 是满射，Tr 是单射，并且该复合可以归一化为恒等映射。若 b=0，仅能得出该恒等式为零，

不能推断分支映射可逆。本稿不省略这个非零条件。

核对说明：`LastMapNorm.lean` 的 `tr_hi`、`br_xi`、`br_tr` 实际给出上述关系；c_{λ,σ} 在下游称为

`cBr`，标量 b 对应 `brConst`。同一文件的 `cBr_ne` 直接引用 `capConst`。

定理 AX.2（伴随性与缩放复合的范数界）
设 (V,B)、(W,B′) 为正定 Hermitian 空间，P:V→W 与 A:W→V 为线性映射，满足

   B(Ay,x)=B′(y,Px)，对所有 x∈V,y∈W；

   P A = κ·id_W，其中 κ>0。

则对任意 x∈V，有 B′(Px,Px)≤κB(x,x)，即 ‖P‖²≤κ。

证明：利用正定性，对向量 κx−A(Px) 考虑其自内积：

   0 ≤ B(κx−APx,κx−APx)。

展开并使用伴随关系 B(APx,x)=B′(Px,Px)，以及 B(APx,APx)=B′(Px,PAPx)=κB′(Px,Px)，得到

   0 ≤ κ²B(x,x)−2κB′(Px,Px)+κB′(Px,Px)

    = κ²B(x,x)−κB′(Px,Px)。

因为 κ>0，除以 κ 得 B′(Px,Px)≤κB(x,x)，证毕。

在表示论应用中，P 可以取分支限制映射，A 取由配对定义的伴随映射；AX.1 给出 PA 的标量来源。于是对分

支映射的范数控制不再是完全额外的分析估计，而直接来自 Capelli 系数和另一个经过归一化的正标量。


AY. 有限维消去系数对全局误差的贡献

引理 AY.1（截断缺额的稀疏例外界）
对任意指标集 I⊆{0,…,n−1}，若 |I|≤3，则

   D₁ ≤ 3D₀ + ∑_{i∉I}(λ_i−λ_{i+1})。

证明：对 i∈I，min(g_i,D₀)≤D₀；对 i∉I，min(g_i,D₀)≤g_i。故

   D₁=∑_{i∈I}min(g_i,D₀)+∑_{i∉I}min(g_i,D₀)
    ≤ |I|D₀+∑_{i∉I}g_i

    ≤ 3D₀+∑_{i∉I}g_i。

证毕。该引理把可能的特殊分支落点限制在至多三处，从而让剩余每处的局部成本通过原权重的相邻间隔控

制。对应 Lean 的 `TruncatedDefectBound`。


---


引理 AY.2（Weyl 维数界）
若 ν₀≥⋯≥ν_n 为整数，则 Weyl 维数公式中每个正根因子满足

   1 ≤ [ν_i−ν_j+j−i]/(j−i) ≤ ν₀−ν_n+n，0≤i<j≤n。

证明：ν_i−ν_j≥0，故左界成立；右边分子可用 ν₀−ν_n+(j−i) 估计，而 j−i≥1，因此该分式不超过

ν₀−ν_n+1≤ν₀−ν_n+n。共有 n(n+1)/2 对 i<j。逐因子相乘得

   1 ≤ dim V_ν ≤ (ν₀−ν_n+n)^{n(n+1)/2}。

证毕。这给出另一个可独立控制的整数/维数成本，不能直接用它替代 Theta Lift 的协体积估计，但它能用于

限制分支后有限维表示的规模。对应 `Numeric.lean` 的 `weyl_dimension_bound`。


AZ. 完整数值例子与严格的源码适配
取 n=2，λ=(7,4,1)，σ=(6,2)。此时 D₀=(6−4)+(2−1)=3，g₀=g₁=3，故 D₁=6。两个允许区间为 R₀={4,5,6,7}、

R₁={1,2,3,4}，平移后 I₀={4,5,6,7}、I₁={0,1,2,3}，确实严格分离。

整数选择系数共有 nD₁=12 个因子。直接精确乘法得到 c_{λ,σ}=20736≠0；统一上界 B=7−1+2−1=7，故 |

c_{λ,σ}|≤7¹²=13,841,287,201。

竞争分支 μ=(7,1) 与 λ 交错，并满足同一 D₀=3。因为 μ₀=7∈R₀ 但 μ₀≠σ₀=6，三重乘积中 (i,v,j)=(0,7,0) 因子

为 0，所以 P_{λ,σ}(7,1)=0。

这个例子同时检查了三个容易弄错的细节：必须先删去 v=σ_i；内层乘积依赖 j；区间分离发生在 v−i 坐标，而

不是原始权重 v 的坐标。


BA. 本轮真正闭合了什么，尚缺什么
本编闭合：交错权推出同缺额区间归属；截断区间的根数；移位区间分离；Capelli 整数系数的非零性与精确

上界；在已知 Capelli 特征值公式时的谱消去；最高权泛函下 Capelli 特征值公式的排列展开；伴随性给出的

范数界；最多三处稀疏例外的缺额估计；Weyl 维数界。以上不需要把整个 RH 或主不等式 (M) 当作已知。

本编没有闭合：实际自守 theta kernel 的所有谱分解假设、分支测试向量的构造、局部周期归一化常数 b 的明

确非零界，以及这些分支代价如何与全局 Rallis/Sha 输入定量拼接。这些仍属于原证明真正困难的几何与表示

论部分。

相较 V1.6，这次不是再完成一个纯数字不等式，而是恢复了一个能进入原证明的整数系数选择机制，证明了该

系数为什么不会为零，以及它给最终高度估计带来的对数损失到底有多大。全文的“完成百分比”不宜依据本

编新增页数直接改变；依然需要主算术不等式 (M) 的深层几何链完全闭合。


                               

---


本编源码索引
-   交错权、缺额、选择多项式定义：src/Formalism/BranchSandwichDivisors/StatementR.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/StatementR.lean

-   区间包含和缺额相同的判据：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/

    MemBranchRangeOfDefectEq.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/

    MemBranchRangeOfDefectEq.lean

-   交错求和和截断整数根数：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/

    Interlace.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/Interlace.lean

-   CapConst、CapLog、WeylDimBound 证

    明：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/Numeric.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/Numeric.lean

-   分支整数系数在下游的定理导出：src/Formalism/BranchSandwichDivisors/

    DivFromPassageAndNorm.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/DivFromPassageAndNorm.lean

-   Capelli 最高权特征值与过滤消去：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

    BranchingAdmissibleFacts.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

    BranchingAdmissibleFacts.lean

-   cBr_ne、br_tr 与伴随范数

    界：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LastMapNorm.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LastMapNorm.lean

校验材料 `branch_capelli_exact_certificate.py` 逐项检查 n=1、2、3、4 的多组小最高权样本：包含构造的

整系数非零、幂次数、绝对值上界、所有同缺额竞争分支被消去和稀疏缺额上界。它是辅助查错，不代替本编

的全称量词证明。


                                    

---


BB. 非半单权过滤上的 Capelli 消去定理（V1.8 新增）
上一编的 AW.2 在 V=⊕V_μ 的显式半单直和上很容易证明。但实际 Lean 源码中的中间多项式模 W 未必已经写

成这种直和。要从“每个允许最高权上的特征值”推出整个模上的消去结论，必须证明一条有限权支撑归纳。

这一编完整恢复 BranchMap.lean 的 bmE_sep_op、bm_kill，并把它们同 rCap_kill 接起来。


定理 BB.1（抽象权过滤消去定理：精确假设）
设 R 是特征 0 的整环，M 是 R 上带有有限权支撑分解的多项式模；写 π_β 为权 β 的线性投影。对任意 F∈M，

只有有限多个 π_βF 非零，并且若所有 π_βF=0，则 F=0。设 W⊆M 是子模，B 为权集合，ω:B→ℤ 为优先次序

函数，A⊆B 为允许权集合，b∈B 为待保留的目标权。

设有一族 R-线性算子 C(u):M→M（u∈ℤ），以及整数值函数 χ(β,u)∈ℤ。要求如下四条性质：

（H1）C(u) 两两交换，并与每个 π_β 交换；C(u)W⊆W。

（H2）对任意 0≠F∈W，若 β 是 F 的实际权支撑中使 ω 最大的某个权，则 β∈A 且 C(u)

(π_βF)=χ(β,u)π_βF，对所有 u∈ℤ 成立。注意只要求最大权层成为特征向量，不要求整个 W 半单。

（H3）不同的允许权能够被整数谱区分：若 β,γ∈A 且 β≠γ，则存在 u∈ℤ，使 χ(β,u)≠χ(γ,u)。

（H4）存在有限整数列表 L，使每个 β∈A\{b} 都存在 u∈L 满足 χ(β,u)=0。

令 T_L 为 L 中 C(u) 按固定顺序的算子乘积。则对每个 F∈W，若 π_bF=0，必有 T_L F=0。

这就是无需先分解 W 的消去命题。证明分成两个完整引理：有限权谱分离与权支撑下降。


引理 BB.2（非零整数倍的有限谱分离算子）
在 BB.1 的（H1）—（H3）下，固定一个允许权 β₀∈A 和一个不含 β₀ 的有限权集 S⊆B。存在算子 Q 与非零

整数 q，满足：

  （i）Q 与所有 C(u)、π_β 交换，且 QW⊆W；

  （ii）若 C(u)F=χ(β₀,u)F 对所有 u 成立，则 QF=qF；

  （iii）若 G∈W 且 G 的权支撑包含于 S，则 QG=0。

证明：对 |S| 归纳。若 S=∅，取 Q=id、q=1；由于权投影联合忠实，支撑为空的 G=0，故（iii）成立。

设 S 非空，取 β₁∈S 使 ω(β₁) 在 S 中最大，令 S′=S\{β₁}。由归纳假设，存在 Q′、非零 q′，对 S′ 和目标 β₀ 满

足三个结论。若 β₁∉A，则任何 G∈W 的非零权支撑若包含于 S，不可能包含 β₁；否则 β₁ 是实际最大权，违

背（H2）。所以同一个 Q′、q′ 即适用于 S。

余下假设 β₁∈A。由于 β₀≠β₁，（H3）给出 u₁ 使 d=χ(β₀,u₁)−χ(β₁,u₁) 为非零整数。置

  T=C(u₁)−χ(β₁,u₁)·id，   Q=Q′T，   q=q′d ≠0。

由（H1）和归纳假设，Q 仍与所有 C(u)、π_β 交换并保持 W。若 F 是 β₀ 的共同特征向量，则 TF=dF，故

QF=Q′(dF)=qF，证得（ii）。


---


若 G∈W 且 supp(G)⊆S：倘若 π_{β₁}G=0，T 不会产生任何新权，故 supp(TG)⊆S′；倘若 π_{β₁}G≠0，则

β₁ 在实际支撑中最大，由（H2）

  π_{β₁}(TG)=[C(u₁)−χ(β₁,u₁)](π_{β₁}G)=0。

其余权亦不会因 T 出现新的支撑，因此两种情形都有 supp(TG)⊆S′。归纳假设于是给出 QG=Q′(TG)=0，证得

（iii）。有限归纳完成。证毕。

这一构造的关键是全程只做整数系数算子乘法。q 可能很大，但这里只用 q≠0；不会把 1/q 加进最终格的分

母预算。


定理 BB.3（无半单假设的有限权支撑下降）
证明 BB.1 的结论。对 k=|supp(F)| 归纳。k=0 时 F=0，结论显然。设 k>0，在实际权支撑中取某个 ω-最大权

β₀。由（H2）它是允许权，并且 π_{β₀}F 是所有 C(u) 的共同特征向量。由于 π_bF=0，β₀≠b。令 S=supp(F)

\{β₀}。用 BB.2 构造 Q、q≠0。

首先证明 QF 是全局共同特征向量，而非仅仅它的最高权部分。固定 u，令

  H_u=C(u)F−χ(β₀,u)F。

由于 C(u) 保持 W，H_u∈W；由投影交换性及（H2），π_{β₀}H_u=0；对支撑外的其他权也仍为零。因此

supp(H_u)⊆S。根据 BB.2（iii），QH_u=0；又 Q 与 C(u) 交换，故

  C(u)(QF)=Q(C(u)F)=χ(β₀,u)QF。

利用（H4）选 u₀∈L 使 χ(β₀,u₀)=0。因为 QF 对每个 C(u) 都是特征向量，

  T_L(QF) = [∏_{u∈L}χ(β₀,u)]QF=0。

构造新的向量 F′=qF−QF。因 Q 保持 W，F′∈W；因 Q 与投影交换且由 BB.2（ii）作用于最大权层，

  π_{β₀}F′ = qπ_{β₀}F−Qπ_{β₀}F=0。

其他权的支撑没有扩张，所以 supp(F′)⊆S，严格少于 k 个。并且 π_bF′=qπ_bF−Qπ_bF=0。根据归纳假设

T_L(F′)=0。结合上一式，

  0=T_L(F′)=qT_L(F)−T_L(QF)=qT_L(F)。

R 为特征 0 整环，所以非零整数 q 在 R 中不是零因子；多项式模 M 作为自由 R-模是无挠的。于是 T_L(F)=0。

归纳完成。证毕。


BC. 从抽象消去回到最高权 Capelli 算子

命题 BC.1（实际 Lean 数据与 BB.1 的逐项对应）
在 BranchMap.lean 中取 M=R[(Fin(n+1)×Fin n) 个变量]，W=bmW(n,λ,d) 为相应的 dual-Weyl/权约束子

模，权空间由最后一行变量的加权齐次投影 zcomp(β) 给出。置


---


  ω(β)=∑_{j=0}^{n−1}(j+1)β_j；

  χ_β(u)=∏_{j=0}^{n−1}[u+j−(λ_j−β_j)]；

  C(u)=rCap(u)，   b_j=λ_j−σ_j。

（H1）由 rCap_comm、zcomp_comm_rCap 以及 capelliDeterminantFirstRows_mem_bmW 提供；

（H2）是 rCap_top：它从实际最大最后一行权分量提取一个允许分支并给出准确的 Capelli 特征值；（H3）

由 bm_sep 提供；（H4）由 bm_list_kills 提供。

因而上节 BB.3 可以逐字应用于 W 中任意满足 zcomp(b)G=0 的多项式 G，得到：

  [∏_{u∈bmList(λ,σ)}rCap(u)]G=0。

这与源码 BranchingAdmissibleFacts.lean 的 rCap_kill 完全同型；它是针对尚未明确分裂的多项式模的核消

去定理，不是先假定半单直和后得到的同义反复。


引理 BC.2（为什么竞争分支必命中某个零特征值）
若最大权 β 不等于 b，但其分支最高权 μ=λ−β 与 σ 有相同的总缺额，那么上一编 AU.3 已证明 μ_i∈R_i。取 i

使 μ_i≠σ_i，令 u=μ_i−i。由于 μ_i∈R_i\{σ_i}，这个 u 是 bmList(λ,σ) 的某一项；而 χ_β(u) 的 j=i 因子为

  u+i−(λ_i−β_i)=(μ_i−i)+i−μ_i=0。

这就从有限区间组合证明了（H4），并且对实际最高权过滤中的所有允许竞争者统一有效，不需要逐个枚举

所有分支。


命题 BC.3（最后要保留的整数不是归纳过程中出现的 q）
当 G 纯处于目标权 b 时，目标 Capelli 特征值乘积为

  ∏_{u∈bmList(λ,σ)}χ_b(u)=c_{λ,σ}≠0。

该恒等式即 bm_list_prod，且非零性由 AV.4 证明。BB.2 中用于剥离权过滤的整数 q 仅是归纳证明的中间乘

子，证明中从未把 q 倒置。故最终整性/高度成本仍由 c_{λ,σ} 主导，不应把中途辅助 q 的大小误算进分母。这

是对 V1.7“半单谱投影”论证的实质性强化。


BD. 示例、证明边界与下一段依赖

实例 BD.1（检查竞争最高权的零根）
沿用 V1.7 的 n=2，λ=(7,4,1)，σ=(6,2)。目标最后一行权 b=(1,2)，χ_b(u)=(u−6)(u−1)。

另一个同缺额交错分支 μ=(7,1) 对应 β=(0,3)，所以 χ_β(u)=(u−7)u。选 i=0、u=7，此时 χ_β(7)=0，而

χ_b(7)=6≠0。另一竞争者 μ=(5,3) 对应 β=(2,1)，选择 u=5，得到 χ_β(5)=0、χ_b(5)=−4≠0。

这些算例只用来检查移位索引与特征多项式的符号，不能替代一般消去定理。一般结论依靠上面的“有限谱分

离 + 权支撑下降”两层归纳。


---


审计 BD.2（与半单性有关的一个危险误用）
不能仅因 χ_β(u)=0，就断言 C(u) 消去一个广义特征向量。例如在一个 Jordan 块上，C=χI+N 且 N≠0、

N²=0，若 χ=0，则 C=N 未必为零。V1.7 的半单直和证明不能直接用在这种情形。

BB.3 之所以有效，是因为（H2）对任何 W 内向量的实际“最高”权层都给出严格特征向量性质，而（H1）

防止 C(u) 混合权。于是消去算子先作用于真实最高层，余下部分通过归纳下降。这些强假设正是 Lean 的

rCap_top、rCap_comm、zcomp_comm_rCap 所提供的内容；缺少其中任一条，结论都不能无条件成立。


本编达成的严谨结论
已经闭合：抽象有限谱分离算子的整数构造及其三条性质；不假设半单分解的全局消去归纳；最高权竞争者对

应零 Capelli 特征值；目标整数特征值乘积与 c_{λ,σ} 的一致性。因而 V1.7 将 rCap_kill 标作“未展开”的过

滤归纳缺口，在本编已完成自然语言重构。

仍未闭合：rCap_top 所依赖的 dual-Weyl 模表示论输入、最高分量为何满足最高权/本征性质的底层多项式计

算；整系数局部格上这些映射的精细范数/除子估计；以及上述分支算子怎样从实际 Theta Lift 核与

Galois/Sha 估计中被构造出来。主算术不等式 (M) 仍然没有完整自然语言证明。


本编源码索引（固定仓库快照）
-   抽象有限谱分离、非半单消去、具体整数根列表、特征值乘积：src/Formalism/

    BranchSandwichDivisors/BranchIsometryProofs/BranchMap.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/BranchMap.lean

-   具体 rCap_kill 与最高权本征值

    rCap_top：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

    BranchingAdmissibleFacts.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

    BranchingAdmissibleFacts.lean

-   同缺额插入区间判据：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/

    MemBranchRangeOfDefectEq.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/

    MemBranchRangeOfDefectEq.lean

-   非零整数上界与对数成本：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/

    Numeric.lean


                                    

---


    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/Numeric.lean

-   非交换 Capelli 算子的定义与权分量关

    系：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/BranchMap.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/BranchMap.lean

-   分支映射实际应用及配对关系：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

    LastMapNorm.lean

    https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a
    2b03b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LastMapNorm.lean

版本状态：V1.8 为总稿的一个已严格条件化的局部证明章节；不以本轮新增页数线性推高总体完成百分比。总

体仍按“主算术不等式 M 及原始几何构造尚未闭合”的标准评估。


第十二编：有限域分支重数与第三步高度不等式（V1.9 新增）
本编由原始 Lean 仓库的 MultPlace、MultProd、PlaceBound、MultSharpOfPlaceBound、

BranchSandwichDiii 和 StepDiii 等实际引理直接还原。它位于 V1.7—V1.8 的 Capelli 分支算子之后，把“如

何选中一个分支”推进到“一个分支有多少重数、在所有有限位相乘时偏离主尺度多少，以及这项偏差如何进

入高度不等式”。

证明结构分成四层：纯组合计数；有限素位乘积误差；有限群字符投影与局部表示论的分界；第三步高度不等

式的所有系数。前两层和第四层在本编独立给出完整证明，第三层的字符投影也独立证明，但抛物诱导的

Whittaker 重数精确公式仍作为带名称的外部算术输入保留。这一划分防止将复杂的局部表示论混同于容易的

二项式计算。


BE. 从分块标签到局部重数的二项式上界

定义 BE.1（分块标签与重数系数）
固定整数 r≥1，令 I={0,1,…,r−1}。给出一个分块标签函数 b:I→ℕ；它可以具有重复值，且不要求各个标签对

应的块大小相等。记 A=b(I) 为实际出现的标签集合。对于 j≥0，定义 N_j 为满足 |{i∈I:b(i)∈J}|=j 的标签子集

J⊆A 的个数。该定义与 Lean 的 splitDoublingNBlock b j 一致。

                                    N_j = #{J⊆A : |b⁻¹(J)|=j}.


                                 

---


引理 BE.2（N₀=1 且 Nⱼ≤C(r,j)）
证明：J=∅ 显然对应空原像；反之若 J⊆A 且 b⁻¹(J)=∅，则 J 中任何标签都必须有某个原像而又无原像，矛

盾，所以 J=∅。故 N₀=1。

对固定 j，把所有上述 J 送到 S_J=b⁻¹(J)⊆I。若 S_J=S_K，由于 J,K⊆A，任一标签 z∈J 都有 i∈I 使 b(i)=z；

于是 i∈S_J=S_K，从而 z∈K。反向相同，因此 J=K。故 J↦S_J 是到 I 的 j 元子集集合的单射。此集合大小为

C(r,j)，故 N_j≤C(r,j)。j>r 时右端为零，正好也排除了超出总秩的标签子集。证毕。


定义 BE.3（有限域主项与非零函数 γ）
取整数 q≥2，定义 γ_q(0)=1，γ_q(ℓ)=q^ℓ−q^{ℓ−1}（ℓ≥1）。所有 γ_q(ℓ) 都非负，并且 γ_q(ℓ)≤q^ℓ。令

1≤k≤r≤q，定义：

                              M_k(q,b) = Σ_{j=0}^k N_j γ_q(k−j).

从定义直接分离 j=0 项：

                      M_k(q,b) = (q^k−q^{k−1}) + Σ_{j=1}^k N_j γ_q(k−j).


引理 BE.4（阶乘不等式与组合项逐项上界）
对每个整数 j≥1，有 j!≥2^{j−1}。这是因为 j!=1·2·3·…·j，其中 j−1 个因子均至少为 2；j=1 时等号成

立。又有 C(r,j)j!=r(r−1)…(r−j+1)≤r^j（若 j>r 则左端为零）。于是

                                 C(r,j)·2^{j−1} ≤ r^j. (j≥1)

在 r≤q 及 j≤k 条件下，由 γ_q(k−j)≤q^{k−j} 可得

                     N_j γ_q(k−j) ≤ C(r,j)q^{k−j} ≤ r q^{k−1}·2^{−(j−1)}.

第二个不等式的最后一步使用 r^j≤r q^{j−1}，并且只对 q≥2 这样的正数作除法；所以不存在零分母或负数反

向问题。


定理 BE.5（局部分支重数两侧界：MultPlace）
假设 q≥2，1≤k≤r≤q，N₀=1，0≤N_j≤C(r,j)，γ_q(0)=1，γ_q(ℓ)=q^ℓ−q^{ℓ−1}。那么：

                      q^k(1−1/q) ≤ M_k(q,b) ≤ q^k(1+(2r−1)/q). (BE.5)

证明下界：BE.3 中除 j=0 外的每一项都非负，故 M_k≥q^k−q^{k−1}=q^k(1−1/q)。

证明上界：利用 BE.4 并将有限几何级数放大为完整无穷级数，得

              Σ_{j=1}^k N_j γ_q(k−j) ≤ r q^{k−1}Σ_{i=0}^{k−1}2^{−i} ≤ 2r q^{k−1}.


                               

---


与 j=0 项合并：M_k≤q^k−q^{k−1}+2r q^{k−1}=q^k(1+(2r−1)/q)。至此常数 2r−1 的两个来源完全可见：原主

项的 −1 与其余组合项的 +2r。证毕。

也可采用二项式定理给出另一种校验：Σ_{j=1}^k C(r,j)q^{−j}≤(1+1/q)^r−1≤exp(r/q)−1≤2r/q，因为

0≤r/q≤1 且 exp(t)≤1+2t（0≤t≤1）。后一不等式来自 exp 的凸性和 e−1<2。两条独立证明的常数完全一

致。

【审计说明】BE.5 已经是一般组合命题，但并没有单独证明“自守表示的真实 Whittaker 重数等于

M_k(q,b)”。这个等式是下一节必须准确标出的额外输入。


BF. 跨有限位的乘积逼近：MultProd 的完整证明

引理 BF.1（有限乘积的 Bernoulli 下界）
若 0≤x_i≤1 且指标集有限，则 ∏_i(1−x_i)≥1−Σ_i x_i。对指标数作归纳即可：假设前 n 项乘积 P_n≥1−S_n

且 P_n≥0，则 P_n(1−x)≥(1−S_n)(1−x)=1−(S_n+x)+S_n x≥1−(S_n+x)；这里 S_n x≥0。空积等于 1，故初

始情形成立。


引理 BF.2（小正数的指数上界）
对 0≤t≤1，有 exp(t)≤(1−t)exp(0)+t exp(1)=1+(e−1)t≤1+2t。第一步是凸函数在区间 [0,1] 上低于连接端点

的弦，第二步用 e<3。因而下面的全部上界都不需要把 exp(t) 偷换成其一次 Taylor 近似。


定理 BF.3（全球分支重数的乘积夹逼）
设 V 为有限指标集，|V|=2f，其中 f≥0；给定实数 r≥1、g>0，满足 4fr≤g。对 v∈V 给定 q_v≥g 和非负

n_v，且

                       q_v^k(1−1/q_v) ≤ n_v ≤ q_v^k(1+(2r−1)/q_v).

其中 k≥0 为固定整数。定义主尺度 Q=∏_{v∈V} q_v^k，那么

                      (1−8fr/g)Q ≤ ∏_{v∈V}n_v ≤ (1+8fr/g)Q. (BF.3)

证明：若 V 为空，则 f=0，所有乘积均等于 1，结论直接成立。以下设 V 非空，则 2f=|V|≥1；从 r≥1、g≥4fr

得 g≥2。因此每个 q_v≥2，尤其 0≤1/q_v≤1，且所有 q_v^k 为正。将逐位不等式相乘得到

                     Q∏_v(1−1/q_v) ≤ ∏_v n_v ≤ Q∏_v(1+(2r−1)/q_v).

下界：BF.1 及 q_v≥g 给出

                     ∏_v(1−1/q_v) ≥ 1−Σ_v 1/q_v ≥ 1−2f/g ≥ 1−8fr/g.

最后一次比较只用 r≥1 和 f≥0；该下界在 8fr/g>1 时可能为负，但仍然正确，并未擅自要求 8fr/g<1。
                             

---


上界：利用 1+t≤exp(t)（t≥0）以及 exp 的乘法公式，有

                   ∏_v(1+(2r−1)/q_v) ≤ exp((2r−1)Σ_v1/q_v) ≤ exp(4fr/g).

因为 2r−1≤2r 且 Σ_v1/q_v≤2f/g。又 0≤4fr/g≤1，应用 BF.2 得 exp(4fr/g)≤1+8fr/g。上界亦证毕。


推论 BF.4（把乘积重数转成分支秩的相对误差）
若这些 q_v 分别为一个辅助数域指定的有限余域大小，并且实际表示论重数的乘积分解给出 M=∏_v n_v，则

取 n̄=∏_v q_v^k、δ=8fr/g，BF.3 恰好是

                              (1−δ)n̄ ≤ M ≤ (1+δ)n̄,   δ=8fr/g.

这里 δ 未必小于 1。若后续需要平均斜率传递中更强的 δ≤1/3，则使用另外的尺度假设 g≥24frQ₀、Q₀≥1：

这时 δ=8fr/g≤1/(3Q₀)≤1/3。两处量词和条件不可混淆。V1.5 的 PassageAssembly 正是对后一种强化范围

工作的。


BG. 从 Whittaker 重数到有限位乘积：严格标出外部接口

引理 BG.1（有限群字符投影的迹公式）
设 H 是有限群，ρ:H→GL_ℂ(V) 为有限维复表示，ψ:H→ℂ× 为一维群特征。定义线性算子

                             P_ψ = (1/|H|) Σ_{h∈H} ψ(h)⁻¹ ρ(h).

对每个 g∈H，重新索引 h↦g⁻¹h 得 ρ(g)P_ψ=ψ(g)P_ψ，因此 Im(P_ψ) 包含于 ψ-特征空间

V_ψ={v:ρ(g)v=ψ(g)v，对一切 g}。若 v∈V_ψ，则 P_ψ v=(1/|H|)Σ_hψ(h)⁻¹ψ(h)v=v，故 Im(P_ψ)=V_ψ、

P_ψ²=P_ψ。

由于幂等算子的特征值仅为 0 或 1，且它是沿着 Ker(P_ψ) 到 Im(P_ψ) 的投影，故 Tr(P_ψ)=dim_ℂ V_ψ。利

用迹的线性性：

                      |H| dim_ℂ V_ψ = Σ_{h∈H} Tr(ρ(h)) ψ(h)⁻¹. (BG.1)

这就证明了 Lean 的 card_mul_finrank_eig 所用的有限群正交公式，不需援引任何表示不可约分解或深层自

守形式理论。注意 ψ 需要是群特征，不能把任意复值函数放进公式。


引理 BG.2（局部迹的乘积分解）
若 H=∏_v H_v，每个 H_v 有一维特征 ψ_v，且相应迹函数对局部坐标因子化 Tr ρ(h)=∏_v θ_v(h_v)，则：

              Σ_{h∈H}Trρ(h)·ψ(h)⁻¹ = ∏_v Σ_{h_v∈H_v} θ_v(h_v)·ψ_v(h_v)⁻¹.


                              

---


这只是有限求和的分配律；与 |H|=∏_v|H_v| 和 BG.1 结合可得对应特征空间维数为各个局部整数重数的乘

积。在实际 Lean 上，这就是 levelMult_ofLocal 的核心代数机制。


命题 BG.3（抽象 MultPlace 与真实局部表示论的准确接合）
实际辅助域的局部重数写为 nPos ψ (parInd b σ) ρ k，即抛物诱导表示在特定 unipSym 子群的加性特征本征

空间的复维数。为了应用 BE.5，必须证明精确等式

          nPos ψ (parInd b σ) ρ k = Σ_{j=0}^k splitDoublingNBlock(b,j)·γ_q(k−j). (BG.3)

其假设包括 ψ 非平凡、σ 满足 IsCuspDatum，以及 ρ+k+1≤r。Lean 中此公式名为

symmetricPositionCharMultiplicity_parabolicInduction（经 nPos_parInd），其证明首先在 ρ=0 的情形使

用退化 Whittaker 分解及 Levi 块的 cusp 条件，再利用位置平移的递推式处理 ρ>0。这些是独立的有限群表示

论命题，不是 BE.5 的数学推论。

一旦 (BG.3) 成立，组合界 BE.5 立即给出 PlaceBound；再以 BG.1—BG.2 因子化重数并应用 BF.3，得到

MultSharp，因此 (BG.3) 是这一条分支秩路线从算术表示论到初等不等式的准确切割线。

【审计说明】已在本编证明：BG.1 的字符投影与 BG.2 的有限求和恒等式。尚未独立重构：退化 Whittaker 维

数和抛物诱导 Mackey 分解给出 (BG.3) 的一般定理。当前仍以 Lean 源码为依据，不把 BG.3 冒充新的自然语

言闭合证明。


BH. 第三步高度项的显式吸收：BranchSandwichDiii

定义 BH.1（参数及前提，逐个写出）
令 P 为有限的复嵌入指标集，T⊆P 是顶层位置集合，f≥|P|。设实参数 m≥1、N≥m、0≤k、S≥0、η≥0、

b′≥0、La≥L≥0，CT≥0、Cev≥0，以及日志参数 T₀=logT≥0，满足 T₀≤CT·m·L 与 0≤log(2a)≤2La。

对每个 τ∈P，给出 λ₁(τ)、n_τ、D₀(τ)、D₁(τ)、logc(τ)、logξ(τ)，并假设：

                       n_τ = λ₁(τ)−D₀(τ),   D₀(τ) ≤ S+mη+1_{τ∈T}b_T(τ).

                        D₁(τ)≤3D₀(τ)+S+η,    logc(τ)≤(N−1)D₁(τ)log(2a).

                                   logξ(τ)≤[N(N−1)/2]log(2a).

在顶层 τ∈T，λ₁(τ)=a_T(τ)−(N−k)/2，且 b_T(τ)≤b′；在其他 τ∉T，λ₁(τ)≥S−(N−1)/2。最后，h_P≤−Σ_τ

n_τT₀+Σ_τ(2logc(τ)+logξ(τ))+ev，且 ev≤Cev·fN²La。

这些假设逐条对应 StatementR.lean 的 BranchSandwichDiii；引理的目标不是声称它们自动成立，而是证明

其一旦成立，所有误差的常数确实只需 16+CT+Cev。


---


引理 BH.2（三个统一的基础预算）
由 CT≥0、m≤N、L≤La、m≥1，依次得到

                       0≤T₀≤CT·N·La,       η≤mη,    0≤N−1≤N.

令 B≥0，若 D₀(τ)≤S+mη+B，则：

                         D₁(τ)≤3(S+mη+B)+S+η≤4(S+mη)+3B.

从 logc 的前提与 0≤log(2a)≤2La，逐项乘以非负数，有

                 2logc(τ)≤4N·La·D₁(τ)≤16NLa(S+mη)+12BNLa. (BH.2a)

又由 N≥1 及 logξ 的前提得

                           logξ(τ)≤N(N−1)La≤N²La. (BH.2b)

这两项是全部高度常数的主要来源：16 对应 2logc 中的 4×4；12 对应顶层额外 B 的 4×3。


引理 BH.3（顶层位置的精确主项保留）
若 τ∈T，则 n_τ=a_T(τ)−(N−k)/2−D₀(τ)。由于 k≥0、T₀≥0，结合 BH.2 的 B=b′，得

                     −n_τ T₀ ≤ −a_T(τ)T₀ +(N/2+S+mη+b′)CT·N·La.

再加上 (BH.2a)—(BH.2b)，合并系数：

                                −n_τT₀+2logc(τ)+logξ(τ)

            ≤−a_T(τ)T₀+(CT+12)b′NLa+(CT+16)(S+mη)NLa+(CT/2+1)N²La. (BH.3)

这里没有先对 −a_T(τ)T₀ 取绝对值或粗糙放大；正是保留这一项，最后才能得到含素数主项的有效高度不等

式。


引理 BH.4（非顶层位置不产生顶层主项）
若 τ∉T，结合 λ₁(τ)≥S−(N−1)/2 与 D₀(τ)≤S+mη，得到

                        −n_τT₀=(-λ₁(τ)+D₀(τ))T₀≤((N−1)/2+mη)T₀.

放大 (N−1)/2≤N/2，并使用 T₀≤CT NLa，得到 (CT/2)N²La + CT mη NLa 的上界。使用 BH.2 的 B=0，再得

                                −n_τT₀+2logc(τ)+logξ(τ)

                       ≤(CT+16)(S+mη)NLa+(CT/2+1)N²La. (BH.4)

BH.4 对每个非顶层位置成立，不依赖任何顶层参数 a_T 或 b′，所以求和时不会在 P\T 上错误地重复主项。


                            

---


定理 BH.5（完整高度求和不等式）
在 BH.1 的全部假设下，有

             h_P ≤ −Σ_{τ∈T} a_T(τ)T₀ + (16+CT+Cev)[|T|b′N+f(S+mη)N+fN²]La. (BH.5)

证明：把 BH.3 对 τ∈T 求和，把 BH.4 对 τ∈P\T 求和，所有主项仅在 T 上出现。由于 |P|≤f，且 S+mη、N、

La、CT 均非负，得到

                              h_P ≤ −Σ_T a_TT₀ +(CT+12)|T|b′NLa

                              +(CT+16)f(S+mη)NLa +(CT/2+1)fN²La +ev.

按假设 ev≤Cev fN²La。由 CT,Cev≥0，严格逐项有 CT+12≤16+CT+Cev；

CT+16≤16+CT+Cev；CT/2+1+Cev≤16+CT+Cev。把三个非负预算统一以最大的系数乘，立即得到 (BH.5)。

证毕。


推论 BH.6（Lean 最终第三步的常数 C 与 2b′）
实际 StepDiiiRecord 的顶层误差输入可能以 2b′ 的形式出现。把 BH.5 中的 b′替换成 2b′，并设

C≥2(16+CT+Cev)，那么

                      h_P ≤ −Σ_T a_TT₀ + C[|T|b′N+f(S+mη)N+fN²]La. (BH.6)

理由：括号中所有三项均非负，并且 |T|(2b′)N+f(S+mη)N+fN² ≤2[|T|b′N+f(S+mη)N+fN²]。整个差额的吸收

是单纯实数不等式，不再需要引入额外表示论条件。该结果对应 GlobalBoundRefinements.lean 的

third_descent_inequality。


BI. 逐项验收、有限整数证书与真正剩余的表示论输入

审计 BI.1（精确测试的作用与局限）
附随的 Python 程序 mult_branch_exact_certificate.py 仅使用整数、二项式系数及 fractions.Fraction；它

不作浮点近似。它验证了所有允许局部系数在最小、最大两端时的上下界；随机性也未引入，例子由确定的有

限参数循环产生。全球乘积使用有理数的上下端界；高度项则在一组最紧约束上以有理数计算逐项比较。

测试记录：989 组局部 (q,r,k) 极端系数、300 组全球乘积端点、2112 组高度参数饱和情形，全部通过。有限

检验用于发现符号、指数、常数与索引误写；不能代替前述任意参数的一般证明。


审计 BI.2（已闭合的和未闭合的量词）
-   已独立闭合：BE.2 的 N₀=1、组合单射以及局部二项式界；BE.5 的双侧误差和常数 2r−1；BF.3 的全球乘

    积界和 δ=8fr/g；BG.1 的有限群字符投影；BH.5、BH.6 的分支高度常数。


---


-   已经落实 Lean 的对象对接：局部重数 nPos 到 PlaceBound，经有限特征子空间的迹公式和

    levelMult_ofLocal 到 MultSharp，再经全局分支秩近等引入 V1.5 的均值斜率比较。

-   尚未独立闭合：BG.3 的精确 Whittaker—抛物诱导乘积公式，以及其退化 Whittaker 分解、Levi cusp 数

    据和位置递推；所有本地表示论数据确实来自实际 Theta Lift 构造；核心 Sha/Galois 输入与主算术不等式

    (M)。

-   页数与完成度：新增部分没有改变最终“自然语言证明＜500 页”的上限，也不据此机械上调约 15% 的整

    体粗略进度。只有深层输入完全闭合，才接近最终验收。


BI.3（固定 Lean 提交的源码索引）
组合上界与有限位乘积：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/Numeric.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/Numeric.lean

抽象 MultPlace、MultProd 与高度结论定义：src/Formalism/BranchSandwichDivisors/StatementR.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Formalism/BranchSandwichDivisors/StatementR.lean

真实分块标签计数、γ 及 nPos 定

义：src/Development/AbelianVarietyTheory/Definitions/Divisors/SplitDoublingNBlock.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Development/AbelianVarietyTheory/Definitions/Divisors/SplitDoublingNBlock.lean

有限域 Whittaker 公式后继组合证明：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

SumNumBlockSetsMulGammaTwoSidedBounds.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

SumNumBlockSetsMulGammaTwoSidedBounds.lean

退化 Whittaker / 抛物诱导主等式：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

SymmetricPositionCharMultiplicityParabolicInduct.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

SymmetricPositionCharMultiplicityParabolicInduct.lean

PlaceBound 的实际调

用：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/PlaceBound.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/PlaceBound.lean


---


局部群迹、各位相乘及 MultSharp：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

MultSharpOfPlaceBound.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/MultSharpOfPlaceBound.lean

16+CT+Cev 的第三步高度计算：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/

StepDiii.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/StepDiii.lean

由第三步到最终 C 常

数：src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/GlobalBoundRefinements.lean

https://github.com/CocoSgt/riemann-hypothesis-lean/blob/7cbf7a0c32fca1badf05931879a37c3f8a2b0
3b4/src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/GlobalBoundRefinements.lean

其他阅读校核：Michael O. Rubinstein 等协作的解释性工作稿（2026-11-

21）：https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf 。Taylor Dupuy

编辑的 AI-generated 讲义（2026-11-21）：https://tdupu.github.io/riemann-public/riemann-book.pdf 。

两份材料均可提供路线背景，但都不能替代原始证明；尤其没有完成主不等式 (M) 的全部独立自然语言证明。

下一优先缺口：退化 Whittaker 公式 (BG.3) 的 Mackey 分解证明，以及它所依赖的非退化字符、双陪集分层

和 cuspidality 的准确使用。这是“实际局部重数确实满足已证明的二项式界”最后仍未独立闭合的一块表示

论内核。


BJ. 有限群 Mackey 双陪集的严格维数公式：深入 BG.3 的表示论起点

定义 BJ.1（以等变函数构造诱导表示）
设 G 为有限群，P,H≤G 是子群，σ:P→GLℂ(W) 是有限维复表示，ψ:H→ℂ× 是一维特征。诱导表示

Ind_P^Gσ 可在以下空间上实现：V={f:G→W : f(pg)=σ(p)f(g)，对任意 p∈P,g∈G}。令 G 从右作用：(ρ(h)f)

(g)=f(gh)。该约定与另一种以左平移定义的诱导表示在有限群情形相互等价，但后面的共轭式取向必须按照此

处约定计算。

我们要计算 V 的 ψ-特征子空间 V_ψ={f∈V:f(gh)=ψ(h)f(g)，对所有 g∈G,h∈H}。由于 G 有限，P\G/H 只有有

限个双陪集。对每个代表 x∈G 记 H_x=P∩xHx⁻¹，并设

                             W_x={w∈W : σ(t)w=ψ(x⁻¹tx)w，∀t∈H_x}.


定理 BJ.2（Mackey 双陪集公式，完全独立证明）
在 BJ.1 的假设下，有天然的向量空间同构


---


             V_ψ ≅ ⊕_{x∈P\G/H} W_x,     dimℂ V_ψ = Σ_{x∈P\G/H}dimℂ W_x. (BJ.2)

证明第一步（评价映射）：给定 f∈V_ψ，在每个双陪集代表 x 处取 w_x=f(x)。若 t∈H_x，则 t=xhx⁻¹，其中

h=x⁻¹tx∈H，因此

                           σ(t)w_x=f(tx)=f(xh)=ψ(h)f(x)=ψ(x⁻¹tx)w_x.

故 w_x∈W_x。所有评价组合成线性映射 Φ:V_ψ→⊕_x W_x。

证明第二步（逆向构造）：反之给定一族 w_x∈W_x，对每个 g∈G 选择唯一双陪集代表 x 使 g∈PxH，再任

取分解 g=pxh，定义 f(g)=σ(p)ψ(h)w_x。必须证明结果不依赖分解。若 pxh=p′xh′，则

t=p′⁻¹p=xh′h⁻¹x⁻¹∈H_x。由 w_x∈W_x，

                                    σ(t)w_x=ψ(h′h⁻¹)w_x.

于是 σ(p)ψ(h)w_x=σ(p′)σ(t)ψ(h)w_x=σ(p′)ψ(h′h⁻¹)ψ(h)w_x=σ(p′)ψ(h′)w_x。定义良好。

证明第三步（等变性与互逆）：对 p₀∈P 与 h₀∈H，

                       f(p₀·pxh·h₀)=σ(p₀p)ψ(hh₀)w_x=σ(p₀)ψ(h₀)f(pxh).

因此 f 同时满足左 P 等变与右 H 的 ψ-特征条件，属于 V_ψ。取 g=x 给出 f(x)=w_x；另一方面任意 f∈V_ψ 的

值均由 f(pxh)=σ(p)ψ(h)f(x) 唯一决定。两构造互逆，得到同构和维数公式。证毕。


推论 BJ.3（尖点性消去一个双陪集的充分条件）
保留上述数据。若某个 x 的交群 H_x 内存在子群 U≤H_x，使 ψ(x⁻¹ux)=1（u∈U）并且

W^U={w∈W:σ(u)w=w，∀u∈U}={0}，那么 W_x={0}。因为每个 w∈W_x 在 U 上的特征值均为 1，只能落入

零不变子空间。

这个命题恰好说明尖点性何以在双陪集计算中发挥作用：尖点表示对恰当的抛物根幂子群没有不变向量，因而

相应双陪集无法提供一个 Whittaker 特征向量。注意“尖点性”只有在已定位到正确的 U、并检验 ψ 在 U 上

确实平凡之后才能使用；直接说“尖点 ⇒ 非顶层全部消失”是不充分的。


命题 BJ.4（双陪集分类到块标签系数的尚未闭合桥梁）
将 G 取为 GL_r(F_q)，P 为由非降分块标签 b 定义的 blockTri，H 为一族幺幺根群（unip），ψ 为边上非退化

加性字符。标准 Bruhat 消元将 g 化为 g=p·w·u，其中 w 为置换矩阵，p∈P，u∈H。对指定割点 j，源码

的双陪集分类又分三种情况：

（甲）置换 w 使相邻根上的 b(w(c)) 顺序与 cutEdge 条件一致，且前 j 个位置和其余位置不具有相同块标签。

此时按键 (1_{b(i)∉J},−b(i)) 排序，得到规范代表 w_J，其中 J⊆im(b)、|b⁻¹(J)|=j。每个保留的 J 恰好贡献一

个 Levi Whittaker 维数。


                               

---


（乙）某个相邻根违反上述顺序时，源码构造交群中的非平凡根字符，并使用

coindEigen_eq_bot_of_root_in_unipotent_radical 消去对应双陪集。

（丙）前后两侧存在相同块标签时，源码借助 coindEigen_eq_bot_of_block_cut_cuspidal 和

IsCuspDatum.cusp 消去对应双陪集。

要把这段分类升格为独立证明，需要展开：(1) Bruhat 的规范分解及子群成员资格；(2) 甲的规范代表唯一性

和穷尽性；(3) 乙的根字符正交；(4) 丙的实际 cusp 不变量消去；(5) 各保留代表的交群特征空间与

LeviWhittaker 空间的同构。V1.9 已完整证明 BJ.2 和 BJ.3，但 (1)—(5) 尚以 Lean 的具体结构性引理为依据。

              whCut_ψ(Ind_P^Gσ;j)=N_j·leviWh_ψ(b,σ). (BJ.4，待补具体双陪集分类)

另一个需要单独证明的根交换恒等式为 nPos_ψ(τ,ρ,k)=nPos_ψ(τ,ρ+1,k)（ρ+k+2≤r），将位置 ρ 化到 0；在

ρ=0 时还需 nPos_ψ(τ,0,k)=Σ_{j≤k}γ_q(k−j)whCut_ψ(τ,j)。两式与 (BJ.4) 结合并使用 cuspidal Levi

Whittaker 维数为 1，才真正推出 BG.3。单有 BJ.2 不足以得出 Whittaker 显式公式。


实例 BJ.5（重复块大小下 Nⱼ 不等于二项式系数）
取 r=5，b=(0,0,1,1,2)，实际标签集合为 {0,1,2}，三个标签分别占据 2、2、1 个指标。可逐个列举满足原像大

小 j 的标签子集，得到 (N₀,N₁,N₂,N₃,N₄,N₅)=(1,1,2,2,1,1)。特别是 N₂=2 远小于 C(5,2)=10；不能把组合上界误

写为精确等式。

令 q=7、k=3，则 γ_7(3)=294、γ_7(2)=42、γ_7(1)=6、γ_7(0)=1，实际模型重数为

M₃=294+42+2·6+2·1=350，位于 BE.5 的区间 [294,784] 中。这也检查了 γ_q(0)=1 与主项 q^k−q^{k−1} 的

归一化。


审计 BJ.6（本次比 V1.8 新推进到了哪里）
已经完全独立补上的是一般有限群的双陪集诱导表示公式 BJ.2，以及精确的 cusp 消去充分条件 BJ.3。有限域

GL_r 的具体等式还需要上述 (1)—(5)，但现在每个关键输入都被分离成可以进一步证明的具体问题，而不是笼

统地称为“一次 Mackey 分解”。

Lean 定

位：Development/AbelianVarietyTheory/Proofs/DivisorProofs/DegenerateWhittakerDimParabolicInduc

tionCuspidal.lean 的 exists_pm、sort_mem_iff、exists_set、

degenerateWhittakerDim_parabolicInduction；以及

FinrankEigenCoindMackeyDoubleCosetsStatement.lean、

CoindEigenEqBotOfRootInUnipotentRadicalStatement.lean、

CoindEigenEqBotOfBlockCutCuspidalStatement.lean、


                                

---


CoindEigenSortingPermEqLeviWhittakerStatement.lean。固定提交：

7cbf7a0c32fca1badf05931879a37c3f8a2b03b4。


第十三编：Whittaker 双陪集的两条消去引理（V2.0 新增）
这一编接着 BJ.4 中尚未闭合的（乙）（丙）两类双陪集。以下仅使用有限域 GL_r 的矩阵初等变换、共轭置

换、群特征定义和 IsCuspDatum 给出的尖点不变向量条件；不借用已待证明的全局 Theta Lift 结论。所给结

论与源代码的 eig_eq_bot_of_radical、eig_eq_bot_of_cut 分别同型。


BK. 非平凡根字符对非目标双陪集的消去

引理 BK.1（初等矩阵的精确逆元与共轭）
设 F 是任意域、i≠j 为 r 阶矩阵索引、t∈F。令 E_{ij} 是仅在位置 (i,j) 等于 1 的矩阵单位。因为 i≠j，E_{ij}

²=0；因此

                               (I+tE_{ij})(I−tE_{ij})=I−t²E_{ij}²=I.

故 u_{ij}(t)=I+tE_{ij} 总在 GL_r(F) 内，其逆为 u_{ij}(−t)。若 w∈S_r 是一个置换，P_w 为对应置换矩阵（P_w

e_a=e_{w(a)}），则

                         P_w⁻¹u_{w(a),w(c)}(t)P_w=u_{a,c}(t). (BK.1)

证明：对各个矩阵单位逐项计算，(P_w⁻¹ E_{w(a),w(c)}P_w)_{ij}=(E_{w(a),w(c)})_{w(i),w(j)}，只有

(i,j)=(a,c) 非零。线性性和 P_w⁻¹IP_w=I 给出结论。


定理 BK.2（Root in unipotent radical ⇒ 特征空间为零）
令 b:{0,…,r−1}→ℕ 为块标签函数，P=blockTri(b)，σ:P→GLℂ(W) 满足 IsCuspDatum.infl：凡 p∈P 且所有同

块矩阵元与单位阵一致，均有 σ(p)=id。令 ψ:(F,+)→ℂ× 非平凡。令 H 为上三角幺幺群，用 cutEdge(j) 选取除

跨割点 j 之外的相邻上三角矩阵元，并定义 χ(h)=ψ(edgeSum_cut(h))。

假设存在 a,c 满足 c=a+1、c≠j，以及 b(w(a))<b(w(c))。设 x=P_w。则 Mackey 双陪集交群上的 χ-特征向量

空间为零：

                   W_x={v∈W: σ(p)v=χ(x⁻¹px)v，∀p∈P∩xHx⁻¹}={0}. (BK.2)

证明第一步（取一个真正非平凡的字符值）：ψ 非平凡意味着存在 t∈F 使 ψ(t)≠1。令 i=w(a)、k=w(c)；因为

w 为置换，i≠k。构造 g=I+tE_{i,k}。

第二步（同时具有两个互相冲突的性质）：b(i)<b(k)，所以 g 的唯一非对角非零项位于 P 允许的块三角位置，

g∈P。此外 g 在任意同块指标对 (s,t)（b(s)=b(t)）处等于单位阵，因此 IsCuspDatum.infl 强制 σ(g)=id。


---


第三步（共轭处恰被 cutEdge 捕捉）：由 BK.1，x⁻¹gx=I+tE_{a,c}。因为 c=a+1 且 c≠j，(a,c) 处的非零元属

于选定的 cutEdge(j)，并且 x⁻¹gx 的其他上三角项都为零，所以 x⁻¹gx∈H，且 edgeSum_cut(x⁻¹gx)=t。故

g∈P∩xHx⁻¹、χ(x⁻¹gx)=ψ(t)≠1。

最后取任意 v∈W_x。其特征条件给出 σ(g)v=ψ(t)v，而左侧又因 σ(g)=id 等于 v。因此 (1−ψ(t))v=0。由于 ℂ 是

域且 ψ(t)≠1，必有 v=0。证毕。

该证明精确使用两个条件：不等式 b(w(a))<b(w(c)) 使 g 在 P 中却被 σ 平凡化；cutEdge 的非割点条件 c≠j 确

保 g 的共轭在特征中产生非 1 因子。若缺少其中任何一个，结论均不能直接推出。


BL. 跨分块割点的同标签项由尖点性消去

定义 BL.1（跨割点的同块根子群）
固定割点 j 与置换 w，设 S=w({0,…,j−1})。在块三角群 P 中考虑子群 U_S，元素 u 的所有非对角非单位矩阵元

只能出现在 (s,t) 满足 s∈S、t∉S、b(s)=b(t) 的位置。由于这些矩阵元都由 S 行指向补集列，矩阵单位的乘积

E_{s,t}E_{s′,t′} 不能同时落在同类型位置；所以这些允许的非对角块组成平方为零的理想，U_S 的确是一个幺

幺子群。


引理 BL.2（跨割点根群上的 cutEdge 字符恒等于 1）
设 x=P_w，u∈U_S。共轭 x⁻¹ux 具有非对角支持仅在位置 (a,c) 满足 a<j≤c。由 a<j≤c 可知 c>a，所以 x⁻¹ux

是上三角且所有对角元为 1；因而 x⁻¹ux∈H。

另一方面，cutEdge(j) 要求 c=a+1 且 c≠j。若一个非零元满足 a<j≤c 且 c=a+1，则只能有 a=j−1、c=j，这恰

好被条件 c≠j 排除。因此没有一个非零元会被 cutEdge(j) 统计：

                     edgeSum_cut(x⁻¹ux)=0， χ(x⁻¹ux)=ψ(0)=1. (BL.2)

注意这是纯粹的支持集与相邻边关系，不依赖指数估计、余域大小，也不要求实际加性字符有特别的阶。


定理 BL.3（Block cut cuspidal ⇒ 特征空间为零）
假设 IsCuspDatum.cusp 的具体条件成立：若某个 S⊆{0,…,r−1} 切开至少一个相同的 b-标签，即存在 i∈S、

k∉S 且 b(i)=b(k)，则每个在 U_S 下固定的向量必为零。

设存在 a,c 使 a<j≤c 且 b(w(a))=b(w(c))。则 i=w(a)∈S、k=w(c)∉S 且 b(i)=b(k)，故这个 S 满足 cusp 条件。

由 BJ.1 令 W_x 为诱导表示在交群 P∩xHx⁻¹ 上的 χ-特征空间。

任取 v∈W_x 与 u∈U_S。BL.2 给出 u∈P∩xHx⁻¹、χ(x⁻¹ux)=1，从而 σ(u)v=χ(x⁻¹ux)v=v。因此 v 在整个 U_S

下不变。由 IsCuspDatum.cusp 条件，v=0。于是 W_x={0}。证毕。


                             

---


这条证明的逻辑顺序非常重要：并不是凭“尖点表示”这四个字直接丢弃任意双陪集，而是先具体构造割点

S，再证明 χ 在 U_S 上平凡，最后才应用针对这个 S 的 cusp 条件。


BM. 这两项怎样改变局部 Whittaker 公式的真实剩余量
结合 BJ.2 与 BK.2、BL.3，Mackey 双陪集求和中，凡某置换具有（乙）某条非割点相邻根的块标签上升，或

者（丙）割点两侧存在共同块标签，其贡献均严格为 0。故剩余项只能来自既满足非割点相邻块标签非增、又

没有割点跨侧同块标签的置换。

源码接下来使用 Bruhat 分解和按块标签排序的规范代表，把这些幸存双陪集同集合 J⊆im(b)、|b⁻¹(J)|=j 一一

对应，并利用同块 Levi 投影证明每个幸存项的维数等于 leviWh；最后通过 cusp 条件把此值规范为 1。这些后

续具体命题仍需进一步独立展开。

                已闭合：Mackey 抽象公式 + 非平凡根字符消去 + 尖点性跨割点消去。

                  仍未闭合：幸存双陪集规范分类 + Levi 特征空间等价 + 位置递推。

固定源码：src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/

CoindEigenEqBotOfRootInUnipotentRadical.lean 中的 exists_elem、eig_eq_bot_of_radical；

CoindEigenEqBotOfBlockCutCuspidal.lean 中的 eig_eq_bot_of_cut；

DegenerateWhittakerDimParabolicInductionCuspidal.lean 中的 exists_pm、exists_set 与

degenerateWhittakerDim_parabolicInduction。上述推导只处理局部表示论的精确子问题；全局 Theta

Lift、积分核、Sha 上界及 (M) 仍未完成自然语言闭合。


第十四编：幸存 Whittaker 双陪集与分块子集的规范对应（V2.1 新增）
在前一编，所有“根字符非平凡”与“跨割点同标签”的双陪集已经被独立消去。因此剩下的主要问题是一类

有限排列组合：未被消去的置换是否恰好由 splitDoublingNBlock 所计数的标签子集表示。本编完整处理组合

分类和代表的互异性，仍将 Bruhat 分解作为传统的已知标准矩阵分解定理。


BN. 允许置换的结构与排序分类

定义 BN.1（幸存置换）
令 b:{0,…,r−1}→ℕ 非降，j∈{0,…,r}，w 是 {0,…,r−1} 的置换。称 w 在割点 j 处允许，如果 (i) 对所有相邻位置

a,c=a+1，只要 c≠j，便有 b(w(c))≤b(w(a))；(ii) 对所有 a<j≤c，都有 b(w(a))≠b(w(c))。

条件 (i) 说明序列 b(w(0)),…,b(w(r−1)) 在前 j 项和后 r−j 项中分别非增；条件 (ii) 则说明每种标签不可能同时出

现在两个部分。这正好是 BK.2、BL.3 消去之后保留下来的两类局部限制。


                                

---


引理 BN.2（被割点隔开的标签集合）
对允许置换 w，令 J_w={b(w(a)):0≤a<j}。因为 w 为双射，每个标签 z 在 w 的排列中出现的次数恰好等于原

始 b⁻¹(z) 的大小。若 z∈J_w，条件 (ii) 排除了在后 r−j 项再次出现 z，所以 b⁻¹(J_w) 恰好由 w(0),…,w(j−1) 组

成。因此

                          J_w ⊆ im(b), |b⁻¹(J_w)|=j. (BN.2)

特别地，当 j=0 时 J_w=∅；当 j=r 时 J_w=im(b)。故边界情形无须删去，也与 N₀=1 的定义保持一致。


引理 BN.3（有序多重集合的唯一性）
设 A=(a₁,…,a_s)、B=(b₁,…,b_s) 为两个非增的整数序列，且每个整数值在两序列中出现次数相同，则 A=B。

证明可归纳于 s：由于最大值及其重数由多重集合决定，a₁=b₁ 等于共同最大值；删掉首项后仍具有相同多重

集合且仍非增，应用归纳假设。空序列情况平凡。


定理 BN.4（每个幸存排列归约到规范排序代表）
设 J⊆im(b)，|b⁻¹(J)|=j。定义规范置换 w_J：先将 b 值属于 J 的所有索引放在前 j 位，按照 b 值从大到小排

序；再将其他索引放在后 r−j 位，同样按照 b 值从大到小排序。遇到相同 b 值时按照原索引从小到大排序，以

得到真正唯一的置换。

这一定义使用的排序键与源代码 key b J i=(1_{b(i)∉J},−b(i)) 同型；最后的原索引顺序只是确定并列项的规范

代表。

若 w 为任一允许置换，取 J=J_w。BN.2 保证 w 的前 j 位恰好包含 b⁻¹(J) 的所有元素，后段恰好包含剩余元

素；BN.1 保证两段的 b 值分别非增。w_J 也具有相同的两段多重集合，且按定义非增。对每段应用 BN.3，得

到

                       b(w(a))=b(w_J(a))，对所有 0≤a<r. (BN.4)

令 p=w·w_J⁻¹，视作置换矩阵。由 BN.4，对每个列 c，p 把基向量 e_{w_J(c)} 送到 e_{w(c)}，且这些行、

列具有同一 b 标签；因此 p 是按 b 的同标签子空间作块置换的矩阵，属于 blockTri(b)。于是

x_w=p·x_{w_J}，故 x_w 与 x_{w_J} 属于同一个 P—U 双陪集。证毕。


引理 BN.5（不同标签子集产生不同双陪集）
假设 p∈blockTri(b)、u∈U（上三角幺幺群），而两个置换矩阵满足 pP_w=P_{w′}u。则 u=P_{w′}⁻¹pP_w，

逐矩阵元素计算 u_{cc}=p_{w′(c),w(c)}。由于 u_{cc}=1，此 p 元素非零。blockTri 的定义立即推出 b(w′

(c))≤b(w(c))：若反过来 b(w(c))<b(w′(c))，这个元素必须等于零。

把逐项不等式在 c 上求和。由于 w 与 w′ 都是置换，Σ_c b(w′(c))=Σ_i b(i)=Σ_c b(w(c))。在每项均满足 ≤、总

和相等的有限序列中，每项必然相等。因此


---


                           b(w′(c))=b(w(c))，对所有 c. (BN.5)

若 w=w_J、w′=w_K 均为规范代表，前 j 个位置出现的标签集合分别是 J、K。由 BN.5，两者前 j 个 b 值逐项

相等，故 J=K。于是 J↦P x_{w_J}U 是单射。BN.4 已经证明它对允许双陪集满射，所以它恰好一一对应所有

幸存双陪集。证毕。


推论 BN.6（局部重数公式中的 Nⱼ 确实来自双陪集）
在已接受 GL_r(F_q) 的标准 Bruhat 双陪集分解 G=⋃_{w∈S_r}P·x_w·U 的条件下，BN.4—BN.5 给出：

BK.2、BL.3 消去所有不允许代表后，剩下的双陪集总数等于

                  # {J⊆im(b): |b⁻¹(J)|=j}=splitDoublingNBlock(b,j)=N_j.

这不是一个“粗略不超过 C(r,j)”的结论，而是一个精确的分类结论；它说明 BE.2 的组合对象为什么恰好会出

现在有限群的退化 Whittaker 公式里。


BO. 仍需完成的 Levi 同构与最终乘积公式

引理 BO.1（Levi 同块投影的代数机制）
对于块三角矩阵 p∈P，定义 L(p) 为保留 b(i)=b(k) 的矩阵元、把跨块矩阵元全部设零的矩阵。由于 p 及 p⁻¹ 都

块三角，逐项展开矩阵乘法可知 L(pq)=L(p)L(q)、L(p)L(p⁻¹)=I。这说明 L(p) 可逆且 L:P→P 是群同态。

又因为 p⁻¹L(p) 的所有同块矩阵元均与单位阵一致，IsCuspDatum.infl 给出 σ(p⁻¹L(p))=id，进而

σ(p)=σ(L(p))。因此对当前 cuspidal 模而言，P 的作用只依赖于其 Levi（同块对角）部分，不依赖于被放弃的

跨块根群。


命题 BO.2（幸存交群表示须与 Levi Whittaker 模同构）
规范排列 w_J 同时具备如下性质：同一 b 标签内的原索引次序被保留；该标签所有元素处在割点的同一侧；

每侧的 b 标签按规定顺序排列。由此，在同块矩阵元上，原始块内相邻边 blkEdge(b) 与经 w_J 共轭后的

cutEdge(j) 恰好对应。跨块的矩阵元在 Levi 投影中为零。

因而可预计，Mackey 交群内的 ψ-特征子空间 W_{w_J}，等于 σ 在块内幺幺子群上对相应 Whittaker 字符的

特征空间。这就是代码 eig_conj_eq_leviWh 的结论。上一段的群同态 L 已证明，但为使此等式成为完整独立

证明，还必须把两种根群的正反包含及对应字符的逐项相等写全；目前先保留为具体明确的待补小引理。

若该 Levi 空间等价成立，则每个幸存双陪集贡献相同维数 leviWh(ψ,b,σ)，配合 BN.6 与 BJ.2 得

                     whCut(ψ, parInd(b,σ), j)=N_j · leviWh(ψ,b,σ).


                            

---


最后，若使用有限域 GL 各 Levi 块上不可约尖点表示的标准 Whittaker 唯一性及存在性（本仓库的

leviWh_eq_one），得到 leviWh=1。该有限域表示论定理并非这两页组合分类的推论，不应被写成“显

然”。


BP. 精确进度界面（不掩盖仍存的困难）
截至 V2.1，BG.3 的四类前提中：Mackey 双陪集维数公式已独立闭合；根字符和尖点性双消去已独立闭合；

幸存代表与标签子集的精确一一对应已独立闭合（使用标准 Bruhat 分解）。尚未完整独立闭合的是 Levi 交群

的正反包含和字符对应、leviWh=1 的表示论证明，以及从 whCut 到 nPos 的 mirabolic 递推与对称位置根交

换。

主算术不等式 (M) 的整体 Theta Lift、内积公式、积分模型、Galois/Sha 输入也仍未闭合；本轮推进主要减少

了 (M) 上游“有限域重数和一般位置”路线中的可疑引用，而非完成了 RH 证明。

源代码定位：DegenerateWhittakerDimParabolicInductionCuspidal.lean 的 key、sort_mem_iff、

exists_set、blk_eq_of_rel 及最后 degenerateWhittakerDim_parabolicInduction；

CoindEigenSortingPermEqLeviWhittaker.lean 的 bd、sigma_levi、edge_iff、eig_conj_eq_leviWh。


第十五编：Levi–Whittaker 特征空间的严格双向识别（V2.2 新增）
上一编 BO.2 明确标出尚待完成的“Levi 交群的双向包含和字符一致”问题。本编不依赖预设的半单分解，也

不把 LeviWh=1 当作组合恒等式的结果，而是单独证明等式 eig_conj_eq_leviWh。为避免偷换对象，以下始

终把两个特征子空间看作同一个 P-表示 V 的子空间，然后以元素条件逐项证明其集合相等。


BQ. 分块矩阵与 Levi 投影

定义 BQ.1（矩阵群、标签及同块投影）
令 F 为域，b:{0,…,r−1}→ℕ 为非降函数；P={p∈GLᵣ(F): b(k)<b(i) ⇒ pᵢₖ=0} 是按 b 分块的上三角抛物子群。定

义 L(p)ᵢₖ=pᵢₖ（当 b(i)=b(k)），其余置零。后者正是原矩阵的块对角部分，注意同一块内部允许有上下三角任

意矩阵元。


引理 BQ.2（同块投影尊重乘法且保逆）
设 p,q∈P。先比较 (L(pq))ᵢₖ 和 (L(p)L(q))ᵢₖ。若 b(i)≠b(k)，前者按定义为零；后者每一项 L(p)ᵢₕL(q)ₕₖ 若非

零，则必须同时满足 b(i)=b(h)=b(k)，矛盾，因此也为零。


                               

---


若 b(i)=b(k)，将 (pq)ᵢₖ=Σₕ pᵢₕqₕₖ 按 h 的标签分类。当 b(h)<b(i) 时由 p∈P 得 pᵢₕ=0；当 b(h)>b(i)=b(k) 时由

q∈P 得 qₕₖ=0。故仅有 b(h)=b(i) 的项可能存在，这正是 L(p)L(q) 的求和。因此 L(pq)=L(p)L(q)。同理

L(I)=I，于是 L(p)L(p⁻¹)=I=L(p⁻¹)L(p)：L(p) 可逆且 L(p)⁻¹=L(p⁻¹)。

                              L(pq)=L(p)L(q),   L(p⁻¹)=L(p)⁻¹. (BQ.2)


引理 BQ.3（尖点数据的 inflation 条件使 σ 通过 L 分解）
取 P 在复向量空间 V 上的表示 σ，假设 IsCuspDatum.infl：若 p∈P 的每个同块矩阵元均等于单位矩阵的相应

项，则 σ(p)=id。对任意 p∈P，利用 BQ.2 得 L(p⁻¹L(p))=L(p)⁻¹L(L(p))=I，其中 L(L(p))=L(p)。故 p⁻¹L(p) 符合

inflation 条件。

从而 σ(p⁻¹L(p))=id，而 σ(p⁻¹L(p))=σ(p)⁻¹σ(L(p))，所以 σ(p)=σ(L(p))。这是由明示的 inflation 假设推导出的

结论；若没有该假设，单凭 σ 是 P 表示不能断言它忽略非对角分块。

                                  ∀p∈P, σ(p)=σ(L(p)). (BQ.3)


BR. 规范置换保留的根边结构

定义 BR.1（两套需要比较的边集）
沿用 BN：j 为割点，J 是完整标签子集，w=w_J 先把 J 中的全部块放在前 j 位，再把其他块放在后 r−j 位；每

部分按标签从大到小，同标签索引保持自然递增。令 x=P_w 为相应置换矩阵。定义

E_blk={(i,i+1):b(i)=b(i+1)}，E_cut={(a,a+1):a+1≠j}。对矩阵 p，记 S_blk(p)=Σ_{(i,k)∈E_blk}pᵢₖ，

S_cut(p)=Σ_{(a,c)∈E_cut}p_{w(a),w(c)}。


引理 BR.2（同标签的前后关系与区间凸性）
若 b(w(a))=b(w(c)) 且 a<c，则 w(a)<w(c)，因为同标签元素被按原索引升序排列。反过来，在同标签的两个

原索引 i<k 之间，任一原索引 h 满足 i<h<k 时，由 b 非降可得 b(i)≤b(h)≤b(k)，从而 b(h)=b(i)。由于这一标

签在 w 序列中完整地占据割点一侧的一段，h 也恰落在 w⁻¹(i) 与 w⁻¹(k) 之间。

特别地，设 a<c 且 b(w(a))=b(w(c))。那么 w(a) 与 w(c) 是相邻原索引，当且仅当 a,c 为相邻位置；并且后一种

相邻不可能跨越割点 j，因为同一标签不能占据两侧。此论证对 r=1 和 j=0、j=r 亦成立，条件中的“无交叉同

标签”此时分别是平凡或自动满足。


定理 BR.3（精确的相邻边等价）
对任意 a,c，额外假设 b(w(a))=b(w(c))，便有

                             (w(c)=w(a)+1) ⇔ (c=a+1 且 c≠j). (BR.3)


---


证明左推右：由同标签升序知 a<c。若 c≥a+2，取 e=a+1，BR.2 告诉我们 w(e) 是严格位于 w(a) 和 w(c) 之间

的同标签原索引，和 w(c)=w(a)+1 矛盾。故 c=a+1；同标签不可横跨割点，故 c≠j。证明右推左：由同标签升

序知 w(a)<w(c)。若 w(c)≥w(a)+2，取原索引 i=w(a)+1，则 b(i)=b(w(a))，其在 w 的位置必须严格位于 a 与 c

之间，违反 c=a+1。证毕。


定理 BR.4（字符边和恒等式）
对于任意 p∈P，逐对比较 S_cut 与 S_blk 的求和项。通过 w 的双射可将 S_blk 改写为 Σ_{a,c}

1_{E_blk(w(a),w(c))}p_{w(a),w(c)}。若 b(w(a))=b(w(c))，BR.3 证明两边的边判别函数恰相同。

若 b(w(a))≠b(w(c))，E_blk 项为零。右边仅可能在 c=a+1≠j 时出现；但规范排序在割点内部让

b(w(c))≤b(w(a))，结合标签不相等得到 b(w(c))<b(w(a))。由于 p 属于 P，这一位置的矩阵元 p_{w(a),w(c)}

=0，因此 S_cut 也没有贡献。所有矩阵元逐项一致，故

                         S_cut(p)=S_blk(p),   对每个 p∈P. (BR.4)


这是未经任何空间维数比较的有限求和恒等式；其严格成立依赖于 w 的同标签稳定排序及 p 的块三角零元条

件，不能推广到任意置换或任意 GL 矩阵。


BS. 两个群交集的正反 Levi 转移

定义 BS.1（待比较的两个特征空间）
令 U⊂GLᵣ(F) 为全部上幺幺矩阵，H_x={p∈P:x⁻¹px∈U}，H_0=P∩U。设 ψ:(F,+)→ℂ× 是任意加性字符，在

H_x 上定义 χ_x(p)=ψ(S_cut(p))，在 H_0 上定义 χ_0(p)=ψ(S_blk(p))。再令

W_x={v∈V:∀p∈H_x,σ(p)v=χ_x(p)v}，W_0={v∈V:∀p∈H_0,σ(p)v=χ_0(p)v}。


引理 BS.2（从 H₀ 到 Hₓ）
设 p∈H_0。其 L(p) 的非对角元仅在同一个 b 块内；由于 p∈U，同块矩阵元在原索引顺序上没有下三角项。

规范置换 w 严格保持每个块内的原索引次序，故 (x⁻¹L(p)x)_{ac}=L(p)_{w(a),w(c)} 在 a>c 时为零。每个对角

项为 1，因此 x⁻¹L(p)x∈U。故 L(p)∈H_x。


引理 BS.3（从 Hₓ 到 H₀）
设 p∈H_x。若 b(i)≠b(k)，则 L(p)ᵢₖ=0；若 b(i)=b(k) 且 i>k，写 i=w(a)、k=w(c)。同标签保持原始顺序，所

以 i>k 蕴含 a>c。由 x⁻¹px∈U，pᵢₖ=(x⁻¹px)_{ac}=0。又 L(p) 的对角均为 1，于是 L(p)∈U，即 L(p)∈H_0。注

意这里不需要 p 本身为普通上三角；它只有在同块投影后才被证明落入 H_0。


                             

---


定理 BS.4（Levi–Whittaker 子空间作为集合完全相等）
先证明 W_x⊆W_0。给定 v∈W_x、p∈H_0，由 BQ.3 有 σ(p)v=σ(L(p))v；由 BS.2 有 L(p)∈H_x，故右侧等于

ψ(S_cut(L(p)))v。BR.4 将其化为 ψ(S_blk(L(p)))v，而 L(p) 保留所有同块相邻边，所以

S_blk(L(p))=S_blk(p)。因此 σ(p)v=χ_0(p)v。由于 p 任意，v∈W_0。

反过来证明 W_0⊆W_x。给定 v∈W_0、p∈H_x，由 BQ.3 有 σ(p)v=σ(L(p))v；由 BS.3 有 L(p)∈H_0，故右

侧等于 ψ(S_blk(L(p)))v=ψ(S_blk(p))v。再用 BR.4，将其变成 ψ(S_cut(p))v=χ_x(p)v，因此 v∈W_x。

                  W_x=W_0,    dimℂ W_x=dimℂ W_0=leviWh(ψ,b,σ). (BS.4)


两方向完全对称但转移的子群不一样：第一个方向使用 L(H_0)⊆H_x，第二个方向使用 L(H_x)⊆H_0。这也闭

合了 V2.1 中 BO.2 保留的具体技术缺口，准确对应 Lean 定理 eig_conj_eq_leviWh。


BT. 与局部重数计数的正式闭合点
由 V1.9 的 Mackey 特征空间维数直和公式、V2.0 的两类“必为零”消去、V2.1 的允许双陪集与标签子集的一

一对应，以及 BS.4 对每个幸存双陪集贡献的识别，严格推出

                     whCut(ψ, parInd(b,σ),j)=Nⱼ · leviWh(ψ,b,σ). (BT.1)


这里 Nⱼ=#{J⊆im(b): |b⁻¹(J)|=j}，使用了标准有限域 GL 的 Bruhat 分解。BT.1 的本地表示论证明链已经可以用

通常数学定理逐项核查；但将 leviWh=1 写入右端仍需要有限群 Gelfand–Graev/Whittaker 存在与唯一性证

明，不能因为 BT.1 闭合就声称完整局部重数定理已无任何输入。


第十六编：根交换的无黑箱维数比较（V2.2 新增）
位置递推 nPos(ρ,k)=nPos(ρ+1,k) 并不要求任意两个特征子群彼此包含。本编先从零证明适用于有限群的“交

错共轭分离”维数比较，再将两个具体矩阵子群代入并给出构造性初等矩阵见证。这样避免把一句“由 root

exchange”当作空洞黑箱。


BU. 有限群字符投影的单射引理

定理 BU.1（交错共轭分离引理）
设 G 为有限群，A,B≤G，τ:G→GL(V) 是有限维复表示。设函数 χ:G→ℂ 在 A、B 上分别为乘法特征，χ(1)=1。

记 V_A={v:τ(a)v=χ(a)v，∀a∈A}，V_B 类似。假设对于每个 b∈B\A，存在 a∈A，使 b⁻¹ab∈A 且

χ(b⁻¹ab)≠χ(a)。则 dim V_A≤dim V_B。


                              

---


证明第一步（特征投影）。对有限子群 H=A 或 B，令 Q_H=Σ_{h∈H}χ(h)⁻¹τ(h)。因为 χ 在 H 上是特征，

χ(h)≠0；指标平移表明 Q_H(V)⊆V_H，并且当 v∈V_H 时 Q_Hv=|H|v。因此把 Q_B 限制到 V_A 并把陪域取

为 V_B，得到一个线性映射 T:V_A→V_B。只须证明它单射。

第二步（交叠项）。设 v∈V_A 且 T(v)=Q_Bv=0。在恒等式 0=Q_AQ_Bv=Σ_{b∈B}χ(b)⁻¹Q_Aτ(b)v 中考虑

b∈A∩B。由于 τ(b)v=χ(b)v，且 Q_Av=|A|v，该项恰为 |A|v。

第三步（非交叠项消失）。设 b∈B\A，取假设所给 a∈A，a′=b⁻¹ab∈A。令 z=Q_Aτ(b)v。因

Q_Aτ(a)=χ(a)Q_A，得到 τ(a)z=χ(a)z；另一方面 τ(a)τ(b)v=τ(b)τ(a′)v=χ(a′)τ(b)v，施加 Q_A 得 τ(a)z=χ(a′)z。

两特征值不等，故 z=0。因此此 b 对 Q_AQ_Bv 的贡献为零。

第四步（单射）。综上 0=|A|·|A∩B|·v。两个有限群基数均为正整数，在 ℂ 中非零，故 v=0。于是 T 单射，

dim V_A≤dim V_B。完全不需要 A⊆B，也不需要 τ 不可约，更不需要存在一个预先给定的半单最高权直和。

证毕。

            ∀b∈B\A, ∃a∈A: b⁻¹ab∈A 且 χ(b⁻¹ab)≠χ(a) ⇒ dim V_A≤dim V_B. (BU.1)


BV. 位置根交换中的两个显式幺幺子群

定义 BV.1（A、B 与唯一需要交换的根）
设 F 为有限域、0≤ρ、1≤k、ρ+k+2≤r。记 U 为 GLᵣ(F) 的上幺幺群，c=ρ+k+1。置

                  A={g∈U:g_{ρ,j}=0，ρ<j<c}; B={g∈U:g_{j,c}=0，ρ<j<c}. (BV.1)


源码的 cyc(ρ,k) 是把索引区间 ρ,…,ρ+k 向左循环一格的置换：π(ρ)=ρ+1，…，π(ρ+k−1)=ρ+k，π(ρ+k)=ρ，

区间外不动。将矩阵行列同时按 π 重排后，U_sym(ρ,k) 的上幺幺条件与被禁矩阵元条件恰好变为 A 的两个条

件。因而原来的 V_{ρ,k} 与 V_A 由表示 τ(P_π) 给出线性同构。

更精确地，令 S_{α,h}(g)=Σ_{(i,j)∈symEdge(α,h)}gᵢⱼ。根据 symEdge 的明确定义，它包含所有相邻边，但排

除进入 α 和 α+h 的两条边，并将其替换为特殊边 (α−1,α+h)。逐项代入 π 的四段索引公式可验证 S_{ρ,k}

(π⁻¹gπ)=S_{ρ+1,k}(g)；这里不需要 τ 的具体矩阵元，只是边集的双射重命名。

                       χ(g)=ψ(S_{ρ+1,k}(g)),   dim V_{ρ,k}=dim V_A. (BV.2)


引理 BV.3（χ 在 A、B 上均为群特征）
在 U 中，相邻上对角元满足 (xy)_{i,i+1}=x_{i,i+1}+y_{i,i+1}，因为所有中间指标 j 的乘积项只可能来自 j=i 或

j=i+1。特殊根 (ρ,c) 的矩阵元满足 (xy)_{ρ,c}=x_{ρ,c}+y_{ρ,c}+Σ_{ρ<j<c}x_{ρ,j}y_{j,c}。

若 x,y∈A，则每个 x_{ρ,j}=0；若 x,y∈B，则每个 y_{j,c}=0。故两种情况下交叉项均为 0。S_{ρ+1,k}

(xy)=S_{ρ+1,k}(x)+S_{ρ+1,k}(y)，于是 χ(xy)=χ(x)χ(y)。且 χ(I)=1。这正是 BU.1 所需的字符条件。


---


引理 BV.4（共轭初等矩阵的精确展开）
令 E_{pq} 为标准矩阵单位（p≠q），T_{pq}(s)=I+sE_{pq}。任取上幺幺 g，有

                      (g⁻¹ T_{pq}(s) g)_{iℓ}=δ_{iℓ}+(g⁻¹)_{ip}·s·g_{qℓ}. (BV.4)


这是由 g⁻¹(I+sE_{pq})g=I+s(g⁻¹e_p)(e_qᵀg) 直接得出的秩一恒等式。由于 g 与 g⁻¹ 都上三角，i>p 时

(g⁻¹)_{ip}=0，ℓ<q 时 g_{qℓ}=0。这两个零元条件足以处理后面所有被禁行、被禁列及普通相邻边，不需要复

杂的非交换群展开。


BW. 两个方向分别构造分离见证

引理 BW.1（从 B\A 到 A 的见证）
取 b∈B\A。因为 A 是子群，b⁻¹∈B\A；因此存在 ρ<j<c 使 d=(b⁻¹)_{ρ,j}≠0。由 ψ 非平凡取 t∈F 使 ψ(t)≠1，

设 s=t/d，并令 a=T_{j,c}(s)。注意 p=j、q=c；这是正确的指标，不能误写成 T_{ρ,j}。

矩阵 a∈A，因为 a 在第 ρ 行的禁用列无非对角元。由 BV.4，对任意 ρ<ℓ<c，(b⁻¹ab)_{ρ,ℓ}=δ_{ρℓ}

+d·s·b_{c,ℓ}=0，原因是 b 上三角且 ℓ<c。其余上幺幺条件由共轭仍属于 U 保证，故 b⁻¹ab∈A。

比较字符：对 a，特殊边 (ρ,c) 的值为零，而普通相邻边 (j,c) 即使相邻，也因终点 c 被 symEdge 排除，故

χ(a)=1。对 b⁻¹ab，由 BV.4，(ρ,c) 元等于 d·s·b_{c,c}=t。其余 symEdge 普通相邻边的增量都为零：终点

ℓ<c 时 b_{c,ℓ}=0，终点 ℓ>c 时对应行 i=ℓ−1≥c>j，使 (b⁻¹)_{i,j}=0；终点 ℓ=c 是排除边。因此

χ(b⁻¹ab)=ψ(t)≠1=χ(a)。


引理 BW.2（从 A\B 到 B 的见证）
取 b∈A\B，则存在 ρ<j<c 使 e=b_{j,c}≠0。仍取 ψ(t)≠1，设 s=t/e，令 a=T_{ρ,j}(s)；这次 p=ρ、q=j，恰好

与上一引理互换。显然 a∈B，因为其禁用列 c 上没有第 ρ+1,…,c−1 行的项。

对任意 ρ<i<c，由 BV.4，(b⁻¹ab)_{i,c}=δ_{ic}+(b⁻¹)_{i,ρ}·s·e=0，因为 i>ρ、b⁻¹ 上三角。因此 b⁻¹ab∈B。

对字符，a 的唯一非零上对角元在 (ρ,j)，若 j=ρ+1，普通边因终点 ρ+1 被排除，若 j>ρ+1 则它并非相邻边，所

以 χ(a)=1。

对 b⁻¹ab，特殊根 (ρ,c) 元为 (b⁻¹)_{ρρ}s b_{j,c}=t；每条被 symEdge 保留的普通相邻边 (i,i+1)，若 i>ρ 则

(b⁻¹)_{iρ}=0，若 i<ρ 则 i+1<j，故 b_{j,i+1}=0；i=ρ 的相邻边终点 ρ+1 被排除。因此其他边无增量，

χ(b⁻¹ab)=ψ(t)≠χ(a)。


                                  

---


定理 BW.3（有限域位置根交换）
BV.2 将 nPos(ψ,τ,ρ,k) 对应到 dim V_A，而 nPos(ψ,τ,ρ+1,k) 按定义为 dim V_B。由 BV.3，χ 在 A、B 上为群

特征。将 BW.1 代入 BU.1 得 dim V_A≤dim V_B；将 BW.2 中 A、B 交换后再代入 BU.1 得 dim V_B≤dim

V_A。所以两者相等。

                       nPos(ψ,τ,ρ,k)=nPos(ψ,τ,ρ+1,k), ρ+k+2≤r. (BW.3)


这一定理不依赖 τ 不可约或尖点性，而只依赖有限域、ψ 非平凡及两个明确的幺幺子群。它对应源码

RootExchange.nPos_succ，且两条初等矩阵见证在正文明确标注，已纠正审读时可能发生的指标误认。


BX. 边界、模型测试与仍需证明的下游引理
边界检验：当 ρ=0、k=1、r=3 时，A={g∈U:g₀₁=0}、B={g∈U:g₁₂=0}，而 χ(g)=ψ(g₀₂)。对 b=I+uE₀₁∈B\A，

选 a=I+sE₁₂∈A；由 b⁻¹ab=I+sE₁₂−usE₀₂，得到 χ(a)=1、χ(b⁻¹ab)=ψ(−us)。对 b=I+vE₁₂∈A\B，选

a=I+sE₀₁∈B；由 b⁻¹ab=I+sE₀₁+svE₀₂，同样获得非平凡字符差异。这两个具体计算完整展示了 BU.1 两边不等

式的根交换机制。

配套脚本 lean_root_exchange_exact_certificate.py 在 F₅ 上独立执行整数模运算，覆盖置换后子群与字符

5,950 组、B\A 方向见证 5,389 组、A\B 方向见证 5,349 组，以及 Levi 边字符传递 1,288 组。每个检查只涉及

有限域算术，不使用浮点数。有限参数检验不能取代正文的任意 r、ρ、k 的证明。

截至本版：先前 Levi 交群等价与位置根交换的两个具体缺口已经给出可逐步验算的自然语言证明。仍需进一

步展开 (i) 从 whCut(0,k) 到 Whittaker 分块求和的 mirabolic 等变函数计数；(ii) 各 Levi 块的非退化

Whittaker 空间存在与唯一性；(iii) 全局 Theta Lift、内积范数与 Galois/Sha 推导。特别是还没有解决主算术

不等式 (M)；绝不能以本地子引理闭合替代整个 RH 的证明。

固定源码：CocoSgt/riemann-hypothesis-lean, 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4；

CoindEigenSortingPermEqLeviWhittaker.lean 的 bd_mul、sigma_levi、edge_iff、

eig_conj_eq_leviWh；SymmetricPositionCharMultiplicitySuccEq.lean 的 finrank_eig_le、cyc、

mem_conj_iff、edgeSum_conj、conj_elem、conj_elem_zero、nPos_succ；DefGroup.lean 的

symEdge。


第十七编：有限群 Fourier 投影与根交换的抽象定理（V2.3 新增）
V2.2 已给出位置参数 ρ 的根交换。本编处理证明链中另一种、性质不同的根交换：有限幺幺子群的两个坐标

特征通过 Heisenberg 型二阶矩阵元相互转换。这里首先证明一个对所有有限群复表示都成立的 Fourier 分


                                

---


解，再证明由双线性乘法缺陷产生的特征空间维数守恒。该论证独立于自动形式、数域、Theta Lift 和任何

RH 结论。


BY. 字符投影的完整 Fourier 分解

引理 BY.1（有限域加性字符的正交关系）
令 F 为含 q 个元素的有限域，ψ:(F,+)→ℂ× 为非平凡加性字符。对任何 t∈F，有 Σ_{c∈F}ψ(ct)=q（t=0）或 0

（t≠0）。当 t=0，每项为 ψ(0)=1。若 t≠0，取 a∈F 使 ψ(a)≠1，并把求和指标由 c 平移为 c+a/t；此操作不

改变总和，却把每项乘上 ψ(a)，故 (1−ψ(a))Σ_cψ(ct)=0。因 1−ψ(a)≠0，和为零。

                              Σ_{c∈F}ψ(ct)=q·1_{t=0}. (BY.1)


引理 BY.2（有限群特征子空间的归一化投影）
设 G 为有限群，τ:G→GL(V) 为有限维复表示，K≤G 为子群，h:K→F 为群同态（用加法记值）。定义 P_{K,h}

=|K|⁻¹Σ_{x∈K}ψ(−h(x))τ(x)。对任意 y∈K，以 x↦yx 重排求和可得 τ(y)P_{K,h}=ψ(h(y))P_{K,h}，故 P 的像落

在 V_{K,h}:={v:τ(y)v=ψ(h(y))v，∀y∈K}。反过来若 v∈V_{K,h}，则 P(v)=|K|⁻¹Σ_xψ(−h(x))ψ(h(x))v=v。于是

P 是到 V_{K,h} 的幂等投影，其迹正好是维数。

                     tr(P_{K,h})=dimℂ V_{K,h};   P_{K,h}²=P_{K,h}. (BY.2)


定理 BY.3（核群特征空间的 Fourier 直和维数公式）
设 f,ℓ:K→F 都是加法同态，且 ℓ 满射。记 C=kerℓ，并令 W_C={v∈V:τ(x)v=ψ(f(x))v，∀x∈C}，

W_t={v∈V:τ(x)v=ψ(f(x)+tℓ(x))v，∀x∈K}。则

                           dimℂ W_C = Σ_{t∈F} dimℂ W_t. (BY.3)

证明：由于 ℓ 满射，|K|=q|C|。由 BY.2，Q_C=|C|⁻¹Σ_{x∈C}ψ(−f(x))τ(x) 是 W_C 的投影，Q_t=|K|⁻¹Σ_{x∈K}

ψ(−f(x)−tℓ(x))τ(x) 是 W_t 的投影。交换有限求和顺序，得到 Σ_tQ_t=|K|⁻¹Σ_{x∈K}ψ(−f(x))

[Σ_tψ(−tℓ(x))]τ(x)。BY.1 说明中括号仅在 ℓ(x)=0 时为 q；所以 Σ_tQ_t=(q/|K|)Σ_{x∈C}ψ(−f(x))τ(x)=Q_C。对

双方取迹，借助 BY.2 即得等式。不要求这些 W_t 两两互不相交，维数公式来自投影恒等式而非随意断言直

和。


引理 BY.4（共轭平移下的所有 Fourier 模式同维）
沿用 BY.3。再假设对于任意 a∈F，存在 y_a∈G 满足：对所有 x∈K，y_a⁻¹xy_a∈K、ℓ(y_a⁻¹xy_a)=ℓ(x)、

f(y_a⁻¹xy_a)=f(x)+aℓ(x)。因为 K 有限，单射共轭使 y_a⁻¹Ky_a=K。对 v∈W_t、x∈K，有


                              

---


τ(x)τ(y_a)v=τ(y_a)τ(y_a⁻¹xy_a)v=ψ(f(x)+(a+t)ℓ(x))τ(y_a)v。因此 τ(y_a) 将 W_t 线性同构到 W_{t+a}；同理

逆映射由 τ(y_a)⁻¹ 给出。所有 t 维数均相同，结合 BY.3 得

                               dimℂ W_C=q·dimℂ W_0. (BY.4)

上述条件明确使用的是 f 的共轭平移，不是“表示有 Fourier 对称性”的口头假设。后面会由一条具体的上三

角矩阵乘法公式构造这些 y_a。


BZ. Heisenberg 型乘法缺陷与两向根交换

定理 BZ.1（双线性缺陷的特征空间交换）
令 D≤G 为有限子群，f,ℓ,m:D→F 为函数。假设 ℓ、m 是加法同态，并且 f(xy)=f(x)+f(y)+ℓ(x)m(y)

（x,y∈D）。记 K=ker m，K′=kerℓ；进一步假设 ℓ|_K 与 m|_{K′} 均满射。则 f 在 K 和 K′ 上分别是加法同态，

并有

                            dim V_{K,ψ∘f}=dim V_{K′,ψ∘f}. (BZ.1)

证明首先核查群论恒等式。对 y,u∈D，置 z=y⁻¹uy，满足 yz=uy。因为 ℓ、m 是同态且 F 加法交换，

ℓ(z)=ℓ(u)、m(z)=m(u)。将 yz=uy 两边分别按 f 的乘法公式展开并约去 f(y)，得到

                            f(y⁻¹uy)=f(u)+ℓ(u)m(y)−ℓ(y)m(u). (BZ.2)

当 u∈K 时 m(u)=0，故 f(y⁻¹uy)=f(u)+ℓ(u)m(y)。取任意 t∈F，从 m|_{K′} 满射得到 y∈K′，使 m(y)=t。此时 y

共轭保持 K 与 ℓ，给出 BY.4 所需的 f 变换，所以 dim V_{K∩K′,f}=q·dim V_{K,f}。

反过来，当 u∈K′ 时 ℓ(u)=0，故 f(y⁻¹uy)=f(u)−ℓ(y)m(u)。从 ℓ|_K 满射取 y∈K 使 ℓ(y)=−t，可把 f 改成 f+t m；

再次应用 BY.4，得到 dim V_{K∩K′,f}=q·dim V_{K′,f}。两个等式的左边相同且 q>0，因此可约去 q 得

BZ.1。

这个证明对任意有限群复表示成立，亦不要求 D 是 Heisenberg 群本身。真正必要的是 (i) 两坐标同态；(ii) f

的交叉乘积精确只有一项 ℓ(x)m(y)；(iii) 两方向的满射条件。缺少任何一条都不能直接调用 BZ.1。


第十八编：矩阵元的实在化、割点迁移与 q−1 频率分离（V2.3 新增）
上一编是纯抽象群论。本编把 BZ.1 的所有条件落实到上幺幺矩阵上，确认没有把群表示的半单性或

Whittaker 唯一性当作隐含前提。与源码 FinrankMirabolicWhittakerEigenspace.lean 中的 pat、dm_step、

dm_chain、dm_fourier 一一对应。


                               

---


CA. 模式群与唯一的非线性交叉项

定义 CA.1（上幺幺模式群）
记 U_n(F) 为所有 n×n 上幺幺矩阵。对整数 0≤a<e≤e′≤m<n（在本引理中重点取 e′=e+1），定义

pat(a,e,e′,m) 为满足下列禁用矩阵元条件的 U_n 子群：u_{a,j}=0（a<j<e），以及 u_{i,m}=0（e′≤i<m）。

不在这些矩形支撑内的上三角矩阵元可以非零。作为源码对象，它的乘法闭性来自上三角乘法的下三角项消失

与模式支撑对中间指标的稳定性。


引理 CA.2（三组不同模式之间的核等式）
取 a<e<m，令 D=pat(a,e,e+1,m)，K=pat(a,e,e,m)，K′=pat(a,e+1,e+1,m)。在 D 中唯一允许跨越“源行 a—

中间指标 e—目标列 m”的两个变量是 ℓ(u)=u_{a,e} 与 m₀(u)=u_{e,m}。由定义直接可见 K={u∈D:u_{e,m}=0}

=ker m₀，K′={u∈D:u_{a,e}=0}=kerℓ。

对 x,y∈D，计算 (xy)_{a,m}=Σ_{j=0}^{n−1}x_{a,j}y_{j,m}。上三角性排除 j<a 与 j>m；j=a,m 的两项分别是

y_{a,m}、x_{a,m}。对 a<j<e，x_{a,j}=0；对 e<j<m，y_{j,m}=0。余下唯一的交叉项来自 j=e，故

                       (xy)_{a,m}=x_{a,m}+y_{a,m}+x_{a,e}y_{e,m}. (CA.2)

对 (a,e) 元，Σ_{a<j<e}x_{a,j}y_{j,e}=0，因为每个 x_{a,j}=0，故 ℓ(xy)=ℓ(x)+ℓ(y)。对 (e,m) 元，Σ_{e<j<m}

x_{e,j}y_{j,m}=0，因为每个 y_{j,m}=0，故 m₀(xy)=m₀(x)+m₀(y)。取任意只涉及相邻上对角元的求和

E(u)=Σ_{(i,i+1)∈Ω}u_{i,i+1}，上幺幺矩阵的每条相邻元在乘法下都相加，所以 E(xy)=E(x)+E(y)。于是

                     f(u):=E(u)+u_{a,m} ⇒ f(xy)=f(x)+f(y)+ℓ(x)m₀(y). (CA.3)


引理 CA.3（原子初等矩阵保证双向满射）
对于任意 t∈F，I+tE_{a,e} 属于 K：它没有禁用的源行条目（j<e），其列 m 条目也全为零，且

ℓ(I+tE_{a,e})=t。类似地 I+tE_{e,m} 属于 K′：它的源行 a 上没有非零项，且列 m 的禁用范围仅 i≥e+1；由

m₀(I+tE_{e,m})=t 得 m₀|_{K′} 满射。CA.2–CA.3 的每一个假设都已核查，因此可无条件调用 BZ.1，得到

                             dim V_{K,ψ∘f}=dim V_{K′,ψ∘f}. (CA.4)

这就是源码 dm_step 的核心：将模式群一处禁用条件从列 m 的 (e,m) 移到行 a 的 (a,e)，对满足上述局部范围

的任意有限维复表示，其相应字符特征空间维数不变。逐次令 e=a+1,a+2,…,m−1，即得到 dm_chain 所需的

整个链式传递。


                                

---


CB. 由对角共轭产生的非零 Fourier 模式等价

定义 CB.1（两个层级的模式群）
取 0≤a<m<n，并定义 H_a=pat(0,0,a,m)、H_{a+1}=pat(0,0,a+1,m)。在 H_{a+1} 中，矩阵元 u_{a,m} 对乘

法是加法同态：若 a<i<m，则 i≥a+1 导致右矩阵的 u_{i,m}=0，于是乘法没有交叉项。H_a 恰好是 H_{a+1}

中 u_{a,m}=0 的核。记 f_m(u)=Σ_{i+1≠m}u_{i,i+1}，即不跨越割点 m 的相邻边求和。


引理 CB.2（有限域 Fourier 参数的精确 q−1 分拆）
由 BY.3，若 π 是包含 H_{a+1} 的群 P 的任意有限维复表示，则 H_a 的 f_m-特征空间维数等于 Σ_{t∈F}

H_{a+1} 的 (f_m+t·u_{a,m})-特征空间维数。证明里使用的坐标 u_{a,m} 的满射由 I+tE_{a,m}∈H_{a+1} 明

确提供。

为了比较非零参数 s,t，取对角矩阵 d=diag(d_i)，其中 d_i=s/t（i<m）且 d_i=1（i≥m）。若 s,t≠0，该矩阵

可逆，且在 mirabolic 群（末行固定）内。共轭 d⁻¹ud 在 m 两侧保持所有被 f_m 统计的相邻元不变：这些边

的两端有相同 d_i；而 (d⁻¹ud)_{a,m}=(t/s)u_{a,m}。因而 f_m(d⁻¹ud)+s(d⁻¹ud)_{a,m}=f_m(u)+t u_{a,m}。

对角共轭构成两个特征空间的线性同构。

        dim V_{H_a,f_m}=dim V_{H_{a+1},f_m}+(q−1)dim V_{H_{a+1},f_m+u_{a,m}}. (CB.2)

因而式中系数 q−1 是 q 个 Fourier 频率按零频率和全部非零频率分组后的准确基数，并非某个增长估计。这种

细分只有在 mirabolic 群允许上述对角矩阵时成立；对于任意 P≤GL_n 不一定成立。


引理 CB.3（循环置换迁移与串联）
令 m=a+c+1，并考虑位置循环置换 ω_{a,c}，其在 a,a+1,…,a+c 上把每个索引递增一位，把末位 a+c 送回 a，

在该区间外固定。由 m=a+c+1 可见 ω 固定所有 ≥m 的索引，故其置换矩阵位于末行固定的 mirabolic 群。对

所有矩阵元按 (ω(i),ω(j)) 重编号，可以把 CA 的最后一个模式群及字符 f_m(u)+u_{a,m} 同时变为以

symEdge(a,c) 编码的目标模式和字符。

实际核查分两类：首先，只要某个上三角矩阵元在旧模式中被强制为零，共轭后的同位置要么仍在新模式的强

制零集合，要么落在新模式的下三角；其次，剩余非零条目中，旧相邻边与新 symEdge 所保留的相邻边一一

对应，而单独的 (a,m) 元对应 symEdge 的那条长跳边。由于循环与逆循环均可执行同样检查，所以不是单向

维数不等式，而是两个特征空间的双射。

再用 CA.4 把禁止元从列 m 一格格移动到源行 a，就可把 symEdge(a+1,c) 的特征空间移回 symEdge(a,c) 的

特征空间。于是源码中的 dm_sym_succ、dm_chain、dm_perm 构成一条可迭代的有限矩阵操作链。这一

段要求 0≤a、1≤c、m=a+c+1<n，以及置换矩阵属于表示群；这些参数条件必须在每次迭代时逐项保留。


                               

---


第十九编：Mirabolic 特征重数卷积公式的有限归纳（V2.3 新增）


CC. 递推量的严格定义与两条基础等式
设 q=|F|，r=k+1，P={g∈GL_r(F):第 r−1 行与单位矩阵相同}。P 含全部上幺幺矩阵、所有固定末位的置换矩

阵，以及对角上在末位取 1 的矩阵。令 π 是 P 的任意有限维复表示；所有特征空间的维数均是非负整数。记

H(A,χ)=dimℂ{v:π(u)v=χ(u)v，∀u∈A}。对 0≤a≤m≤k 定义

               T(a,m)=H(pat(0,0,a,m), ψ∘cutSum_m); D(m)=H(U_r,ψ∘cutSum_m).

                      S(a,c)=H(pat(0,0,a,a+c), ψ∘symSum_{a,c}), a+c≤k.

这里 cutSum_m=Σ_{i+1≠m}u_{i,i+1}；symSum_{a,c}=Σ_{symEdge(a,c)}u_{i,j}。当 a=0 时 symEdge(0,c)

的长边分支不可能发生，剩下的恰是 cutEdge(c)。又两个模式群相同，故 S(0,c)=T(0,c)。当 a=m 时

pat(0,0,m,m)=U_r，故 T(m,m)=D(m)。这两条边界恒等式是后面归纳的起点，不能省略。


引理 CC.1（移动 symEdge 起点不改变特征重数）
对任意 0≤a、c≥0、a+c≤k，有 S(a,c)=S(0,c)=T(0,c)。证明固定 c 对 a 归纳：初始 a=0 是定义。若已知位置

a，将 symSum_{a+1,c} 写成“不进入 a+1、a+c+1 的相邻边和”加 (a,a+c+1) 的矩阵元；用 CA.4 的根交换链

把这条长跳边的禁用模式挪到另一侧，再以 CB.3 中固定末位的循环置换把它送回 symSum_{a,c}。每一步既

变换群也变换字符，故确为同构而不是仅形式上相等。迭代即证。

                                    S(a,c)=T(0,c). (CC.1)


引理 CC.2（沿割点逐格剥离时出现 q−1）
对 a<m≤k，令 c=m−a−1。CB.2 使 T(a,m) 分裂为 T(a+1,m) 和 (q−1) 倍的一条非零频率空间；CB.3 中的循环

置换又把非零频率特征空间化成 S(a,c)。因此得到精确等式

                          T(a,m)=T(a+1,m)+(q−1)S(a,m−a−1). (CC.2)

在 CC.2 中，每项都是同一个具体 P 表示 π 的一个复子空间的维数；不存在因换场而改变表示或把算子重数当

作群阶的步骤。将 CC.1 代入，可将其右边的 S 完全写成固定起点的 T(0,c)。


定理 CC.3（单一割点的完全递推）
对固定 m，以 c=m−a 为归纳参数。c=0 时 a=m，得 T(m,m)=D(m)。当 c≥1，设 a=m−c，由 CC.2 有

T(a,m)=T(a+1,m)+(q−1)S(a,c−1)。按归纳假设，T(a+1,m)=D(m)+(q−1)Σ_{j=0}^{c−2}T(0,j)，而 CC.1 给出

S(a,c−1)=T(0,c−1)。相加恰得

                  T(a,m)=D(m)+(q−1)Σ_{j=0}^{m−a−1}T(0,j), 0≤a≤m. (CC.3)


---


特别取 a=0，写 W_m=T(0,m)，即获得一个完全有限的自然数递推

                      W_m=D_m+(q−1)Σ_{j=0}^{m−1}W_j, 0≤m≤k. (CC.4)


CD. 递推的显式求解与 γ 权重

定理 CD.1（有限递推解的卷积恒等式）
令 γ_q(0)=1，且对 ℓ≥1 定义 γ_q(ℓ)=q^ℓ−q^{ℓ−1}=(q−1)q^{ℓ−1}。对任意非负整数序列 D_m，若 W_m 满足

CC.4，则

                             W_m=Σ_{j=0}^{m} γ_q(m−j)D_j. (CD.1)

证明可只用形式幂级数（无分析收敛问题）：记 W(z)=Σ_{m≥0}W_m z^m、D(z)=Σ_{m≥0}D_m z^m，则

CC.4 在每一项 z^m 的系数层面等价于 W(z)=D(z)+(q−1)[z/(1−z)]W(z)。因此 [1−qz]W(z)=[1−z]D(z)，即

W(z)=[(1−z)/(1−qz)]D(z)。展开 [(1−z)/(1−qz)]=1+Σ_{ℓ≥1}(q^ℓ−q^{ℓ−1})z^ℓ，逐项比较系数即得 CD.1。若递

推只在 0≤m≤k 有效，可将 D、W 在 k 之后任意延长并按公式继续递推；所比较的前 k+1 个系数不受延长方

式影响。

另可直接检验归纳关系：对 ℓ≥1，有 γ_q(ℓ)=(q−1)Σ_{i=0}^{ℓ−1}γ_q(i)，因为 Σ_{i=0}^{ℓ−1}γ_q(i)=q^{ℓ−1}

（ℓ=1 时等于 1，其余按几何级数望远镜相消）。这说明卷积正是唯一满足 CC.4 的解。


定理 CD.2（Mirabolic–Whittaker 的精确有限域公式）
将 CC.4 代入 CD.1，并把 W_k=T(0,k) 识别为 mirabolic 的 U_sym(0,k) 字符特征空间、D_j 识别为全部 U_r 的

cutEdge(j) 字符特征空间，得到

    dim V_{U_sym(0,k),ψ∘symSum_{0,k}} = Σ_{j=0}^{k} γ_q(k−j) dim V_{U_r,ψ∘cutSum_j}. (CD.2)

这是 V1.9 以组合重数上界为起点时尚未自行展开的基本公式。它现在由 Fourier 正交、显式矩阵根交换、循

环置换、对角缩放及有限递推的唯一性给出推导路线。注意 CD.2 的对象是末行固定的 mirabolic 群 P 的任意

复表示；它尚不是一般 GL_r(F) 的公式。


                                

---


第二十编：从 Mirabolic 群下降／回升到 GL 的表示空间（V2.3 新增）


CE. 一般有限群表示的商群下降引理
设 G 是有限群、τ 是 G 的复表示，Q≤G，ρ:Q→P 是满射群同态，χ:Q→ℂ× 是群特征。令 ˜τ(q)=χ(q)⁻¹τ(q)，

并设 M={v∈V:˜τ(n)v=v，∀n∈kerρ}。由于 kerρ 是正规子群，˜τ(Q) 保持 M：对 n∈kerρ、q∈Q，有

˜τ(n)˜τ(q)v=˜τ(q)˜τ(q⁻¹nq)v=˜τ(q)v。

于是 ˜τ 在 M 上通过 Q/kerρ≅P 因子化，诱导出表示 π:P→GL(M)：π(ρ(q))v=χ(q)⁻¹τ(q)v。其良定义性来自等

像元素的差商在 kerρ 中，对 M 作用恒等。


定理 CE.1（带扭曲字符的下降等维定理）
设 H≤P，c:H→ℂ× 为特征；令 ˜H=ρ⁻¹(H)≤Q。对 q∈˜H 定义 d(q)=χ(q)c(ρ(q))。则由上述定义有

                       π(ρ(q))v=c(ρ(q))v ⇔ τ(q)v=d(q)v, q∈˜H, v∈M. (CE.1)

证明右推左时须首先说明 v∈M；若 n∈kerρ⊆˜H，则 d(n)=χ(n)c(1)=χ(n)，所以 τ(n)v=χ(n)v 等价于

˜τ(n)v=v。因此任何满足右端全部等式的 v 自动属于 M。再由满射 ρ 和 CE.1 的点态等价得到原表示在 ˜H 上的

d-特征空间，与下降表示 π 在 H 上的 c-特征空间具有同一个底层向量集合；包含映射是线性同构，因而维数

相等。

该引理的逻辑是先固定 kerρ 上的 χ-等变条件，再识别商群特征空间；它不是直接声称“限制一个更小的子群

不改变特征空间维数”。原仓库 PosOne.exists_descent 使用的正是这个模式。


CF. 尾部上幺幺群与角块群的精确对接
取任意 r≥k+1。设 Q⊂GL_r(F) 为保留左上 (k+1)×(k+1) 方块、其余尾部沿上幺幺方向延伸的群。令 ρ:Q→P

为取左上角块，其中 P 是 k+1 阶末行固定的 mirabolic 群；由于将角块矩阵按块对角方式嵌回 Q，ρ 满射。令

χ 取自尾部相邻矩阵元的 ψ-加性字符，即 χ(q)=ψ(S_tail(q))。

对于 U_sym(r;0,k) 与 U_r 的任意 cutEdge(j) 特征条件，矩阵边集按左上角块和尾部严格分解：S_{sym/full}

(q)=S_corner(ρ(q))+S_tail(q)。从加性字符的乘法性得 ψ(S_{sym/full}(q))=χ(q)ψ(S_corner(ρ(q)))。与此同

时，该全群子集恰是 ρ 对相应角块特征子群的逆像。因此满足 CE.1 的全部条件。

将 mirabolic 公式 CD.2 的左边与每个右边分别用 CE.1 识别回原 GL_r(F) 表示 τ 的子空间，即得任意 r≥k+1、

任意复表示 τ 的公式

                       nPos(ψ,τ,0,k)=Σ_{j=0}^k γ_q(k−j)·whCut(ψ,τ,j). (CF.1)


                                  

---


CF.1 再与 V2.2 的位置根交换 nPos(ρ,k)=nPos(0,k)、V2.1–V2.2 的 Mackey 幸存双陪集计数以及相应的 Levi

特征空间识别相连接，就恢复局部重数恒等式

              nPos(ψ,parInd(b,σ),ρ,k)=Σ_{j=0}^k N_j·γ_q(k−j)·leviWh(ψ,b,σ). (CF.2)

此处 N_j 是总大小为 j 的完整标签块子集个数；将 leviWh=1 代入 (CF.2) 需要额外的有限 GL 鞅/尖点表示非退

化 Whittaker 存在唯一性（Gelfand–Graev）定理。我们仍把该定理单列为待用的深层输入，而不从 Fourier

组合恒等式中“凭空证明”它。


CG. 依赖边界、可机械复算项与进度审计
本轮能够独立复核的普适部分是 BY.1–BY.4 的字符正交与投影、BZ.1 的双线性根交换、CA.2–CA.4 的上三角

矩阵检验、CB.2 的非零频率同维，以及 CC.4→CD.1 的整系数卷积求解。mirabolic 具体模式的完整搬运和尾

部角块对接在正文给出了明确对象、有限项分割与置换方法；它们与原 Lean 文件的 dm_perm、

dm_sym_succ、nPos_zero_eq_sum 对应，阅读时仍须逐一核验其所有退化指标范围。

配套脚本 mirabolic_fourier_exact_certificate.py 进行 45 组有限域字符置换诊断、7,680 组卷积递推诊断、

9,800 组模式群乘法和核结构诊断及 70 组三指标可行性检查。脚本用整数模 5 与 Python 任意精度整数，无浮

点；测试只用于发现指标和符号错误，不代替任何上面的全称数学证明。

仍然没有实现 RH/GRH 的人类独立证明：局部表示论中 Gelfand–Graev 非退化特征空间存在唯一性还需沿专

门源码继续还原；宏观上，Theta Lift 的主要范数上界、Galois 同调与 Sha 窗口估计、主算术不等式 (M) 依旧

未闭合。V2.3 只是逐项降低这些前置引理的黑箱依赖，进度不应按页数机械提高。

本轮对应固定提交 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4，核心源码路

径：Development/AbelianVarietyTheory/Proofs/DivisorProofs/

FinrankMirabolicWhittakerEigenspace.lean（finrank_eig_fourier, finrank_eig_half,

finrank_eig_exchange, dm_step, dm_chain, dm_perm, dm_fourier, solve_rec, mirabolic_whittaker）；

同目录 SymmetricPositionCharMultiplicityEqSumDegenerate.lean（exists_descent,

nPos_zero_eq_sum）。


第二十一编：有限域 GL 的非退化 Whittaker 唯一性（V2.4 新增）
上一编的 (CF.2) 只差 leviWh=1 这个深层表示论输入。本编先解决上界“至多一维”，再在下一编解决下

界“至少一维”。为保证独立核查，不以“Gelfand–Graev 定理”一词代替证明，而是逐一给出字符双侧平均

算子的消失、反对角转置的矩阵固定性、压缩 Hecke 交换性以及从不可约性推出维数 1 的过程。


                                  

---


CH. 抽象有限群的字符 Hecke 压缩

引理 CH.1（双侧平均的缩放和零化规则）
设 G 为有限群，U≤G，χ:U→ℂ× 为一维特征，τ:G→GL(V) 为有限维复表示。令 A=Σ_{u∈U}χ(u)⁻¹τ(u)，

e=A/|U|。由 V2.3 的 BY.2，e 是到 W={v:τ(u)v=χ(u)v（∀u∈U）} 的投影。对任意 a,b∈U、g∈G，求和重排

给出 Aτ(a)=χ(a)A、τ(b)A=χ(b)A，因此

                              Aτ(a g b)A=χ(a)χ(b) Aτ(g)A. (CH.1)

若 a g=g b 且 χ(a)≠χ(b)，那么 CH.1 对 (ag) 和 (gb) 的两种写法给出 χ(a)Aτ(g)A=χ(b)Aτ(g)A。在 ℂ 中二者系数

差非零，故 Aτ(g)A=0。这是后面所有“不相容双陪集”消失的完整线性代数理由。


定理 CH.2（反自同构判据使压缩 Hecke 算子交换）
再假设有反自同构 s:G→G 满足 s(xy)=s(y)s(x)、s²=id、s(U)=U，并且 χ(s(u))=χ(u)（u∈U）。假设每个 g∈G

都能写作 g=a n b（a,b∈U），而对应的 n 满足二择一条件：若每对满足 x n=n y 的 x,y∈U 都有 χ(x)=χ(y)，则

s(n)=n；否则存在某对 x,y 使 χ(x)≠χ(y)，据 CH.1 可推出 Aτ(n)A=0。

在相容情形，由 s(n)=n、χ(s(a))=χ(a)、χ(s(b))=χ(b) 和 CH.1 得 Aτ(s(g))A=Aτ(s(b)n

s(a))A=χ(b)χ(a)Aτ(n)A=Aτ(g)A。不相容情形，两边都因 CH.1 及反自同构将不相容见证交换而为零。因此对任

意 g 成立

                                  Aτ(s(g))A=Aτ(g)A. (CH.2)

现在展开中间 A，得到 Aτ(g)Aτ(h)A=Σ_{u∈U}χ(u)⁻¹ Aτ(g u h)A。令求和指标 u↦s(u)，是 U 的双射；

χ(s(u))⁻¹=χ(u)⁻¹。利用 CH.2 和反乘法性，把每项 Aτ(g u h)A 化为 Aτ(s(h) s(u) s(g))A，再合并中间求和，得到

Aτ(g)Aτ(h)A=Aτ(s(h))Aτ(s(g))A。再用 CH.2 两次，最终

                          eτ(g)eτ(h)e=eτ(h)eτ(g)e, ∀g,h∈G. (CH.3)

这里没有任何“交换的算子自动可同时对角化”之类的错误断言；我们下一引理只需复数域上的共同特征向量

存在性。


引理 CH.3（压缩交换性与不可约性推出 dim W≤1）
假设 τ 不可约。若 W=0，则结论显然。否则考察 W 上的有限族算子 T_g=(eτ(g)e)|_W，g∈G。由 CH.3 它们两

两交换。复向量空间 W 非零且有限维，任何有限个相互交换的算子都存在共同特征向量：先取某一非标量算

子的一个非零特征子空间，交换性保证其他算子保持它，再对维数归纳；若每个算子都是标量则任取非零向

量。于是存在 0≠w∈W，使每个 T_g w=c_g w。


                              

---


不可约性说明 span{τ(g)w:g∈G}=V，因为这是非零且 G 不变的子空间。对等式两边施加 e，由于 ew=w 与

eτ(g)w=T_gw=c_gw，推出 e(V)⊆ℂw。然而 e(V)=W 且 w∈W，故 W=ℂw，dim W=1。

                          不可约 τ + (CH.3) ⇒ dim W≤1. (CH.4)


CI. GLᵣ(F) 的反对角转置与单项矩阵

定义 CI.1（反自同构）
对 r×r 矩阵令 J 为反对角线上全为 1 的置换矩阵，定义 s(g)=J gᵀ J。由于 J²=I，s(xy)=s(y)s(x)，s²=id。若 U

为上幺幺子群，则 s(U)=U：反序转置将严格上三角仍送到严格上三角。定义 S(u)=Σ_{i=0}^{r−2}u_{i,i+1} 与

χ(u)=ψ(S(u))，则 S(s(u))=S(u)，因为索引 i 被映为 r−2−i。χ 在 U 上是群特征，原因是相邻上对角元对乘法可

加。


引理 CI.2（每个 Bruhat 单项代表的唯一兼容性）
经典 Bruhat 分解把每个 g∈GLᵣ(F) 写成 g=u n v，u,v∈U，n 为单项矩阵（每列恰一个非零元）。写 n=P_w

diag(t)，w 是 {0,…,r−1} 上的置换、每个 t_a∈F×。若 χ 对 n 是双侧相容的，即对任意 x,y∈U 满足 x n=n y

总有 χ(x)=χ(y)，则 s(n)=n。下面只用相邻初等矩阵证明这一点。

对任意 a<b 且 w(a)<w(b)，任选 z∈F，令 x=I+z t_a E_{w(a),w(b)}、y=I+z t_b E_{a,b}。两者都属于 U，直接

在矩阵元上算得 x n=n y：两边在 (w(a),b) 增加的项均为 z t_a t_b，其余项不变。

由相容性得 ψ(z t_a·1_{w(b)=w(a)+1})=ψ(z t_b·1_{b=a+1})，对每个 z∈F 成立。非平凡加性字符可分离任

何非零系数：如果 c≠d，取 z 使 ψ(z(c−d))≠1。因此必有两个指示函数同时为 0 或同时为 1，并在后一种情况

下 t_a=t_b。综上，在 a<b 且 w(a)<w(b) 时有

                     [w(b)=w(a)+1] ⇔ [b=a+1]; b=a+1 ⇒ t_a=t_b. (CI.2)


引理 CI.3（反序置换的完整组合刚性）
设 f(i)=r−1−w(i)。由 CI.2，数列 H(i)=i+f(i) 非降：如果在相邻 i,i+1 处下降，则 f(i)≥f(i+1)+2，反序关系给出

w(i+1)≥w(i)+2；但在相邻 i,i+1 且 w(i)<w(i+1) 时，CI.2 要求 w(i+1)=w(i)+1，矛盾。

反过来，数列 H′(i)=i+f⁻¹(i) 也非降。若在 i,i+1 处下降，则 f⁻¹(i)≥f⁻¹(i+1)+2；记 a=f⁻¹(i+1)、b=f⁻¹(i)，可得

a<b，且 w(a)=r−2−i、w(b)=r−1−i，二者相邻。CI.2 迫使 b=a+1，矛盾。

H 与 H′ 是同一多重集合中的元素，只是排列顺序不同：对每个 j，H′(f(j))=f(j)+j=H(j)。两个数列都已按非降次

序排列，因此逐项相等，i+f(i)=i+f⁻¹(i)，得 f(i)=f⁻¹(i)，即 f²=id。


                             

---


再看 t 的兼容性。若 H(i)=H(j) 且 i<j，因 H 非降，i 与 j 之间每个相邻对 k,k+1 也有 H(k)=H(k+1)，所以

f(k+1)=f(k)−1，即 w(k+1)=w(k)+1。CI.2 因而给出 t_k=t_{k+1}；逐段相乘得 t_i=t_j。取 j=f(i)，因 f²=id，

H(f(i))=f(i)+f²(i)=H(i)，故 t_{f(i)}=t_i。

                                          f²=id,   t_{f(i)}=t_i. (CI.3)

用 CI.3 检查 s(n) 的非零位置：原矩阵 n 在 (w(i),i) 取值 t_i；反序转置后的单项位置取自 w′

(i)=rev∘w⁻¹∘rev(i)。f²=id 等价于 w′=w。它的对应系数是 t_{f(i)}，由 CI.3 等于 t_i；因此 s(n)=n。这里完整证

明了 CH.2 所需的 Bruhat 单项代表固定性，而不是援引未说明的“反自同构显然固定相容单项元”。


定理 CI.4（有限 GL 不可约表示的非退化 Whittaker 上界）
任取有限域 F、非平凡 ψ、整数 r≥0、任意有限维复不可约 τ:GLᵣ(F)→GL(V)。将 CH.2 的 G、U、χ、s 分别取

为 GLᵣ(F)、上幺幺群、ψ∘S 与 CI.1 的反对角转置。Bruhat 分解提供任意 g=u n v；若 n 双侧字符相容，CI.2–

CI.3 证明 s(n)=n；若不相容，CH.1 已证明相应压缩算子为零。因此 CH.3 的交换性和 CH.4 的维数结论适用：

                                          dimℂ Wh_ψ(τ) ≤ 1. (CI.4)

整个上界论证仅用有限群上平均、Bruhat 分解、有限排列序列的单调性以及复数域上的共同特征向量；与尖

点性无关。它对应 Lean 的 GGFree.whDim_le_one。


第二十二编：尖点数据的 Whittaker 存在性与多块唯一性（V2.4 新增）


CJ. 从最后一列向第一列的 Fourier 下降

定义 CJ.1（列稳定子与未来相邻边）
取非降块标签 b:{0,…,r−1}→ℕ，P_b 为其抛物子群，σ 为满足 IsCuspDatum 的非零有限维复表示。设

H_k={u∈U_r:u 的所有列 j<k 与单位矩阵同列}，0≤k≤r。于是 H_r={I}、H_0=U_r。对 H_k 上已经确定

的“未来边”字符 ψ∘S_{>k}，其中 S_{>k}(u)=Σ_{i,i+1 为同块相邻且 i+1>k}u_{i,i+1}，记 W_k 为其特征子空

间。目标是从 W_r=V≠0 开始，反向归纳证明每个 W_k≠0。


引理 CJ.2（列根群上的有限 Fourier 不消失）
固定 0≤k<r，设 W_{k+1}≠0。令 C_k={I+Σ_{i<k}x_iE_{ik}: x∈F^k}。由于 E_{ik}E_{jk}=0（i,j<k），有

C_k≅(F^k,+)。H_{k+1} 在 C_k 的共轭下保持，且“未来边”字符不变，因此 C_k 在 W_{k+1} 上诱导线性表

示。


                                      

---


对 0≠v∈W_{k+1} 和每个 ℓ∈F^k，定义 Fourier 分量 v_ℓ=Σ_{x∈F^k}ψ(−Σ_iℓ_i x_i)σ(C_k(x))v。用 BY.1 逐

坐标应用字符正交得到 Σ_{ℓ∈F^k}v_ℓ=q^k v≠0。所以至少存在 ℓ 使 v_ℓ≠0，且指标平移证明

σ(C_k(x))v_ℓ=ψ(Σ_iℓ_i x_i)v_ℓ。由 C_k 保持 W_{k+1}，这个非零向量仍符合全部已确定的未来边条件。

               存在 ℓ∈F^k 和 0≠v_ℓ∈W_{k+1}，使 C_k(x)v_ℓ=ψ(ℓ·x)v_ℓ. (CJ.2)


引理 CJ.3（inflation 与尖点性筛掉错误列字符）
由 IsCuspDatum.infl，只有同块的矩阵元能够在 σ 中产生非平凡作用。若 i<k 且 b(i)≠b(k)，则单独的 E_{ik}

是不同块之间的根元，在 σ 下恒为单位，故 CJ.2 中的 ℓ_i 必须为零。于是在支撑内必有 b(i)=b(k)，即 ℓ 的全

部非零项都处于 k 所属的同一块。

当 ℓ=0 时，若 k 的上一位置 k−1 仍位于同一块，则 CJ.2 得到的向量在“跨过 k”的指定根群上也不变。令

S={i:i<k}，该集合将同一个 b 块一分为二；它所确定的上幺幺根群，对该向量作用平凡。其余未来边特征不包

含任何跨割点边，故这与 IsCuspDatum.cusp 的零向量条件矛盾。因此在 k−1 与 k 同块时，ℓ 不能为零。

如果 k 是一个新块的首项，则没有同块的相邻边 (k−1,k)，目标字符在本列本应为零。这时 ℓ=0 正符合目标要

求，无需改变。注意 k=0 时根群 C_0 平凡，亦自动属于这一边界情况。


引理 CJ.4（非零列字符归一到相邻根）
设 ℓ≠0 且支撑都在块 S={i<k:b(i)=b(k)}，并令 c=k−1。由 b 的非降性，S 非空蕴含 b(c)=b(k)。可以构造一个

只在这些同块、且索引 <k 的位置偏离单位矩阵的 h∈P_b，使行向量 ℓ h=e_c（c 坐标为 1、其余为 0）。构造

完全显式：若 ℓ_c≠0，令 A=e_c(ℓ−e_c)（外积矩阵），取 h=I−ℓ_c⁻¹ A。因为 A²=(ℓ_c−1)A，所以 (I−ℓ_c⁻¹ A)

(I+A)=I，h 可逆；并且 ℓ A=ℓ_c(ℓ−e_c)，故 ℓ h=e_c。若 ℓ_c=0，先取 a∈S 使 ℓ_a≠0，右乘初等矩阵

I+E_{a,c}，将新列字符的 c 坐标变为 ℓ_a≠0，再应用上述构造。

两次矩阵变换的非零位置始终位于同一 b 块且索引 <k，故 h 确属 P_b，且其与 H_k 的共轭保留“未来边”条

件。按列群共轭计算，σ(h⁻¹)v_ℓ 的列特征从 ℓ 变成 ℓ h=e_c，并且仍非零。其在当前列的字符恰为

ψ(u_{k−1,k})（若 b(k−1)=b(k)），与未来边相乘后就是 W_k 所要求的完整字符。因而归纳得到 W_k≠0。


定理 CJ.5（尖点数据的同块 Whittaker 存在性）
从 H_r={I}、W_r=V≠0 起，对 k=r−1,…,0 依次应用 CJ.2、CJ.3、CJ.4：每一步或者直接得到正确零列字符，

或者由同块变换将非零列字符化成唯一相邻根。于是 W_0≠0，即

             dimℂ{v:σ(u)v=ψ(Σ_{b(i)=b(i+1)}u_{i,i+1})v，∀u∈P_b∩U_r} ≥1. (CJ.5)

这是对源码 `eig_ne_bot` 的人类证明级解释。其非零性不是由 CI.4 的上界推出来的：上界允许维数为 0，而

下界真正使用了 IsCuspDatum.infl 和 cusp 以及有限域 Fourier 正交。


                              

---


CK. 多块抛物表示的同时唯一性

引理 CK.1（将表示还原到全部 GL 块的直积）
将非降标签 b 的相同值构成的连续区间依次列为 I_1,…,I_s，长度为 n_1,…,n_s。块对角嵌入 D:∏_{c=1}^s

GL_{n_c}(F)→P_b 及抽取全部同块子矩阵的投影 B:P_b→∏_c GL_{n_c}(F) 满足 B∘D=id。因为 σ 在 P_b 的非

对角块核上按 inflation 条件平凡，故 σ(p)=σ(D(B(p)))。因此 V 实际上是直积群 H=∏_cGL_{n_c}(F) 的一个不

可约表示：任何 H 不变子空间经 D 和 B 的因子化也是 P_b 不变子空间。

令 U_c 是第 c 个 GL 块的上幺幺群，χ_c 取对应的非退化相邻边字符。对每个 c 定义归一化字符投影 e_c=|

U_c|⁻¹Σ_{u∈U_c}χ_c(u)⁻¹σ(D(1,…,u,…,1))。不同 c 的矩阵作用彼此交换，因此 e_c 与另一块的所有作用算

子及投影均交换。所求总 Whittaker 子空间是 W={v:e_cv=v，∀c}=e_1⋯e_s(V)。


引理 CK.2（每个单块的压缩算子交换）
对单个 c，将 V 视作 GL_{n_c}(F) 的有限维复表示。这里并不需要它不可约。由 Maschke 定理可把这个有限群

表示分解为不可约表示的直和；CI.4 说明在每个不可约直和项上，相应 e_c 的像至多一维，故 (e_cσ_c(g)e_c)

和 (e_cσ_c(h)e_c) 在每项上都只是标量算子（零维项中都为零）。因此在整个 V 上两者交换。

                 e_cσ_c(g)e_cσ_c(h)e_c=e_cσ_c(h)e_cσ_c(g)e_c. (CK.2)


定理 CK.3（所有块同时固定的特征空间至多一维）
假设 W≠0。对于每个 c 与 g∈GL_{n_c}(F)，定义 T_{c,g}=(e_cσ_c(g)e_c)|_W。各 T 均保持 W：本块的 e_c

保证 c 块条件，其他块的 e_d 因交换性不受影响。由 CK.2，同一块的 T 两两交换；不同块的 T 因其原始表示

操作交换而两两交换。故复有限维空间 W 存在所有 T_{c,g} 的共同非零特征向量 w。

因为 H=∏GL_{n_c}(F) 的作用在 V 上不可约，H 对 w 的轨道张成 V。对任意分块群元素 h=(g_1,…,g_s)，由各

块投影互相交换、w 固定于每个 e_c、各 T_{c,g}w 为标量倍，可得 e_1⋯e_sσ(h)w=(∏_cλ_{c,g_c})w。对轨

道张成取线性组合，得到 W=e_1⋯e_s(V)⊆ℂw。反向包含显然，故 W=ℂw，dim W=1；若 W=0 则 dim

W=0。

                                 dimℂ W≤1. (CK.3)


定理 CK.4（尖点表示的 Levi–Whittaker 重数精确为 1）
由 CJ.5，维数至少为 1；由 CK.3，维数至多为 1，所以严格地

                               leviWh(ψ,b,σ)=1. (CK.4)


                           

---


这个等式所用条件必须原样保留：F 为有限域、ψ 是非平凡加性字符、b 非降、σ 非零且不可约、σ 对不同块

的上幺幺根群平凡，以及 σ 满足跨块割点的 cusp 条件。把 CK.4 带回上一版 CF.2，即得到局部完整重数等式

nPos=Σ_j N_jγ_q(k−j)，与 V1.9 的二项式上、下界合并后，可直接用于全球重数扰动。


CL. 复核证书、剩余宏观缺口与使用范围
在 F₅ 上的独立枚举脚本 gelfand_monomial_exact_certificate.py 对 n≤4 的全部置换和全部非零对角权，以

及 n=5 的全部置换与单位对角权，共检查 6,685 组单项矩阵数据，其中 641 组通过 transvection 相容条件；

这些相容样本全部满足反对角转置固定性和相应的置换／权向量恒等式。这只检验 CI.2–CI.3 的有限实例；一

般性证明是正文的单调重排论证。

就局部有限域分支重数而言，V1.9–V2.4 依次补上了组合双侧界、Mackey 双陪集、两类尖点／根字符消去、

幸存块计数、Levi 特征空间同构、位置根交换、mirabolic Fourier 卷积以及本版的 Whittaker 存在唯一性。

仍需对上述长篇连锁论证进行跨章节符号和退化参数复核；不能以单个有限算例的通过代替整个形式化依赖的

编译验证。

最关键的全局主不等式 (M) 仍远未闭合。特别是 Theta Lift 的几何比较、有限位和无穷位的范数估计、Galois

上同调与 Sha 窗口上界，尚不能由本版局部表示论自动推出。即使本编证明了 CK.4，也只是给出了 RH 证明

链中的一个深层但局部的必要环节。

源码锚定：CocoSgt/riemann-hypothesis-lean，提交 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4；

WhittakerSpaceDimFiniteGLLeOne.lean 的 gelfand、perm_fixed、sg_monomial、whDim_le_one；

ExistsColumnCharacterEigenSubmoduleNeBot.lean 的 exists_eigenvector_of_stable、colEl；

ExistsBlockTriVecMulEqSinglePred.lean 的 rank-one 归一构造；FinrankLeOne.lean 的 step、

eig_ne_bot、finrank_le_one、leviWh_eq_one。


第二十三编：整数化 Reynolds 算子与全球格的有限指数桥梁（V2.5 新增）
前文已将有限域分支重数公式与部分局部范数界还原；但从这些局部信息到全球高度，必须进一步控制群等变

特征部分与格映射的先后顺序。此处如果直接宣称“映射与特征子空间相交交换”，一般是错误的。原仓库

GlobalBoundRefinements.lean 的 LevelInclType / LocalGlobalIncl / LevelInclLocal 正是解决这类分母损失

的中间接口。本编将该接口完全写成一个可以独立检查的交换代数定理。


CM. 群特征格的前向包含与反向整数倍包含
定理 CM.1（整数化 Reynolds 双侧包含）。设 O 为特征零域 K 中的整环，Γ 为有限群，m=|Γ|≥1。设 V₀、E

为有限维 K 向量空间，ρ₀:Γ→GL_K(V₀)、ρ₁:Γ→GL_K(E) 为表示，χ:Γ→O× 是乘法特征。设 i:V₀→E 为 Γ-等变

K-线性映射，即 iρ₀(γ)=ρ₁(γ)i。设 A⊆V₀ 为 O-子模且 ρ₀(γ)A=A。定义


---


  T₀={v∈V₀:ρ₀(γ)v=χ(γ)v (∀γ∈Γ)}, T₁={w∈E:ρ₁(γ)w=χ(γ)w}.

并定义两个 O-子模 R′=i(A∩T₀) 与 R=i(A)∩T₁。那么严格有

  m R ⊆ R′ ⊆ R.    (CM.1)

证明前向包含 R′⊆R：取 y=i(a)，a∈A∩T₀。则 y∈i(A)。对任意 γ，ρ₁(γ)y=iρ₀(γ)a=i(χ(γ)a)=χ(γ)y，故

y∈T₁，于是 y∈R。

证明整数倍包含 mR⊆R′：取 y∈R。可选 a∈A 使 i(a)=y，而 y∈T₁。直接在 O-格内构造

  Pχ(a)=Σ_{γ∈Γ} χ(γ)⁻¹ ρ₀(γ)a.    (CM.2)

因为 χ(γ)∈O×、A 对 Γ 稳定，每一项都在 A 中，所以 Pχ(a)∈A。令 δ∈Γ，把求和变量由 γ 换为 t=δγ，可得

  ρ₀(δ)Pχ(a)=Σ_t χ(δ⁻¹t)⁻¹ρ₀(t)a = χ(δ) Pχ(a).

故 Pχ(a)∈T₀。另一方面，i(Pχ(a))=Σ_γ χ(γ)⁻¹ρ₁(γ)y；因 y∈T₁，每一项等于 y，总和恰为 m y。因此

my∈i(A∩T₀)=R′。证毕。

强调：CM.2 没有使用 1/m，也不要求 m 在 O 中可逆；这正是它能保留整数格信息的原因。若 m 在 O 中为单

位，CM.1 蕴涵 R′=R；但在代数整数环 O_K 中，m>1 通常不是单位，故不能擅自去掉这一损失。


CN. 每个极大理想处的格包含如何拼回全球
引理 CN.1（极大理想局部判别）。设 O 是含单位的交换环，M、N 为某个 O-模 E 的子模。若对任意极大理

想 𝔪 都有 M_𝔪⊆N_𝔪，则 M⊆N。这里允许 E 有挠，亦无需先假设 M、N 有限生成。

证明。假设有 x∈M 但 x∉N。考虑理想 I_x={a∈O:ax∈N}。若 1∈I_x，便有 x∈N，与假设矛盾，所以 I_x 是

真理想。由极大理想存在定理，取 𝔪⊇I_x。局部包含给出 x/1∈N_𝔪，于是存在 s∉𝔪 使 sx∈N，即

s∈I_x⊆𝔪，矛盾。证毕。

定理 CN.2（点态比较推出全球双侧格包含）。设 O 为代数整数环、Γ 有限、m=|Γ|。设 R,R′⊆E 为 O-子模。假

设对每个极大理想 𝔭，都有一个满足 CM.1 全部假设的局部数据表示，使局部像格、特征像格恰分别为 R_𝔭、

R′_𝔭。则

  m R ⊆ R′ ⊆ R.    (CN.1)

证明。在每个 𝔭 处，CM.1 给出 m R_𝔭⊆R′_𝔭⊆R_𝔭。由 CN.1 分别应用于 (M,N)=(mR,R′) 和 (R′,R)，可得全球

双侧包含。这里对每个极大理想所用的表示 i、A 可以不同，但必须证明其两个局部结果确实对应同一对全球

格的局部化；这项“局部识别”属于 Theta 几何构造必须另证的输入，不能由纯代数自动产生。


CO. 把群阶的分母损失变成显式共体积误差
定理 CO.1（指数上界）。设 K/ℚ 为 n 次数域，O=O_K，E 为 d 维 K-向量空间，R、R′ 是 E 内满秩 O-格，并且

m R⊆R′⊆R，其中 m≥1 为整数。则商群 R/R′ 有限，且

  [R:R′] ≤ m^(n d), 0 ≤ log[R:R′] ≤ n d log m.   (CO.1)


                                    

---


证明。R′ 包含 mR，因此自然商映射 R/mR→R/R′ 满射，故 [R:R′]≤#(R/mR)。作为 Dedekind 整环上的满秩

格，R 为秩 d 的有限生成射影 O-模。射影模在任意素理想处局部自由；对 O/(m) 的各有限局部因子逐一计

数，得到 #(R/mR)=#(O/(m))^d。数域中 #(O/(m))=m^n，故所求上界为 m^(nd)。m=1 时两格相等，公式仍

成立。

推论 CO.2（对数共体积）。给 E⊗_ℚℝ 固定任何平移不变 Lebesgue 测度，令 vol(R) 为作为实格的共体积，

则

    vol(R′)/vol(R)=[R:R′], 0≤log vol(R′)−log vol(R)≤n d log m. (CO.2)

证明。R′⊆R 且有限指数，任取 R 的 ℤ-基与 R′ 的 ℤ-基，后者相对前者的整数变换矩阵行列式绝对值等于

[R:R′]；共体积乘以同一行列式绝对值，因此比值与指数相同。对不同论文的均值斜率 μ，须先核定其定义符

号：若 μ=−log vol，则本式的差号应反向，不能未经核对移植。


CP. 不能省掉的损失：指数 2 的完全反例
例 CP.1。令 O=ℤ、K=ℚ、Γ=C₂={1,s}，V₀=ℚ²，E=ℚ，ρ₀(s)(x,y)=(y,x)，ρ₁(s)=id，χ≡1，i(x,y)=x+y，A=ℤ²。

则 A 稳定，i 等变。T₀={(t,t):t∈ℚ} 是对角线；T₁=ℚ。于是

    R′=i(ℤ²∩T₀)=2ℤ， R=i(ℤ²)∩T₁=ℤ.

故 R′≠R，且 [R:R′]=2=m，恰达到 CO.1 在 n=d=1 时的最优上界。对 y=1∈R，可取 a=(1,0)，整数化

Reynolds 给出 Pχ(a)=(1,1)，其像 i(Pχ(a))=2=|Γ|·1。这也具体展示了若错误地把前后取不变部分视作可交

换，就会少算恰好一个素数 2 的整数指数。


CQ. 放回 RH 证明链：已完成的代数步骤与尚待证明的几何输入
本编新增一个无条件成立的、可独立检查的全球代数桥梁：只要源端与目标端的格映射、Γ 等变性、特征子空

间和每处局部识别确实存在，就有 |Γ|R⊆R′⊆R；在满秩情况下引起的对数共体积差至多

[K:ℚ]·dim_K(E)·log|Γ|。这把早期的“某种分母损失”变成了明确的整数指数和可用于高度估计的量。

但这些纯代数引理不证明原项目所需的 Theta Lift 存在、积分变换的非退化性、比较映射的 Galois 等变性、

数域各处局部格与目标格的同构、或目标核空间具有固定维数；这些是未来全局几何步骤必须独立展开的输

入。因此本章是 LevelInclType / LocalGlobalIncl / LevelInclLocal 的自然语言闭合，而不是主算术不等式 (M)

的闭合。

源码对应：CocoSgt/riemann-hypothesis-lean，固定提交

7cbf7a0c32fca1badf05931879a37c3f8a2b03b4；src/Formalism/BranchSandwichDivisors/

BranchIsometryProofs/GlobalBoundRefinements.lean 中的 level_inclusion_type、

local_global_inclusion、level_inclusion_local，另见 VacLev.sharp 中显示整数倍损失无法一般消除的例

子。


                                    

---


第二十四编：链式交织、三角形分母与有限指数账本（V2.6）
源码固定版本：CocoSgt/riemann-hypothesis-lean，提交

7cbf7a0c32fca1badf05931879a37c3f8a2b03b4。对应

src/Formalism/BranchSandwichDivisors/BranchIsometryProofs/GlobalBoundRefinements.lean 中

chain_move、chain_key'、chain_coupled_key、chain_scalar 与 chain_denominator_coupled。本编是

一般线性代数和交换代数证明，并非 Theta Lift 或主算术不等式 (M) 的无条件建立。


CR. 非交换链映射的标量交织公式
设 F 是域，n≥0，V₀,…,Vₙ 是 F-向量空间，Uⱼ:Vⱼ→Vⱼ 为线性自映射，Kⱼ:Vⱼ→Vⱼ₊₁ 为线性映射（0≤j<n）。设

cⱼ∈F×，且逐级满足


为突出顺序，复合写为 Kₙ₋₁⋯K₀，右侧作用在向量上。令 ；定义空复合为恒等映射。

定理 CR.1（带幂次的链式交织）。对 M≥n 和 x∈V₀，成立


证明。 首先由 (CR.1) 及 cⱼ≠0，得到 KⱼUⱼ=cⱼ⁻¹Uⱼ₊₁Kⱼ。归纳于正整数 s，可知 KⱼUⱼˢ=cⱼ⁻ˢUⱼ₊₁ˢKⱼ。对 (CR.2) 再归

纳于链长 j：j=0 时，两侧均是 U₀ᴹx。假设长度 j 的公式成立，在左侧再作用 Kⱼ，便有


由于 Uⱼ₊₁ᴹ⁻ʲ=Uⱼ₊₁ᴹ⁻ʲ⁻¹·Uⱼ₊₁，这恰好是长度 j+1 的公式。只用到了非零标量可逆与线性映射结合律；没有假定

Kⱼ 可逆，也没有假定不同层的 Uⱼ 本身相等。证毕。


CS. 加上两个终端映射的精确恒等式
再给定 V꜀、Vₗ，A:Vₙ→V꜀，B:V꜀→Vₗ，U꜀ 和 Uₗ 为各自的线性自映射，并取 cₙ,cₙ₊₁∈F×，满足


令 m=n+2（注意这里 m 表示链中全部交织步数，不是上一编的群阶）。

定理 CS.1（耦合链恒等式）。记


则


证明。 用 (CR.2) 取 M=m，首先取得前 n 个系数 cⱼ⁻⁽ᵐ⁻ʲ⁾ 和 Uₙ²。由 CS.1 可得 A Uₙ²=cₙ⁻² U꜀²A；继而 B

U꜀²=cₙ₊₁⁻²Uₗ²B。这样直接转移会多出一个 Uₗ，故必须保留终端算子的正确交错次序：


最后一个等号不是把 B U꜀² 直接改写成 cₙ₊₁⁻²Uₗ²B，而是先分离第一个 U꜀：B U꜀²=(B U꜀)U꜀=cₙ₊₁⁻¹Uₗ B U꜀。因

此两个终端幂次分别为 2 与 1，合并恰得 (CS.2)。这个次序核对对避免多出一次 Uₗ 尤为重要。证毕。


---


CT. 每一步的局部标量如何形成一个全局整数
令 R 为整环，F 为其分式域或包含 R 的域，T∈R 为非零元。令 为有限指标集，γ(v) 为非负整数，

cⱼ(v)∈F×，并设 cⱼ=∏ᵥcⱼ(v)。假设对 0≤j<m 及任意 v 都有


设 G=∑ᵥγ(v)，H=m(m+1)/2。

定理 CT.1（三角形分母可积性）。标量


实际上属于 R，且可以显式写成


证明。 把 CT.3 的右边展开，得到 T 的指数为 ，系数部分是 。因为 ，它恰等于 CT.2。每个 dⱼ,ᵥ∈R，而 R 对有

限乘积与非负整数次幂封闭，故 D∈R。此处不需要 R 为主理想整环，也不需要分母本身属于 R；关键是逐位

置的比值已落入 R。证毕。

定理 CT.2（局部赋值账本）。若 F=K 是数域 K、R=O_K 为其整数环，p 是非零素理想，规范化离散赋值为

vₚ，则


证明。 赋值对乘积可加且 vₚ(dⱼ,ᵥ)≥0，逐项加权求和即得；没有对不同素位之间的负赋值进行未经证明的抵

消。证毕。


CU. 将链式公式转成目标格的整数成员关系
假设 Vⱼ、V꜀、Vₗ 都是 F-向量空间，Lⱼ⊆Vⱼ、L꜀⊆V꜀、Lₗ⊆Vₗ 为 R-子模。设 e≥0，给定下列明确的额外前提：


定理 CU.1（耦合链清分母）。若 x∈L₀，则


证明。 从 x∈L₀ 出发依次使用 CU.1，可按归纳得到 。此时再依次作用 U꜀A、UₗB，得到 。由 CS.2，左侧目标

量等于 PZ，其中 P=∏ⱼ cⱼ⁻⁽ᵐ⁻ʲ⁾；由 CT.2，TᴳᴴP=D∈R。于是目标左侧等于 D·(TᵐᵉZ)，属于 Lₗ。证毕。

提醒：CU.1 中各个带 Tᵉ 的格保持性，是源码 chain_denominator_coupled 输入的算术部分；本编只证明它

们足以推出 CU.2，不证明 Theta/Weil 几何天然提供这些格保持性。


CV. 与 V2.5 的 Reynolds 群阶损失放进同一指数界
定理 CV.1（条件性双层格指数界）。令 K 为 n_K 次数域、O_K 整数环、E 为 d 维 K-空间，R、S、R′ 为 E 内

满秩 O_K 格。设 0≠a∈O_K，g≥1 为整数，且


则


---


证明。 对任意满秩 O_K-格 X，商 X/aX 的阶为 |N(a)|ᵈ；这是乘以 a 在底层 n_Kd 维 ℚ-向量空间上的行列式绝

对值。由 aR⊆S，商映射 R/aR→R/S 满射，给出 [R:S]≤|N(a)|ᵈ。同理 S/gS→S/R′ 满射，给出

[S:R′]≤g^(n_Kd)。有限指数相乘 [R:R′]=[R:S][S:R′]，于是 CV.2 成立。证毕。

特别地，若另有经过证明的格包含 ，并且 S 到 R′ 的特征投影满足 V2.5 的群阶夹逼 ，才可以在 CV.2 中取

a=T^(me+GH)、g=|Γ|，推得


必要的逻辑边界： CU.2 仅给出一类特定输出的分母可清除；它本身不能推出上述完整格的夹逼包含。要用

CV.3，仍需另外证明构造的输出张成满秩格，以及包含方向正确。把“某些生成元落在目标格”偷换为“目标

格全体受某个指数控制”，会造成严重的逻辑跳跃。


CW. 可复现的低维精确校验与失败样例
单维模型中取 n=2，K₀=K₁=A=B=1，c₀=2、c₁=3、c₂=5、c₃=7，U₀=1、U₁=2、U₂=6、U꜀=30、Uₗ=210。此时

m=4，CS.2 左边为 1，而右边的分母为


其右边的 Z 恰为 210·30·6·2=75600，故等式确切成立。若错误地给 c₃ 分配指数 2 而非 1，则立刻不成

立。

                                                                        6·2
取 R=ℤ、F=ℚ、T=2、m=3、 为单点、γ=1、c₀=c₁=c₂=2，则每个 dⱼ,ᵥ=1∈ℤ，H=6，故 D=2               (-6)=1，恰展示

了“六次分母”与“三角形六次分子”抵消。这不是纯浮点检查，配套程序使用分数域精确算术。


CX. 源码核对与未闭合的关键输入
本编完整重构的代数定理对应 chain_move、chain_key'、chain_coupled_key、chain_scalar 和

chain_denominator_coupled 的核心数学机制。其整体链条为


加上 V2.5 的群阶投影可获得一套条件性指数误差账本。不过仍必须追踪 Theta Lift 提供的 Uⱼ、Kⱼ、A、B、

U꜀、Uₗ 是否满足这些精确交织关系，以及所有待比较格的满秩性、局部格保持性、复合映射非退化性与范数

归一化。在这些条件得到独立证明之前，不能声称获得了 RH 主不等式 (M) 或其最终的无条件常数界。


CY. 分母误差的素理想分解：从总上界恢复每一处的精确长度
定义 CY.1。设 K 为次数 n_K 的数域，O=O_K，V 是 d 维 K-向量空间，R、S 为 V 内满秩 O-格，且 0≠a∈O 满

足 aR⊆S⊆R。对任意非零素理想 𝔭，令 ℓ_𝔭=length_{O_𝔭}((R/S)_𝔭)。这是一个有限非负整数，且只有有限

多个 𝔭 使 ℓ_𝔭≠0。

定理 CY.2（素理想级精确指数公式）。记 N𝔭=#(O/𝔭)，v_𝔭(a) 为 (a) 在 𝔭 处的阶，则


                           

---


证明。O_𝔭 是离散赋值环，取其一致化元 π_𝔭。因为 R、S 皆为同秩 d 的格，局部的初等因子定理给出

R_𝔭≅O_𝔭^d，且在适当基下 S_𝔭=⊕_{i=1}^d π_𝔭^{t_i}O_𝔭，所有 t_i≥0。包含 aR_𝔭⊆S_𝔭 等价于

t_i≤v_𝔭(a)。于是 ℓ_𝔭=∑_i t_i≤d·v_𝔭(a)。每一个 O_𝔭/(π_𝔭^{t_i}) 的有限群阶为 (N𝔭)^{t_i}；由于 R/S 是

有限 O-模，其有限群阶等于各素理想局部分量群阶之积，便得精确式。若 𝔭∤a，则 v_𝔭(a)=0，故 ℓ_𝔭=0。证

毕。

推论 CY.3（误差的真实支集）。指数只在 𝔭|a 的素位有贡献，而非每一个坏约化位都必然付出损失。对照

(CV.2) 可写出更精确的


这个版本把“群阶与链式分母的最大允许误差”和“真实产生的局部长度”区分开。后续若能够从 Theta 局部

格辨认 ℓ_𝔭，可以严格缩小 (CV.3) 的误差；但在未识别前，仍应保留上界，不能擅自把 ℓ_𝔭 当作 0。

例 CY.4。K=ℚ、d=2、R=ℤ²、a=30，令 S=2ℤ⊕15ℤ。则 aR⊆S⊆R，真实指数 [R:S]=30，而粗界为

30²=900。对应素位的长度分别是 ℓ₂=1、ℓ₃=1、ℓ₅=1。这说明若能恢复每处的初等因子，会大幅减少由最粗范

数界引入的常数。


CZ. 对数高度中“三角指数只付半份”的准确有限加权恒等式
接下来核对源文件 DualLevelType.lean 中 DenominatorPayment 的纯代数部分。设 Λ 为有限集、Π⊆Λ，实

权 w_λ 满足 Σ_{λ∈Λ}w_λ=L，以及 Σ_{λ∈Π}w_λ=L/2。设 m,e,G 为实参数，H=m(m+1)/2；令每个位置的支

付预算为 e_λ=me+1_{λ∈Π} GH。

定理 CZ.1（加权支付恒等式）。严格有


证明。展开有限求和后，左侧等于 2me·Σ_Λw_λ+2GH·Σ_Πw_λ。分别代入 L 和 L/2 即得 (2me+GH)L。除

了有限求和的分配律，未使用任何算术几何假设。这里的 1/2 不是估计松弛，而是 Π 的总权重精确等于总权重

一半的条件。

定理 CZ.2（实际支付不超过预算）。若另有 w_λ≥0，且每个实际指数 E_λ≤e_λ，则


证明。对每个 λ，由 w_λ≥0 得 w_λE_λ≤w_λe_λ，求和再乘 2，应用 CZ.1。没有 w_λ≥0 就不能进行这一步

比较；也不能用一个没有证明的“复嵌入成对”口号代替 Π 权重恰为 L/2 的等式。证毕。

证明状态核对。CZ.1 与 CZ.2 作为实数有限和恒等式已闭合；但在 RH 主不等式中应用它们，必须从具体的无

穷位度量、CM 嵌入集合和正规化权重证明 Σ_Λw=L、Σ_Πw=L/2，并证明实际需要清除的格分母指数 E_λ 确

实受相应 e_λ 控制。本编尚未闭合这些深层几何输入。


                           

---


DA. 两个来源的格指数损失如何在同一处进行精确审计
如果有全局格链 R₂⊆R₁⊆R₀，且非零 T∈O_K 与整数 g≥1 满足 T^Q R₀⊆R₁⊆R₀、gR₁⊆R₂⊆R₁

（Q=me+GH），则逐素位的长度相加满足


证明。有限长度模的短正合列 0→R₁/R₂→R₀/R₂→R₀/R₁→0 在局部化后仍正合，长度可加。分别使用 CY.1 的

两段标量包含上界，再取和即可。于是总指数满足


由 DA.1 还可知：若一个素位同时不整除 (T) 与整数 g，则它没有这种纯标量分母损失。反过来说，如果 Theta

几何构造仍在该素位产生局部缺陷，那么这一缺陷不能归咎于本章的算子链分母或 Reynolds 投影，必须在另

一项估计里单独支付。

需要强调两个常见的误用。其一，DA.1 只涉及已经证明存在、方向正确且满秩的格链；仅有一个对单个向量

的清分母公式并不建立这种格链。其二，式中 log|N_{K/ℚ}(T)| 与 CZ.1 的 L=log T（用于无穷位权重的符号）

并非可直接互换，只有确认 T 是正有理整数且使用相容的数域归一化后，才有 log|N(T)|=n_K log T。


DB. V2.6 阶段验收与下一段对接
本编的代数部分已经追踪到固定源码 GlobalBoundRefinements.lean 的 chain_move、chain_key’、

matrix_commute、chain_coupled_key、chain_scalar、chain_denominator_coupled，进一步把

DualLevelType.lean 的 DenominatorPayment 展开成纯有限和恒等式。各处的确切指数和最重要的量词前

提都已列出；数值程序使用 Fraction / SymPy 的精确有理数进行非交换矩阵交织校验，并不替代一般证明。

此刻距离 RH 主不等式尚差的关键不是再次做算术求和，而是：逐层对象在 Theta Lift 中的具体定义，U 与 K

的实际交织等式、各局部格保持性的起源、CM 权重对称性，以及最后比较得到的像格是否具有足够秩。在这

些条件完成之前，整体完成度不宜因页数而人为上调。


                            

---


第二十五编：Theta 轨道质量、代表元独立及非退化性界限（V2.7）
固定源码：CocoSgt/riemann-hypothesis-lean，提交 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4；对

照 src/Formalism/ThetaLiftIndependence/Statement.lean、ThetaOrbitSums/OrbitSum.lean、

LatLiftIndep.lean、ClassRepsDefinite.lean。本章额外推导的 lcm 清分母为独立代数精化，不声称已被上游

RH 最终定理使用。


DC. 区分有限群轨道、正定格类以及 Theta 核
源码中出现三种不同的求和：有限群 H 在有限集 X 上的轨道和、正定格属中有限多个等距类的加权和，以及有

限核 K(i,j) 的变换及其复合。前者的归一化包含 1/|H|，第二种的每个类包含 1/|Aut(L)|，第三种在每层包含一

次中间权重。必须先证明相容性，不能直接将其中一种的等式当成另一种的具体几何结论。

正定格的整体等距群未必有限；不能对它写下 1/|G| 的有限平均。但正定格自身的自同构群有限；如果属中等

距类个数有限，类求和可以定义成有限和。两个有限性事实分别具有独立的数学来源。


DD. 轨道—稳定子和的完整推导
定理 DD.1。 设有限群 H 作用于有限集 X，F:X→Q 为轨道常值函数，Ω=X/H 为轨道集合，r_O 是任意代表，

则


证明。将左侧按轨道拆分成 Σ_O |O|F(r_O)/|H|。轨道—稳定子定理给出 |O||H_{r_O}|=|H|，逐项代入即得。换

代表 r_O 为 h·r_O 时，F 不变，稳定子变为 hH_{r_O}h⁻¹、阶不变，故两边与选取无关。这个证明只要求群

与集合有限、系数允许除以非零整数；不含自动形式或 Rallis 定理。证毕。

例 DD.2。 H=S₃，令 X 是 H/C₂（3 点）、H/C₃（2 点）和 H/H（1 点）的无交并。三个轨道的稳定子阶为 2、

3、6。取 F=1，则左边 |X|/|H|=6/6=1，右边为 1/2+1/3+1/6=1。若误把每个代表都乘 1/|H|，则只得到

3/6=1/2，可立即暴露错误。


DE. 正定格类权重与代表元无关性
设 K 为数域，V 为有限维 K-空间，O_K 为整数环，h 为相容的正定厄米形式，L 为满秩格。令 C 为其属中有限

个等距类，取每类一代表 M_C，并设 a_C=|Aut_h(M_C)|∈Z_{>0}。若 f、Θ 在全局等距变换下不变，则定义


定理 DE.1。 DE.1 不依赖代表的选取。事实上，若 N=gM_C，则 u↦gug⁻¹ 为 Aut_h(M_C)→Aut_h(N) 的显式

群同构，逆映射为 v↦g⁻¹vg。因此 a_C 不变；假设的 f、Θ 也不变。两个代表集各自恰好覆盖每个等距类一

次，逐类双射求和即可。

引理 DE.2（稳定子有限）。 若从 h 取得的底层实正定二次型 Q 使 M_C 为离散满秩格，则 Aut_h(M_C) 有

限。选格的 Z-基 e₁,…,e_N。任一等距格自同构将 e_i 送入有限集 {v∈M_C:Q(v)=Q(e_i)}；该集合是格与一个


---


紧椭球的交，因而有限。全部自同构由这些基的像决定，故数量有限。若 h 非正定则“等长格向量有限”不成

立，不能照搬。属的等距类数有限另需经典正定格有限类定理；此处并未重新证明它。


DF. 最小通用整数分母——lcm 优于全部乘积
定理 DF.1。 令 C 为非空有限集、a_C≥1 为整数，D=lcm_C a_C。对所有整数 z_C，


而且 D 是使此式对所有 z_C 同时成立的最小正整数。

证明。逐项 a_C|D，故左边是整数。反过来，若 D’ 对任意 z_C 都有该性质，对某固定 C₀ 取 z_{C₀}=1、其他

均为 0，则 a_{C₀}|D’；对所有 C₀ 重复，推出 D|D’。证毕。

推论 DF.2（素位最优预算）。 对每个素数 p，


这是唯一分解的直接结论。若 a_C=2、3、6，则最小通用分母 D=6，而直接乘积是 36。特定求和还可能因抵

消而需要更小分母，例如三个 z_C 都是 1 时，总和恰好为 1。但“对所有类系数同时有效”的最小分母仍是

6。


DG. 与每类链式分母结合后的精确界
令 A 为无挠 Z-模、A_Q=A⊗Q；每个 u_C∈A_Q，且已知 b_C∈Z_{>0} 满足 b_Cu_C∈A。将 a_C 理解为稳定

子阶，b_C 理解为该类核值的独立清分母倍数。令


定理 DG.1。 有


证明。每个 D_/(a_Cb_C) 是整数，故 D_u_C/a_C = D_*/(a_Cb_C)∈A。有限和仍在 A 中。证毕。X

定理 DG.2（通用最小性）。 若允许 A=Z 且 u_C 独立取遍 b_C⁻¹Z，则 D_* 为普遍成立所需的最小正整数：对

每个 C₀ 取 u_{C₀}=1/b_{C₀}、其余为 0，即迫使 a_{C₀}b_{C₀}|D’；取 lcm 即得。

推论 DG.3。 对每个素数 p，


如果 b_C 都是同一个 B，则 D_*=B·lcm_Ca_C；如果 b_C 不同，则 max(v_p(a_C)+v_p(b_C)) 与 max

v_p(a_C)+max v_p(b_C) 一般不相等。后一式仅为可能较弱的上界。

必要边界。 V2.6 的链式清分母可以提供候选 b_C，但必须先针对真正的 Theta 核证明各类输入满足其算子交

织和格保持前提。更重要的是 DG.2 只证明一个给定和（或一族给定和）属于 A，没有证明任何两个满秩格之

间的包含关系。要套用 V2.6 的共体积界，必须另证足够秩的像格、含入方向与局部满秩性。


---


DH. 有限加权 Theta 核的伴随与复合公式
设 I、J 是有限集，a_i、b_j 为严格正实权，K(i,j)∈C。定义


定理 DH.1（加权核伴随）。


证明。展开左边，利用权重的实数性将复共轭移进有限和，得到 Σ_iΣ_j a_i

b_j·overline(f_i)·overline(K(i,j))·g_j。交换求和顺序，恰是右边。这与源码 kerOp、kerAdj、wip 的抽象

写法一致，但仅此不能建立其具体核是否满足所需函数空间收敛性。证毕。

定理 DH.2（核复合）。 若再给出第三有限集 M、另一个核 L(j,k)，则二次核为


证明。展开两次核变换并交换有限求和，内层指标 j 的权重 b_j 恰好出现一次。若在此处重复或遗漏 b_j，就

会破坏伴随与复合的相容性。证毕。

定理 DH.3（带权 Hilbert–Schmidt 界）。 记 ||f||²_I=Σ_i a_i|f_i|²，则


证明。对固定 j，用 Cauchy–Schwarz 作用于 (sqrt(a_i)f_i)_i 与 (sqrt(a_i)K(i,j))_i，得到 |(Kf)_j|²≤||f||

²_I·Σ_i a_i|K(i,j)|²。乘 b_j 后对 j 求和即可。注意右端可大可小：要得到主不等式 (M) 使用的数量级，尚需实

际核函数的高斯衰减或算术界，而不是抽象线性代数。证毕。


DI. Rallis 内积恒等式与非退化性的精确逻辑关系
令 E、F 为有限维复内积空间，θ:E→F 为线性映射，S⊆E 为非零子空间。假定存在 α∈C，使任意 x,y∈S 满足


源中抽象 RallisHyp 的标量写作 α=c·L·∏_vZ_v。这一写法并不自动证明 α 非零，更不意味着每个局部因子

已拥有正性证明。

定理 DI.1（标量正性与零映射）。 取任意非零 x∈S，有 α=||θx||²/||x||²，因此 α 必为非负实数。若 α=0，则 θ|

_S=0；如果 θ|_S 非零，则 α>0。

定理 DI.2（正标量导致单射及 Gram 缩放）。 若 α>0，范数恒等式 ||θx||²=α||x||² 说明 θ|S 单射。取 S 的任意

基 e₁,…,e_d，则两组 Gram 矩阵满足 G{θ(e)}=α G_e，故


                                

---


此处仅证明一处复内积的 Gram 行列式缩放（对应实体积乘 α^{d/2}）。将其转化为全球 O_K-格的范数和高度

界，需要另外处理所有无穷位、有限位、局部指数及度量正规化。证毕。

定理 DI.3（伴随不变性是必要前提）。 设 P_S 是 E→S 的正交投影。DI.1 在内积非退化条件下等价于


证明。对每个 y∈S，〈θ†θx,y〉=〈θx,θy〉=α〈x,y〉。两边相减得到 θ†θx−αx 与 S 正交，等价于其在 S 上

的投影为零。只有另行证明 θ†θ(S)⊆S，才可去掉 P_S 并推出 θ†θx=αx。这正是源码 RallisAdj 的另一条独

立输入。证毕。

反例 DI.4。 E=C²、F=C，令 S=span{(1,0)}，θ(x,y)=x+y。θ 在 S 上保持内积，故 DI.1 以 α=1 成立；但

θ†θ(1,0)=(1,1)≠(1,0)。问题来自 θ†θ(1,0)∉S。如果忽略伴随像稳定性，便会把“仅在 S 上的矩阵元等

式”错误升级成“整个 E 内的向量等式”。

反例 DI.5（核质量与满秩无关）。 任意有限集和正权重，取 K(i,j)=0，则轨道质量、代表元无关、核伴随、核

复合、清分母等全部形式代数结论成立，但核映射为零。即便 K(i,j)=1 且 |I|=|J|=2，核映射非零却只有秩 1。

这表明主不等式 (M) 中的多映射像空间秩估计，必须由另外的迹公式与几何信息承担。


DJ. 独立精确算术校验
配套 theta_mass_and_adjoint_exact_certificate_v27.py 使用 Python 的 Fraction 在 S₃ 三类轨道上验证 |

X|/|H|=Σ1/|Stab|=1、lcm(2,3,6)=6<2·3·6=36，并用有理矩阵检验带权核的伴随、两层核复合、Hilbert–

Schmidt 平方不等式以及 DI.4 的伴随不稳定反例。证书是有限模型的反错检查，不能替代上面的通用证明，

也不能代替具体的无限维 Theta Lift 分析。


DK. 与既有 164 页讲解稿的互补关系与验收
Michael O. Rubinstein 2026-11-21 工作稿 The Alpöge–Claude proof of the Riemann hypothesis explained

for the Riemann zeta function：https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-

paper.pdf。其 Part II/III 已把 (M) 推出 RH 的解析步骤与若干局部估计写成自然语言；但明确承认 (M) 自身的

算术核心仍需引用 Lean 开发中的深层输入。我们本编不把这部讲解稿当作 (M) 已经被传统数学证明的证据。

已闭合的范围：有限轨道和、给定有限正定类集时的代表独立、最小整数清分母、逐类双层分母、有限加权核

伴随及复合、HS 界、Rallis 正标量的条件性后果与反例。

未闭合的范围：正定格类与具体 Theta 构造的全部联系、自动形式函数空间的收敛性及度量比较、逐处局部积

分性与几何交织、Rallis 局部因子非零性、像空间满秩与多映射一般位置、全球格的正确包含方向、主算术不

等式 (M) 及其 Dirichlet 扭曲。与 V2.6 相同：清除某类核值的分母，决不等于建立了足够秩的像格的全球共体

积比较。
