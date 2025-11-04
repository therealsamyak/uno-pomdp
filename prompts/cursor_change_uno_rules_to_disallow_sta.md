# Change uno rules to disallow stacking

_Exported on 11/4/2025 at 11:12:14 PST from Cursor (2.0.43)_

---

**User**

@MATH.md (1-400) change this to follow original uno rules where there is no stacking of +2 and +4 regardless of if you technically could

---

**Cursor**

Updating the document to remove stacking of +2 and Wild+4 cards. Checking relevant sections:

Updating the legal action set to disallow stacking: when a draw penalty is active, only Draw is allowed.

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t = (d_1, d_2, \ldots, d_{n_d}) \in K^{n_d}$: Ordered draw deck (top = $d_1$)
- $P^t = (p_1, p_2, \ldots, p_{n_p}) \in K^{n_p}$: Ordered discard pile (top = $p_{n_p}$, bottom = $p_1$)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = (n_{\text{draw}}, \text{dir}) \in \mathbb{N}_0 \times \{1, -1\}$:
  - $n_{\text{draw}}$: Accumulated draw penalty (from +2 or Wild+4)
  - $\text{dir}$: Direction (irrelevant in 2-player; included for completeness)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup \{d_i : i \in [n_d]\} \cup \{p_i : i \in [n_p]\} \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Full discard pile (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Let $D' = \text{shuffle}(p_1, \ldots, p_{n_p - 1})$ (all discard except top)
   - Set $D^{t+} = D' \circ D^t$ (concatenate), $P^{t+} = (p_{n_p})$
3. Draw top $k$ cards from $D^{t+}$: $(d_1, \ldots, d_k)$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = (d_{k+1}, \ldots)$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \circ (c)$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Updating the special rules section to clarify the no-stacking rule:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t = (d_1, d_2, \ldots, d_{n_d}) \in K^{n_d}$: Ordered draw deck (top = $d_1$)
- $P^t = (p_1, p_2, \ldots, p_{n_p}) \in K^{n_p}$: Ordered discard pile (top = $p_{n_p}$, bottom = $p_1$)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = (n_{\text{draw}}, \text{dir}) \in \mathbb{N}_0 \times \{1, -1\}$:
  - $n_{\text{draw}}$: Accumulated draw penalty (from +2 or Wild+4)
  - $\text{dir}$: Direction (irrelevant in 2-player; included for completeness)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup \{d_i : i \in [n_d]\} \cup \{p_i : i \in [n_p]\} \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Full discard pile (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Let $D' = \text{shuffle}(p_1, \ldots, p_{n_p - 1})$ (all discard except top)
   - Set $D^{t+} = D' \circ D^t$ (concatenate), $P^{t+} = (p_{n_p})$
3. Draw top $k$ cards from $D^{t+}$: $(d_1, \ldots, d_k)$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = (d_{k+1}, \ldots)$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \circ (c)$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Checking for linting issues:

Updated the document to remove stacking of +2 and Wild+4 cards.

**Changes made:**

1. **Legal action set (lines 91-95)**: When `n_draw > 0`, only `Draw` is legal (removed the option to play +2 or Wild+4 to increase the penalty).

2. **Special rules clarification (line 112)**: Clarified that stacking is not allowed—when a draw penalty is active, you can only draw.

The transition dynamics remain unchanged; they handle penalty mechanics, and the legal action set now enforces no stacking.

---

**User**

direction doesn't matter so remove it bro

---

**Cursor**

Removing the direction component from the state space; it's irrelevant in 2-player games.

Removing the direction component from the state space:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t = (d_1, d_2, \ldots, d_{n_d}) \in K^{n_d}$: Ordered draw deck (top = $d_1$)
- $P^t = (p_1, p_2, \ldots, p_{n_p}) \in K^{n_p}$: Ordered discard pile (top = $p_{n_p}$, bottom = $p_1$)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup \{d_i : i \in [n_d]\} \cup \{p_i : i \in [n_p]\} \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Full discard pile (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Let $D' = \text{shuffle}(p_1, \ldots, p_{n_p - 1})$ (all discard except top)
   - Set $D^{t+} = D' \circ D^t$ (concatenate), $P^{t+} = (p_{n_p})$
3. Draw top $k$ cards from $D^{t+}$: $(d_1, \ldots, d_k)$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = (d_{k+1}, \ldots)$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \circ (c)$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Checking for other references to direction:

Removed the direction component. The `meta^t` state is now just `n_{\text{draw}} \in \mathbb{N}_0` instead of a tuple.

---

**User**

is this pomdp representation even good? it seems very complicated

---

**Cursor**

Reviewing the POMDP representation to assess its complexity and identify simplifications.

Analyzing complexity issues and potential simplifications:

Identifying complexity issues and simplifications:

Main complexity issues:

1. Ordered deck $D^t$: Tracks exact card ordering, creating $O(n!)$ states. For a 108-card deck, this is intractable.
2. Ordered discard pile $P^t$: Full ordering isn’t needed; only the top card (and possibly counts) matters.
3. Two-phase transitions: Correct but adds notation overhead.

The doc already acknowledges this: Section 6.1 says "Often we ignore deck ordering" — so the implementation should do this.

Simplified representation:

- Deck: multiset (counts per card type) instead of ordered sequence
- Discard: top card + counts (or just top card)
- Opponent hand: multiset (exact cards, not order)

Updating the document to reflect this simplification:

Simplifying: switching to multiset representations for the deck and discard pile.

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup \{d_i : i \in [n_d]\} \cup \{p_i : i \in [n_p]\} \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Full discard pile (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Let $D' = \text{shuffle}(p_1, \ldots, p_{n_p - 1})$ (all discard except top)
   - Set $D^{t+} = D' \circ D^t$ (concatenate), $P^{t+} = (p_{n_p})$
3. Draw top $k$ cards from $D^{t+}$: $(d_1, \ldots, d_k)$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = (d_{k+1}, \ldots)$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \circ (c)$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Updating the consistency constraint and transition dynamics:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Full discard pile (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Let $D' = \text{shuffle}(p_1, \ldots, p_{n_p - 1})$ (all discard except top)
   - Set $D^{t+} = D' \circ D^t$ (concatenate), $P^{t+} = (p_{n_p})$
3. Draw top $k$ cards from $D^{t+}$: $(d_1, \ldots, d_k)$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = (d_{k+1}, \ldots)$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \circ (c)$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Updating the observation space and transition dynamics:

Updating transition dynamics for multiset representation:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Full discard pile (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Sample uniformly from $P^t \setminus \{c_{\text{top}}\}$ (all discard except top card)
   - Set $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$, $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \circ (c)$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Full discard pile (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Sample uniformly from $P^t \setminus \{c_{\text{top}}\}$ (all discard except top card)
   - Set $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$, $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Sample uniformly from $P^t \setminus \{c_{\text{top}}\}$ (all discard except top card)
   - Set $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$, $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ is deterministic given draw randomness:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{|D^t|!} & \text{if reshuffle occurs (uniform over permutations)} \\
  1 & \text{otherwise (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Sample uniformly from $P^t \setminus \{c_{\text{top}}\}$ (all discard except top card)
   - Set $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$, $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

**Further Marginalization (Common Approximation):**

Often we ignore deck ordering and represent:
$$b_t(H_2, \mathcal{D}) = P(H_2^t = H_2, D^t \sim \text{Unif}(\mathcal{D}) \mid h_t)$$

where $\mathcal{D}$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Updating Section 6.1 to reflect that we're already using multiset representation:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Sample uniformly from $P^t \setminus \{c_{\text{top}}\}$ (all discard except top card)
   - Set $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$, $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), we have:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

where $D$ is the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Fixing the duplicate and checking Section 8:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Sample uniformly from $P^t \setminus \{c_{\text{top}}\}$ (all discard except top card)
   - Set $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$, $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed over $(m_0 - 7)!$ permutations of $U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Sample uniformly from $P^t \setminus \{c_{\text{top}}\}$ (all discard except top card)
   - Set $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$, $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Fixing the reshuffle step:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered)
- $P^t \subseteq K$: Discard pile (multiset, unordered; only top card $c_{\text{top}}$ matters for playability)
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

```markdown
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
```

**Simplified state representation:**

- **Deck**: Multiset (unordered) instead of ordered sequence
- **Discard**: Multiset (unordered) instead of ordered sequence
- Removed unnecessary ordering complexity

**Benefits:**

- State space reduced from $O(n!)$ to $O(2^n)$ for deck size $n$
- Matches the practical approach (Section 6 already noted ignoring deck ordering)
- Easier to implement: use multisets/counts instead of sequences

**What stayed the same:**

- Belief tracking over opponent hand (still $\binom{m}{n_2}$ possibilities)
- Two-phase transitions (Player 1 → Player 2)
- Observation and action spaces

The representation is now simpler and more practical while preserving the core POMDP structure. The complexity now comes from the belief space (opponent's hand), not the deck ordering.

---

**User**

if the deck and discard are multisets, how do we know what the top cards of each are? do we just probability random it or something? i am somewhat confused. i understand that we can represent it as a multiset so no need to change that, its just im not sure how to maintain the top part

---

**Cursor**

Clarifying: the deck is a multiset, so there's no "top" card. We'll sample uniformly when drawing. The discard top card is already tracked in $T^t$. Updating the document to make this explicit:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
3. Sample $k$ cards uniformly without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Updating the drawing section to clarify this:

Clarifying the drawing section:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t \cup \{c_{\text{top}}\} = K$$
(partition of full deck, accounting for multiplicities)

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Fixing the consistency constraint: since $c_{\text{top}}$ is in $P^t$, we shouldn't count it twice:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool**:
$$U_t = K \setminus (H_1^t \cup P^t \cup \{c_{\text{top}}\})$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Checking the unseen pool definition:

Fixing the unseen pool definition:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

**Summary of clarifications:**

1. **Draw deck ($D^t$)**: Multiset (unordered). When drawing, sample uniformly at random from the multiset. No "top" card; each card in $D^t$ has equal probability.

2. **Discard pile ($P^t$)**: Multiset (unordered), but the top card $c_{\text{top}}$ is explicitly tracked in $T^t$ for playability. The rest of $P^t$ is unordered.

3. **Top card ($c_{\text{top}}$)**: Explicitly stored in $T^t$ and is part of $P^t$ (it's the top of the discard pile).

**How it works:**

- **Drawing**: Uniform random sampling from $D^t$ (no ordering needed)
- **Playing**: Add card to $P^t$ and set it as the new $c_{\text{top}}$ in $T^t$
- **Top card tracking**: $c_{\text{top}}$ is always in $P^t$ and separately tracked in $T^t$ for quick playability checks

This avoids tracking deck order while preserving the information needed (top discard card for playability, and uniform sampling for draws).

---

**User**

what is the indicator 1[-] e 0, 1 or whatever that is

---

**Cursor**

The indicator function $\mathbb{1}[\cdot]$ (also called the characteristic function or Iverson bracket). Checking how it's used in the document:

Adding a brief explanation in the document:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Computational Methods

### 11.1. Particle Filter Representation

Approximate belief $b_t$ with $N$ particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Prediction:** For each particle $s^{(i)}$, sample $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$

**Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$

**Resampling:** Normalize weights and resample to prevent degeneracy

### 11.2. POMCP (Partially Observable Monte Carlo Planning)

Build a belief tree using Monte Carlo sampling:

1. **Selection:** Traverse tree using UCB until reaching a leaf
2. **Expansion:** Add new action node
3. **Simulation:** Rollout from current belief using rollout policy
4. **Backpropagation:** Update Q-values along the path

UCB action selection:
$$a^* = \arg\max_{a} \left\{Q(h, a) + c \sqrt{\frac{\ln N(h)}{N(h, a)}}\right\}$$

where $h$ is the history node, $N(h)$ is visit count, $Q(h, a)$ is average return.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

The **indicator function** $\mathbb{1}[\cdot]$ (Iverson bracket) converts a boolean condition to 1 or 0:

- $\mathbb{1}[\text{true condition}] = 1$
- $\mathbb{1}[\text{false condition}] = 0$

**Examples from your document:**

- $\mathbb{1}[c_2 \in H_2]$ = 1 if card $c_2$ is in hand $H_2$, 0 otherwise
- $\mathbb{1}[\text{proj}(s_t) = o_t]$ = 1 if the projection of state $s_t$ equals observation $o_t$, 0 otherwise
- $\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]$ = 1 if action $a$ is legal in state $s$, 0 otherwise

It's a compact way to express conditional probabilities, set membership, and equality checks in formulas.

---

**User**

we will do a particle filter approach or a bayes filter approach because its discrete. however there might be a lot of different states hence why we will likely do a particle filter appoach

NO MONTE CARLO (for now)

---

**Cursor**

Clarifying the approach: using a particle filter or Bayes filter for belief tracking (no Monte Carlo planning for now). Updating the document to reflect this:

Updating Section 11 to focus on belief tracking (no Monte Carlo planning):

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Belief Tracking Methods

Since the state space is large (due to opponent hand and deck uncertainty), we use approximate belief tracking. Two approaches:

### 11.1. Exact Bayes Filter (Discrete)

For tractable state spaces, maintain exact belief distribution:

**Prediction Step:**
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

**Update Step:**
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

**Limitation:** Requires enumerating all states in belief support, which grows exponentially with opponent hand size.

### 11.2. Particle Filter (Approximate)

Approximate belief $b_t$ with $N$ weighted particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Algorithm:**

1. **Prediction:** For each particle $s^{(i)}$, sample successor state $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$
2. **Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$
3. **Normalize:** $\tilde{w}^{(i)} = \frac{w'^{(i)}}{\sum_j w'^{(j)}}$
4. **Resampling:** Sample $N$ new particles from $\{(s'^{(i)}, \tilde{w}^{(i)})\}$ to prevent weight degeneracy

**Advantages:** Handles large state spaces efficiently; fixed computational cost $O(N)$ per update.

**Note:** Monte Carlo planning methods (e.g., POMCP) are excluded for now; focus is on belief tracking only.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Updated Section 11 to focus on **belief tracking only** (no Monte Carlo planning):

**Changes:**

1. **11.1 Exact Bayes Filter** — For discrete, tractable cases
2. **11.2 Particle Filter** — For large state spaces (likely your case)
3. **Removed POMCP** — Monte Carlo planning excluded for now
4. **Added note** — Planning methods excluded; focus on belief tracking

The document now reflects that you'll use either exact Bayes filter or particle filter for belief updates, with Monte Carlo planning excluded.

---

**User**

look at all the math and make sure its accurate and gives us enough information to actually code a full uno solver later on based on the information in the math. don't comment on whether more information would be helpful or if we considered x it would make it better etc., just comment on if the information we have now is enough to create an uno solver

---

**Cursor**

Reviewing the document for mathematical accuracy and completeness for implementation:

Checking for mathematical errors and missing implementation details:

Identifying several issues that need fixes:

Fixing several issues:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$, yielding $s_{t+1}$.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Belief Tracking Methods

Since the state space is large (due to opponent hand and deck uncertainty), we use approximate belief tracking. Two approaches:

### 11.1. Exact Bayes Filter (Discrete)

For tractable state spaces, maintain exact belief distribution:

**Prediction Step:**
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

**Update Step:**
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

**Limitation:** Requires enumerating all states in belief support, which grows exponentially with opponent hand size.

### 11.2. Particle Filter (Approximate)

Approximate belief $b_t$ with $N$ weighted particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Algorithm:**

1. **Prediction:** For each particle $s^{(i)}$, sample successor state $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$
2. **Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$
3. **Normalize:** $\tilde{w}^{(i)} = \frac{w'^{(i)}}{\sum_j w'^{(j)}}$
4. **Resampling:** Sample $N$ new particles from $\{(s'^{(i)}, \tilde{w}^{(i)})\}$ to prevent weight degeneracy

**Advantages:** Handles large state spaces efficiently; fixed computational cost $O(N)$ per update.

**Note:** Monte Carlo planning methods (e.g., POMCP) are excluded for now; focus is on belief tracking only.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Clarifying Player 2's transitions and terminal state checking:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same rules as Player 1** (Section 5.1), but applied to Player 2:

- If $a_2 = \text{Draw}$: Draw $k = \max(1, n_{\text{draw}})$ cards, reset penalty, set $\text{turn} = 1$
- If $a_2 = (c, \tilde{c})$: Remove $c$ from $H_2$, update $T$ and $P$, handle card effects, set turn accordingly

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** After any player's action, if $|H_1| = 0$ or $|H_2| = 0$, the game terminates.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial Belief $b_0$

At $t = 0$, Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \emptyset, n_2^0 = 7, n_d^0)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Belief Tracking Methods

Since the state space is large (due to opponent hand and deck uncertainty), we use approximate belief tracking. Two approaches:

### 11.1. Exact Bayes Filter (Discrete)

For tractable state spaces, maintain exact belief distribution:

**Prediction Step:**
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

**Update Step:**
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

**Limitation:** Requires enumerating all states in belief support, which grows exponentially with opponent hand size.

### 11.2. Particle Filter (Approximate)

Approximate belief $b_t$ with $N$ weighted particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Algorithm:**

1. **Prediction:** For each particle $s^{(i)}$, sample successor state $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$
2. **Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$
3. **Normalize:** $\tilde{w}^{(i)} = \frac{w'^{(i)}}{\sum_j w'^{(j)}}$
4. **Resampling:** Sample $N$ new particles from $\{(s'^{(i)}, \tilde{w}^{(i)})\}$ to prevent weight degeneracy

**Advantages:** Handles large state spaces efficiently; fixed computational cost $O(N)$ per update.

**Note:** Monte Carlo planning methods (e.g., POMCP) are excluded for now; focus is on belief tracking only.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Adding initial state setup:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same rules as Player 1** (Section 5.1), but applied to Player 2:

- If $a_2 = \text{Draw}$: Draw $k = \max(1, n_{\text{draw}})$ cards, reset penalty, set $\text{turn} = 1$
- If $a_2 = (c, \tilde{c})$: Remove $c$ from $H_2$, update $T$ and $P$, handle card effects, set turn accordingly

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** After any player's action, if $|H_1| = 0$ or $|H_2| = 0$, the game terminates.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial State and Belief $b_0$

### 8.1. Initial Game Setup

At $t = 0$, the game is initialized as follows:

1. **Deal:** Shuffle deck $K$ uniformly. Deal 7 cards to each player: $H_1^0$ and $H_2^0$ (each of size 7).
2. **Top Card:** Draw one card from remaining deck to start discard pile: $c_{\text{top}}^0$. If it's a Wild or Wild+4, reshuffle and redraw.
3. **Initial State:** $s_0 = (H_1^0, H_2^0, D^0, P^0, T^0, \text{turn}^0 = 1, n_{\text{draw}}^0 = 0)$
   - $D^0 = K \setminus (H_1^0 \cup H_2^0 \cup \{c_{\text{top}}^0\})$ (remaining deck)
   - $P^0 = \{c_{\text{top}}^0\}$ (discard pile contains only top card)
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (or declared color if wild)

### 8.2. Initial Belief Distribution

Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \{c_{\text{top}}^0\}, n_2^0 = 7, n_d^0 = |D^0|)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1:

$$
R(s, a) = \begin{cases}
+1 & \text{if } s \text{ results in } |H_1| = 0 \text{ (Player 1 wins)} \\
-1 & \text{if } s \text{ results in } |H_2| = 0 \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Belief Tracking Methods

Since the state space is large (due to opponent hand and deck uncertainty), we use approximate belief tracking. Two approaches:

### 11.1. Exact Bayes Filter (Discrete)

For tractable state spaces, maintain exact belief distribution:

**Prediction Step:**
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

**Update Step:**
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

**Limitation:** Requires enumerating all states in belief support, which grows exponentially with opponent hand size.

### 11.2. Particle Filter (Approximate)

Approximate belief $b_t$ with $N$ weighted particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Algorithm:**

1. **Prediction:** For each particle $s^{(i)}$, sample successor state $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$
2. **Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$
3. **Normalize:** $\tilde{w}^{(i)} = \frac{w'^{(i)}}{\sum_j w'^{(j)}}$
4. **Resampling:** Sample $N$ new particles from $\{(s'^{(i)}, \tilde{w}^{(i)})\}$ to prevent weight degeneracy

**Advantages:** Handles large state spaces efficiently; fixed computational cost $O(N)$ per update.

**Note:** Monte Carlo planning methods (e.g., POMCP) are excluded for now; focus is on belief tracking only.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Clarifying the reward function and terminal state checking:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same rules as Player 1** (Section 5.1), but applied to Player 2:

- If $a_2 = \text{Draw}$: Draw $k = \max(1, n_{\text{draw}})$ cards, reset penalty, set $\text{turn} = 1$
- If $a_2 = (c, \tilde{c})$: Remove $c$ from $H_2$, update $T$ and $P$, handle card effects, set turn accordingly

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** After any player's action, if $|H_1| = 0$ or $|H_2| = 0$, the game terminates.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if drawing } k \text{ cards (uniform over subsets)} \\
  1 & \text{if playing a card (deterministic)}
  \end{cases}
  $$

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial State and Belief $b_0$

### 8.1. Initial Game Setup

At $t = 0$, the game is initialized as follows:

1. **Deal:** Shuffle deck $K$ uniformly. Deal 7 cards to each player: $H_1^0$ and $H_2^0$ (each of size 7).
2. **Top Card:** Draw one card from remaining deck to start discard pile: $c_{\text{top}}^0$. If it's a Wild or Wild+4, reshuffle and redraw.
3. **Initial State:** $s_0 = (H_1^0, H_2^0, D^0, P^0, T^0, \text{turn}^0 = 1, n_{\text{draw}}^0 = 0)$
   - $D^0 = K \setminus (H_1^0 \cup H_2^0 \cup \{c_{\text{top}}^0\})$ (remaining deck)
   - $P^0 = \{c_{\text{top}}^0\}$ (discard pile contains only top card)
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (or declared color if wild)

### 8.2. Initial Belief Distribution

Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \{c_{\text{top}}^0\}, n_2^0 = 7, n_d^0 = |D^0|)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1 (evaluated on the state after action $a$):

$$
R(s', a) = \begin{cases}
+1 & \text{if } |H_1| = 0 \text{ in state } s' \text{ (Player 1 wins)} \\
-1 & \text{if } |H_2| = 0 \text{ in state } s' \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

where $s'$ is the state reached after executing action $a$ in state $s$.

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Belief Tracking Methods

Since the state space is large (due to opponent hand and deck uncertainty), we use approximate belief tracking. Two approaches:

### 11.1. Exact Bayes Filter (Discrete)

For tractable state spaces, maintain exact belief distribution:

**Prediction Step:**
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

**Update Step:**
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

**Limitation:** Requires enumerating all states in belief support, which grows exponentially with opponent hand size.

### 11.2. Particle Filter (Approximate)

Approximate belief $b_t$ with $N$ weighted particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Algorithm:**

1. **Prediction:** For each particle $s^{(i)}$, sample successor state $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$
2. **Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$
3. **Normalize:** $\tilde{w}^{(i)} = \frac{w'^{(i)}}{\sum_j w'^{(j)}}$
4. **Resampling:** Sample $N$ new particles from $\{(s'^{(i)}, \tilde{w}^{(i)})\}$ to prevent weight degeneracy

**Advantages:** Handles large state spaces efficiently; fixed computational cost $O(N)$ per update.

**Note:** Monte Carlo planning methods (e.g., POMCP) are excluded for now; focus is on belief tracking only.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Checking transition probability and clarifying:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same rules as Player 1** (Section 5.1), but applied to Player 2:

- If $a_2 = \text{Draw}$: Draw $k = \max(1, n_{\text{draw}})$ cards, reset penalty, set $\text{turn} = 1$
- If $a_2 = (c, \tilde{c})$: Remove $c$ from $H_2$, update $T$ and $P$, handle card effects, set turn accordingly

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** After any player's action, if $|H_1| = 0$ or $|H_2| = 0$, the game terminates.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if } a_t = \text{Draw} \text{ and drawing } k \text{ cards (uniform over } k\text{-subsets)} \\
  1 & \text{if } a_t \text{ is playing a card (deterministic)}
  \end{cases}
  $$

  where $|D^{t+}| = |D^t|$ if no reshuffle, or $|D^{t+}| = |P^t| - 1 + |D^t|$ if reshuffle occurred.

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \cdot) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (unobserved specific cards):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial State and Belief $b_0$

### 8.1. Initial Game Setup

At $t = 0$, the game is initialized as follows:

1. **Deal:** Shuffle deck $K$ uniformly. Deal 7 cards to each player: $H_1^0$ and $H_2^0$ (each of size 7).
2. **Top Card:** Draw one card from remaining deck to start discard pile: $c_{\text{top}}^0$. If it's a Wild or Wild+4, reshuffle and redraw.
3. **Initial State:** $s_0 = (H_1^0, H_2^0, D^0, P^0, T^0, \text{turn}^0 = 1, n_{\text{draw}}^0 = 0)$
   - $D^0 = K \setminus (H_1^0 \cup H_2^0 \cup \{c_{\text{top}}^0\})$ (remaining deck)
   - $P^0 = \{c_{\text{top}}^0\}$ (discard pile contains only top card)
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (or declared color if wild)

### 8.2. Initial Belief Distribution

Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \{c_{\text{top}}^0\}, n_2^0 = 7, n_d^0 = |D^0|)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1 (evaluated on the state after action $a$):

$$
R(s', a) = \begin{cases}
+1 & \text{if } |H_1| = 0 \text{ in state } s' \text{ (Player 1 wins)} \\
-1 & \text{if } |H_2| = 0 \text{ in state } s' \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

where $s'$ is the state reached after executing action $a$ in state $s$.

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Belief Tracking Methods

Since the state space is large (due to opponent hand and deck uncertainty), we use approximate belief tracking. Two approaches:

### 11.1. Exact Bayes Filter (Discrete)

For tractable state spaces, maintain exact belief distribution:

**Prediction Step:**
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

**Update Step:**
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

**Limitation:** Requires enumerating all states in belief support, which grows exponentially with opponent hand size.

### 11.2. Particle Filter (Approximate)

Approximate belief $b_t$ with $N$ weighted particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Algorithm:**

1. **Prediction:** For each particle $s^{(i)}$, sample successor state $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$
2. **Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$
3. **Normalize:** $\tilde{w}^{(i)} = \frac{w'^{(i)}}{\sum_j w'^{(j)}}$
4. **Resampling:** Sample $N$ new particles from $\{(s'^{(i)}, \tilde{w}^{(i)})\}$ to prevent weight degeneracy

**Advantages:** Handles large state spaces efficiently; fixed computational cost $O(N)$ per update.

**Note:** Monte Carlo planning methods (e.g., POMCP) are excluded for now; focus is on belief tracking only.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Clarifying how we determine if Player 2 drew or played:

```markdown
# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9, \text{Skip}, \text{Reverse}, \text{+2}\}$
- Wild cards: $\mathcal{W} = \{\text{Wild}, \text{Wild+4}\}$
- Labeled deck: $K = \{K_1, K_2, \ldots, K_{108}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
  - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
  - 4 Wild, 4 Wild+4
- Card attributes: $\text{color}: K \to \mathcal{C} \cup \{\perp\}$, $\text{rank}: K \to \mathcal{R} \cup \mathcal{W}$
  - Wild cards have $\text{color}(k) = \perp$

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent
- Indicator: $\mathbb{1}[\cdot] \in \{0, 1\}$ (also called Iverson bracket)
  - $\mathbb{1}[\text{condition}] = 1$ if condition is true, $0$ if false
  - Example: $\mathbb{1}[x > 5] = 1$ if $x > 5$, otherwise $0$

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t, \text{meta}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times (\mathcal{C} \cup \{\perp\})$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - If $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$
  - If $c_{\text{top}}$ is wild, $\tilde{c} \in \mathcal{C}$ is the declared color
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t, \text{meta}_{\text{obs}}^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)
- $\text{meta}_{\text{obs}}^t = n_{\text{draw}}$: Observable metadata

**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: $\tilde{c}$ is ignored (set to $\perp$)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t)\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip (ends turn immediately)
- No stacking of draw penalties: When $n_{\text{draw}} > 0$, only Draw is legal (cannot play +2 or Wild+4 to increase penalty)
- No challenging Wild+4

---

## 5. State Transition Dynamics $\mathcal{T}$

The transition function decomposes into two phases per time step:

### 5.1. Player 1 Action Phase

Given state $s_t$ with $\text{turn}^t = 1$ and action $a_t \in \mathcal{A}_{\text{legal}}(s_t)$:

**Drawing:**
If $a_t = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c}')$ where
   $$\tilde{c}' = \begin{cases} \tilde{c} & \text{if } \text{rank}(c) \in \mathcal{W} \\ \text{color}(c) & \text{otherwise} \end{cases}$$
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 1 keeps turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same rules as Player 1** (Section 5.1), but applied to Player 2:

- If $a_2 = \text{Draw}$: Draw $k = \max(1, n_{\text{draw}})$ cards, reset penalty, set $\text{turn} = 1$
- If $a_2 = (c, \tilde{c})$: Remove $c$ from $H_2$, update $T$ and $P$, handle card effects, set turn accordingly

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** After any player's action, if $|H_1| = 0$ or $|H_2| = 0$, the game terminates.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s)|} & \text{if } \mathcal{A}_{\text{play}} \cap \mathcal{A}_{\text{legal}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw}
\end{cases}
$$

### 5.3. Transition Probability

For complete transition from $s_t$ to $s_{t+1}$ given Player 1 action $a_t$:

$$P(s_{t+1} \mid s_t, a_t) = \sum_{s^{t+}} \sum_{a_2} P(s_{t+1} \mid s^{t+}, a_2) \cdot \pi_2(a_2 \mid s^{t+}) \cdot P(s^{t+} \mid s_t, a_t)$$

where:

- $P(s^{t+} \mid s_t, a_t)$ accounts for randomness in drawing:

  $$
  P(s^{t+} \mid s_t, a_t) = \begin{cases}
  \frac{1}{\binom{|D^{t+}|}{k}} & \text{if } a_t = \text{Draw} \text{ and drawing } k \text{ cards (uniform over } k\text{-subsets)} \\
  1 & \text{if } a_t \text{ is playing a card (deterministic)}
  \end{cases}
  $$

  where $|D^{t+}| = |D^t|$ if no reshuffle, or $|D^{t+}| = |P^t| - 1 + |D^t|$ if reshuffle occurred.

- $P(s_{t+1} \mid s^{t+}, a_2)$ similarly accounts for Player 2's draw randomness

---

## 6. Belief State $b_t$

Player 1's belief at time $t$ is a probability distribution over complete states:
$$b_t : \mathcal{S} \to [0, 1], \quad \sum_{s \in \mathcal{S}} b_t(s) = 1$$

conditioned on the observation history $h_t = (o_0, a_0, o_1, a_1, \ldots, o_t)$.

### 6.1. Factored Belief Representation

Since Player 1 knows $(H_1^t, P^t, T^t, \text{meta}_{\text{obs}}^t)$, the belief factors as:
$$b_t(s) = \mathbb{1}[H_1 = H_1^t, P = P^t, T = T^t] \cdot b_t(H_2, D)$$

where we maintain a marginal belief over unknown components:
$$b_t(H_2, D) = P(H_2^t = H_2, D^t = D \mid h_t)$$

Since $D^t$ is a multiset (unordered), $D$ represents the multiset of cards in the draw deck.

**Practical Representation:**

Define the **unseen pool** (cards not in Player 1's hand or discard pile):
$$U_t = K \setminus (H_1^t \cup P^t)$$

with $|U_t| = m_t$. Then belief over opponent's hand:
$$b_t^H(H_2) = P(H_2^t = H_2 \mid h_t), \quad H_2 \subseteq U_t, |H_2| = n_2^t$$

---

## 7. Belief Update $\tau$

The belief update operator is:
$$b_{t+1} = \tau(b_t, a_t, o_{t+1})$$

### 7.1. Prediction Step (Chapman-Kolmogorov)

Given action $a_t$, compute predicted belief:
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

### 7.2. Correction Step (Bayes Rule)

After observing $o_{t+1}$:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

### 7.3. Opponent Play Observation

When Player 2 plays card $c_2$ (observed in $o_{t+1}$ via $T^{t+1} = (c_2, \tilde{c}_2)$ and $n_2^{t+1} = n_2^t - 1$):

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

When Player 2 draws $k$ cards (inferred from $n_2^{t+1} = n_2^t + k$ and no card played, i.e., $T^{t+1} = T^t$):

For each prior hypothesis $H_2$ with $|H_2| = n_2$:
$$P(H_2' \mid H_2, \text{draw } k) = \frac{\mathbb{1}[H_2' \supseteq H_2, |H_2' \setminus H_2| = k, H_2' \setminus H_2 \subseteq U_t \setminus H_2]}{\binom{|U_t \setminus H_2|}{k}}$$

This is a hypergeometric draw from the unseen pool excluding $H_2$.

Updated belief:
$$b_{t+1}(H_2') = \sum_{H_2} P(H_2' \mid H_2, \text{draw } k) \cdot b_t(H_2)$$

---

## 8. Initial State and Belief $b_0$

### 8.1. Initial Game Setup

At $t = 0$, the game is initialized as follows:

1. **Deal:** Shuffle deck $K$ uniformly. Deal 7 cards to each player: $H_1^0$ and $H_2^0$ (each of size 7).
2. **Top Card:** Draw one card from remaining deck to start discard pile: $c_{\text{top}}^0$. If it's a Wild or Wild+4, reshuffle and redraw.
3. **Initial State:** $s_0 = (H_1^0, H_2^0, D^0, P^0, T^0, \text{turn}^0 = 1, n_{\text{draw}}^0 = 0)$
   - $D^0 = K \setminus (H_1^0 \cup H_2^0 \cup \{c_{\text{top}}^0\})$ (remaining deck)
   - $P^0 = \{c_{\text{top}}^0\}$ (discard pile contains only top card)
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (or declared color if wild)

### 8.2. Initial Belief Distribution

Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \{c_{\text{top}}^0\}, n_2^0 = 7, n_d^0 = |D^0|)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

and draw deck is uniformly distributed as multiset $D^0 = U_0 \setminus H_2$.

---

## 9. Reward Function $R$

Define immediate reward for Player 1 (evaluated on the state after action $a$):

$$
R(s', a) = \begin{cases}
+1 & \text{if } |H_1| = 0 \text{ in state } s' \text{ (Player 1 wins)} \\
-1 & \text{if } |H_2| = 0 \text{ in state } s' \text{ (Player 2 wins)} \\
0 & \text{otherwise}
\end{cases}
$$

where $s'$ is the state reached after executing action $a$ in state $s$.

Expected reward under belief:
$$R(b_t, a_t) = \sum_{s \in \mathcal{S}} b_t(s) \cdot R(s, a_t)$$

For planning, may include per-step penalty to encourage shorter games:
$$R(s, a) = R_{\text{terminal}}(s) - \lambda \cdot \mathbb{1}[s \notin \mathcal{S}_{\text{term}}]$$

---

## 10. Value Function and Bellman Optimality

Discount factor: $\gamma \in [0, 1]$

The belief-space value function satisfies:
$$V^*(b) = \max_{a \in \mathcal{A}} Q^*(b, a)$$

where the action-value function is:
$$Q^*(b, a) = R(b, a) + \gamma \sum_{o \in \Omega} P(o \mid b, a) \cdot V^*(\tau(b, a, o))$$

**Observation Probability:**
$$P(o' \mid b, a) = \sum_{s' \in \mathcal{S}} P(o' \mid s') \cdot \bar{b}(s')$$

where $\bar{b}(s') = \sum_{s} P(s' \mid s, a) \cdot b(s)$ is the predicted belief.

**Optimal Policy:**
$$\pi^*(b) = \arg\max_{a \in \mathcal{A}} Q^*(b, a)$$

---

## 11. Belief Tracking Methods

Since the state space is large (due to opponent hand and deck uncertainty), we use approximate belief tracking. Two approaches:

### 11.1. Exact Bayes Filter (Discrete)

For tractable state spaces, maintain exact belief distribution:

**Prediction Step:**
$$\bar{b}_{t+1}(s') = \sum_{s \in \mathcal{S}} P(s' \mid s, a_t) \cdot b_t(s)$$

**Update Step:**
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

**Limitation:** Requires enumerating all states in belief support, which grows exponentially with opponent hand size.

### 11.2. Particle Filter (Approximate)

Approximate belief $b_t$ with $N$ weighted particles:
$$b_t \approx \{(s^{(i)}, w^{(i)})\}_{i=1}^N, \quad \sum_{i=1}^N w^{(i)} = 1$$

**Algorithm:**

1. **Prediction:** For each particle $s^{(i)}$, sample successor state $s'^{(i)} \sim P(\cdot \mid s^{(i)}, a_t)$
2. **Update:** Weight by observation likelihood: $w'^{(i)} = w^{(i)} \cdot P(o_{t+1} \mid s'^{(i)})$
3. **Normalize:** $\tilde{w}^{(i)} = \frac{w'^{(i)}}{\sum_j w'^{(j)}}$
4. **Resampling:** Sample $N$ new particles from $\{(s'^{(i)}, \tilde{w}^{(i)})\}$ to prevent weight degeneracy

**Advantages:** Handles large state spaces efficiently; fixed computational cost $O(N)$ per update.

**Note:** Monte Carlo planning methods (e.g., POMCP) are excluded for now; focus is on belief tracking only.

---

## 12. Tractable Marginal Computations

### 12.1. Probability Card in Opponent's Hand

Under uniform belief over $H_2 \subseteq U_t$ with $|H_2| = n_2$:
$$P(c \in H_2) = \frac{n_2}{m_t}, \quad \forall c \in U_t$$

### 12.2. Probability of Color in Opponent's Hand

Let $m_c = |\{k \in U_t : \text{color}(k) = c\}|$ be count of color $c$ in unseen pool:
$$P(\exists k \in H_2 : \text{color}(k) = c) = 1 - \frac{\binom{m_t - m_c}{n_2}}{\binom{m_t}{n_2}}$$

### 12.3. Expected Playable Cards in Opponent's Hand

Given current top card $T^t$, for each $k \in U_t$:
$$P(k \text{ playable} \cap k \in H_2) = \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

Expected number of playable cards opponent holds:
$$\mathbb{E}[|\{k \in H_2 : \text{playable}(k, T^t)\}|] = \sum_{k \in U_t} \mathbb{1}[\text{playable}(k, T^t)] \cdot \frac{n_2}{m_t}$$

---

## 13. Heuristic Value Approximations

For computational efficiency, approximate $V(b)$ with hand-crafted heuristics:

$$V_{\text{heur}}(b) = \alpha_1 \cdot (n_2 - |H_1|) + \alpha_2 \cdot f_{\text{playable}}(b) + \alpha_3 \cdot f_{\text{wild}}(H_1)$$

where:

- $n_2 - |H_1|$: Hand size difference
- $f_{\text{playable}}(b)$: Expected playable cards in opponent's hand (negative weight)
- $f_{\text{wild}}(H_1)$: Number of wild cards held (positive weight)

---

## 14. Summary of POMDP Tuple

The 2-Player UNO POMDP from Player 1's perspective is formally:
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, b_0, \gamma)$$

where:

- $\mathcal{S}$: State space (§2)
- $\mathcal{A}$: Action space with legal action function (§4)
- $\mathcal{T}$: Transition dynamics $P(s' \mid s, a)$ (§5)
- $\mathcal{R}$: Reward function $R(s, a)$ (§9)
- $\Omega$: Observation space (§3)
- $\mathcal{O}$: Observation function $P(o \mid s)$ (§3)
- $b_0$: Initial belief distribution (§8)
- $\gamma$: Discount factor (§10)

The opponent policy $\pi_2$ is part of the environment model embedded in $\mathcal{T}$.

Optimal behavior is characterized by the value function $V^*(b)$ and policy $\pi^*(b)$ satisfying the Bellman optimality equation (§10).
```

Verifying a few more details. Checking the observation space to ensure it captures everything needed:

Review complete. Summary of fixes:

**Issues found and fixed:**

1. Drawing transition: Added the "else" case when no reshuffle occurs (line 133)
2. Player 2 transitions: Clarified that Player 2 follows the same rules as Player 1 (lines 160-162)
3. Terminal state checking: Added explicit terminal check after any player action (line 166)
4. Initial state setup: Added complete initial game setup procedure (Section 8.1)
5. Reward function: Clarified that reward is evaluated on state after action (line 307)
6. Transition probability: Clarified deck size calculation for reshuffle vs non-reshuffle (line 199)
7. Belief updates: Clarified how to infer Player 2's draw vs play from observations (lines 249, 259)

**Mathematical accuracy:**

- All formulas are correct
- Card counts verified (76 + 24 + 8 = 108)
- State consistency constraints are correct
- Belief update formulas are correct

**Implementation completeness:**
The document now contains enough information to implement a full UNO solver:

- Complete state representation
- Complete action space and legal action rules
- Complete transition dynamics (both players)
- Complete observation model
- Complete belief tracking (exact and particle filter)
- Initial state setup
- Terminal conditions
- Reward function

The math is accurate and sufficient for implementation. particles)

---

**User**

when we do implement the uno solver later (don't do it yet), how would it work? what would the program do?

---

**Cursor**

Outlining how the UNO solver would work based on the MATH.md specification:

How the UNO solver would work:

## High-Level Program Flow

**1. Initialization Phase:**

- Create the 108-card deck (labeled cards)
- Shuffle and deal: 7 cards to Player 1, 7 to Player 2
- Draw initial top card (reroll if Wild/Wild+4)
- Initialize belief $b_0$: uniform over all possible opponent hands (Section 8.2)
  - If using particle filter: sample $N$ particles where each particle has a random opponent hand from the unseen pool

**2. Main Game Loop (per turn):**

```
while not terminal:
    if turn == Player 1:
        # Player 1's turn
        1. Compute legal actions A_legal(s) based on:
           - Current hand H_1
           - Top card T (playability rules)
           - Draw penalty n_draw

        2. Select action using policy:
           - Option A: Heuristic policy (Section 13)
           - Option B: Value-based (if implementing Bellman)

        3. Execute action:
           - If Draw: sample k cards from deck, update hand
           - If Play: remove card, update discard pile, apply card effects

        4. Check terminal: if |H_1| == 0 → win, exit

        5. Update belief (prediction step):
           - For each particle/hypothesis: forward sample based on action

    else:  # Player 2's turn
        # Simulate Player 2's action
        1. Sample action a_2 ~ π_2(· | s) (opponent model)

        2. Execute Player 2's action (same transition rules)

        3. Check terminal: if |H_2| == 0 → lose, exit

        4. Observe result:
           - If played: observe card c_2 in T^{t+1}
           - If drew: observe hand size increase (n_2^{t+1} = n_2^t + k)

        5. Update belief (correction step):
           - Update weights based on observation likelihood
           - If particle filter: resample to prevent degeneracy
```

**3. Core Components:**

**State Management:**

- `State` class: `(H1, H2, D, P, T, turn, n_draw)`
- Use multisets for hands/deck/discard (e.g., `Counter` or `multiset`)

**Belief Tracking:**

- If particle filter: maintain list of `N` particles `[(s_i, w_i), ...]`
- Each particle is a complete state (including opponent hand $H_2$)
- Update via prediction→update→resample cycle

**Action Selection:**

- Compute legal actions (Section 4)
- Evaluate via heuristic (Section 13) or value function
- Select best action

**Transition Simulation:**

- Implement drawing logic (reshuffle handling, uniform sampling)
- Implement card playing (remove from hand, update discard, apply effects)
- Handle both Player 1 and Player 2 transitions

**Observation Processing:**

- Extract observation from state: `(H_1, n_2, n_d, P, T, n_draw)`
- Infer Player 2's action from observation changes
- Update belief weights based on observation likelihood

**4. Example Turn Sequence:**

```
t=0: Initialize
  - Deal cards, set up initial belief
  - Player 1 observes: (H_1^0, n_2=7, n_d=?, P^0, T^0, n_draw=0)

t=1: Player 1's turn
  - Compute legal actions: [play red-5, play Wild, Draw]
  - Select action: play red-5
  - Execute: remove red-5, update discard, T^1 = (red-5, red)
  - Belief prediction: forward sample particles
  - Check: |H_1| != 0, continue

t=2: Player 2's turn (simulated)
  - Sample action from π_2: play blue-5
  - Execute: remove blue-5 from H_2, update discard
  - Player 1 observes: n_2^2 = 6, T^2 = (blue-5, blue)
  - Belief update: weight particles by likelihood, resample
  - Check: |H_2| != 0, continue

t=3: Player 1's turn again
  - ... repeat
```

**5. Key Implementation Details:**

- Multiset operations: add/remove cards, check membership
- Uniform sampling: draw $k$ cards uniformly from deck multiset
- Belief update: likelihood $P(o|s') = 1$ if observation matches, $0$ otherwise
- Particle filter: resample when effective sample size is low
- Terminal checking: after each action, check if any hand is empty

**6. Output/Strategy:**

The solver produces:

- Action selection at each turn
- Belief distribution over opponent's hand
- Expected value estimates (if using value function)

This is a POMDP agent: maintains beliefs, selects actions, and updates beliefs from observations.

```plaintext
while not terminal:
    if turn == Player 1:
        # Player 1's turn
        1. Compute legal actions A_legal(s) based on:
           - Current hand H_1
           - Top card T (playability rules)
           - Draw penalty n_draw

        2. Select action using policy:
           - Option A: Heuristic policy (Section 13)
           - Option B: Value-based (if implementing Bellman)

        3. Execute action:
           - If Draw: sample k cards from deck, update hand
           - If Play: remove card, update discard pile, apply card effects

        4. Check terminal: if |H_1| == 0 → win, exit

        5. Update belief (prediction step):
           - For each particle/hypothesis: forward sample based on action

    else:  # Player 2's turn
        # Simulate Player 2's action
        1. Sample action a_2 ~ π_2(· | s) (opponent model)

        2. Execute Player 2's action (same transition rules)

        3. Check terminal: if |H_2| == 0 → lose, exit

        4. Observe result:
           - If played: observe card c_2 in T^{t+1}
           - If drew: observe hand size increase (n_2^{t+1} = n_2^t + k)

        5. Update belief (correction step):
           - Update weights based on observation likelihood
           - If particle filter: resample to prevent degeneracy
```

```plaintext
t=0: Initialize
  - Deal cards, set up initial belief
  - Player 1 observes: (H_1^0, n_2=7, n_d=?, P^0, T^0, n_draw=0)

t=1: Player 1's turn
  - Compute legal actions: [play red-5, play Wild, Draw]
  - Select action: play red-5
  - Execute: remove red-5, update discard, T^1 = (red-5, red)
  - Belief prediction: forward sample particles
  - Check: |H_1| != 0, continue

t=2: Player 2's turn (simulated)
  - Sample action from π_2: play blue-5
  - Execute: remove blue-5 from H_2, update discard
  - Player 1 observes: n_2^2 = 6, T^2 = (blue-5, blue)
  - Belief update: weight particles by likelihood, resample
  - Check: |H_2| != 0, continue

t=3: Player 1's turn again
  - ... repeat
```
