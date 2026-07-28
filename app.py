import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_exact_plan(w_mm):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 1. THE WALLS (Concrete texture blocks)
    # Left Wall
    ax.add_patch(patches.Rectangle((-150, -100), 150, 200, facecolor='#eeeeee', hatch='...'))
    # Right Wall (based on Width)
    ax.add_patch(patches.Rectangle((w_mm, -100), 150, 200, facecolor='#eeeeee', hatch='...'))

    # 2. THE RED PROFILES (Simplified technical shapes)
    # Wall Profile (Left)
    ax.add_patch(patches.Rectangle((0, -40), 40, 80, linewidth=1.5, edgecolor='red', facecolor='none'))
    # Middle Hinge Profile (Assume door starts at 60% of width)
    hinge_x = w_mm * 0.6
    ax.add_patch(patches.Rectangle((hinge_x, -40), 60, 80, linewidth=1.5, edgecolor='red', facecolor='none'))
    # End Profile (Right)
    ax.add_patch(patches.Rectangle((w_mm-40, -40), 40, 80, linewidth=1.5, edgecolor='red', facecolor='none'))

    # 3. THE GLASS PANELS
    # Fixed Panel (Left to Hinge)
    ax.plot([40, hinge_x], [0, 0], color='skyblue', linewidth=4, label='Fixed Glass')
    
    # Door Panel (Open at 45 degrees)
    door_length = w_mm - hinge_x - 40
    angle = np.deg2rad(45)
    dx = door_length * np.cos(angle)
    dy = door_length * np.sin(angle)
    ax.plot([hinge_x + 60, hinge_x + 60 + dx], [0, dy], color='skyblue', linewidth=4, alpha=0.6)
    # Dashed Door (Closed position)
    ax.plot([hinge_x + 60, w_mm - 40], [0, 0], color='gray', linestyle='--', linewidth=1)

    # 4. THE DOOR SWING ARC (The "Exact" detail)
    arc = patches.Arc((hinge_x + 60, 0), width=door_length*2, height=door_length*2, 
                      theta1=0, theta2=45, linestyle='--', color='gray')
    ax.add_patch(arc)

    # 5. LABELS
    ax.text(w_mm/2, -150, "PLAN", fontsize=14, fontweight='bold', ha='center')
    
    # Clean up
    ax.set_xlim(-200, w_mm + 200)
    ax.set_ylim(-300, 500)
    ax.set_aspect('equal')
    ax.axis('off')
    
    return fig

# --- STREAMLIT INTERFACE ---
st.title("Canvas ZenScreen: Plan View Generator")
width = st.slider("Total Width (mm)", 800, 2500, 1500)

if st.button("Generate Exact Plan View"):
    fig = draw_exact_plan(width)
    st.pyplot(fig)
