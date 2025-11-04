# 2-Player UNO POMDP (Player 1 Perspective)

## 1. Notation and Primitive Sets

**Card Universe**

- Colors: $\mathcal{C} = \{\text{red}, \text{yellow}, \text{blue}, \text{green}\}$
- Ranks: $\mathcal{R} = \{0, 1, 2, \ldots, 9}$

- Labeled deck: $K = \{K_1, K_2, \ldots, K_{76}\}$ where each $K_i$ is uniquely labeled
  - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color

**Temporal and Logical Primitives**

- Time: $t \in \mathbb{N}_0 = \{0, 1, 2, \ldots\}$
- Players: $\mathcal{P} = \{1, 2\}$ where Player 1 is the agent

---

## 2. State Space $\mathcal{S}$

A complete state is a tuple:
$$s_t = (H_1^t, H_2^t, D^t, P^t, T^t, \text{turn}^t) \in \mathcal{S}$$

**Components:**

- $H_i^t \subseteq K$: Player $i$'s hand (multiset)
- $D^t \subseteq K$: Draw deck (multiset, unordered). When drawing, sample uniformly at random from $D^t$.
- $P^t \subseteq K$: Discard pile (multiset, unordered). The top card $c_{\text{top}}$ is explicitly tracked in $T^t$; the rest $P^t \setminus \{c_{\text{top}}\}$ is unordered.
- $T^t = (c_{\text{top}}, \tilde{c}) \in K$: Active top card and declared color
  - $c_{\text{top}}$ is the card on top of the discard pile (used for playability rules)
- $\text{turn}^t \in \{1, 2\}$: Active player

**State Consistency Constraint:**
$$H_1^t \cup H_2^t \cup D^t \cup P^t = K$$
(partition of full deck, accounting for multiplicities). Note: $c_{\text{top}} \in P^t$ (it's the top card of the discard pile).

**Terminal States:**
$$\mathcal{S}_{\text{term}} = \{s \in \mathcal{S} : |H_1| = 0 \text{ or } |H_2| = 0\}$$

---

## 3. Observation Space $\Omega$

Player 1's observation at time $t$:
$$o_t = (H_1^t, n_2^t, n_d^t, P^t, T^t) \in \Omega$$

**Components:**

- $H_1^t$: Player 1's hand (fully observed)
- $n_2^t = |H_2^t| \in \mathbb{N}_0$: Opponent's hand size
- $n_d^t = |D^t| \in \mathbb{N}_0$: Draw deck size
- $P^t$: Discard pile multiset (visible)
- $T^t$: Top card and declared color (visible)

---

## 4. Action Space $\mathcal{A}$

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**
$$\mathcal{A}_{\text{play}} = c$$

**Draw Actions:**
$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

- Draws one card normally
- 
**Legal Action Set:**

For state $s_t$ with Player 1's turn ($\text{turn}^t = 1$), define $\mathcal{A}_{\text{legal}}(s_t) \subseteq \mathcal{A}$:

$$
\mathcal{A}_{\text{legal}}(s_t) =
$$

where



**2-Player Special Rules:**

- We only consider numbers and colors cards for this game.
