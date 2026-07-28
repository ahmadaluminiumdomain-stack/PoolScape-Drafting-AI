import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_exploded_assembly(w_mm, h_mm):
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # --- 1. DEFINING THE "DNA" OF THE PARTS ---
    # Wall Profile (Red)
    wall_prof = patches.Rectangle((0, 0), 40, h_mm, color='red', alpha=0.8, label='C-31')
    # Glass (Blue)
    glass = patches.Rectangle((100, 0), 12, h_mm, color='skyblue', alpha=0.6, label='Glass')
    # Door Frame (Green)
    door_frame = patches.Rectangle((200, 0), 50, h_mm, color='green', alpha=0.8, label='C-39')

    # --- 2. PLACING THE EXPLODED PARTS ---
    # We "offset" them (add space) so it looks like the assembly diagram
    ax.add_patch(wall_prof)
    ax.add_patch(glass)
    ax.add_patch(door_frame)

    # --- 3. ADDING THE "BUBBLE CALLOUTS" (The Circles A, B, C) ---
    def add_callout(x, y, label):
        # Circle
        circle = patches.Circle((x, y), 25, color='black', fill=False)
        ax.add_patch(circle)
        # Letter
        ax.text(x, y, label, ha='center', va='center', fontsize=10, fontweight='bold')

    # Placement of Callouts (matching your screenshot)
    add_callout(20, h_mm/2, "B") # Wall Profile
    add_callout(106, h_mm/2 + 200, "I") # Glass
    add_callout(225, h_mm/2 - 200, "D") # Door Frame

    # --- 4. THE DOOR SWING (Dashed Lines) ---
    ax.plot([250, 600], [h_mm, h_mm+300], color='gray', linestyle='--')
    ax.plot([250, 600], [0, -300], color='gray', linestyle='--')

    # Formatting
    ax.set_xlim(-100, 1000)
    ax.set_ylim(-500, h_m + 500)
    ax.axis('off')
    return fig

# --- INTERFACE ---
st.title("Canvas ZenScreen: Assembly Diagram Generator")
w = st.sidebar.number_input("Width", value=1500)
h = st.sidebar.number_input("Height", value=2100)

if st.button("Generate Assembly Illustration"):
    fig = draw_exploded_assembly(w, h)
    st.pyplot(fig)
