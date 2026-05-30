from flask import Flask, render_template, request, jsonify

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from qiskit import QuantumCircuit

import json
import os
import re

# =========================================
# OPTIONAL QISKIT METAL
# =========================================

try:
    from qiskit_metal import designs
    METAL_AVAILABLE = True
except:
    METAL_AVAILABLE = False

# =========================================

app = Flask(__name__)

HISTORY_FILE = "chat_history.json"

# =========================================
# LOAD HISTORY
# =========================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

# =========================================
# SAVE HISTORY
# =========================================

def save_history(history):

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# =========================================
# LOAD RAG DATA
# =========================================

with open("rag_data.txt", "r", encoding="utf-8") as f:
    rag_texts = f.readlines()

# =========================================
# SIMPLE RAG
# =========================================

def retrieve_context(query):

    query_words = query.lower().split()

    matched = []

    for text in rag_texts:

        score = 0

        for word in query_words:

            if word in text.lower():
                score += 1

        if score > 0:
            matched.append((score, text))

    matched.sort(reverse=True)

    context = ""

    for item in matched[:3]:
        context += item[1]

    return context

# =========================================
# QUANTUM CHIP GENERATOR
# =========================================
def generate_chip(qubits):

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np

    fig, ax = plt.subplots(figsize=(14,8))

    bg = "#060816"

    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    ax.axis("off")

    white = "#F3F8FF"
    cyan = "#8EF7E7"
    yellow = "#FFD84D"
    pink = "#FF5DBB"

    # =====================================================
    # MAIN PANEL
    # =====================================================

    panel = patches.FancyBboxPatch(

        (-7,-5),

        15,
        10,

        boxstyle="round,pad=0.4",

        facecolor="#090B18",

        edgecolor="#1c233a",

        linewidth=2
    )

    ax.add_patch(panel)

    # =====================================================
    # TITLE
    # =====================================================

    ax.text(

        0,
        4.5,

        f"{qubits}-Qubit Quantum Processor",

        fontsize=26,

        color="white",

        ha="center",

        fontweight="bold"
    )

    # =====================================================
    # SUBSTRATE BORDER
    # =====================================================

    outer = patches.Rectangle(

        (-5.2,-3.9),

        9,
        7.8,

        linewidth=1.5,

        linestyle="--",

        edgecolor=cyan,

        facecolor="none",

        alpha=0.45
    )

    ax.add_patch(outer)

    # =====================================================
    # MAIN CHIP BORDER
    # =====================================================

    border = patches.Rectangle(

        (-4.4,-3.2),

        7.4,
        6.4,

        linewidth=3.5,

        edgecolor=white,

        facecolor="none"
    )

    ax.add_patch(border)

    # =====================================================
    # GLOW LINE
    # =====================================================

    def glow_line(x1,y1,x2,y2,color,width):

        for a,w in [

            (0.03,width+10),
            (0.05,width+6),
            (0.08,width+3)

        ]:

            ax.plot(

                [x1,x2],
                [y1,y2],

                color=color,

                linewidth=w,

                alpha=a,

                solid_capstyle="round"
            )

        ax.plot(

            [x1,x2],
            [y1,y2],

            color=color,

            linewidth=width,

            solid_capstyle="round"
        )

    # =====================================================
    # FEEDLINES
    # =====================================================

    glow_line(-4.4,0,-5.3,0,white,3)
    glow_line(3,-0,3.9,0,white,3)

    glow_line(0,3.2,0,4.1,white,3)
    glow_line(0,-3.2,0,-4.1,white,3)

    # =====================================================
    # BOND PADS
    # =====================================================

    pads = [

        (-5.45,-0.16),
        (3.75,-0.16),

        (-0.16,4.0),
        (-0.16,-4.3)

    ]

    for x,y in pads:

        pad = patches.Rectangle(

            (x,y),

            0.32,
            0.32,

            facecolor=white,

            edgecolor=white
        )

        ax.add_patch(pad)

    # =====================================================
    # RESONATOR
    # =====================================================

    def resonator(x,y):

        for i in range(5):

            xx = x + i*0.18

            glow_line(
                xx,
                y,
                xx,
                y+0.55,
                cyan,
                2.4
            )

    # =====================================================
    # QUBIT
    # =====================================================

    def qubit(x,y,label):

        glow = patches.Rectangle(

            (x-0.34,y-0.34),

            0.68,
            0.68,

            linewidth=8,

            edgecolor=pink,

            facecolor="none",

            alpha=0.05
        )

        ax.add_patch(glow)

        box = patches.Rectangle(

            (x-0.34,y-0.34),

            0.68,
            0.68,

            linewidth=2,

            edgecolor=pink,

            facecolor="#101425"
        )

        ax.add_patch(box)

        ax.text(

            x,
            y,

            label,

            color=pink,

            fontsize=14,

            ha="center",

            va="center",

            fontweight="bold"
        )

    # =====================================================
    # POSITIONS
    # =====================================================

    q1 = (-1.45,1.0)
    q2 = (1.45,1.0)

    q3 = (-1.45,-1.0)
    q4 = (1.45,-1.0)

    # =====================================================
    # QUBITS
    # =====================================================

    qubit(*q1,"Q1")
    qubit(*q2,"Q2")

    qubit(*q3,"Q3")
    qubit(*q4,"Q4")

    # =====================================================
    # RESONATORS
    # =====================================================

    resonator(-1.95,1.85)
    resonator(0.95,1.85)

    resonator(-1.95,-1.95)
    resonator(0.95,-1.95)

    # =====================================================
    # COUPLING BUS
    # =====================================================

    # =====================================================
    # COUPLING BUS
    # =====================================================
    glow_line(-1.1, 1.0, 1.1, 1.0, yellow, 2.2)
    glow_line(-1.1, -1.0, 1.1, -1.0, yellow, 2.2)
    glow_line(-1.45, 0.7, -1.45, -0.7, yellow, 2.2)
    glow_line(1.45, 0.7, 1.45, -0.7, yellow, 2.2)
    
    # =====================================================
    # LEGEND PANEL
    # =====================================================

    legend = patches.FancyBboxPatch(

        (4.2,-0.2),

        2.7,
        3.2,

        boxstyle="round,pad=0.2",

        facecolor="#101321",

        edgecolor="#31384f",

        linewidth=1.2
    )

    ax.add_patch(legend)

    items = [

        ("Silicon Substrate", cyan),
        ("CPW Feedline", white),

        ("Readout Resonator", cyan),
        ("Transmon Qubit", pink),

        ("Coupling Bus", yellow),
        ("Bond Pad / Port", white)
    ]

    yy = 2.4

    for txt,col in items:

        ax.add_patch(

            patches.Rectangle(

                (4.45,yy),

                0.22,
                0.22,

                edgecolor=col,

                facecolor="none",

                linewidth=1.8
            )
        )

        ax.text(

            5.0,
            yy+0.11,

            txt,

            fontsize=10,

            color="white",

            va="center"
        )

        yy -= 0.48

    # =====================================================
    # INFO PANEL
    # =====================================================

    info = patches.FancyBboxPatch(

        (4.2,-3.1),

        2.7,
        1.6,

        boxstyle="round,pad=0.2",

        facecolor="#101321",

        edgecolor="#31384f",

        linewidth=1.2
    )

    ax.add_patch(info)

    ax.text(

        4.45,
        -1.8,

        "• Grid topology\n"
        "• Uniform coupling\n"
        "• Scalable architecture\n"
        "• Easy calibration",

        fontsize=10,

        color="white",

        va="top"
    )

    # =====================================================
    # FOOTER
    # =====================================================

    footer = patches.FancyBboxPatch(

        (-6.5,-4.7),

        13,
        0.45,

        boxstyle="round,pad=0.08",

        facecolor="#0a0d18",

        edgecolor="#1e293b",

        linewidth=1
    )

    ax.add_patch(footer)

    ax.text(

        -6.0,
        -4.5,

        "Silicon Substrate (10x10mm)",

        fontsize=9,

        color=cyan
    )

    ax.text(

        -0.9,
        -4.5,

        "CPW Coupling Bus (5.0mm)",

        fontsize=9,

        color=yellow
    )

    ax.text(

        3.2,
        -4.5,

        "Readout Resonator (7.0mm)",

        fontsize=9,

        color=white
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(-7,8)
    ax.set_ylim(-5,5)

    # =====================================================
    # SAVE
    # =====================================================

    plt.savefig(

        "static/chip.png",

        dpi=500,

        bbox_inches="tight",

        facecolor=fig.get_facecolor()
    )

    plt.close()
# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    history = load_history()

    return render_template(
        "index.html",
        history=history
    )

# =========================================
# CHAT API
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    user_input = request.json["message"]

    text = user_input.lower()

    context = retrieve_context(user_input)

    # =====================================
    # GREETINGS
    # =====================================

    greetings = [
        "hi",
        "hello",
        "hey",
        "hola"
    ]

    if text.strip() in greetings:

        bot_response = (
            "Hello 👋\n\n"
            "I am QuantumRAG AI.\n\n"
            "I can generate superconducting "
            "quantum processor layouts using:\n\n"
            "• Qiskit\n"
            "• Qiskit Metal\n"
            "• Retrieval-Augmented Generation\n\n"
            "Try prompts like:\n"
            "• Create 4 qubit chip\n"
            "• Generate 8 qubit processor\n"
            "• Design superconducting QPU"
        )

        return jsonify({
            "reply": bot_response,
            "image": ""
        })

    # =====================================
    # HELP
    # =====================================

    if "help" in text:

        bot_response = (
            "QuantumRAG AI Help\n\n"
            "Supported prompts:\n\n"
            "• Create 4 qubit chip\n"
            "• Generate 6 qubit processor\n"
            "• Design superconducting QPU\n"
            "• Build transmon architecture"
        )

        return jsonify({
            "reply": bot_response,
            "image": ""
        })

    # =====================================
    # CHIP GENERATION
    # =====================================

    match = re.search(r'(\d+)\s*qubit', text)

    if match:

        qubits = int(match.group(1))

        qc = QuantumCircuit(qubits)

        for i in range(qubits):
            qc.h(i)

        if qubits > 1:

            for i in range(qubits - 1):
                qc.cx(i, i + 1)

        # OPTIONAL QISKIT METAL

        if METAL_AVAILABLE:
            design = designs.DesignPlanar()

        # =====================================
        # GENERATE IMAGE
        # =====================================

        generate_chip(qubits)

        # =====================================
        # BOT RESPONSE
        # =====================================

        bot_response = f"""
✅ Quantum Blueprint Successfully Generated

🧠 Processor:
{qubits}-Qubit Superconducting Transmon Processor

⚙️ Architecture:
• Symmetric CPW coupling topology
• Resonator-coupled transmon qubits
• Cryogenic superconducting layout
• Quantum bus interconnect structure

🎨 Layout Guide:
• Pink/Blue/Green/Yellow = Qubit zones
• Colored fingers = Resonators
• Yellow lines = Coupling buses
• Outer frame = Silicon substrate

📡 Hardware Characteristics:
• Microwave signal routing
• Josephson-junction based qubits
• Fabrication-ready planar design
• Low-temperature quantum operation

📚 RAG Knowledge:
{context}
"""

        history = load_history()

        history.append({
            "user": user_input,
            "bot": bot_response
        })

        save_history(history)

        return jsonify({

            "reply": bot_response,

            "image": "/static/chip.png"

        })

    # =====================================
    # DEFAULT RESPONSE
    # =====================================

    bot_response = (
        "I can help you generate superconducting "
        "quantum processor layouts.\n\n"

        "Try prompts like:\n"
        "• Create 4 qubit chip\n"
        "• Generate 8 qubit processor\n"
        "• Design quantum architecture"
    )

    return jsonify({
        "reply": bot_response,
        "image": ""
    })

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=False)