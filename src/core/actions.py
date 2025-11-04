"""
Action space A for 2-player UNO POMDP.

Follows MATH.md §4: Action Space
"""

from dataclasses import dataclass
from typing import Optional, Union

from .cards import Card, Color


@dataclass(frozen=True)
class PlayAction:
    """
    Play action (c, c̃) where:
    - card: Card c to play from hand
    - declared_color: Color c̃ to declare

    Rules:
    - For non-wild cards: c̃ must equal color(c)
    - For wild cards: c̃ ∈ C is the player's choice

    Every play action always includes a color declaration.
    """

    card: Card
    declared_color: Color

    def __post_init__(self):
        # Validate color declaration
        if not self.card.is_wild():
            # Non-wild cards must declare their inherent color
            if self.card.color != self.declared_color:
                raise ValueError(
                    f"Non-wild card {self.card} must declare its inherent color "
                    f"{self.card.color}, not {self.declared_color}"
                )

    def __repr__(self) -> str:
        if self.card.is_wild():
            return f"Play({self.card.rank.value} → {self.declared_color.value})"
        return f"Play({self.card.color.value} {self.card.rank.value})"


@dataclass(frozen=True)
class DrawAction:
    """
    Draw action.

    Draws one card normally, or n_draw cards if penalty is active.
    """

    def __repr__(self) -> str:
        return "Draw"


# Type alias for all actions
Action = Union[PlayAction, DrawAction]


def create_play_action(
    card: Card, declared_color: Optional[Color] = None
) -> PlayAction:
    """
    Helper to create a play action with automatic color inference.

    Args:
        card: Card to play
        declared_color: Color to declare (required for wild cards)

    Returns:
        PlayAction with appropriate color declaration
    """
    if card.is_wild():
        if declared_color is None:
            raise ValueError(f"Must specify declared_color for wild card {card}")
        return PlayAction(card, declared_color)
    else:
        # Non-wild cards use their inherent color
        if declared_color is not None and declared_color != card.color:
            raise ValueError(
                f"Cannot override color for non-wild card {card}: "
                f"inherent color is {card.color}, not {declared_color}"
            )
        return PlayAction(card, card.color)
