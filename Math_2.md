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
