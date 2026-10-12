
"""Logic-Based Nim Tutor AI
Features:
1. Optimal normal Nim strategy using XOR
2. Minimax verification
3. CSP position generation using backtracking
4. Rule-based explanations and hints
5. Misere Nim support
6. Benchmark on 50 positions
7. Imperfect-opponent simulation
"""

import random
import time
from functools import lru_cache


# --------------------------------------------------
# 1. NIM THEORY AND XOR
# --------------------------------------------------

def nim_sum(heaps):
    """Calculate the XOR of all heap sizes."""
    result = 0
    for heap in heaps:
        result ^= heap
    return result


def is_winning_position(heaps, misere=False):
    """Determine whether the current position is winning."""
    heaps = [h for h in heaps if h > 0]

    if not heaps:
        return False

    if misere and all(h == 1 for h in heaps):
        # In misere Nim, the player taking the last
        # object loses. Odd heaps of size 1 are losing.
        return len(heaps) % 2 == 0

    return nim_sum(heaps) != 0


def explain_position(heaps, misere=False):
    """Explain the current position in simple language."""
    value = nim_sum(heaps)

    print("\nCurrent heaps:", heaps)
    print("Nim-sum:", value)

    if misere:
        print("Rule: The player taking the last object loses.")
        if all(h <= 1 for h in heaps):
            if sum(h > 0 for h in heaps) % 2 == 1:
                print("Reason: Odd number of single-object heaps.")
                print("This is a losing position.")
            else:
                print("Reason: Even number of single-object heaps.")
                print("This is a winning position.")
            return

    if value == 0:
        print("Reason: Nim-sum is zero.")
        print("This is a losing position with perfect play.")
    else:
        print("Reason: Nim-sum is nonzero.")
        print("This is a winning position with perfect play.")


# --------------------------------------------------
# 2. OPTIMAL AI MOVE
# --------------------------------------------------

def optimal_move(heaps, misere=False):
    """
    Return (heap_index, amount_to_remove, explanation).
    heap_index is zero-based.
    Return None if no legal move exists.
    """
    heaps = list(heaps)

    if not any(heaps):
        return None

    if misere:
        nonempty = [i for i, h in enumerate(heaps) if h > 0]
        large = [i for i in nonempty if heaps[i] > 1]
        ones = len(nonempty) - len(large)

        if len(large) == 1:
            i = large[0]

            # Leave an even number of heaps of size 1
            # to the opponent.
            target = 1 if ones % 2 == 0 else 0
            amount = heaps[i] - target

            return (
                i,
                amount,
                f"Misere endgame: reduce heap {i + 1} "
                f"to {target}, leaving an even number "
                "of single-object heaps."
            )

        if len(large) == 0:
            # All remaining heaps contain one object.
            i = nonempty[0]
            amount = 1

            return (
                i,
                amount,
                "Misere endgame: remove one object to "
                "control the parity of the remaining heaps."
            )

    value = nim_sum(heaps)

    if value != 0:
        for i, heap in enumerate(heaps):
            target = heap ^ value

            if target < heap:
                amount = heap - target
                new_heaps = list(heaps)
                new_heaps[i] = target
                new_value = nim_sum(new_heaps)

                explanation = (
                    f"Nim-sum was {value}. Reduce heap {i + 1} "
                    f"from {heap} to {target}, removing "
                    f"{amount}. The new nim-sum is {new_value}."
                )

                return i, amount, explanation

    # If the position is losing, choose a legal move.
    # Against perfect play, no move can guarantee a win.
    i = max(range(len(heaps)), key=lambda j: heaps[j])

    return (
        i,
        1,
        "The nim-sum is zero. This is a losing position "
        "with perfect play, so choose a legal move and "
        "hope the opponent makes a mistake."
    )


def apply_move(heaps, index, amount):
    """Apply a legal move and return a new heap list."""
    if not 0 <= index < len(heaps):
        raise ValueError("Invalid heap number.")

    if amount < 1 or amount > heaps[index]:
        raise ValueError("Invalid number of objects to remove.")

    result = list(heaps)
    result[index] -= amount
    return result


# --------------------------------------------------
# 3. MINIMAX SOLVER
# --------------------------------------------------

@lru_cache(maxsize=None)
def minimax_winning(state):
    """
    Normal Nim minimax.
    True means the current player can force a win.
    The player with no legal moves loses.
    """
    if not any(state):
        return False

    for i, heap in enumerate(state):
        for amount in range(1, heap + 1):
            next_state = list(state)
            next_state[i] -= amount
            next_state = tuple(next_state)

            if not minimax_winning(next_state):
                return True

    return False


def compare_rules_and_minimax(number_of_positions=50):
    """Compare XOR reasoning and minimax on random positions."""
    rng = random.Random(42)

    positions = []

    for _ in range(number_of_positions):
        heap_count = rng.randint(1, 4)
        heaps = [
            rng.randint(0, 6)
            for _ in range(heap_count)
        ]

        if not any(heaps):
            heaps[0] = 1

        positions.append(tuple(heaps))

    start = time.perf_counter()
    rule_results = [
        is_winning_position(p) for p in positions
    ]
    rule_time = time.perf_counter() - start

    minimax_winning.cache_clear()

    start = time.perf_counter()
    minimax_results = [
        minimax_winning(p) for p in positions
    ]
    minimax_time = time.perf_counter() - start

    agreement = sum(
        a == b
        for a, b in zip(rule_results, minimax_results)
    )

    print("\nRULE-BASED AI VS MINIMAX")
    print("-" * 40)
    print(f"Positions tested: {number_of_positions}")
    print(f"Agreement: {agreement}/{number_of_positions}")
    print(f"Agreement percentage: "
          f"{agreement / number_of_positions * 100:.2f}%")
    print(f"Rule-based time: {rule_time:.6f} seconds")
    print(f"Minimax time: {minimax_time:.6f} seconds")

    for i, (position, rule, mm) in enumerate(
        zip(positions, rule_results, minimax_results), 1
    ):
        print(
            f"{i:02d}. {list(position)} | "
            f"Rules: {'WIN' if rule else 'LOSS'} | "
            f"Minimax: {'WIN' if mm else 'LOSS'}"
        )

    if agreement != number_of_positions:
        print("WARNING: A disagreement needs investigation.")


# --------------------------------------------------
# 4. CSP: CONSTRAINT SATISFACTION POSITION GENERATOR
# --------------------------------------------------

def generate_positions(
    number_of_heaps,
    minimum_size,
    maximum_size,
    target="zero",
    limit=10
):
    """
    Generate heap positions satisfying an XOR constraint.
    Uses recursive backtracking and checks XOR feasibility
    when the final heap is assigned.
    """
    if number_of_heaps < 1:
        raise ValueError("Number of heaps must be at least 1.")

    if minimum_size < 0 or maximum_size < minimum_size:
        raise ValueError("Invalid heap-size range.")

    if target not in ("zero", "nonzero"):
        raise ValueError("Target must be zero or nonzero.")

    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    results = []
    assignment = []

    def backtrack(depth, current_xor):
        if len(results) >= limit:
            return

        if depth == number_of_heaps:
            matches = (
                current_xor == 0
                if target == "zero"
                else current_xor != 0
            )

            if matches:
                results.append(assignment.copy())

            return

        remaining = number_of_heaps - depth - 1

        for value in range(minimum_size, maximum_size + 1):
            next_xor = current_xor ^ value

            # Final-variable propagation:
            # once every variable is assigned, XOR must
            # satisfy the requested constraint.
            if remaining == 0:
                matches = (
                    next_xor == 0
                    if target == "zero"
                    else next_xor != 0
                )

                if not matches:
                    continue

            assignment.append(value)
            backtrack(depth + 1, next_xor)
            assignment.pop()

            if len(results) >= limit:
                return

    backtrack(0, 0)
    return results


def run_csp_generator():
    print("\nCSP POSITION GENERATOR")

    try:
        count = int(input("Number of heaps: "))
        minimum = int(input("Minimum heap size: "))
        maximum = int(input("Maximum heap size: "))
        target = input(
            "Nim-sum target (zero/nonzero): "
        ).strip().lower()
        limit = int(input("Number of positions to generate: "))

        positions = generate_positions(
            count, minimum, maximum, target, limit
        )

        print(f"\nGenerated {len(positions)} positions:")

        for position in positions:
            print(
                f"{position} -> nim-sum = "
                f"{nim_sum(position)}"
            )

    except ValueError as error:
        print("Invalid input:", error)


# --------------------------------------------------
# 5. IMPERFECT OPPONENT SIMULATION
# --------------------------------------------------

def simulate_opponent(games=200, mistake_probability=0.25):
    """
    Estimate AI win rate in normal Nim from [3, 4, 5].
    The opponent chooses a random legal move with the
    given probability; otherwise it uses optimal Nim.
    """
    if not 0 <= mistake_probability <= 1:
        raise ValueError("Mistake probability must be from 0 to 1.")

    rng = random.Random(7)
    ai_wins = 0

    for _ in range(games):
        heaps = [3, 4, 5]
        ai_turn = True

        while any(heaps):
            if ai_turn:
                move = optimal_move(heaps)
                i, amount, _ = move
                heaps = apply_move(heaps, i, amount)
            else:
                if rng.random() < mistake_probability:
                    legal_moves = [
                        (i, amount)
                        for i, heap in enumerate(heaps)
                        for amount in range(1, heap + 1)
                    ]
                    i, amount = rng.choice(legal_moves)
                else:
                    i, amount, _ = optimal_move(heaps)

                heaps = apply_move(heaps, i, amount)

            if not any(heaps):
                if ai_turn:
                    ai_wins += 1
                break

            ai_turn = not ai_turn

    return ai_wins, games, ai_wins / games


# --------------------------------------------------
# 6. PLAY AGAINST THE AI AND RECEIVE HINTS
# --------------------------------------------------

def play_game():
    print("\nPLAY NIM AGAINST AI")
    print("Normal Nim: taking the last object wins.")
    print("Enter a move as: heap_number objects_to_remove")
    print("Type 'hint' for an explanation.")

    raw = input("Enter starting heap sizes (e.g. 3 4 5): ")

    try:
        heaps = [int(x) for x in raw.split()]

        if not heaps or any(h < 0 for h in heaps) or not any(heaps):
            raise ValueError

    except ValueError:
        print("Enter nonnegative integers with at least one object.")
        return

    while any(heaps):
        print("\nCurrent heaps:", heaps)
        print("Nim-sum:", nim_sum(heaps))

        command = input("Your move or hint: ").strip().lower()

        if command == "hint":
            move = optimal_move(heaps)
            print("Tutor:", move[2])
            continue

        try:
            parts = command.split()

            if len(parts) != 2:
                raise ValueError

            heap_number, amount = map(int, parts)
            heaps = apply_move(heaps, heap_number - 1, amount)

        except ValueError:
            print("Invalid move. Example: 2 1")
            continue

        if not any(heaps):
            print("You took the last object. You win!")
            return

        i, amount, explanation = optimal_move(heaps)

        print("\nAI tutor:", explanation)
        heaps = apply_move(heaps, i, amount)

        print(f"AI removes {amount} from heap {i + 1}.")
        print("New heaps:", heaps)

        if not any(heaps):
            print("AI took the last object. AI wins!")
            return


# --------------------------------------------------
# 7. MAIN MENU
# --------------------------------------------------

def main():
    while True:
        print("\n" + "=" * 42)
        print("       LOGIC-BASED NIM TUTOR AI")
        print("=" * 42)
        print("1. Play against the AI")
        print("2. Explain Nim theory")
        print("3. Generate CSP positions")
        print("4. Compare rules vs minimax on 50 positions")
        print("5. Simulate imperfect opponent")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            play_game()

        elif choice == "2":
            print("\nNORMAL NIM THEORY")
            print("Nim-sum = XOR of all heap sizes.")
            print("Nim-sum != 0: winning position.")
            print("Nim-sum == 0: losing position with perfect play.")
            print("Choose a heap h and reduce it to h XOR nim-sum.")
            print("\nMISERE NIM")
            print("Taking the last object loses.")
            print("When all nonempty heaps have size 1, parity")
            print("determines whether the position is winning.")

            raw = input("Enter heaps to explain, e.g. 3 4 5: ")

            try:
                heaps = [int(x) for x in raw.split()]
                if not heaps or any(h < 0 for h in heaps):
                    raise ValueError
                explain_position(heaps)
            except ValueError:
                print("Please enter nonnegative heap sizes.")

        elif choice == "3":
            run_csp_generator()

        elif choice == "4":
            compare_rules_and_minimax(50)

        elif choice == "5":
            try:
                probability = float(
                    input("Opponent mistake probability (0 to 1): ")
                )
                wins, total, rate = simulate_opponent(
                    games=200,
                    mistake_probability=probability
                )
                print(f"AI wins: {wins}/{total}")
                print(f"Estimated AI win rate: {rate:.1%}")
                print("This estimate applies to this simulation setup.")
            except ValueError as error:
                print("Invalid input:", error)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Please select an option from 1 to 6.")


if __name__ == "__main__":
    main()
