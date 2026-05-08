import tkinter as tk
from tkinter import messagebox
from collections import deque
import math

# =========================================================
# MISSIONARIES & CANNIBALS AI
# Ultra Modern GUI + Smooth Animation + BFS
# =========================================================

TOTAL_M = 3
TOTAL_C = 3

MOVES = [
    (1, 0),
    (2, 0),
    (0, 1),
    (0, 2),
    (1, 1)
]

# =========================================================
# COLORS
# =========================================================

BG = "#0a0a12"
PANEL = "#151520"
RIVER = "#00aaff"
BANK = "#16351f"
NEON = "#00ffe1"
RED = "#ff3b5f"
SHADOW = "#050505"

# =========================================================
# BFS LOGIC
# =========================================================

def is_valid(state):

    m_left, c_left, boat = state

    m_right = TOTAL_M - m_left
    c_right = TOTAL_C - c_left

    if m_left < 0 or c_left < 0:
        return False

    if m_left > TOTAL_M or c_left > TOTAL_C:
        return False

    if m_left > 0 and c_left > m_left:
        return False

    if m_right > 0 and c_right > m_right:
        return False

    return True


def get_successors(state):

    successors = []

    m_left, c_left, boat = state

    for m, c in MOVES:

        if boat == 0:
            new_state = (
                m_left - m,
                c_left - c,
                1
            )

        else:
            new_state = (
                m_left + m,
                c_left + c,
                0
            )

        if is_valid(new_state):
            successors.append(new_state)

    return successors


def bfs():

    start = (3, 3, 0)
    goal = (0, 0, 1)

    queue = deque()
    queue.append((start, [start]))

    visited = set()

    while queue:

        current, path = queue.popleft()

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in get_successors(current):

            if neighbor not in visited:
                queue.append(
                    (neighbor, path + [neighbor])
                )

    return None


# =========================================================
# GUI
# =========================================================

class AI3DGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("3D Missionaries & Cannibals AI")
        self.root.geometry("1400x680")
        self.root.configure(bg=BG)

        self.solution = bfs()
        self.step = 0
        self.auto = False
        self.wave_offset = 0

        # =================================================
        # TITLE
        # =================================================

        title = tk.Label(
            root,
            text="MISSIONARIES & CANNIBALS AI",
            font=("Orbitron", 34, "bold"),
            fg=NEON,
            bg=BG
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            root,
            text="3D BFS VISUALIZATION",
            font=("Arial", 14),
            fg="white",
            bg=BG
        )
        subtitle.pack()

        # =================================================
        # MAIN CANVAS
        # =================================================

        self.canvas = tk.Canvas(
            root,
            width=1280,
            height=420,
            bg=PANEL,
            highlightthickness=0
        )
        self.canvas.pack(pady=25)

        # =================================================
        # STATUS PANEL
        # =================================================

        self.info = tk.Label(
            root,
            text="",
            font=("Arial", 16, "bold"),
            fg="white",
            bg=BG
        )
        self.info.pack()

        self.move_text = tk.Label(
            root,
            text="",
            font=("Arial", 13),
            fg=NEON,
            bg=BG
        )
        self.move_text.pack(pady=10)

        # =================================================
        # CONTROLS
        # =================================================

        controls = tk.Frame(root, bg=BG)
        controls.pack(pady=20)

        self.make_button(
            controls,
            "◀ Previous",
            "#252525",
            self.prev_step
        ).grid(row=0, column=0, padx=12)

        self.make_button(
            controls,
            "Next ▶",
            "#00aa88",
            self.next_step
        ).grid(row=0, column=1, padx=12)

        self.make_button(
            controls,
            "Auto Simulation",
            "#0066ff",
            self.start_auto
        ).grid(row=0, column=2, padx=12)

        self.make_button(
            controls,
            "Reset",
            "#aa2222",
            self.reset
        ).grid(row=0, column=3, padx=12)

        self.animate_scene()
        self.show_state()

    # =====================================================
    # BUTTON STYLE
    # =====================================================

    def make_button(self, parent, text, color, command):

        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=NEON,
            activeforeground="black",
            font=("Arial", 13, "bold"),
            width=16,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=12
        )

    # =====================================================
    # 3D CHARACTER
    # =====================================================

    def draw_3d_character(self, x, y, color, label):

        # SHADOW
        self.canvas.create_oval(
            x + 10,
            y + 55,
            x + 60,
            y + 75,
            fill="#000000",
            outline=""
        )

        # BODY SHADOW
        self.canvas.create_oval(
            x + 5,
            y + 5,
            x + 55,
            y + 55,
            fill="#111111",
            outline=""
        )

        # BODY
        self.canvas.create_oval(
            x,
            y,
            x + 50,
            y + 50,
            fill=color,
            outline=""
        )

        # HIGHLIGHT
        self.canvas.create_oval(
            x + 8,
            y + 8,
            x + 20,
            y + 20,
            fill="white",
            outline=""
        )

        # LABEL
        self.canvas.create_text(
            x + 25,
            y + 25,
            text=label,
            font=("Arial", 14, "bold"),
            fill="black"
        )

    # =====================================================
    # 3D BOAT
    # =====================================================

    def draw_boat(self, x, y):

        # SHADOW
        self.canvas.create_polygon(
            x + 10, y + 50,
            x + 140, y + 50,
            x + 120, y + 80,
            x + 20, y + 80,
            fill="#000000",
            outline=""
        )

        # BOAT BODY
        self.canvas.create_polygon(
            x, y,
            x + 130, y,
            x + 110, y + 30,
            x + 20, y + 30,
            fill="#8B4513",
            outline=NEON,
            width=3
        )

        # BOAT TOP
        self.canvas.create_polygon(
            x + 10, y - 10,
            x + 120, y - 10,
            x + 130, y,
            x, y,
            fill="#A0522D",
            outline=""
        )

        # BOAT LABEL
        self.canvas.create_text(
            x + 65,
            y + 12,
            text="BOAT",
            fill="white",
            font=("Arial", 12, "bold")
        )

    # =====================================================
    # ANIMATION
    # =====================================================

    def animate_scene(self):

        self.wave_offset += 5

        self.show_state()

        self.root.after(90, self.animate_scene)

    # =====================================================
    # DRAW SCENE
    # =====================================================

    def show_state(self):

        self.canvas.delete("all")

        state = self.solution[self.step]

        m_left, c_left, boat = state

        m_right = TOTAL_M - m_left
        c_right = TOTAL_C - c_left

        # =================================================
        # BACKGROUND DEPTH EFFECT
        # =================================================

        self.canvas.create_rectangle(
            0, 0, 1280, 560,
            fill=PANEL,
            outline=""
        )

        # LEFT BANK
        self.canvas.create_polygon(
            0, 0,
            350, 40,
            350, 520,
            0, 560,
            fill=BANK,
            outline=""
        )

        # RIGHT BANK
        self.canvas.create_polygon(
            930, 40,
            1280, 0,
            1280, 560,
            930, 520,
            fill=BANK,
            outline=""
        )

        # RIVER
        self.canvas.create_polygon(
            350, 40,
            930, 40,
            930, 520,
            350, 520,
            fill=RIVER,
            outline=""
        )

        # =================================================
        # WATER ANIMATION
        # =================================================

        # WATER WAVES ONLY INSIDE RIVER

        for i in range(350, 930, 35):
            y = 220 + math.sin(
                (i + self.wave_offset) * 0.04
            ) * 12

            self.canvas.create_arc(
                i,
                y,
                i + 45,
                y + 18,
                start=0,
                extent=180,
                style="arc",
                outline="white",
                width=2
            )

        # =================================================
        # BANK LABELS
        # =================================================

        self.canvas.create_text(
            170,
            45,
            text="LEFT BANK",
            fill="white",
            font=("Arial", 22, "bold")
        )

        self.canvas.create_text(
            1110,
            45,
            text="RIGHT BANK",
            fill="white",
            font=("Arial", 22, "bold")
        )

        # =================================================
        # LEFT CHARACTERS
        # =================================================

        for i in range(m_left):

            self.draw_3d_character(
                90,
                120 + i * 120,
                "white",
                "M"
            )

        for i in range(c_left):

            self.draw_3d_character(
                230,
                120 + i * 120,
                RED,
                "C"
            )

        # =================================================
        # RIGHT CHARACTERS
        # =================================================

        for i in range(m_right):

            self.draw_3d_character(
                1030,
                120 + i * 120,
                "white",
                "M"
            )

        for i in range(c_right):

            self.draw_3d_character(
                1170,
                120 + i * 120,
                RED,
                "C"
            )

        # =================================================
        # 3D BOAT
        # =================================================

        boat_x = 280 if boat == 0 else 860

        self.draw_boat(
            boat_x,
            390
        )

        # =================================================
        # STATUS
        # =================================================

        self.info.config(
            text=(
                f"STEP {self.step + 1}/{len(self.solution)}"
                f"   •   "
                f"LEFT: {m_left}M {c_left}C"
                f"   •   "
                f"RIGHT: {m_right}M {c_right}C"
            )
        )

        # =================================================
        # MOVE TEXT
        # =================================================

        if self.step > 0:

            prev = self.solution[self.step - 1]

            pm, pc, _ = prev

            moved_m = abs(pm - m_left)
            moved_c = abs(pc - c_left)

            move = f"Boat moved "

            if moved_m:
                move += f"{moved_m} Missionary(s)"

            if moved_c:
                move += f" and {moved_c} Cannibal(s)"

            self.move_text.config(text=move)

        else:
            self.move_text.config(
                text="Initial State"
            )

    # =====================================================
    # CONTROLS
    # =====================================================

    def next_step(self):

        if self.step < len(self.solution) - 1:

            self.step += 1
            self.show_state()

        else:

            messagebox.showinfo(
                "SUCCESS",
                "Everyone crossed safely 😎"
            )

    def prev_step(self):

        if self.step > 0:

            self.step -= 1
            self.show_state()

    def reset(self):

        self.step = 0
        self.auto = False
        self.show_state()

    # =====================================================
    # AUTO PLAY
    # =====================================================

    def start_auto(self):

        self.auto = True
        self.auto_play()

    def auto_play(self):

        if self.auto:

            if self.step < len(self.solution) - 1:

                self.step += 1
                self.show_state()

                self.root.after(
                    1700,
                    self.auto_play
                )

            else:

                self.auto = False

                messagebox.showinfo(
                    "COMPLETED",
                    "Optimal BFS solution found 🔥"
                )


# =========================================================
# RUN APP
# =========================================================

root = tk.Tk()

app = AI3DGUI(root)

root.mainloop()