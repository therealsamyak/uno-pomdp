"""
Card universe and deck generation for UNO POMDP.

Follows MATH.md §1: Notation and Primitive Sets
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Color(Enum):
    """Colors: C = {red, yellow, blue, green}"""

    RED = "red"
    YELLOW = "yellow"
    BLUE = "blue"
    GREEN = "green"


class Rank(Enum):
    """Ranks: R = {0, 1, 2, ..., 9, Skip, Reverse, +2} ∪ W = {Wild, Wild+4}"""

    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    SKIP = "Skip"
    REVERSE = "Reverse"
    DRAW_TWO = "+2"
    WILD = "Wild"
    WILD_DRAW_FOUR = "Wild+4"


@dataclass(frozen=True)
class Card:
    """
    A unique card in the labeled deck K = {K_1, K_2, ..., K_108}.

    Each card has:
    - id: Unique label K_i
    - rank: Card rank from R ∪ W
    - color: Card color from C ∪ {⊥} (⊥ for wild cards)
    """

    id: int
    rank: Rank
    color: Optional[Color]  # None (⊥) for wild cards

    def __repr__(self) -> str:
        if self.color is None:
            return f"Card({self.id}: {self.rank.value})"
        return f"Card({self.id}: {self.color.value} {self.rank.value})"

    def is_wild(self) -> bool:
        """Check if card is wild (color = ⊥)"""
        return self.color is None

    def is_action_card(self) -> bool:
        """Check if card is Skip, Reverse, +2, or Wild+4"""
        return self.rank in {
            Rank.SKIP,
            Rank.REVERSE,
            Rank.DRAW_TWO,
            Rank.WILD_DRAW_FOUR,
        }


def generate_deck() -> list[Card]:
    """
    Generate the full UNO deck K with 108 uniquely labeled cards.

    Composition:
    - 76 colored number cards: 1 zero per color, 2 each of 1-9 per color
    - 24 colored action cards: 2 each of Skip, Reverse, +2 per color
    - 4 Wild
    - 4 Wild+4

    Returns:
        List of 108 unique Card objects with sequential IDs
    """
    deck: list[Card] = []
    card_id = 0

    # Colored number cards
    for color in Color:
        # One zero per color
        deck.append(Card(card_id, Rank.ZERO, color))
        card_id += 1

        # Two each of 1-9 per color
        for rank_val in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            rank = Rank(rank_val)
            for _ in range(2):
                deck.append(Card(card_id, rank, color))
                card_id += 1

    # Colored action cards (2 each of Skip, Reverse, +2 per color)
    action_ranks = [Rank.SKIP, Rank.REVERSE, Rank.DRAW_TWO]
    for color in Color:
        for rank in action_ranks:
            for _ in range(2):
                deck.append(Card(card_id, rank, color))
                card_id += 1

    # Wild cards (4 Wild, 4 Wild+4)
    for _ in range(4):
        deck.append(Card(card_id, Rank.WILD, None))
        card_id += 1

    for _ in range(4):
        deck.append(Card(card_id, Rank.WILD_DRAW_FOUR, None))
        card_id += 1

    assert len(deck) == 108, f"Expected 108 cards, got {len(deck)}"
    return deck
