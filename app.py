import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO

# --- PAGE SETUP ---
st.set_page_config(page_title="Pool Scape Professional PDF", layout="wide")
st.title("🏗️ Pool Scape: Technical Drawing Engine")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Drawing Dimensions")
client = st.sidebar.text_input("Client Name", "DMITRY IGNATOV")
project = st.sidebar.text_input("Project", "G +1 VILLA")
W = st.sidebar.number_input("Span/Width (m)", value=2.67)
H = st.sidebar.number_input("Height (m)", value=2.80)

def create_professional_plot(w_m, h_m):
    # 1. Create the figure
    fig, ax = plt.subplots(figsize=(10, 12))
    
    # 2. DRAWING LOGIC (Section View)
    # Ground Floor Level
    ax.axhline(y=0, color='black', linewidth=1.5)
    ax.text(-1.2, 0.05, "GROUND FLOOR", fontsize=8, fontweight='bold')

    # Foundation Footing (0.6m x 0.6m)
    # centered at x=0
    footing = patches.Rectangle((-0.3, -0.6), 0.6, 0.6, linewidth=1.2, edgecolor='black', facecolor='#eeeeee', hatch='///')
    ax.add_patch(footing)
    
    # PCC Layer (0.1m)
    pcc = patches.Rectangle((-0.3, -0.7), 0.6, 0.1, linewidth=1.2, edgecolor='black', facecolor='#cccccc')
    ax.add_patch(pcc)
    
    # Column (150mm = 0.15m)
    column = patches.Rectangle((-0.075, 0), 0.15, h_m, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(column)
    
    # Top Beam (Horizontal)
    beam = patches.Rectangle((-w_m/2, h_m-0.15), w_m, 0.15, linewidth=1.5, edgecolor='black', facecolor='none')
    ax.add_patch(beam)

    # 3. ANNOTATIONS (Matching your PDF text)
    ax.text(0.4, h_m/2, f"150X150X{int(h_m*1000)}MM ALUMINUM\nSUPPORTING COLUMN\nPOWDER COATED", fontsize=9)
    ax.text(0.4, -0.3, "600X600X600 FOUNDATION\nTO ENGINEERS DETAILS", fontsize=8)
    ax.text(0.4, -0.65, "10CM THICK PCC", fontsize=8)
    ax.text(0, -0.5, "Y12 @ 20 CM C/C", fontsize=8, ha='center', color='blue', fontweight='bold')

    # 4. DIMENSIONS (Red Lines)
    # Total Height Dim
    ax.annotate('', xy=(-0.5, 0), xytext=(-0.5, h_m), arrowprops=dict(arrowstyle='<->', color='red'))
    ax.text(-0.6, h_m/2, f"{h_m:.2f}m", color='red', fontweight='bold', rotation=90, va='center')
    
    # Total Width Dim
    ax.annotate('', xy=(-w_m/2, h_m+0.2), xytext=(w_m/2, h_m+0.2), arrowprops=dict(arrowstyle='<->', color='red'))
    ax.text(0, h_m+0.3, f"{w_m:.2f}m Span", color='red', fontweight='bold', ha='center')

    # 5. TITLE BLOCK BOX (Bottom Right)
    stats = f"CLIENT: {client}\nPROJECT: {project}\nDATE: 28/07/2026\nCONTRACTOR: POOL SCAPE LLC"
    plt.gcf().text(0.6, 0.15, stats, fontsize=10, bbox=dict(facecolor='white', edgecolor='black'))

    # Clean up the graph look
    ax.set_xlim(-w_m, w_m)
    ax.set_ylim(-1.5, h_m + 1)
    ax.axis('off')
    plt.title("ALUMINIUM PERGOLA SECTION-1", fontsize=14, fontweight='bold')
    
    return fig

# --- RENDER LOGIC ---
if st.button("🚀 Generate Technical Drawing"):
    # Create the figure
    fig = create_professional_plot(W, H)
    
    # Show preview on screen (FIXED PART)
    st.pyplot(fig)
    
    # Create PDF for download
    buf = BytesIO()
    fig.savefig(buf, format="pdf", bbox_inches='tight')
    st.download_button(
        label="📥 Download Professional PDF",
        data=buf.getvalue(),
        file_name="PoolScape_Drawing.pdf",
        mime="application/pdf"
    )
