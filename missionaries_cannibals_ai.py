import streamlit as st
import math
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Arc

# =========================================================
# MISSIONARIES & CANNIBALS AI
# Streamlit Version + BFS Visualization
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
# DRAW CHARACTER
# =========================================================

def draw_character(ax, x, y, color, label):

    # Shadow
    shadow = Circle((x + 0.05, y - 0.05), 0.28, color="black", alpha=0.4)
    ax.add_patch(shadow)

    # Body
    body = Circle((x, y), 0.28, color=color)
    ax.add_patch(body)

    # Highlight
    highlight = Circle((x - 0.1, y + 0.1), 0.07, color="white")
    ax.add_patch(highlight)

    # Label
    ax.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="black"
    )


# =========================================================
# DRAW BOAT
# =========================================================

def draw_boat(ax, x, y):

    boat = Polygon(
        [
            (x, y),
            (x + 1.3, y),
            (x + 1.1, y - 0.3),
            (x + 0.2, y - 0.3)
        ],
        closed=True,
        facecolor="#8B4513",
        edgecolor=NEON,
        linewidth=2
    )

    ax.add_patch(boat)

    ax.text(
        x + 0.65,
        y - 0.12,
        "BOAT",
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold"
    )


# =========================================================
# DRAW SCENE
# =========================================================

def draw_scene(state, wave_offset=0):

    m_left, c_left, boat = state

    m_right = TOTAL_M - m_left
    c_right = TOTAL_C - c_left

    fig, ax = plt.subplots(figsize=(14, 5))

    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)

    ax.axis("off")

    # Left Bank
    left_bank = Polygon(
        [(0, 0), (3, 0), (3, 6), (0, 6)],
        closed=True,
        facecolor=BANK
    )
    ax.add_patch(left_bank)

    # River
    river = Polygon(
        [(3, 0), (11, 0), (11, 6), (3, 6)],
        closed=True,
        facecolor=RIVER
    )
    ax.add_patch(river)

    # Right Bank
    right_bank = Polygon(
        [(11, 0), (14, 0), (14, 6), (11, 6)],
        closed=True,
        facecolor=BANK
    )
    ax.add_patch(right_bank)

    # Water Waves
    for i in range(30):

        x = 3 + i * 0.27

        y = 3 + math.sin((i + wave_offset) * 0.4) * 0.15

        wave = Arc(
            (x, y),
            0.3,
            0.12,
            theta1=0,
            theta2=180,
            color="white",
            linewidth=1
        )

        ax.add_patch(wave)

    # Bank Labels
    ax.text(
        1.5,
        5.5,
        "LEFT BANK",
        color="white",
        fontsize=16,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        12.5,
        5.5,
        "RIGHT BANK",
        color="white",
        fontsize=16,
        fontweight="bold",
        ha="center"
    )

    # Left Missionaries
    for i in range(m_left):

        draw_character(
            ax,
            1,
            4.5 - i,
            "white",
            "M"
        )

    # Left Cannibals
    for i in range(c_left):

        draw_character(
            ax,
            2,
            4.5 - i,
            RED,
            "C"
        )

    # Right Missionaries
    for i in range(m_right):

        draw_character(
            ax,
            12,
            4.5 - i,
            "white",
            "M"
        )

    # Right Cannibals
    for i in range(c_right):

        draw_character(
            ax,
            13,
            4.5 - i,
            RED,
            "C"
        )

    # Boat
    boat_x = 3.5 if boat == 0 else 9

    draw_boat(ax, boat_x, 1.2)

    return fig


# =========================================================
# STREAMLIT APP
# =========================================================

st.set_page_config(
    page_title="Missionaries & Cannibals AI",
    layout="wide"
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {BG};
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <h1 style='text-align:center; color:{NEON};'>
    MISSIONARIES & CANNIBALS AI
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center;'>3D BFS VISUALIZATION</h4>",
    unsafe_allow_html=True
)

solution = bfs()

if "step" not in st.session_state:
    st.session_state.step = 0

if "wave" not in st.session_state:
    st.session_state.wave = 0

state = solution[st.session_state.step]

# Draw Scene
fig = draw_scene(state, st.session_state.wave)

st.pyplot(fig)

# =========================================================
# STATUS
# =========================================================

m_left, c_left, boat = state

m_right = TOTAL_M - m_left
c_right = TOTAL_C - c_left

st.markdown(
    f"""
    <div style='text-align:center; font-size:22px;'>
    STEP {st.session_state.step + 1}/{len(solution)}
    <br><br>
    LEFT: {m_left}M {c_left}C
    &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;
    RIGHT: {m_right}M {c_right}C
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# MOVE DESCRIPTION
# =========================================================

if st.session_state.step > 0:

    prev = solution[st.session_state.step - 1]

    pm, pc, _ = prev

    moved_m = abs(pm - m_left)
    moved_c = abs(pc - c_left)

    move = "Boat moved "

    if moved_m:
        move += f"{moved_m} Missionary(s)"

    if moved_c:
        move += f" and {moved_c} Cannibal(s)"

else:
    move = "Initial State"

st.markdown(
    f"""
    <h4 style='text-align:center; color:{NEON};'>
    {move}
    </h4>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CONTROLS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    if st.button("◀ Previous"):

        if st.session_state.step > 0:
            st.session_state.step -= 1
            st.session_state.wave += 1
            st.rerun()

with col2:

    if st.button("Next ▶"):

        if st.session_state.step < len(solution) - 1:
            st.session_state.step += 1
            st.session_state.wave += 1
            st.rerun()
        else:
            st.success("Everyone crossed safely 😎")

with col3:

    if st.button("Auto Simulation"):

        for i in range(
            st.session_state.step,
            len(solution) - 1
        ):

            st.session_state.step += 1
            st.session_state.wave += 1

            time.sleep(1)

            st.rerun()

        st.success("Optimal BFS solution found 🔥")

with col4:

    if st.button("Reset"):

        st.session_state.step = 0
        st.session_state.wave = 0

        st.rerun()