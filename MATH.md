2-person UNO solver. We are playing from the perspective of **Player1**.


## Deck Structure 
4 main colors: red, yellow, blue, green

{0} - 1 per color

{1, 2, ..., 9} - 2 per color

{SKIP, REVERSE} - 2 per color

{+2} - 2 per color

{WILDCARD, +4} - 4 total

Each card would be represented in the pile(array) by $R_0$ ~ $R_9$

$$ K = \{\text{card deck}\}$$

Let $K = \{K_1, K_2, \ldots, K_{108}\}$ be the complete card deck.


## System Definitions

We plan to model this as a POMDP.

<br/>
### State Space $S$

$$s = \{H_1, H_2, K_d, K_p, K_t\} \in S$$

where:
- $H_1$: Player 1 hand
- $H_2$: Player 2 hand (hidden)
- $K_d$: Cards currently in deck
- $K_p$: Cards in the pile
- $K_t$: Card currently on top of pile

<br/>
### Observation Space $\Omega$

$$o = \{H_1, N_2, N_d, K_p, K_t\} \in \Omega$$

Includes Player 2's response to Player 1's action (reflected in $K_t$).


<br/>
### Action Space $A$

Let $\mathcal{C} = \{\text{red, yellow, blue, green}\}$ be the set of colors.

$$A = A_{\text{draw}} \cup A_{\text{play}}$$

where:

**Draw actions**:
$$A_{\text{draw}} = \{D_i : i \in \{0, 1, 2, 4\}\}$$
- $D_0$: Draw 0 cards (forced by opponent's SKIP or REVERSE)
- $D_1$: Draw 1 card (voluntary draw)
- $D_2$: Draw 2 cards (forced by opponent's +2)
- $D_4$: Draw 4 cards (forced by opponent's +4)

**Play actions**:
$$A_{\text{play}} = \{(P, j, c) : j \in H_1, c \in \mathcal{C}\}$$

where $(P, j, c)$ means: Play card $j$ from hand with resulting color $c$.

- For **non-wild cards**: $c = \text{color}(j)$ (the card's own color)
- For **WILD/+4 cards**: $c \in \mathcal{C}$ is the player's choice


<br/>
$$a \in A = \begin{cases}
D_i & \text{draw } i \text{ cards, } i \in \{0, 1, 2, 4\} \\
(P, j, c) & \text{play card } j \text{ with resulting color } c
\end{cases}$$


<br/>
### Transition Probabilities $P(s' \mid s, a)$

$s, s' \in S$,
$a \in A$


Then control returns to Player 1.