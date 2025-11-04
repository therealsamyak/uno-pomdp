"""
Display utilities for CLI interface.
"""

from typing import Optional

from ..core import (
    Action,
    Card,
    Color,
    DrawAction,
    Observation,
    PlayAction,
)


# Color codes for terminal output
COLOR_CODES = {
    Color.RED: "\033[91m",
    Color.YELLOW: "\033[93m",
    Color.BLUE: "\033[94m",
    Color.GREEN: "\033[92m",
}
RESET = "\033[0m"
BOLD = "\033[1m"


def colorize(text: str, color: Optional[Color]) -> str:
    """Add terminal color codes to text"""
    if color is None:
        return text
    return f"{COLOR_CODES.get(color, '')}{text}{RESET}"


def format_card(card: Card) -> str:
    """Format a card for display"""
    if card.is_wild():
        return f"[{card.rank.value}]"

    color_str = colorize(card.color.value[:3].upper(), card.color)
    rank_str = card.rank.value
    return f"[{color_str} {rank_str}]"


def format_hand(hand: list[Card], show_indices: bool = True) -> str:
    """
    Format a hand of cards for display.

    Args:
        hand: Cards to display
        show_indices: Whether to show card indices

    Returns:
        Formatted string
    """
    if not hand:
        return "Empty hand"

    lines = []
    for i, card in enumerate(hand, 1):
        card_str = format_card(card)
        if show_indices:
            lines.append(f"{i}. {card_str}")
        else:
            lines.append(card_str)

    if show_indices:
        return "\n".join(lines)
    else:
        return " ".join(lines)


def format_top_card(top_card) -> str:
    """Format the top card"""
    card_str = format_card(top_card.card)
    declared = colorize(top_card.declared_color.value.upper(), top_card.declared_color)
    return f"{card_str} (active color: {declared})"


def display_game_state(observation: Observation, turn_player: int = 1) -> None:
    """
    Display the current game state.

    Args:
        observation: Current observation
        turn_player: Whose turn it is (1 or 2)
    """
    print("\n" + "=" * 60)
    print(f"{BOLD}GAME STATE{RESET}")
    print("=" * 60)

    # Top card
    print(f"\n{BOLD}Top Card:{RESET}")
    print(f"  {format_top_card(observation.top_card)}")

    # Draw penalty
    if observation.draw_penalty > 0:
        print(
            f"\n{BOLD}⚠️  Draw Penalty Active: {observation.draw_penalty} cards{RESET}"
        )

    # Player 1's hand
    print(f"\n{BOLD}Your Hand ({len(observation.hand_1)} cards):{RESET}")
    print(format_hand(observation.hand_1, show_indices=True))

    # Opponent info
    print(f"\n{BOLD}Opponent:{RESET}")
    print(f"  Hand size: {observation.opponent_hand_size} cards")

    # Deck info
    print(f"\n{BOLD}Deck:{RESET} {observation.deck_size} cards remaining")

    # Turn indicator
    print(f"\n{BOLD}Turn:{RESET} Player {turn_player}")
    print("=" * 60)


def display_actions(actions: list[Action]) -> None:
    """
    Display available actions.

    Args:
        actions: Legal actions
    """
    print(f"\n{BOLD}Available Actions:{RESET}")

    for i, action in enumerate(actions, 1):
        if isinstance(action, DrawAction):
            print(f"{i}. Draw cards")
        elif isinstance(action, PlayAction):
            card_str = format_card(action.card)
            if action.card.is_wild():
                color_str = colorize(
                    action.declared_color.value.upper(), action.declared_color
                )
                print(f"{i}. Play {card_str} → {color_str}")
            else:
                print(f"{i}. Play {card_str}")


def display_action(action: Action, player: int, player_name: str = None) -> None:
    """
    Display an action taken by a player.

    Args:
        action: Action taken
        player: Player number
        player_name: Optional custom player name (e.g., "AI", "You")
    """
    if player_name:
        player_str = f"{BOLD}{player_name}{RESET}"
    else:
        player_str = f"{BOLD}Player {player}{RESET}"

    if isinstance(action, DrawAction):
        print(f"  {player_str} draws cards")
    elif isinstance(action, PlayAction):
        card_str = format_card(action.card)
        if action.card.is_wild():
            color_str = colorize(
                action.declared_color.value.upper(), action.declared_color
            )
            print(f"  {player_str} plays {card_str} → {color_str}")
        else:
            print(f"  {player_str} plays {card_str}")


def format_action(action: Action) -> str:
    """
    Format an action as a string.

    Args:
        action: Action to format

    Returns:
        Formatted action string
    """
    if isinstance(action, DrawAction):
        return "Draw"
    elif isinstance(action, PlayAction):
        card_str = format_card(action.card)
        if action.card.is_wild():
            color_str = colorize(
                action.declared_color.value.upper(), action.declared_color
            )
            return f"{card_str} → {color_str}"
        else:
            return card_str
    return str(action)


def display_winner(winner: int, num_turns: int) -> None:
    """
    Display game result.

    Args:
        winner: Winner (1, 2, or 0 for draw)
        num_turns: Number of turns played
    """
    print("\n" + "=" * 60)
    print(f"{BOLD}GAME OVER{RESET}")
    print("=" * 60)

    if winner == 0:
        print("Result: DRAW")
    else:
        print(f"Winner: {BOLD}Player {winner}{RESET}")

    print(f"Turns played: {num_turns}")
    print("=" * 60)


def clear_screen() -> None:
    """Clear the terminal screen"""
    import os

    os.system("clear" if os.name != "nt" else "cls")


def display_move_log(
    moves: list[tuple[int, Action, int, int]], max_recent: int = 10
) -> None:
    """
    Display recent move history.

    Args:
        moves: List of (player, action, hand_size_after, turn_number) tuples
        max_recent: Maximum number of recent moves to show
    """
    if not moves:
        return

    print(f"\n{BOLD}Move History (last {min(len(moves), max_recent)}):{RESET}")
    print("-" * 60)

    start_idx = max(0, len(moves) - max_recent)
    for i, (player, action, hand_size, turn) in enumerate(
        moves[start_idx:], start=start_idx + 1
    ):
        player_name = "🤖 AI" if player == 1 else "👤 You"
        action_str = format_action(action)
        print(f"  {i}. {player_name}: {action_str} (hand: {hand_size} cards)")

    print("-" * 60)


def display_compact_state(
    top_card,
    hand_1_size: int,
    hand_2_size: int,
    deck_size: int,
    draw_penalty: int,
    turn_player: int,
) -> None:
    """
    Display compact game state for AI vs AI.

    Args:
        top_card: Top card info
        hand_1_size: Player 1 hand size
        hand_2_size: Player 2 hand size
        deck_size: Deck size
        draw_penalty: Active draw penalty
        turn_player: Current turn player
    """
    top_str = format_top_card(top_card)
    turn_str = f"{BOLD}Player {turn_player}{RESET}"
    penalty_str = f" | ⚠️  Penalty: {draw_penalty}" if draw_penalty > 0 else ""

    print(
        f"\n  Top: {top_str} | P1: {hand_1_size} cards | P2: {hand_2_size} cards | Deck: {deck_size}{penalty_str} | Turn: {turn_str}"
    )
