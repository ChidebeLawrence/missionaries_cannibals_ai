import streamlit as st
import math
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Arc

# =========================================================
# MISSIONARIES & CANNIBALS AI
# NORMAL STREAMLIT DISPLAY VERSION
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

    # SHADOW
    shadow = Circle(
        (x + 0.06, y - 0.06),
        0.30,
        color="black",
        alpha=0.5
    )
    ax.add_patch(shadow)

    # BODY
    body = Circle(
        (x, y),
        0.30,
        color=color
    )
    ax.add_patch(body)

    # HIGHLIGHT
    highlight = Circle(
        (x - 0.1, y + 0.1),
        0.08,
        color="white"
    )
    ax.add_patch(highlight)

    # LABEL
    ax.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        fontsize=14,
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
            (x + 1.4, y),
            (x + 1.15, y - 0.35),
            (x + 0.25, y - 0.35)
        ],
        closed=True,
        facecolor="#8B4513",
        edgecolor=NEON,
        linewidth=2.5
    )

    ax.add_patch(boat)

    ax.text(
        x + 0.7,
        y - 0.15,
        "BOAT",
        ha="center",
        va="center",
        color="white",
        fontsize=10,
        fontweight="bold"
    )


# =========================================================
# DRAW SCENE
# =========================================================

def draw_scene(state, wave_offset=0):

    m_left, c_left, boat = state

    m_right = TOTAL_M - m_left
    c_right = TOTAL_C - c_left

    fig, ax = plt.subplots(figsize=(16, 5.5))

    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)

    ax.axis("off")

    # =====================================================
    # LEFT BANK
    # =====================================================

    left_bank = Polygon(
        [(0, 0), (3, 0), (3, 6), (0, 6)],
        closed=True,
        facecolor=BANK
    )
    ax.add_patch(left_bank)

    # =====================================================
    # RIVER
    # =====================================================

    river = Polygon(
        [(3, 0), (11, 0), (11, 6), (3, 6)],
        closed=True,
        facecolor=RIVER
    )
    ax.add_patch(river)

    # =====================================================
    # RIGHT BANK
    # =====================================================

    right_bank = Polygon(
        [(11, 0), (14, 0), (14, 6), (11, 6)],
        closed=True,
        facecolor=BANK
    )
    ax.add_patch(right_bank)

    # =====================================================
    # WATER WAVES
    # =====================================================

    for i in range(45):

        x = 3 + i * 0.19

        y = 3 + math.sin(
            (i + wave_offset) * 0.5
        ) * 0.15

        wave = Arc(
            (x, y),
            0.3,
            0.12,
            theta1=0,
            theta2=180,
            color="white",
            linewidth=1.3
        )

        ax.add_patch(wave)

    # =====================================================
    # BANK LABELS
    # =====================================================

    ax.text(
        1.5,
        5.5,
        "LEFT BANK",
        color="white",
        fontsize=20,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        12.5,
        5.5,
        "RIGHT BANK",
        color="white",
        fontsize=20,
        fontweight="bold",
        ha="center"
    )

    # =====================================================
    # LEFT MISSIONARIES
    # =====================================================

    for i in range(m_left):

        draw_character(
            ax,
            1,
            4.5 - i,
            "white",
            "M"
        )

    # =====================================================
    # LEFT CANNIBALS
    # =====================================================

    for i in range(c_left):

        draw_character(
            ax,
            2,
            4.5 - i,
            RED,
            "C"
        )

    # =====================================================
    # RIGHT MISSIONARIES
    # =====================================================

    for i in range(m_right):

        draw_character(
            ax,
            12,
            4.5 - i,
            "white",
            "M"
        )

    # =====================================================
    # RIGHT CANNIBALS
    # =====================================================

    for i in range(c_right):

        draw_character(
            ax,
            13,
            4.5 - i,
            RED,
            "C"
        )

    # =====================================================
    # BOAT
    # =====================================================

    boat_x = 3.6 if boat == 0 else 9

    draw_boat(
        ax,
        boat_x,
        1.3
    )

    # =====================================================
    # REMOVE EXTRA PADDING
    # =====================================================

    fig.subplots_adjust(
        left=0,
        right=1,
        top=1,
        bottom=0
    )

    return fig


# =========================================================
# STREAMLIT CONFIG
# =========================================================

st.set_page_config(
    page_title="Missionaries & Cannibals AI",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    f"""
    <style>

    html,
    body,
    [data-testid="stAppViewContainer"],
    .stApp {{
        background: {BG};
    }}

    .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1400px;
    }}

    /* TITLE */

    .title {{
        text-align: center;
        color: {NEON};
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 0;
    }}

    .subtitle {{
        text-align: center;
        color: white;
        margin-top: 0;
        margin-bottom: 20px;
    }}

    /* STATUS */

    .status {{
        text-align: center;
        color: white;
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
    }}

    .move {{
        text-align: center;
        color: {NEON};
        font-size: 20px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 20px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SESSION STATE
# =========================================================

solution = bfs()

if "step" not in st.session_state:
    st.session_state.step = 0

if "wave" not in st.session_state:
    st.session_state.wave = 0

# =========================================================
# TITLE
# =========================================================

st.markdown(
    f"""
    <div class="title">
        MISSIONARIES & CANNIBALS AI
    </div>

    <div class="subtitle">
        3D BFS VISUALIZATION
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CURRENT STATE
# =========================================================

state = solution[st.session_state.step]

m_left, c_left, boat = state

m_right = TOTAL_M - m_left
c_right = TOTAL_C - c_left

# =========================================================
# VISUALIZATION
# =========================================================

fig = draw_scene(
    state,
    st.session_state.wave
)

st.pyplot(
    fig,
    use_container_width=True
)

# =========================================================
# STATUS
# =========================================================

st.markdown(
    f"""
    <div class="status">

    STEP {st.session_state.step + 1}/{len(solution)}

    <br>

    LEFT: {m_left}M {c_left}C

    &nbsp;&nbsp;&nbsp; • &nbsp;&nbsp;&nbsp;

    RIGHT: {m_right}M {c_right}C

    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# MOVE TEXT
# =========================================================

if st.session_state.step > 0:

    prev = solution[
        st.session_state.step - 1
    ]

    pm, pc, _ = prev

    moved_m = abs(pm - m_left)
    moved_c = abs(pc - c_left)

    move = "Boat moved "

    if moved_m:
        move += (
            f"{moved_m} Missionary(s)"
        )

    if moved_c:
        move += (
            f" and {moved_c} Cannibal(s)"
        )

else:

    move = "Initial State"

st.markdown(
    f"""
    <div class="move">
        {move}
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CONTROLS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

# =========================================================
# PREVIOUS
# =========================================================

with col1:

    if st.button(
        "◀ Previous",
        use_container_width=True
    ):

        if st.session_state.step > 0:

            st.session_state.step -= 1
            st.session_state.wave += 1

            st.rerun()

# =========================================================
# NEXT
# =========================================================

with col2:

    if st.button(
        "Next ▶",
        use_container_width=True
    ):

        if (
            st.session_state.step
            < len(solution) - 1
        ):

            st.session_state.step += 1
            st.session_state.wave += 1

            st.rerun()

        else:

            st.success(
                "Everyone crossed safely 😎"
            )

# =========================================================
# AUTO SIMULATION
# =========================================================

with col3:

    if st.button(
        "Auto Simulation",
        use_container_width=True
    ):

        for _ in range(
            st.session_state.step,
            len(solution) - 1
        ):

            st.session_state.step += 1
            st.session_state.wave += 1

            time.sleep(1)

            st.rerun()

        st.success(
            "Optimal BFS solution found 🔥"
        )

# =========================================================
# RESET
# =========================================================

with col4:

    if st.button(
        "Reset",
        use_container_width=True
    ):

        st.session_state.step = 0
        st.session_state.wave = 0

        st.rerun()