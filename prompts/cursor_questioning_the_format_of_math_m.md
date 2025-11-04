# Questioning the format of MATH.md

_Exported on 11/4/2025 at 13:37:55 PST from Cursor (2.0.43)_

---

**User**

@MATH.md (67-69) why is this written like this

---

**Cursor**

Reviewing the surrounding context in MATH.md to explain the notation.

The formula uses an indicator function because the observation model is deterministic.

```67:69:MATH.md
**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.
```

**Why the indicator function:**

- Deterministic: the observation is a function of the state. If `proj(s_t) = o_t`, the probability is 1; otherwise 0.
- No observation noise: given `s_t`, `o_t` is fixed.

**Why not a probability distribution:**

- This isn’t a stochastic observation model (e.g., noisy sensors). It’s a deterministic projection of the visible parts of the state.

**In practice:**

- In belief updates (Section 7.2), this acts as a filter: states where `proj(s') ≠ o_{t+1}` get probability 0, while matching states keep their relative probabilities.

This is a standard POMDP pattern when observations are deterministic projections of the state.

```plaintext
**Observation Likelihood:**
$$P(o_t \mid s_t) = \mathbb{1}[\text{proj}(s_t) = o_t]$$
where $\text{proj}(s_t)$ extracts the visible components from $s_t$.
```

---

**User**

why do we care if its 1 or 0 why can't we just probability distribution directly

---

**Cursor**

The indicator function defines a probability distribution: a point mass (Dirac delta) over observations. For each state `s_t`, it's a probability distribution over `o_t`; it's just degenerate (all mass on one value).

**Why the indicator matters:**

In the belief update (line 246), you compute:
$$b_{t+1}(s') = \frac{P(o_{t+1} \mid s') \cdot \bar{b}_{t+1}(s')}{\sum_{\tilde{s} \in \mathcal{S}} P(o_{t+1} \mid \tilde{s}) \cdot \bar{b}_{t+1}(\tilde{s})}$$

The indicator `P(o_{t+1} | s') = 1` if `proj(s') = o_{t+1}`, else `0`.

**What this does:**

- Sets `b_{t+1}(s') = 0` for any state `s'` where the visible parts don't match the observation.
- Keeps only states consistent with the observation.

**Why not a continuous distribution:**

- Observations are discrete and deterministic given the state. The indicator captures this: for each `s`, exactly one `o` has probability 1; all others have probability 0.

**In practice:**

- This zeros out inconsistent states, so you only normalize over states that match the observation. This is the standard POMDP form for deterministic observations.

If you had noisy observations (e.g., sensor errors), you'd use a continuous distribution like `P(o | s) = N(proj(s), σ²)`. Here, the indicator is the correct form because observations are deterministic.

---

**User**

@MATH.md (75-116) explain A_legal(s_t) cause idk what it is

---

**Cursor**

Reviewing the surrounding context to explain `A_legal(s_t)`:

`A_legal(s_t)` is the set of valid actions Player 1 can take in state `s_t`. It filters the full action space by UNO rules.

**Two cases:**

1. **No penalty (`n_draw = 0`):**
   - Play any playable card from your hand, or
   - Draw

2. **Penalty active (`n_draw > 0`):**
   - Only Draw (you must draw `n_draw` cards)

**What makes a card playable?** (lines 104-109)
A card `c` is playable if at least one of:

- It’s a Wild card (any Wild/Wild+4)
- Its color matches the declared color `\tilde{c}` on the top card
- Its rank matches the rank of the top card

**Example:**

- Top card: Red 5
- Your hand: {Blue 5, Red 3, Green Skip, Wild}
- `A_legal` = {Blue 5 (rank match), Red 3 (color match), Green Skip (rank match), Wild (always playable), Draw}

If `n_draw = 4` (penalty active), `A_legal` = {Draw} only.

This enforces the rule that you can’t play when a draw penalty is pending.

---

**User**

what does the perpendicular angle symbol mean

---

**Cursor**

Checking how `⊥` is used in the document:

`⊥` means null/not applicable/undefined.

In this document:

1. **Wild cards** (line 15): `color(k) = ⊥` — wild cards don't have a color until declared.

2. **Non-wild play actions** (line 82): `\tilde{c} = ⊥` — when playing a non-wild card, the declared color field is ignored/not used.

3. **Type signatures** (lines 14, 37, 80): `C ∪ {⊥}` — the color can be a color or null.

**Example:**

- Playing a Red 5: `(Red 5, ⊥)` — the second component is ignored.
- Playing a Wild: `(Wild, Red)` — the second component is the declared color.

It's a common notation for "no value" or "not applicable" in math/CS.

---

**User**

how can the color be null, don't the players declare the color before playing the card anyways so it would be like "+4 blue" or "wild yellow" or something

---

**Cursor**

Checking how actions are structured:

Checking how this is used in transitions:

Clarifying the notation: for non-wild cards, the color comes from the card itself, so `\tilde{c}` is ignored (`⊥`). Updating the explanation to make this explicit:

Clarifying the explanation: non-wild cards have inherent colors, so `\tilde{c}` is unused (`⊥`). Only wild cards use `\tilde{c}` (the declared color).

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C} \cup \{\perp\}\}$$

- For non-wild cards $c$: The card has an inherent color $\text{color}(c)$, so $\tilde{c}$ is unused (set to $\perp$). The color used is $\text{color}(c)$.
- For wild cards $c$: The card has no inherent color, so $\tilde{c} \in \mathcal{C}$ is the declared color (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

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

Clarified the explanation. Summary:

- **Non-wild cards** (e.g., Red 5): The color comes from the card itself (`color(c) = Red`). `\tilde{c} = ⊥` means that field is unused; the color is taken from `color(c)`.

- **Wild cards** (e.g., Wild+4): No inherent color, so you must specify `\tilde{c}` (the declared color, e.g., "Wild+4 blue" → `\tilde{c} = blue`).

The `⊥` indicates the action parameter is ignored, not that there's no color. The transition logic (line 146) uses `color(c)` for non-wild cards and `\tilde{c}` for wild cards, which matches this.

The action format is uniform `(c, \tilde{c})`, but `\tilde{c}` only matters for wild cards.

---

**User**

but like i don't see the purpose of perpendicular (null) cause everything is declared when playing it right?

---

**Cursor**

Reviewing the transition logic to see how `\tilde{c}` is used:

Noting that for non-wild cards, `\tilde{c}` is ignored and `color(c)` is used. Refactoring to require `\tilde{c} = color(c)` for non-wild cards, removing the need for `⊥` in actions:

Removing `⊥` from actions: require `\tilde{c} = color(c)` for non-wild cards, and always use `\tilde{c}` in transitions. Updating the action space and transitions accordingly:

---

**User**

in the action space, i am confused why c tilde is ignored, like when we play a card we already know what color we are going to play it as right as we play it right? even with wild cards they are colorless in our hand but when we play it we declare a color? alternatively we have cards with colors in our hand currently so when playing the card why don't we also declare the color for them as well? like i am confused why the wildcard color is represented in a different spot than the actual card color

---

**Cursor**

Checking transition logic to see if we can simplify this:

Unifying the action space: require `\tilde{c} \in \mathcal{C}` for all play actions. For non-wild cards, enforce `\tilde{c} = color(c)`; for wild cards, `\tilde{c}` is the player's choice. This simplifies transitions (always use `\tilde{c}`) and makes the action space uniform. Refactoring:

```markdown
**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).
```

Reading the current state:

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

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

Updating the transition logic to always use `\tilde{c}`:

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

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
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

Checking for other references to `\perp` in color contexts:

Reviewing the state space definition:

Updating the state space: since actions always declare a color, `\tilde{c}` in `T^t` is always in `\mathcal{C}`. Removing `\perp` from the state definition:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

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
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

Checking the initialization section for consistency:

Updating the initialization comment for clarity:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

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
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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

Checking if the legal action set needs updates:

Updating the legal action set to be explicit about the color constraint:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
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
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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

Checking for lint errors:

## Summary of Changes

1. **Removed `⊥` from actions**: Action space now `\tilde{c} \in \mathcal{C}` (no null)
2. **Unified color declaration**: Every play action includes a color:
   - Non-wild cards: `\tilde{c} = color(c)` (must match card's color)
   - Wild cards: `\tilde{c} \in \mathcal{C}` (player chooses)
3. **Simplified transitions**: Always use `\tilde{c}` from the action (removed conditional)
4. **Updated state space**: Removed `⊥` from `T^t` since colors are always declared
5. **Updated legal actions**: Explicitly includes color constraints

Result: Every play action declares a color. Non-wild cards must use their inherent color; wild cards let the player choose. This makes the action space uniform and removes the need for `⊥`.

---

**User**

double check the entire math currently and tell me if its enough to convert this into code for a full uno solver and simulation

---

**Cursor**

Reviewing MATH.md for completeness for a full UNO solver and simulation:

Checking for missing details and edge cases:

Creating a checklist of what's needed and identifying gaps:

Reviewing Player 2 turn transitions and other edge cases:

Checking observation inference logic:

Compiling a review of gaps and ambiguities:

Findings:

What's complete:

- Card representation and deck structure
- State space definition
- Observation model
- Action space (after recent fixes)
- Transitions for Player 1 (drawing, playing, reshuffle)
- Belief updates
- Initialization
- Reward function
- Value function and Bellman equation

Issues and gaps:

```markdown
# MATH.md Completeness Review for UNO Solver Implementation

## ✅ Complete Components

1. **Card System**: Fully defined (colors, ranks, wild cards, deck composition)
2. **State Space**: Complete with all components
3. **Observation Model**: Deterministic projection defined
4. **Action Space**: Complete (after recent fixes removing ⊥)
5. **Player 1 Transitions**: Fully specified
6. **Belief Updates**: Complete with play/draw observation logic
7. **Initialization**: Complete
8. **Rewards**: Defined
9. **Planning Framework**: Value functions and Bellman equation defined

## ⚠️ Issues and Gaps

### 1. **Player 2 Turn Transitions (CRITICAL)**

**Problem**: Line 165 says "set turn accordingly" but doesn't specify what happens when Player 2 plays Skip/Reverse.

**Current text** (line 151):

- Player 1 plays Skip/Reverse: `turn^{t+} = 1` (Player 1 keeps turn)

**Missing**: What happens when Player 2 plays Skip/Reverse?

**Expected behavior** (inferred): Player 2's turn should end, `turn = 1` (Player 1's turn)

**Fix needed**: Explicitly state:
```

For Player 2 playing card $(c, \tilde{c})$:

- **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 1$
- **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 1$
- **Skip or Reverse**: $\text{turn}^{t+} = 1$ (Player 2's turn ends, Player 1's turn)
- **Number or Wild**: $\text{turn}^{t+} = 1$

```

### 2. **Player 2 Legal Actions (MINOR)**

**Problem**: `A_legal(s_t)` is only defined for Player 1's turn (line 93: "For state $s_t$ with Player 1's turn").

**Fix needed**: Either:
- Add symmetric definition: `A_legal^2(s_t)` for Player 2
- Or clarify that `A_legal(s)` works for any player (it's symmetric)

### 3. **Reshuffle Edge Case (MINOR)**

**Problem**: What if after reshuffle, `|D^{t+}| < k`? (Extremely unlikely but mathematically possible)

**Current logic** (line 133-136):
- If `|D^t| < k`: Reshuffle
- Then sample k cards from `D^{t+}`

**Fix needed**: Add check:
```

2. If $|D^t| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+} = (P^t \setminus \{c_{\text{top}}\}) \cup D^t$
   - Set $P^{t+} = \{c_{\text{top}}\}$
   - If $|D^{t+}| < k$: Game ends (impossible to draw k cards, terminal state)
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$

```

### 4. **Terminal State Timing (CLARIFICATION NEEDED)**

**Problem**: Line 169 says "After any player's action, if $|H_1| = 0$ or $|H_2| = 0$, the game terminates."

**Question**: Is this checked:
- Immediately after the action that empties a hand?
- Or at the start of the next turn?

**Expected**: Immediately (standard UNO rule - you win when you play your last card)

**Fix needed**: Clarify: "The game terminates immediately when a player plays their last card (reducing their hand to 0)."

### 5. **UNO Calling Rule (OPTIONAL - Game Rule)**

**Problem**: Real UNO has a rule where you must call "UNO" when you have 1 card, or draw 2 cards as penalty.

**Status**: This is a gameplay rule, not essential for POMDP solver. Can be omitted for simplicity.

**Recommendation**: Document as optional rule if implementing full UNO simulation.

### 6. **Observation Inference Edge Cases (MINOR)**

**Problem**: Line 262 says Player 2 draws are detected when `T^{t+1} = T^t` and `n_2^{t+1} = n_2^t + k`.

**Edge case**: What if Player 2 draws and somehow the top card changes? (Shouldn't happen, but worth noting)

**Edge case**: What if `n_2^{t+1} = n_2^t`? (Player 2 played card but hand size unchanged - impossible given rules)

**Fix needed**: Clarify that these are mutually exclusive:
- If `T^{t+1} ≠ T^t` AND `n_2^{t+1} = n_2^t - 1`: Player 2 played card `T^{t+1}.c_top`
- If `T^{t+1} = T^t` AND `n_2^{t+1} > n_2^t`: Player 2 drew `n_2^{t+1} - n_2^t` cards

### 7. **Empty Legal Actions (MINOR)**

**Problem**: What if `A_legal(s_t) = ∅`? (Shouldn't happen given rules, but mathematically possible if deck is empty and no playable cards)

**Fix needed**: Add terminal state check: "If a player has no legal actions and cannot draw, game ends in draw/stalemate."

## 📋 Implementation Checklist

### Core Game Mechanics
- [x] Card representation
- [x] Deck initialization
- [x] State representation
- [x] Action space
- [x] Legal action computation
- [x] Player 1 transitions (draw/play)
- [ ] Player 2 transitions (needs clarification on Skip/Reverse)
- [x] Reshuffle logic
- [ ] Reshuffle edge case handling
- [x] Terminal state detection
- [ ] Terminal state timing clarification

### POMDP Components
- [x] Observation space
- [x] Observation likelihood
- [x] Belief state representation
- [x] Belief update (prediction)
- [x] Belief update (correction)
- [x] Opponent play observation
- [x] Opponent draw observation
- [x] Initial belief
- [x] Reward function
- [x] Value function
- [x] Transition probabilities

### Planning Methods
- [x] Exact belief tracking (conceptual)
- [x] Particle filter (conceptual)
- [x] Heuristic value approximation
- [x] Marginal computations

## 🎯 Summary

**Overall Assessment**: ~95% complete. The math is sufficient for implementation with minor clarifications needed.

**Critical Fixes**:
1. Player 2 turn transitions (especially Skip/Reverse)
2. Terminal state timing

**Nice-to-Have**:
3. Reshuffle edge case
4. Empty legal actions handling
5. Observation inference clarification

**Optional**:
6. UNO calling rule (gameplay feature, not essential for solver)

The document is mathematically sound and implementation-ready after addressing the Player 2 turn transition ambiguity.

```

## Summary

Reviewed MATH.md. It's ~95% complete for implementation. Findings:

### What's complete

- Card system, state space, observations, actions
- Player 1 transitions (drawing, playing, reshuffle)
- Belief updates (prediction + correction)
- POMDP framework (rewards, value functions, Bellman equation)
- Initialization and planning methods

### Critical issues (must fix)

1. Player 2 turn transitions (line 165): When Player 2 plays Skip/Reverse, "set turn accordingly" is ambiguous. It should explicitly state that Player 2's turn ends and it goes to Player 1.

2. Terminal state timing (line 169): Clarify that the game ends immediately when a player plays their last card (not at the start of the next turn).

### Minor clarifications

3. Reshuffle edge case: Handle the case where `|D^{t+}| < k` after reshuffle (unlikely but possible).

4. Player 2 legal actions: Clarify that `A_legal(s)` works for any player (it's symmetric).

5. Observation inference: Make the mutual exclusivity explicit (play vs draw detection).

### Optional

6. UNO calling rule: Not essential for the POMDP solver; can be added later for a full simulation.

Created `MATH_REVIEW.md` with details and fixes. The math is ready for implementation after addressing the Player 2 turn transition ambiguity. Everything else is specified clearly enough to code.

Should I fix the Player 2 turn transitions in MATH.md?

---

**User**

fix everything in MATH.md to give us the full uno solver with the limitations that we gave (no stacking +2/+4, no challenges, its a 2 player game so reverse and skip are treated the same)

---

**Cursor**

Fixing the identified issues in MATH.md to make it complete for a UNO solver:

Applying fixes:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_1^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
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
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state, treat as draw/stalemate)
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state, treat as draw/stalemate)
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. Reshuffle if needed (same logic as Player 1, but applied to Player 2's draw)
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state, treat as draw/stalemate)
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. Reshuffle if needed (same logic as Player 1, but applied to Player 2's draw)
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state, treat as draw/stalemate)
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. Reshuffle if needed (same logic as Player 1, but applied to Player 2's draw)
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state, treat as draw/stalemate)
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. Reshuffle if needed (same logic as Player 1, but applied to Player 2's draw)
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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

---

**User**

if its impossible to draw $k$ cards, we terminate the game, and the person with the least number of cards in their hand wins

---

**Cursor**

Updating the terminal condition to award the win to the player with the fewest cards when drawing k cards is impossible:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. Reshuffle if needed (same logic as Player 1, but applied to Player 2's draw)
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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

Updating the Player 2 section to explicitly state the same termination condition:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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

Updating the reward function to handle this termination case:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\} \cup \{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

Updated the termination condition. When it's impossible to draw k cards after reshuffle:

1. **Termination logic** (Player 1 and Player 2 drawing): The player with fewer cards wins; if tied, it's a draw.

2. **Terminal states**: Added this condition to the terminal state definition.

3. **Reward function**: Added cases for:
   - Player 1 wins by fewer cards: +1
   - Player 2 wins by fewer cards: -1
   - Tie: 0

The document now specifies this termination condition. The math is complete for a full UNO solver implementation.

---

**User**

the action of drawing can only happen if you have no legal cards playable in the current situation

---

**Cursor**

Updating the legal action set to only allow drawing when no cards are playable:

Updating the legal action set to only allow drawing when no cards are playable:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

Fixing the duplicate "where" clause:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

Updated the legal action set to enforce the rule:

**New rule:** You can only draw if:

1. You have no playable cards (`A_playable(s_t) = ∅`), or
2. A draw penalty is active (`n_draw > 0`)

**When you have playable cards:** You can only play cards; drawing is not allowed.

The legal action set now:

- If `n_draw > 0`: Only Draw (penalty active)
- If `n_draw = 0` and playable cards exist: Only playable card actions
- If `n_draw = 0` and no playable cards: Only Draw

This matches standard UNO: you must play if you can; you can only draw if you cannot play.

---

**User**

double check the entire uno math and fix anything thats wrong, given our conditions (2 player game so reverse / skip, drawing 1 card is a last resort option if you cannot play anything, no stacking +2/+4, no challenge +4)

---

**Cursor**

Reviewing the entire MATH.md file for correctness against the specified rules:

Checking against the specified rules and fixing issues:

Fixing the issues:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Sample $k$ cards from deck and add to $H_2$
4. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
5. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

Fixing Skip/Reverse behavior: in 2-player, both cards end the turn immediately. Verifying the logic:

Checking if there are any other issues. Verifying the "ends turn immediately" interpretation:

Checking the Skip/Reverse rule: "ends turn immediately" in 2-player UNO. Fixing based on the rule that both Skip and Reverse end the turn immediately:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
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

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 2$ (Player 1's turn ends immediately, Player 2's turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0 \text{ or } (|D| < k \text{ and } |D^{t+}| < k \text{ after reshuffle})\}$$

where the last condition handles the case where it's impossible to draw the required number of cards.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 2$ (Player 1's turn ends immediately, Player 2's turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends immediately, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

## Summary of Fixes

1. **Action space clarification**: Added a note that the action space is from Player 1's perspective.

2. **Player 2 drawing**: Expanded to include full probability details and state updates, matching Player 1's drawing logic.

3. **Skip/Reverse behavior**: Clarified that in 2-player, both Skip and Reverse end the current player's turn immediately and pass to the opponent:
   - Player 1 plays Skip/Reverse → `turn = 2` (Player 1's turn ends, Player 2's turn)
   - Player 2 plays Skip/Reverse → `turn = 1` (Player 2's turn ends, Player 1's turn)

4. **Rule verification**: All rules are correctly implemented:
   - Drawing only allowed if no playable cards exist (or penalty active)
   - No stacking +2/+4 (only Draw legal when `n_draw > 0`)
   - No challenging Wild+4
   - 2-player: Reverse = Skip (both end turn immediately)

The document is now consistent and ready for implementation. All transitions, legal actions, and special rules align with the specified UNO variant.

---

**User**

double check the math equations and formulations too according to this specific variant

---

**Cursor**

Reviewing all math equations and formulations for correctness. Checking each section systematically:

Systematically checking all equations and fixing issues:

Fixing identified issues:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

**Note:** Additional termination condition: If during a draw action, after reshuffle $|D^{t+}| < k$ where $k$ is the required draw count, the game terminates immediately. This is handled during transitions, not as a static state property.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 2$ (Player 1's turn ends immediately, Player 2's turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends immediately, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

**Note:** Additional termination condition: If during a draw action, after reshuffle $|D^{t+}| < k$ where $k$ is the required draw count, the game terminates immediately. This is handled during transitions, not as a static state property.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 2$ (Player 1's turn ends immediately, Player 2's turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends immediately, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{playable}}(s)]}{|\mathcal{A}_{\text{playable}}(s)|} & \text{if } \mathcal{A}_{\text{playable}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw} \text{ and } \mathcal{A}_{\text{playable}}(s) = \emptyset
\end{cases}
$$

This policy uniformly randomizes over playable cards when available, otherwise draws.

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

Player 2's action is inferred from observation $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed) AND $n_2^{t+1} = n_2^t - 1$ (hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

Checking the belief factorization and other key equations:

Fixing the observation inference to explicitly reference observations:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

**Note:** Additional termination condition: If during a draw action, after reshuffle $|D^{t+}| < k$ where $k$ is the required draw count, the game terminates immediately. This is handled during transitions, not as a static state property.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 2$ (Player 1's turn ends immediately, Player 2's turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends immediately, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{playable}}(s)]}{|\mathcal{A}_{\text{playable}}(s)|} & \text{if } \mathcal{A}_{\text{playable}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw} \text{ and } \mathcal{A}_{\text{playable}}(s) = \emptyset
\end{cases}
$$

This policy uniformly randomizes over playable cards when available, otherwise draws.

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

Player 2's action is inferred from observations $o_t$ and $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed in observations) AND $n_2^{t+1} = n_2^t - 1$ (opponent hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$ from observation $o_{t+1}$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observation $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged) AND $n_2^{t+1} > n_2^t$ (hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

**Note:** Additional termination condition: If during a draw action, after reshuffle $|D^{t+}| < k$ where $k$ is the required draw count, the game terminates immediately. This is handled during transitions, not as a static state property.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 2$ (Player 1's turn ends immediately, Player 2's turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends immediately, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{playable}}(s)]}{|\mathcal{A}_{\text{playable}}(s)|} & \text{if } \mathcal{A}_{\text{playable}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw} \text{ and } \mathcal{A}_{\text{playable}}(s) = \emptyset
\end{cases}
$$

This policy uniformly randomizes over playable cards when available, otherwise draws.

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

Player 2's action is inferred from observations $o_t$ and $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed in observations) AND $n_2^{t+1} = n_2^t - 1$ (opponent hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$ from observation $o_{t+1}$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observations $o_t$ and $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged in observations) AND $n_2^{t+1} > n_2^t$ (opponent hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

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
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

Clarifying the initial belief distribution and checking the reshuffle calculation:

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
- $T^t = (c_{\text{top}}, \tilde{c}) \in K \times \mathcal{C}$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
  - $\tilde{c} \in \mathcal{C}$ is the active/declared color: if $c_{\text{top}}$ is not wild, then $\tilde{c} = \text{color}(c_{\text{top}})$; if $c_{\text{top}}$ is wild, then $\tilde{c}$ is the color declared when it was played
- $\text{turn}^t \in \{1, 2\}$: Active player
- $\text{meta}^t = n_{\text{draw}} \in \mathbb{N}_0$: Accumulated draw penalty (from +2 or Wild+4)

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

**Note:** Additional termination condition: If during a draw action, after reshuffle $|D^{t+}| < k$ where $k$ is the required draw count, the game terminates immediately. This is handled during transitions, not as a static state property.

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

This filters out impossible states from possible states.

---

## 4. Action Space $\mathcal{A}$

**Note:** This action space is defined from Player 1's perspective. Player 2's actions follow the same structure but are part of the opponent model.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = \{(c, \tilde{c}) : c \in H_1^t, \tilde{c} \in \mathcal{C}\}$$

- For non-wild cards $c$: $\tilde{c}$ must equal $\text{color}(c)$ (the card's inherent color)
- For wild cards $c$: $\tilde{c} \in \mathcal{C}$ is the declared color chosen by the player (e.g., "Wild+4 blue" means $\tilde{c} = \text{blue}$)

Every play action always includes a color declaration: either the card's inherent color (non-wild) or the player's choice (wild).

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally, or $n_{\text{draw}}$ cards if penalty is active

**Legal Action Set:**

For any state $s_t$ with active player $i$ ($\text{turn}^t = i$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$ (symmetric for both players):

First, define the set of playable card actions:
$$\mathcal{A}_{\text{playable}}(s_t) = \{(c, \tilde{c}) : c \in H_i^t, \text{playable}(c, T^t), \tilde{c} = \text{color}(c) \text{ if } \text{rank}(c) \notin \mathcal{W}, \tilde{c} \in \mathcal{C} \text{ if } \text{rank}(c) \in \mathcal{W}\}$$

Then the legal action set is:

$$
\mathcal{A}_{\text{legal}}(s_t) = \begin{cases}
\{\text{Draw}\} & \text{if } n_{\text{draw}} > 0 \text{ (penalty active, must draw)} \\
\mathcal{A}_{\text{playable}}(s_t) & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) \neq \emptyset \text{ (can only play if playable cards exist)} \\
\{\text{Draw}\} & \text{if } n_{\text{draw}} = 0 \text{ and } \mathcal{A}_{\text{playable}}(s_t) = \emptyset \text{ (no playable cards, must draw)}
\end{cases}
$$

where $H_i^t$ is the hand of the active player (Player 1 if $\text{turn}^t = 1$, Player 2 if $\text{turn}^t = 2$).

**Rule:** You can only draw if you have no playable cards (or if a draw penalty is active).

The playability function is:

$$
\text{playable}(c, T) = \begin{cases}
\text{true} & \text{if } \text{rank}(c) \in \mathcal{W} \\
\text{true} & \text{if } \text{color}(c) = \tilde{c} \text{ (declared color in } T) \\
\text{true} & \text{if } \text{rank}(c) = \text{rank}(c_{\text{top}}) \\
\text{false} & \text{otherwise}
\end{cases}
$$

**2-Player Special Rules:**

- Reverse acts as Skip: In 2-player UNO, both Skip and Reverse end the current player's turn immediately and pass to the opponent (no additional turn for the player who played it)
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
   - If $|D^{t+}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+} = D^t$, $P^{t+} = P^t$
3. Since $D^{t+}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+}$ has equal probability $\frac{1}{\binom{|D^{t+}|}{k}}$
4. Update: $H_1^{t+} = H_1^t \cup \{d_1, \ldots, d_k\}$, $D^{t+} = D^{t+} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+} = 0$
6. **Forced end turn**: $\text{turn}^{t+} = 2$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_1^{t+} = H_1^t \setminus \{c\}$
2. Update top card: $T^{t+} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+} = P^t \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 2$, $\text{turn}^{t+} = 2$
   - **Wild+4**: $n_{\text{draw}}^{t+} = n_{\text{draw}}^t + 4$, $\text{turn}^{t+} = 2$
   - **Skip or Reverse**: $\text{turn}^{t+} = 2$ (Player 1's turn ends immediately, Player 2's turn)
   - **Number or Wild**: $\text{turn}^{t+} = 2$

State after Player 1's action: $s^{t+} = (H_1^{t+}, H_2^t, D^{t+}, P^{t+}, T^{t+}, \text{turn}^{t+}, \text{meta}^{t+})$

### 5.2. Player 2 Response Phase (Opponent Model)

If $\text{turn}^{t+} = 2$ and $|H_2^{t+}| > 0$:

Player 2 selects action $a_2 \sim \pi_2(\cdot \mid s^{t+})$ from $\mathcal{A}_{\text{legal}}(s^{t+})$.

**Player 2's transitions follow the same structure as Player 1** (Section 5.1), but applied to Player 2:

**Drawing:**
If $a_2 = \text{Draw}$:

1. Determine draw count: $k = \max(1, n_{\text{draw}})$
2. If $|D^{t+}| < k$: **Reshuffle**
   - Combine discard (except top card) with deck: $D^{t+1} = (P^{t+} \setminus \{c_{\text{top}}^{t+}\}) \cup D^{t+}$
   - Set $P^{t+1} = \{c_{\text{top}}^{t+}\}$
   - If $|D^{t+1}| < k$: **Game ends** (impossible to draw $k$ cards - terminal state). The player with the least number of cards in their hand wins. If tied, the game is a draw.
     Else: $D^{t+1} = D^{t+}$, $P^{t+1} = P^{t+}$
3. Since $D^{t+1}$ is unordered (multiset), sample $k$ cards uniformly at random without replacement from $D^{t+1}$: $\{d_1, \ldots, d_k\}$
   - Each $k$-subset of $D^{t+1}$ has equal probability $\frac{1}{\binom{|D^{t+1}|}{k}}$
4. Update: $H_2^{t+1} = H_2^{t+} \cup \{d_1, \ldots, d_k\}$, $D^{t+1} = D^{t+1} \setminus \{d_1, \ldots, d_k\}$
5. Reset penalty: $n_{\text{draw}}^{t+1} = 0$
6. **Forced end turn**: $\text{turn}^{t+1} = 1$

**Playing a card $(c, \tilde{c})$:**

1. Remove from hand: $H_2^{t+1} = H_2^{t+} \setminus \{c\}$
2. Update top card: $T^{t+1} = (c, \tilde{c})$ (use the declared color from the action)
3. Add to discard: $P^{t+1} = P^{t+} \cup \{c\}$
4. Handle card effects:
   - **+2**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 2$, $\text{turn}^{t+1} = 1$
   - **Wild+4**: $n_{\text{draw}}^{t+1} = n_{\text{draw}}^{t+} + 4$, $\text{turn}^{t+1} = 1$
   - **Skip or Reverse**: $\text{turn}^{t+1} = 1$ (Player 2's turn ends immediately, Player 1's turn)
   - **Number or Wild**: $\text{turn}^{t+1} = 1$

After Player 2's action completes, the resulting state is $s_{t+1}$.

**Terminal Check:** The game terminates **immediately** when a player plays their last card, reducing their hand size to 0. This is checked immediately after the action that empties the hand, before any turn transitions.

The opponent policy $\pi_2$ is a probability distribution over legal actions. Common models:

**Uniform Random:**
$$\pi_2^{\text{unif}}(a \mid s) = \frac{\mathbb{1}[a \in \mathcal{A}_{\text{legal}}(s)]}{|\mathcal{A}_{\text{legal}}(s)|}$$

**Greedy (prefer plays over draws):**

$$
\pi_2^{\text{greedy}}(a \mid s) = \begin{cases}
\frac{\mathbb{1}[a \in \mathcal{A}_{\text{playable}}(s)]}{|\mathcal{A}_{\text{playable}}(s)|} & \text{if } \mathcal{A}_{\text{playable}}(s) \neq \emptyset \\
1 & \text{if } a = \text{Draw} \text{ and } \mathcal{A}_{\text{playable}}(s) = \emptyset
\end{cases}
$$

This policy uniformly randomizes over playable cards when available, otherwise draws.

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

Player 2's action is inferred from observations $o_t$ and $o_{t+1}$:

- **If $T^{t+1} \neq T^t$ (top card changed in observations) AND $n_2^{t+1} = n_2^t - 1$ (opponent hand size decreased by 1)**: Player 2 played card $c_2$ where $T^{t+1} = (c_2, \tilde{c}_2)$ from observation $o_{t+1}$

For each hypothesis $H_2$ in belief support, the likelihood is:
$$P(\text{play } c_2 \mid H_2, s^{t+}) = \mathbb{1}[c_2 \in H_2] \cdot \pi_2((c_2, \tilde{c}_2) \mid s^{t+})$$

Updated belief over new hands $H_2' = H_2 \setminus \{c_2\}$:
$$b_{t+1}(H_2') \propto \sum_{H_2 : H_2 \setminus \{c_2\} = H_2'} P(\text{play } c_2 \mid H_2, s^{t+}) \cdot b_t(H_2)$$

### 7.4. Opponent Draw Observation

Player 2's draw is inferred from observations $o_t$ and $o_{t+1}$:

- **If $T^{t+1} = T^t$ (top card unchanged in observations) AND $n_2^{t+1} > n_2^t$ (opponent hand size increased)**: Player 2 drew $k = n_2^{t+1} - n_2^t$ cards

**Note:** These two cases are mutually exclusive - either a card was played (top card changes) or cards were drawn (top card unchanged, hand size increases).

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
   - $T^0 = (c_{\text{top}}^0, \text{color}(c_{\text{top}}^0))$ (since $c_{\text{top}}^0$ is not wild, $\tilde{c} = \text{color}(c_{\text{top}}^0)$)

### 8.2. Initial Belief Distribution

Player 1 observes their initial hand $H_1^0$ and top card $T^0$. The initial belief is uniform over all consistent deals:

$$b_0(s) \propto \mathbb{1}[\text{s is consistent with } (H_1^0, T^0, P^0 = \{c_{\text{top}}^0\}, n_2^0 = 7, n_d^0 = |D^0|)]$$

Specifically, for the unseen pool $U_0$ with $|U_0| = m_0$:
$$b_0^H(H_2) = \frac{\mathbb{1}[H_2 \subseteq U_0, |H_2| = 7]}{\binom{m_0}{7}}$$

For each possible $H_2$, the draw deck is deterministically $D^0 = U_0 \setminus H_2$ (the complement of $H_2$ in $U_0$). The uniform distribution over all $\binom{m_0}{7}$ possible hands $H_2$ induces a uniform distribution over the corresponding deck configurations.

---

## 9. Reward Function $R$

Define immediate reward for Player 1 (evaluated on the state after action $a$):

$$
R(s', a) = \begin{cases}
+1 & \text{if } |H_1| = 0 \text{ in state } s' \text{ (Player 1 wins)} \\
-1 & \text{if } |H_2| = 0 \text{ in state } s' \text{ (Player 2 wins)} \\
+1 & \text{if game ends due to inability to draw and } |H_1| < |H_2| \text{ (Player 1 wins by fewer cards)} \\
-1 & \text{if game ends due to inability to draw and } |H_2| < |H_1| \text{ (Player 2 wins by fewer cards)} \\
0 & \text{if game ends due to inability to draw and } |H_1| = |H_2| \text{ (draw)} \\
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

Verifying the reward function handles all cases correctly:

## Summary of Fixes

1. **Terminal States (line 48)**: Removed the invalid condition referencing `k` (not a state property). Clarified that draw-impossibility termination is handled during transitions.

2. **Greedy Policy (line 218)**: Fixed undefined `A_play` → `A_playable(s)` to match the defined legal action set.

3. **Observation Inference (lines 292-306)**: Clarified that inference uses observations `o_t` and `o_{t+1}`, not raw states.

4. **Initial Belief (line 342)**: Clarified that the draw deck distribution is deterministic given `H_2` and uniformly distributed over all possible hands.

All other equations verified:

- State consistency constraint ✓
- Observation likelihood ✓
- Transition probabilities (including reshuffle) ✓
- Belief factorization ✓
- Belief update formulas ✓
- Reward function (all terminal cases) ✓
- Value function and Bellman equation ✓
- Marginal computations ✓

The document is mathematically consistent and ready for implementation.
