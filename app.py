import streamlit as st
import ezdxf
from datetime import date

# --- PAGE SETUP ---
st.set_page_config(page_title="Pool Scape AI Drafting V2", layout="wide")
st.title("🏗️ Pool Scape: Professional Drafting Engine (V2)")
st.write("This engine generates Plan, Elevation, and Section views for DM Approval.")

# --- SIDEBAR: PROJECT INFO ---
st.sidebar.header("1. Project Information")
project_name = st.sidebar.text_input("Project Name", "G +1 VILLA")
client_name = st.sidebar.text_input("Client Name", "DMITRY IGNATOV")
location = st.sidebar.text_input("Location", "Springs 3, Street 8, Villa 18")
drawing_no = st.sidebar.text_input("Drawing No", "PS-001")

# --- SIDEBAR: TECHNICAL SPECS ---
st.sidebar.header("2. Technical Specifications")
category = st.sidebar.selectbox("Category", ["Aluminium Pergola", "Shower Screen"])

if category == "Aluminium Pergola":
    L = st.sidebar.number_input("Length (m)", value=4.0) * 1000  # Convert to mm
    W = st.sidebar.number_input("Width / Span (m)", value=2.67) * 1000
    H = st.sidebar.number_input("Height (m)", value=2.80) * 1000
    col_size = st.sidebar.selectbox("Column Size (mm)", [150, 200])
    finish = st.sidebar.selectbox("Finish", ["Midnight Black", "Majestic Gold", "Rosy Glimmer"])
else:
    W = st.sidebar.number_input("Total Width (mm)", value=1500)
    H = st.sidebar.number_input("Total Height (mm)", value=2100)
    typology = st.sidebar.selectbox("Typology", ["FDF", "FD", "F", "D"])
    glass_thick = st.sidebar.selectbox("Glass (mm)", [10, 12])
    finish = st.sidebar.selectbox("Finish", ["Midnight Black", "Majestic Gold"])

# --- DRAFTING ENGINE V2 ---
def create_drawing():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # --- CONSTANTS & OFFSETS (To keep views separated) ---
    PLAN_OFFSET = (0, 6000)
    ELEV_OFFSET = (0, 3000)
    SEC_OFFSET = (0, 0)

    if category == "Aluminium Pergola":
        # 1. PLAN VIEW (Top Down)
        # Draw 4 Columns
        for x in [0, L-col_size]:
            for y in [0, W-col_size]:
                msp.add_lwpolyline([(PLAN_OFFSET[0]+x, PLAN_OFFSET[1]+y), 
                                    (PLAN_OFFSET[0]+x+col_size, PLAN_OFFSET[1]+y), 
                                    (PLAN_OFFSET[0]+x+col_size, PLAN_OFFSET[1]+y+col_size), 
                                    (PLAN_OFFSET[0]+x, PLAN_OFFSET[1]+y+col_size)], close=True)
        msp.add_text("PLAN VIEW").set_placement((PLAN_OFFSET[0], PLAN_OFFSET[1]-300))

        # 2. FRONT ELEVATION
        # Left Col
        msp.add_lwpolyline([(ELEV_OFFSET[0], ELEV_OFFSET[1]), (ELEV_OFFSET[0]+col_size, ELEV_OFFSET[1]), 
                            (ELEV_OFFSET[0]+col_size, ELEV_OFFSET[1]+H), (ELEV_OFFSET[0], ELEV_OFFSET[1]+H)], close=True)
        # Right Col
        msp.add_lwpolyline([(ELEV_OFFSET[0]+L-col_size, ELEV_OFFSET[1]), (ELEV_OFFSET[0]+L, ELEV_OFFSET[1]), 
                            (ELEV_OFFSET[0]+L, ELEV_OFFSET[1]+H), (ELEV_OFFSET[0]+L-col_size, ELEV_OFFSET[1]+H)], close=True)
        # Top Beam (150mm thick)
        msp.add_lwpolyline([(ELEV_OFFSET[0], ELEV_OFFSET[1]+H-150), (ELEV_OFFSET[0]+L, ELEV_OFFSET[1]+H-150), 
                            (ELEV_OFFSET[0]+L, ELEV_OFFSET[1]+H), (ELEV_OFFSET[0], ELEV_OFFSET[1]+H)], close=True)
        msp.add_text("FRONT ELEVATION").set_placement((ELEV_OFFSET[0], ELEV_OFFSET[1]-300))

        # 3. SECTION VIEW (Technical Detail)
        # Draw Foundation (600x600x600)
        msp.add_lwpolyline([(SEC_OFFSET[0]-225, SEC_OFFSET[1]-600), (SEC_OFFSET[0]+375, SEC_OFFSET[1]-600), 
                            (SEC_OFFSET[0]+375, SEC_OFFSET[1]), (SEC_OFFSET[0]-225, SEC_OFFSET[1])], close=True)
        # Draw Column on top
        msp.add_lwpolyline([(SEC_OFFSET[0], SEC_OFFSET[1]), (SEC_OFFSET[0]+col_size, SEC_OFFSET[1]), 
                            (SEC_OFFSET[0]+col_size, SEC_OFFSET[1]+H), (SEC_OFFSET[0], SEC_OFFSET[1]+H)], close=True)
        # Rebar Symbols (Simple lines)
        msp.add_line((SEC_OFFSET[0]-150, SEC_OFFSET[1]-500), (SEC_OFFSET[0]+300, SEC_OFFSET[1]-500))
        msp.add_text("SECTION VIEW: FOUNDATION DETAIL").set_placement((SEC_OFFSET[0], SEC_OFFSET[1]-800))
        msp.add_text("Y12 @ 20 CM C/C REINFORCEMENT").set_placement((SEC_OFFSET[0]+400, SEC_OFFSET[1]-500))

    else: # SHOWER SCREEN LOGIC
        # Draw Elevation
        msp.add_lwpolyline([(ELEV_OFFSET[0], ELEV_OFFSET[1]), (ELEV_OFFSET[0]+W, ELEV_OFFSET[1]), 
                            (ELEV_OFFSET[0]+W, ELEV_OFFSET[1]+H), (ELEV_OFFSET[0], ELEV_OFFSET[1]+H)], close=True)
        # Handle
        msp.add_circle((ELEV_OFFSET[0]+W-100, ELEV_OFFSET[1]+1050), 30)
        msp.add_text("HANDLE AT 1050mm AFFL").set_placement((ELEV_OFFSET[0]+W+50, ELEV_OFFSET[1]+1050))
        
        # Hinge Rules
        hinge_count = 3 if W > 1200 else 2
        for i in range(hinge_count):
            msp.add_circle((ELEV_OFFSET[0]+50, ELEV_OFFSET[1]+300 + (i*600)), 20)
        msp.add_text(f"{hinge_count} NOS HINGES PROVIDED").set_placement((ELEV_OFFSET[0]-500, ELEV_OFFSET[1]+300))

    # --- GENERAL NOTES & TITLE BLOCK ---
    notes = [
        "GENERAL NOTES:",
        "1. DO NOT SCALE THE DIMENSIONS, FOLLOW WRITTEN DIMENSIONS.",
        "2. ALL DIMENSIONS ARE IN MM UNLESS NOTED.",
        "3. BRING DISCREPANCIES TO CONSULTANT PRIOR TO WORK.",
        "4. DRAWING FOR DUBAI MUNICIPALITY APPROVAL.",
        "",
        f"CLIENT: {client_name}",
        f"PROJECT: {project_name}",
        f"LOCATION: {location}",
        f"FINISH: {finish}",
        f"CONTRACTOR: POOL SCAPE SWIMMING POOL INSTALLATION LLC",
        f"DATE: {date.today()}"
    ]
    for i, note in enumerate(notes):
        msp.add_text(note).set_placement((8000, 6000 - (i*250)))

    filepath = "PoolScape_Technical_Drawing.dxf"
    doc.saveas(filepath)
    return filepath

# --- ACTION BUTTON ---
if st.button("🚀 Generate Technical Set"):
    file = create_drawing()
    st.success("Drawing Generated! Download the file below and open it in AutoCAD or Autodesk Viewer.")
    with open(file, "rb") as f:
        st.download_button("📥 Download AutoCAD (.DXF)", f, file_name=file)

st.divider()
st.info("Expert Tip: Take this .dxf file and drag it into 'viewer.autodesk.com' to see your Plan, Elevation, and Section instantly.")
