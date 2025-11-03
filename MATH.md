# 2-person UNO POMDP (Player1 perspective)

## Deck Structure
$$
\mathcal{C}=\{\text{red},\text{yellow},\text{blue},\text{green}\},\qquad
K=\{K_1,\dots,K_{108}\}
$$
(each $K_i$ encodes color and rank/type; 4 wilds +4 and 4 wildcards are colorless).

---

## System Definitions (POMDP)

### State space $S$
$$
s=\{H_1,H_2,K_d,K_p,K_t,\mathrm{turn},\mathrm{meta}\}\in S
$$
where $H_1$ (Player1 hand, known), $H_2$ (Player2 hand, hidden), $K_d$ (ordered draw deck), $K_p$ (discard pile excluding top), $K_t$ (top card including declared color), $\mathrm{turn}\in\{1,2\}$, $\mathrm{meta}$ (other flags). Terminal iff $|H_i|=0$ for some $i$.

---

### Observation space $\Omega$
Player1 observes:
$$
o=\{H_1,\;N_2,\;N_d,\;K_p,\;K_t,\;\mathrm{meta_{obs}}\}\in\Omega
$$
with $N_2=|H_2|,\;N_d=|K_d|$. Observation model:
$$
P(o\mid s)=\mathbf{1}\big(o \text{ matches visible components of } s\big).
$$

(Partial reveals allowed by making $P(o\mid s)$ non-binary as needed.)

---

### Action space $A$
Let $\mathcal C$ be colors. Actions:
$$
A=A_{\text{draw}}\cup A_{\text{play}}
$$
$$
A_{\text{draw}}=\{D_0,D_1,D_2,D_4\},\qquad
A_{\text{play}}=\{(P,j,c):j\in H_1,\ c\in\mathcal C\}.
$$
Legal plays must match top card color or rank/type or be wilds (see legal constraint below). For non-wild $j$, $c=\text{color}(j)$. Wilds allow any $c\in\mathcal C$.

---

## Legal-action constraint (formal)
For state $s$ and play action $(P,j,c)$:
$$
\text{legal}(s,(P,j,c))=
\begin{cases}
1 & \text{if } j \text{ is wild, or } \text{color}(j)=\text{declared\_color}(K_t),\\
  &\quad\text{or } \text{rank}(j)=\text{rank}(K_t)\\
0 & \text{otherwise}
\end{cases}
$$
If illegal, action is disallowed (or mapped to a forced draw depending on implementation). (Reverse acts as SKIP for 2 players; stacking and +4 challenge **not** modeled.)

---

## Declared color in $K_t$
Treat $K_t$ as pair $(\text{card},\text{declared\_color})$. When playing wild $j$ with declared color $c$:
$$
K_t\leftarrow (j,c).
$$

---

## Transition probabilities $P(s'\mid s,a)$
Decompose into Player1 immediate effect then Player2 response:
$$
s \xrightarrow{a,\xi} s^+ = f_{\text{p1}}(s,a,\xi)
$$
$$
s^+ \xrightarrow{a_2,\zeta} s' = f_{\text{p2}}(s^+,a_2,\zeta)
$$
Then
$$
P(s'\mid s,a)=\sum_{a_2}\int_{\xi,\zeta}\mathbf{1}[s'=f_{\text{p2}}(f_{\text{p1}}(s,a,\xi),a_2,\zeta)]\;
\pi_2(a_2\mid s^+)\;p(\xi,\zeta\mid s,a,a_2)\,d\xi\,d\zeta.
$$
Here $\xi,\zeta$ capture randomness from draws/reshuffles. Reshuffle: if $|K_d|<k$ and a draw of $k$ required, set $K_d\leftarrow\text{shuffle}(K_p)$ (keeping $K_t$ on top) before drawing.

---

## Belief $b$
Belief over full states:
$$
b(s)=P(s\mid h_t)
$$
Compact representation (known components removed):
$$
b_{\mathrm{comp}}(H_2,K_d)=P(H_2,K_d\mid H_1,K_p,K_t,\text{history}).
$$
Often one marginalizes deck ordering and stores $b_H(H_2)$ only:
$$
b(H_2)=\sum_{K_d} b_{\mathrm{comp}}(H_2,K_d).
$$

---

## Exact belief marginal for a single card
Let $U=K\setminus(H_1\cup K_p\cup\{K_t\})$ be unseen multiset with $|U|=m$. If opponent has $n_2$ cards and prior is uniform over subsets of size $n_2$:
$$
\Pr(c\in H_2)=\frac{n_2}{m}\quad\text{for $c\in U$}.
$$
More generally:
$$
\Pr(c\in H_2)=\sum_{H_2:\,c\in H_2} b(H_2).
$$

---

## Belief prediction & Bayes update (general)
Prediction:
$$
\bar b_{t+1}(s')=\sum_{s\in S} P(s'\mid s,a_t)\,b_t(s).
$$
Update:
$$
b_{t+1}(s')=\tau(b_t,a_t,o_{t+1})(s')=\frac{P(o_{t+1}\mid s')\,\bar b_{t+1}(s')}{\sum_{\tilde s}P(o_{t+1}\mid\tilde s)\,\bar b_{t+1}(\tilde s)}.
$$

---

## Belief update when opponent plays a visible card $c$
If observation $o_{t+1}$ includes opponent playing card $c$, then for hypotheses over $H_2$:
$$
\bar b(H_2')=\sum_{H_2} \Pr(H_2'\mid H_2,\text{opponent plays }c, a_t)\,b(H_2),
$$
with
$$
\Pr(H_2'\mid H_2,\text{opponent plays }c, a_t)=
\begin{cases}
\pi_2(\text{play }c\mid H_2,s^+), & \text{if } H_2'=H_2\setminus\{c\}\\[4pt]
0,&\text{otherwise.}
\end{cases}
$$
After computing $\bar b$ restrict to those $H_2'$ consistent with observed counts and renormalize.

If opponent play probability is uniform over legal cards:
$$
\pi_2(\text{play }c\mid H_2,s^+)=
\frac{\mathbf{1}(c\in H_2)\,\mathbf{1}(\text{legal}(s^+,(P,c,\cdot)))}{\sum_{j\in H_2}\mathbf{1}(\text{legal}(s^+,(P,j,\cdot)))}.
$$

---

## Belief update for unobserved opponent draw of $K$ cards
Let unknown pool $U$ size $m$. Opponent holds $n_2$ before draw. They draw $k$ cards unseen. Predicted distribution over new $H_2'$:
$$
\bar b(H_2')=\sum_{H_2}\Pr(H_2'\mid H_2,\text{draw }k)\,b(H_2),
$$
where $\Pr(H_2'\mid H_2,\text{draw }k)$ is computed by combinatorics sampling without replacement from $U\setminus H_2$. If $H_2'$ differs from $H_2$ by acquiring a subset $D$ of size $k'\le k$:
$$
\Pr(H_2'\mid H_2,\text{draw }k)=
\frac{\binom{|U\setminus H_2|}{k'}\cdot\text{[ways to choose specific }D\text{ producing }H_2']}{\binom{|U|}{k}}.
$$
In the simplified aggregated form (marginals) use hypergeometric: for a type/subset $S\subset U$,
$$
\Pr(\text{draw }x\text{ from }S)=\frac{\binom{|S|}{x}\binom{m-|S|}{k-x}}{\binom{m}{k}}.
$$

---

## Belief factorization (practical)
Approximate factorization:
$$
b(H_2,K_d)\approx b_H(H_2)\;b_D(K_d\mid H_2)
$$
or marginalize deck ordering:
$$
b(H_2,K_d)\approx b_H(H_2)\;\frac{1}{\#\{\text{orders consistent}\}}.
$$

---

## Observation model for partial reveals
If only counts or partial info observed:
$$
P(o\mid s)=\mathbf{1}(|H_2|=N_2,\ |K_d|=N_d,\ \text{visible parts match}) .
$$
Or more generally soft observation:
$$
P(o\mid s)=\prod_{i}\ell_i(o_i\mid s_i)
$$
with per-component likelihoods $\ell_i$.

---

## Probability of observation under belief (explicit)
Necessary for normalization and planning:
$$
P(o\mid b,a)=\sum_{s'} P(o\mid s')\sum_s P(s'\mid s,a)\,b(s)
= \sum_{s'} P(o\mid s')\,\bar b_{t+1}(s').
$$

---

## Marginal probability computations used in heuristics
Probability opponent has at least one card of color $c$. Let $m$ be unseen cards and $m_c$ unseen cards of color $c$. Under uniform prior:
$$
\Pr(\exists j\in H_2:\ \text{color}(j)=c)=1-\frac{\binom{m-m_c}{n_2}}{\binom{m}{n_2}}.
$$
Probability opponent holds exactly $x$ copies of type $t$ (multiplicity $m_t$ in $U$):
$$
\Pr(X_t=x)=\frac{\binom{m_t}{x}\binom{m-m_t}{n_2-x}}{\binom{m}{n_2}}.
$$

---

## Belief pruning
Given belief $b$ over hypotheses (e.g., subsets $H_2$), prune low-probability support:
$$
\mathcal S_\epsilon=\{s:\ b(s)>\epsilon\},\qquad b_{\text{pruned}}(s)=\frac{b(s)\mathbf{1}(s\in\mathcal S_\epsilon)}{\sum_{\tilde s\in\mathcal S_\epsilon} b(\tilde s)}.
$$

---

## Reward & Value (unchanged)
Immediate reward $R(s,a)$, expected reward:
$$
R(b,a)=\sum_s b(s)\,R(s,a).
$$
Belief-space Bellman:
$$
V^*(b)=\max_a\Big[R(b,a)+\gamma\sum_o P(o\mid b,a)\,V^*(\tau(b,a,o))\Big].
$$

---

## Notes / modeling choices (constraints)
- No stacking of +2/+4.  
- No +4 challenge.  
- REVERSE acts as SKIP for 2 players.  
Model these by deterministic rules inside $f_{\text{p1}},f_{\text{p2}}$.
