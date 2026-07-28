import streamlit as st
import ezdxf
from datetime import date

# --- PAGE SETUP ---
st.set_page_config(page_title="Pool Scape AI Drafting V2.1", layout="wide")
st.title("🏗️ Pool Scape: Side-by-Side Layout (V2.1)")

# --- SIDEBAR: TECHNICAL SPECS ---
st.sidebar.header("Drawing Parameters")
category = st.sidebar.selectbox("Category", ["Aluminium Pergola", "Shower Screen"])
L = st.sidebar.number_input("Length (m)", value=4.0) * 1000 
W = st.sidebar.number_input("Width (m)", value=2.67) * 1000
H = st.sidebar.number_input("Height (m)", value=2.80) * 1000
col_size = 200 # Standard 200mm

def create_drawing():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # --- HORIZONTAL OFFSETS (Side by Side) ---
    # We move each drawing 6 meters (6000mm) to the right
    PLAN_X = 0
    ELEV_X = L + 2000  # 2 meters gap
    SEC_X = (L + 2000) * 2

    # --- 1. PLAN VIEW (Left) ---
    # Draw 4 Columns
    for x in [0, L-col_size]:
        for y in [0, W-col_size]:
            msp.add_lwpolyline([(PLAN_X+x, y), (PLAN_X+x+col_size, y), 
                                (PLAN_X+x+col_size, y+col_size), (PLAN_X+x, y+col_size)], close=True)
    msp.add_text("PLAN VIEW").set_placement((PLAN_X, -500))

    # --- 2. FRONT ELEVATION (Middle) ---
    # Columns
    msp.add_lwpolyline([(ELEV_X, 0), (ELEV_X+col_size, 0), (ELEV_X+col_size, H), (ELEV_X, H)], close=True)
    msp.add_lwpolyline([(ELEV_X+L-col_size, 0), (ELEV_X+L, 0), (ELEV_X+L, H), (ELEV_X+L-col_size, H)], close=True)
    # Beam
    msp.add_lwpolyline([(ELEV_X, H-150), (ELEV_X+L, H-150), (ELEV_X+L, H), (ELEV_X, H)], close=True)
    msp.add_text("FRONT ELEVATION").set_placement((ELEV_X, -500))

    # --- 3. SECTION VIEW (Right) ---
    # Foundation
    msp.add_lwpolyline([(SEC_X-200, -600), (SEC_X+400, -600), (SEC_X+400, 0), (SEC_X-200, 0)], close=True)
    # Column
    msp.add_lwpolyline([(SEC_X, 0), (SEC_X+col_size, 0), (SEC_X+col_size, H), (SEC_X, H)], close=True)
    msp.add_text("SECTION VIEW").set_placement((SEC_X, -1000))
    msp.add_text("Y12 @ 20 CM C/C").set_placement((SEC_X+500, -400))

    # --- SHEET BORDER ---
    # Draws a box around everything so you know where the drawing ends
    msp.add_lwpolyline([(-1000, -2000), (SEC_X+L+1000, -2000), (SEC_X+L+1000, H+2000), (-1000, H+2000)], close=True)

    filepath = "PoolScape_SideBySide.dxf"
    doc.saveas(filepath)
    return filepath

if st.button("🚀 Generate Side-by-Side Drawing"):
    file = create_drawing()
    st.success("Generated! Scroll out (Zoom Out) in your viewer to see all 3 views.")
    with open(file, "rb") as f:
        st.download_button("📥 Download CAD (.DXF)", f, file_name=file)
