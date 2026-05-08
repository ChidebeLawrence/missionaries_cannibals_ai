# Missionaries and Cannibals AI

## Overview

This project is a graphical simulation of the classic **Missionaries and Cannibals Problem** using **Python** and the **Breadth First Search (BFS)** algorithm from Artificial Intelligence.

The application visualizes how missionaries and cannibals cross a river safely without violating the problem constraints.

The project includes:

* BFS Search Algorithm
* Modern GUI Interface
* 3D-style visual effects
* Animated river waves
* Boat movement simulation
* Step-by-step AI visualization

---

# Problem Description

Three missionaries and three cannibals are on the left side of a river.

They must cross to the right side using a boat with the following conditions:

1. The boat can carry a maximum of two people.
2. If cannibals outnumber missionaries on either side of the river, the missionaries get eaten.
3. The goal is to move everyone safely to the right side.

---

# Artificial Intelligence Concept

This project applies a **standard search algorithm** known as:

## Breadth First Search (BFS)

BFS explores all possible states level-by-level until it finds the safest and shortest solution path.

The algorithm:

* Represents each river configuration as a state
* Generates valid successor states
* Avoids invalid states
* Finds the optimal solution automatically

---

# Features

* Modern futuristic GUI
* 3D-style interface
* Animated river effects
* Interactive controls
* Automatic simulation mode
* Step-by-step navigation
* BFS solution visualization
* Error-safe state validation

---

# Technologies Used

* Python
* Tkinter (GUI)
* Collections Module (`deque`)
* Breadth First Search (BFS)

---

# How to Run the Project

## Step 1: Install Python

Download and install Python from:

[Python Official Website](https://www.python.org?utm_source=chatgpt.com)

---

## Step 2: Save the File

Save the program as:

```text
missionaries_cannibals_ai.py
```

---

## Step 3: Run the Program

Open terminal or command prompt and run:

```bash
python missionaries_cannibals_ai.py
```

---

# Controls

| Button          | Function                        |
| --------------- | ------------------------------- |
| Next            | Move to next state              |
| Previous        | Return to previous state        |
| Auto Simulation | Automatically play the solution |
| Reset           | Restart the simulation          |

---

# Project Structure

```text
missionaries_cannibals_ai.py
README.md
```

---

# Example State Representation

```python
(3, 3, 0)
```

Meaning:

* 3 Missionaries on left
* 3 Cannibals on left
* Boat on left side

---

# Goal State

```python
(0, 0, 1)
```

Meaning:

* Everyone crossed safely
* Boat is on the right side

---

# Learning Outcomes

This project demonstrates:

* Artificial Intelligence problem solving
* State space representation
* BFS search algorithm
* GUI development with Python
* Animation and simulation techniques

---

# Future Improvements

Possible upgrades include:

* Sound effects
* Real character sprites
* DFS and A* algorithms
* Multiplayer/manual gameplay
* Web version using Streamlit
* AI statistics dashboard

---

# Author

Developed using Python and Artificial Intelligence concepts.
