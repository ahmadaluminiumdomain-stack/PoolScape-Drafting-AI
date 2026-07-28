import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

# --- PAGE SETUP ---
st.set_page_config(page_title="Pool Scape PDF Drafter", layout="wide")
st.title("🏗️ Pool Scape: Instant PDF Technical Drawing")

# --- INPUTS ---
st.sidebar.header("Drawing Dimensions")
client = st.sidebar.text_input("Client Name", "DMITRY IGNATOV")
project = st.sidebar.text_input("Project", "G +1 VILLA")
W = st.sidebar.number_input("Span/Width (m)", value=2.67)
H = st.sidebar.number_input("Height (m)", value=2.80)

def generate_pdf_drawing(w_m, h_m):
    # Create the figure (Paper size A3 style)
    fig, ax = plt.subplots(figsize=(12, 16))
    
    # 1. DRAWING THE SECTION (Calculated in Meters)
    # Ground Line
    ax.axhline(y=0, color='black', linewidth=2)
    
    # Foundation (0.6m x 0.6m)
    # Drawing at x=0 for section view
    foundation = patches.Rectangle((-0.3, -0.6), 0.6, 0.6, linewidth=1.5, edgecolor='black', facecolor='#f0f0f0', hatch='...')
    ax.add_patch(foundation)
    
    # PCC Layer (0.1m)
    pcc = patches.Rectangle((-0.3, -0.7), 0.6, 0.1, linewidth=1.5, edgecolor='black', facecolor='#d0d0d0')
    ax.add_patch(pcc)
    
    # Column (0.15m width)
    column = patches.Rectangle((-0.075, 0), 0.15, h_m, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(column)
    
    # 2. LABELS & ANNOTATIONS (Match your PDF style)
    ax.text(0.4, h_m/2, f"150X150X{int(h_m*1000)}MM ALUMINUM\nSUPPORTING COLUMN\nPOWDER COATED", fontsize=10, fontweight='bold')
    ax.text(0.4, -0.3, "600X600X600 FOUNDATION\nTO ENGINEERS DETAILS", fontsize=9)
    ax.text(0.4, -0.65, "10CM THICK PCC", fontsize=9)
    ax.text(0.4, -0.8, "COMPACTED SOIL FILLING", fontsize=9)
    ax.text(0, -0.5, "Y12 @ 20 CM C/C", fontsize=8, ha='center', color='blue')

    # 3. DIMENSION LINES
    ax.annotate('', xy=(-0.4, 0), xytext=(-0.4, h_m), arrowprops=dict(arrowstyle='<->', color='red'))
    ax.text(-0.5, h_m/2, f"{h_m:.2f}m", color='red', rotation=90, va='center')

    # 4. TITLE BLOCK (The Box on the right/bottom)
    title_text = (
        f"CLIENT: {client}\n"
        f"PROJECT: {project}\n"
        f"TITLE: PERGOLA FOOTING\n"
        f"CONTRACTOR: POOL SCAPE SWIMMING POOL INSTALLATION LLC\n"
        f"DATE: 28-07-2026"
    )
    plt.gcf().text(0.65, 0.15, title_text, fontsize=11, bbox=dict(facecolor='none', edgecolor='black', pad=10))

    # --- FINAL CLEANUP ---
    ax.set_xlim(-1.5, 3)
    ax.set_ylim(-1.5, h_m + 1)
    ax.axis('off') # Hide graph axes
    plt.title("ALUMINIUM PERGOLA SECTION-1", fontsize=16, pad=20)
    
    # Save to Buffer
    buf = BytesIO()
    plt.savefig(buf, format="pdf", bbox_inches='tight')
    return buf

# --- SHOW PREVIEW & DOWNLOAD ---
if st.button("🚀 Generate PDF Drawing"):
    pdf_buf = generate_pdf_drawing(W, H)
    
    # Show the user what it looks like as an image first
    st.image(pdf_buf, caption="Drawing Preview", use_container_width=True)
    
    # Provide download button
    st.download_button(
        label="📥 Download Professional PDF",
        data=pdf_buf,
        file_name="PoolScape_Technical_Drawing.pdf",
        mime="application/pdf"
    )
