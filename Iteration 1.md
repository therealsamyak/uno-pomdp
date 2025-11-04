```
{
  "num_players": 4,
  "player_id": 0,                     // you
  "my_hand": ["R5","R9","G2","BReverse","Y+2","W","W+4"],
  "discard_top": "G7",
  "current_color": "G",
  "hand_sizes": [7,7,7,7],            // sizes for each player’s hand (you included)
  "deck_count": 64,                   // unknown cards remaining in draw pile
  "direction": 1,                     // 1 or -1
  "turn": 0,                          // whose turn it is now
  "pending_draw": 0,                  // unresolved +2/+4 total the next player must draw
  "discard_history": ["R0","B5","G7"] // optional but helps belief; top is last element
}

```

```
# uno_next_action.py
# Choose the next UNO move from a single player's observable state
# via Monte-Carlo rollouts on sampled hidden states (particles).
# Standard library only.

import sys, json, random, copy, math
from dataclasses import dataclass
from collections import Counter, defaultdict

# ---------------------------
# Card + deck representation
# ---------------------------

COLORS = ["R", "G", "B", "Y"]
RANKS_NUM = [str(i) for i in range(10)]
RANKS_ACT = ["Skip", "Reverse", "+2"]
WILDS = ["Wild", "+4"]  # We'll encode as color "W"

@dataclass(frozen=True)
class Card:
    color: str  # "R/G/B/Y/W"
    rank: str   # "0-9", "Skip","Reverse","+2","Wild","+4"

    def key(self) -> str:
        if self.color == "W":
            return "W" if self.rank == "Wild" else "W+4"
        # e.g. "R5", "GReverse", "Y+2"
        return f"{self.color}{self.rank}"

    @staticmethod
    def from_key(s: str) -> "Card":
        # Accept "W" or "W+4" for wilds
        if s == "W":
            return Card("W", "Wild")
        if s == "W+4":
            return Card("W", "+4")
        # Otherwise first char is color; rest is rank
        c = s[0]
        r = s[1:]
        return Card(c, r)

def standard_deck():
    deck = []
    for c in COLORS:
        deck.append(Card(c, "0"))
        for _ in range(2):
            for r in RANKS_NUM[1:]:
                deck.append(Card(c, r))
            for a in RANKS_ACT:
                deck.append(Card(c, a))
    for _ in range(4):
        deck.append(Card("W", "Wild"))
        deck.append(Card("W", "+4"))
    return deck

# ---------------------------
# Game mechanics (simulator)
# ---------------------------

class GameState:
    """
    A full-information world state for fast simulation.
    We assume the following rule simplifications for speed:
      - If you DRAW and the drawn card is playable, you MAY immediately play it (common variant).
      - Pending +2/+4 is resolved by next player drawing that many cards and losing the turn.
      - No stacking of +2/+4 across players (keeps logic simple).
    """
    def __init__(self, N, hands, deck, discard, current_color, direction, turn, pending_draw):
        self.N = N
        self.hands = [list(h) for h in hands]  # list of lists[Card]
        self.deck = list(deck)
        self.discard = list(discard)
        self.current_color = current_color
        self.direction = direction
        self.turn = turn
        self.pending_draw = pending_draw
        self.done = False
        self.winner = None

    def copy(self):
        return GameState(
            self.N, self.hands, self.deck, self.discard,
            self.current_color, self.direction, self.turn, self.pending_draw
        )

    # ------------- core helpers -------------

    def _reshuffle_if_needed(self):
        if self.deck:
            return
        # Move all but top of discard into deck and shuffle
        top = self.discard[-1]
        pile = self.discard[:-1]
        random.shuffle(pile)
        self.deck = pile
        self.discard = [top]

    def _draw_one(self):
        self._reshuffle_if_needed()
        if not self.deck:
            return None
        return self.deck.pop()

    def _legal_actions(self, pid):
        """Return list of actions for player pid.
           Action format: ("PLAY", idx, declare_color or None) or ("DRAW",)
        """
        if self.done:
            return [("DRAW",)]  # dummy
        hand = self.hands[pid]
        top = self.discard[-1]
        acts = []
        # If pending draw exists, immediately resolve on current player and skip their own decision
        # (implemented in step turn advancement).
        # We model it by preventing any play on that turn; the turn logic will handle draws.
        if self.pending_draw > 0:
            return [("FORCED_DRAW",)]  # sentinel used internally

        # Otherwise, normal play or draw
        for i, card in enumerate(hand):
            if self._is_playable(card, top):
                if card.color == "W":
                    # Must declare a color
                    for col in COLORS:
                        acts.append(("PLAY", i, col))
                else:
                    acts.append(("PLAY", i, None))
        # Draw always allowed
        acts.append(("DRAW",))
        return acts

    def _is_playable(self, card: Card, top: Card) -> bool:
        return (
            card.color == "W"
            or card.color == self.current_color
            or card.rank == top.rank
        )

    def _apply_card_effects(self, pid, card: Card):
        if card.color != "W":
            self.current_color = card.color
        # Effects
        if card.rank == "Reverse":
            self.direction *= -1
        elif card.rank == "Skip":
            self.turn = (self.turn + self.direction) % self.N
        elif card.rank == "+2":
            self.pending_draw += 2
        elif card.rank == "+4":
            self.pending_draw += 4
        # Win?
        if len(self.hands[pid]) == 0:
            self.done = True
            self.winner = pid

    def _advance_turn(self):
        self.turn = (self.turn + self.direction) % self.N

    def legal_actions(self, pid):
        return self._legal_actions(pid)

    def step(self, pid, action, allow_draw_play=True):
        """
        Apply a single player's action and advance to next player's turn.
        """
        if self.done:
            return

        # Resolve pending draws at the start of the penalized player's turn
        if self.pending_draw > 0:
            if action != ("FORCED_DRAW",):
                # Safety: override with forced draw resolution
                action = ("FORCED_DRAW",)
            k = self.pending_draw
            self.pending_draw = 0
            for _ in range(k):
                c = self._draw_one()
                if c is not None:
                    self.hands[pid].append(c)
            # penalized player loses their turn
            self._advance_turn()
            return

        typ = action[0]
        if typ == "DRAW":
            drawn = self._draw_one()
            if drawn is not None:
                self.hands[pid].append(drawn)
                top = self.discard[-1]
                if allow_draw_play and self._is_playable(drawn, top):
                    # auto-play drawn card for tempo in simulation
                    self.hands[pid].pop()  # remove drawn
                    # If wild drawn, pick declare color as majority color in hand
                    decl = None
                    if drawn.color == "W":
                        decl = self._majority_color(pid) or random.choice(COLORS)
                        self.current_color = decl
                    self.discard.append(drawn)
                    self._apply_card_effects(pid, drawn)
                    if self.done:
                        return
            self._advance_turn()
            return

        if typ == "PLAY":
            _, idx, decl = action
            card = self.hands[pid].pop(idx)
            self.discard.append(card)
            if card.color == "W":
                # Must set color
                self.current_color = decl
            self._apply_card_effects(pid, card)
            if self.done:
                return
            self._advance_turn()
            return

        if typ == "FORCED_DRAW":
            # Should not reach here (handled above), but keep safe
            k = self.pending_draw
            self.pending_draw = 0
            for _ in range(k):
                c = self._draw_one()
                if c is not None:
                    self.hands[pid].append(c)
            self._advance_turn()
            return

    def _majority_color(self, pid):
        cnt = Counter([c.color for c in self.hands[pid] if c.color in COLORS])
        if not cnt:
            return None
        return cnt.most_common(1)[0][0]

# ---------------------------
# Opponent rollout policy
# ---------------------------

def opponent_policy(state: GameState, pid: int):
    acts = state.legal_actions(pid)
    # Forced draw sentinel
    if acts == [("FORCED_DRAW",)]:
        return ("FORCED_DRAW",)

    plays = [a for a in acts if a[0] == "PLAY"]
    if plays:
        # Prefer non-wild plays that keep a majority color for next time
        non_wild = [a for a in plays if state.hands[pid][a[1]].color != "W"]
        candidates = non_wild if non_wild else plays
        # Heuristic: choose a play that sets/keeps the player's majority color if possible
        majority = state._majority_color(pid)
        def score(a):
            card = state.hands[pid][a[1]] if a[0]=="PLAY" else None
            base = 0
            if card and card.color in COLORS and card.color == majority:
                base += 1
            # prefer shedding action cards late: + small bonus
            if card and card.rank in ("Skip","Reverse","+2"):
                base += 0.1
            return base + random.random()*0.01
        return max(candidates, key=score)

    # No play -> DRAW
    return ("DRAW",)

# ---------------------------
# Belief over hidden hands
# ---------------------------

def build_particles(observable, num_particles=256, rng_seed=None):
    """
    Create consistent worlds (hands for all players and deck) matching:
      - my hand
      - discard history and top
      - hand_sizes
      - deck_count
    The exact card identities of opponents & deck are sampled uniformly.
    """
    rnd = random.Random(rng_seed)
    N = observable["num_players"]
    me = observable["player_id"]
    my_hand = [Card.from_key(s) for s in observable["my_hand"]]
    hand_sizes = list(observable["hand_sizes"])
    deck_count = int(observable["deck_count"])
    discard_history = [Card.from_key(s) for s in observable.get("discard_history", [])]
    discard_top = Card.from_key(observable["discard_top"])
    current_color = observable["current_color"]
    direction = observable.get("direction", 1)
    turn = observable["turn"]
    pending_draw = observable.get("pending_draw", 0)

    # Build multiset of all cards, then remove known ones (my hand + discard history)
    full = standard_deck()
    pool = Counter(full)

    def remove_card(pool, card):
        if pool[card] <= 0:
            # Inconsistent; caller must ensure inputs are valid
            return False
        pool[card] -= 1
        if pool[card] == 0:
            del pool[card]
        return True

    # Remove my hand
    for c in my_hand:
        assert remove_card(pool, c), "Inconsistent: my_hand card not in deck"

    # Remove discard history (if any)
    if discard_history:
        for c in discard_history:
            assert remove_card(pool, c), "Inconsistent: discard history card not in deck"
        # Ensure last equals provided top if both given
        assert discard_history[-1] == discard_top, "discard_top must match last of discard_history"
        discard = list(discard_history)
    else:
        # Remove just the provided top
        assert remove_card(pool, discard_top), "Inconsistent: discard_top not in deck"
        discard = [discard_top]

    particles = []
    for _ in range(num_particles):
        # Deal unknowns: create a bag of remaining cards, shuffle, then assign
        bag = []
        for c, k in pool.items():
            bag.extend([c] * k)
        rnd.shuffle(bag)

        # Create opponent hands sized per hand_sizes, but we already know our hand.
        hands = [[] for _ in range(N)]
        hands[me] = list(my_hand)

        # Number of unknown cards needed in each opponent hand:
        needed = [hand_sizes[i] - (len(hands[i]) if i == me else 0) for i in range(N)]
        # Total unknowns to assign to hands:
        to_hands = sum(needed) - 0  # my unknowns are 0
        assert to_hands <= len(bag), "Inconsistent: not enough cards to fill hands"

        pos = 0
        for pid in range(N):
            if pid == me:
                continue
            k = needed[pid]
            hands[pid] = bag[pos:pos+k]
            pos += k

        # Remaining cards: draw deck
        deck = bag[pos:]
        # Optionally trim/extend deck to deck_count if provided is authoritative
        if deck_count is not None:
            if deck_count <= len(deck):
                deck = deck[:deck_count]
            else:
                # If requested deck_count is larger than remaining, we accept shorter deck
                # (better than asserting out; real games will fit).
                pass

        gs = GameState(N, hands, deck, discard, current_color, direction, turn, pending_draw)
        particles.append(gs)

    return particles

# ---------------------------
# Root action enumeration
# ---------------------------

def legal_root_actions_from_observable(observable):
    me = observable["player_id"]
    my_hand = [Card.from_key(s) for s in observable["my_hand"]]
    top = Card.from_key(observable["discard_top"])
    current_color = observable["current_color"]
    pending_draw = observable.get("pending_draw", 0)

    acts = []
    if pending_draw > 0:
        # Your turn but you must eat penalty right away (no defense modeled)
        return [("FORCED_DRAW",)]

    for i, card in enumerate(my_hand):
        if card.color == "W" or card.color == current_color or card.rank == top.rank:
            if card.color == "W":
                for col in COLORS:
                    acts.append(("PLAY", i, col))
            else:
                acts.append(("PLAY", i, None))
    acts.append(("DRAW",))
    return acts

# ---------------------------
# Monte-Carlo evaluation
# ---------------------------

def simulate_to_end(state: GameState, me: int, max_steps=200):
    """
    Play out a game using simple opponent policies (and same for 'me' inside rollouts)
    until terminal or step cap. Return 1 if 'me' wins else 0.
    """
    steps = 0
    while not state.done and steps < max_steps:
        pid = state.turn
        if pid == me:
            # Use same heuristic as opponents during rollout
            action = opponent_policy(state, pid)
        else:
            action = opponent_policy(state, pid)
        state.step(pid, action, allow_draw_play=True)
        steps += 1
    return 1 if state.done and state.winner == me else 0

def estimate_action_value(particles, root_action, me, sims_per_action=128):
    wins = 0
    for _ in range(sims_per_action):
        # Sample a world, clone, apply root action, then simulate
        world = random.choice(particles).copy()
        # If it's somehow not my turn due to inconsistent input, bail low
        if world.turn != me:
            return -1.0
        world.step(me, root_action, allow_draw_play=True)
        if world.done:
            wins += 1 if world.winner == me else 0
        else:
            wins += simulate_to_end(world, me)
    return wins / float(sims_per_action)

def pick_best_action(observable, num_particles=256, sims_total=1024, rng_seed=None):
    me = observable["player_id"]
    actions = legal_root_actions_from_observable(observable)
    if actions == [("FORCED_DRAW",)]:
        return ("DRAW",)  # Surface a real draw; simulator resolves penalty internally

    particles = build_particles(observable, num_particles=num_particles, rng_seed=rng_seed)
    # Split simulation budget across actions (at least 1 each)
    per = max(1, sims_total // max(1, len(actions)))
    scores = []
    for a in actions:
        val = estimate_action_value(particles, a, me, sims_per_action=per)
        scores.append((val, a))
    scores.sort(reverse=True, key=lambda t: t[0])
    return scores[0][1], dict(scores=scores)

# ---------------------------
# I/O helpers
# ---------------------------

def action_to_jsonable(action, my_hand):
    if action == ("FORCED_DRAW",) or action == ("DRAW",):
        return {"type": "DRAW"}
    typ, idx, decl = action
    card = my_hand[idx] if idx is not None else None
    return {
        "type": "PLAY",
        "card": card.key() if card else None,
        "declare_color": decl
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python uno_next_action.py state.json")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        obs = json.load(f)

    best_action, info = pick_best_action(
        obs,
        num_particles=obs.get("num_particles", 256),
        sims_total=obs.get("sims_total", 1024),
        rng_seed=obs.get("seed", None)
    )
    my_hand = [Card.from_key(s) for s in obs["my_hand"]]
    print(json.dumps(action_to_jsonable(best_action, my_hand)))

if __name__ == "__main__":
    main()

```

```
{
  "num_players": 4,
  "player_id": 0,
  "my_hand": ["R5","R9","G2","BReverse","Y+2","W","W+4"],
  "discard_top": "G7",
  "current_color": "G",
  "hand_sizes": [7,7,7,7],
  "deck_count": 64,
  "direction": 1,
  "turn": 0,
  "pending_draw": 0,
  "discard_history": ["R0","B5","G7"],
  "num_particles": 256,
  "sims_total": 1024,
  "seed": 42
}

```