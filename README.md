# nim-logic-tutor-ai
Logic-Based Nim Tutor AI using XOR, minimax, CSP backtracking, and opponent simulation
# Nim Logic Tutor AI

## 1. Project Overview

**Nim Logic Tutor AI** is an Artificial Intelligence project based on the mathematical game Nim. It uses optimal game-playing strategies to determine winning moves and helps users understand the logic behind each decision.

The project also includes a **Constraint Satisfaction Problem (CSP)** extension that generates valid Nim positions based on user-defined constraints, such as the number of heaps, heap-size limits, and Nim-sum conditions.

## 2. Objectives

- Develop an AI agent that plays Nim optimally.
- Implement the Minimax algorithm or Grundy number theory.
- Determine winning and losing positions using XOR operations.
- Generate Nim positions using backtracking.
- Apply CSP constraints to filter valid game positions.
- Explain the mathematical logic behind the AI's decisions.

## 3. Technologies Used

- **Programming Language:** Python 3
- **IDE:** Visual Studio Code
- **AI Concepts:** Game Theory, Optimal Search, Grundy Numbers
- **CSP Techniques:** Backtracking and Constraint Checking
- **Version Control:** Git and GitHub

## 4. Project Features

### A. Nim Game AI

- Supports multiple heaps of objects.
- Allows players to take turns removing objects.
- Ensures that a move removes one or more objects from exactly one heap.
- Uses XOR-based Nim strategy to identify winning moves.
- Determines whether a position is winning or losing under optimal play.

### B. Logic-Based Nim Tutor

- Explains the concept of Nim-sum.
- Demonstrates how XOR operations determine winning positions.
- Identifies moves that change a losing position into a winning one.
- Helps users understand the reasoning behind AI decisions.

## 5. Theory Behind the AI

The Nim game consists of several heaps of objects. During each turn, a player removes one or more objects from exactly one heap.

The AI calculates the **Nim-sum** by performing a bitwise XOR operation on all heap sizes.

For heap sizes \(a_1, a_2, \ldots, a_n\):

**Nim-sum = a₁ XOR a₂ XOR ... XOR aₙ**

- If the Nim-sum is zero, the position is losing for the player whose turn it is, assuming optimal play.
- If the Nim-sum is non-zero, the position is winning for the player whose turn it is, assuming optimal play.

The AI selects a legal move that makes the Nim-sum zero whenever possible.

## 6. Project Structure

```text
nim-logic-tutor-ai/
│
├── nim_ai.py          # Nim game and AI logic
├── README.md          # Project documentation
└── requirements.txt   # Dependencies, if required
```

*Note: The filenames above are an example structure. If your Python files have different names, use your actual filenames in the commands below.*

## 7. Requirements

- Python 3.10 or later
- Visual Studio Code
- Git
- Python extension for VS Code

The project can run using Python's standard library if no external packages are used.

## 10. Expected Outcomes

- An AI agent capable of identifying optimal Nim moves.
- A clear demonstration of XOR-based winning strategies.
- A tutor that explains the reasoning behind decisions.
- A CSP generator that creates positions satisfying specified constraints.
- Practical understanding of game theory, backtracking, and constraint satisfaction.

## 11. Applications

- Artificial Intelligence education
- Game-playing agent development
- Constraint Satisfaction Problems
- Algorithm design and analysis
- Logical reasoning and mathematical problem-solving

## 12. Future Enhancements

- Add a graphical user interface.
- Display heap states visually.
- Show step-by-step explanations for every AI move.
- Add difficulty levels and player-versus-AI modes.
- Improve CSP pruning using partial XOR constraints.
- Store game statistics and compare different strategies.

## 13. Author

**Project:** Nim Logic Tutor AI  
**Domain:** Artificial Intelligence  
**Core Concepts:** Game Theory, XOR Strategy, Backtracking, and CSP

## 14. Conclusion

Nim Logic Tutor AI combines an optimal game-playing strategy with a logic-based tutoring system and a CSP position generator. The project demonstrates how mathematical reasoning and constraint-based search can be applied to develop intelligent systems that make decisions and explain their logic.
