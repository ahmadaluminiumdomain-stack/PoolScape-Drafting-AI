import streamlit as st
import ezdxf
from datetime import date

# --- APP CONFIG ---
st.set_page_config(page_title="Pool Scape AI Drafter", layout="wide")
st.title("🏗️ Pool Scape: Automated Technical Drawing")

# --- SIDEBAR INPUTS ---
st.sidebar.header("1. Drawing Details")
project_type = st.sidebar.selectbox("Project Type", ["Aluminium Pergola", "Shower Screen"])
client_name = st.sidebar.text_input("Client Name", "Dmitry Ignatov")
finish = st.sidebar.selectbox("Finish", ["Midnight Black", "Majestic Gold", "Rosy Glimmer", "Bronze Reverie"])

st.sidebar.header("2. Measurements (Meters)")
if project_type == "Aluminium Pergola":
    L = st.sidebar.number_input("Total Length (m)", value=4.0)
    W = st.sidebar.number_input("Total Width/Span (m)", value=2.37)
    H = st.sidebar.number_input("Total Height (m)", value=2.80)
    col_size = st.sidebar.selectbox("Column Size (mm)", [150, 200]) / 1000
else:
    W = st.sidebar.number_input("Total Width (m)", value=1.20)
    H = st.sidebar.number_input("Total Height (m)", value=2.10)
    glass_thick = st.sidebar.selectbox("Glass Thickness (mm)", [10, 12])
    typology = st.sidebar.selectbox("Typology", ["FDF", "FD", "F", "D", "T-Type"])

# --- THE DRAFTING ENGINE ---
def generate_dxf(p_type):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    if p_type == "Aluminium Pergola":
        # DRAWING A BASIC SECTION
        # Ground Line
        msp.add_line((-1, 0), (W+1, 0))
        # Left Column
        msp.add_lwpolyline([(0, 0), (0, H), (col_size, H), (col_size, 0)], close=True)
        # Right Column
        msp.add_lwpolyline([(W-col_size, 0), (W-col_size, H), (W, H), (W, 0)], close=True)
        # Beam
        msp.add_lwpolyline([(0, H), (W, H), (W, H-0.15), (0, H-0.15)], close=True)
        # Foundation Section
        msp.add_text("FOUNDATION: 600x600x600").set_placement((0, -0.8))
        
    else: # Shower Screen Logic
        # Draw Elevation Rectangle
        msp.add_lwpolyline([(0, 0), (W, 0), (W, H), (0, H)], close=True)
        # Hinge Logic
        hinge_count = 3 if W > 1.2 else 2
        msp.add_text(f"HINGES: {hinge_count} NOS").set_placement((W/2, H/2))

    # ADD DUBAI MUNICIPALITY NOTES
    notes = [
        "GENERAL NOTES:",
        "1. DO NOT SCALE THE DIMENSIONS.",
        "2. DIMENSIONS ARE STRUCTURAL UNLESS NOTED.",
        "3. BRING DISCREPANCIES TO CONSULTANT NOTICE.",
        f"4. DATE: {date.today()}",
        f"5. CONTRACTOR: POOL SCAPE SWIMMING POOL INSTALLATION LLC"
    ]
    for i, note in enumerate(notes):
        msp.add_text(note).set_placement((W + 0.5, H - (i * 0.2)))

    filename = "pool_scape_drawing.dxf"
    doc.saveas(filename)
    return filename

# --- BUTTON & DOWNLOAD ---
if st.button("🚀 Generate Technical Set"):
    file_path = generate_dxf(project_type)
    st.success(f"Success! {project_type} Drawing is ready.")
    with open(file_path, "rb") as f:
        st.download_button("Download CAD File (.DXF)", f, file_name=file_path)
    st.info("Note: Open this file in AutoCAD or any online DXF viewer to see the Plan, Elevation, and Section.")
