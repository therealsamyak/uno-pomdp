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
- $T^t = c_{\text{top}} \in K$: Active top card and declared color
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

The action space consists of playing a card from the hand or drawing from the draw deck.

$$\mathcal{A} = \mathcal{A}_{\text{play}} \cup \mathcal{A}_{\text{draw}}$$

**Play Actions:**

$$\mathcal{A}_{\text{play}} = K$$

where $K = \{K_1, K_2, \ldots, K_{76}\}$ is the set of all uniquely labeled cards. A play action $c \in \mathcal{A}_{\text{play}}$ is executed only if $c \in H_1^t$ (Player 1's hand) and matches the top card $c_{\text{top}}$ in color ($\text{color}(c) = \text{color}(c_{\text{top}})$) or rank ($\text{rank}(c) = \text{rank}(c_{\text{top}})$).

**Draw Action:**

$$\mathcal{A}_{\text{draw}} = \{\text{Draw}\}$$

Executing Draw samples a card $k$ uniformly at random from $D^t$ (with probability $1/|D^t|$ for each $k \in D^t$) and adds it to $H_1^t$. If the drawn $k$ matches $c_{\text{top}}$ in color or rank, the player may choose to play it immediately as a play action; otherwise, the turn ends.

**Legal Action Set:**

For a state $s_t$ with $\text{turn}^t = 1$:

$$\mathcal{A}_{\text{legal}}(s_t) = \{ c \in H_1^t \mid \text{color}(c) = \text{color}(c_{\text{top}}) \lor \text{rank}(c) = \text{rank}(c_{\text{top}}) \} \cup \{\text{Draw}\}$$

The Draw action is always available, even if play actions exist. If no play actions are available, only Draw is legal.


**2-Player Special Rules:**

- We only consider numbers and colors cards for this game.
