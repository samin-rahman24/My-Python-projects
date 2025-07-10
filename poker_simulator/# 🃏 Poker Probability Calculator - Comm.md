🃏 Poker Probability Calculator — Command Line Tool

👋 About This Project
This is a command‑line poker odds calculator I made.
It works out your chances of winning in a Texas Hold’em game — even against multiple opponents — by combining two different methods: exact combinatorial math (when possible) and Monte Carlo simulation (when the calculations get too big).

I made it to practice my Python, work with algorithms, and think about probabilities the same way traders do when evaluating risk/reward in real time.

🚀 How to Run It
📋 Requirements:
Python 3.x

🔷 Open the Project Folder:
bash
Copy
Edit
cd "/Users/srabon/Desktop/Work PC/Coding project/poker_simulator"
🔷 Run from Terminal:
You can run it in 3 different ways depending on what you want to do.

A) Run the Interactive Calculator (default)
Lets you enter your cards, community cards, and number of players, then it calculates everything for you.

bash
Copy
Edit
python3 poker.py
B) Run the Test Suite
Runs a full set of tests to make sure the hand evaluator logic works for all poker hands.

bash
Copy
Edit
python3 poker.py --test
C) Run the Demo
Shows a quick demo of the difference between exact and Monte Carlo methods on a sample hand.

bash
Copy
Edit
python3 poker.py --demo
💡 Why I Made This
✅ I wanted to apply probability and combinatorics in a real, practical problem.
✅ I wanted to practice Python and write clean, modular code.
✅ And I wanted it to feel a little like how traders think — evaluating probabilities and making quick, informed decisions under uncertainty.

It also doubles as a nice little project to show I can write testable, maintainable, and efficient code.

🔷 What It Does
Figures out your odds of winning in a Texas Hold’em game.

Works with 1 to 9 opponents.

Calculates using exact math if possible, or falls back to Monte Carlo simulation if it gets too big.

Gives your best hand, its strength, and advice based on the situation.

⚙️ Features
Hybrid Calculation Engine: Automatically picks between exact combinatorics and simulation for the best balance of speed and accuracy.

Detailed Analysis: Shows your best possible hand, strength, and adjusted odds based on how many players are at the table.

CLI Interface: Clean, professional command‑line tool you can run in different modes.

Well‑Structured Code: Modular, easy to extend, and comes with a full set of tests.

🎯 Example Scenarios You Can Try
Run the calculator and test these situations:

Confident: Your cards: AS AC, Community: KH QD JS, Players: 2

Medium Risk: Your cards: KS QH, Community: JD TS 9C, Players: 3

High Risk: Your cards: 7H 7S, Community: AS KS QS, Players: 5

👨‍💻 Made By Me
I wrote all of it myself — the logic, the CLI interface, the test suite — as a way to improve my Python and to show I can think quantitatively and write solid code.

If you want to see the repo, just let me know!