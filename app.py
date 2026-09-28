import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(
    page_title="Project Checkout & Intake | GenomeTech Studio",
    page_icon="🧬",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b 0%, #0f172a 60%, #020617 100%);
        color: #f1f5f9 !important;
        font-family: 'Inter', sans-serif;
    }
    .intake-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Navigation back to main website
if st.button("← Back to GenomeTech Studio"):
    st.markdown('<meta http-equiv="refresh" content="0;url=https://bhumikasihare.github.io/genometech-studio/">', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 1.5rem 0;">
    <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; padding: 4px 14px; border-radius: 999px; font-size: 0.8rem; font-weight: bold; border: 1px solid rgba(16, 185, 129, 0.4);">SECURE PROJECT INTAKE</span>
    <h1 style="color: white; margin-top: 10px;">Configure & Secure Your Pipeline</h1>
    <p style="color: #94a3b8; max-width: 600px; margin: 0 auto;">Review your selected tier or custom modules, submit your dataset requirements, and proceed with your 30% advance.</p>
</div>
""", unsafe_allow_html=True)

# Backend endpoints
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSsQkADNSxfsePaLn1b4RPN018cIyO8bHnfRtmIYGAawnRtgjBGhWhM35GMRhNrVvfcf3wZE7indbHl/pub?output=csv"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz-pKMSgW-i32k9XAYEPaybbE5V4MV9Pm2boob3PFW10JwqahSPZjlFD1nIoS31KtLt/exec"

# Your exact permanent Razorpay 30% Advance Payment Links
RAZORPAY_LINKS = {
    "Tier 1": "https://rzp.io/rzp/r0bsnBPe",
    "Tier 2": "https://rzp.io/rzp/ppWhefM",
    "Tier 3": "https://rzp.io/rzp/3BGvCKo1",
    "Tier 4": "https://rzp.io/rzp/33zosVfX",
    "Custom": "https://rzp.io/rzp/3BGvCKo1" # Enterprise custom advance fallback
}

col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.markdown('<div class="intake-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Step 1: Project Details & Requirements")
    
    client_email = st.text_input("Research Email Address *", placeholder="pi@university.edu")
    client_name = st.text_input("Full Name / Principal Investigator *", placeholder="Dr. Jane Doe")
    dataset_link = st.text_input("Dataset Link (Google Drive / Dropbox / S3)", placeholder="https://drive.google.com/...")
    project_notes = st.text_area("Specific Research Objectives or Parameters", placeholder="Mention species, reference genome build, or specific analytical constraints...")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="intake-card">', unsafe_allow_html=True)
    st.markdown("### 💰 Step 2: Select Tier or Custom Modules")
    
    selection_type = st.radio("Checkout Path:", ["Option A: Full Tier Bundle", "Option B: Custom Modular Selection"])
    
    selected_tier = "Custom"
    total_price = 0.0
    advance_price = 0.0
    modules_desc = ""
    
    if selection_type == "Option A: Full Tier Bundle":
        tier_choice = st.selectbox("Choose Enterprise Tier:", [
            "Tier 1: Variant Calling ($380 total | $114 advance)",
            "Tier 2: Transcriptomics RNA-Seq ($410 total | $123 advance)",
            "Tier 4: Single-Cell Profiling ($450 total | $135 advance)",
            "Tier 5: Microbiome 16S rRNA ($400 total | $120 advance)"
        ])
        
        if "Tier 1" in tier_choice:
            selected_tier = "Tier 1"
            total_price, advance_price = 380.0, 114.0
        elif "Tier 2" in tier_choice:
            selected_tier = "Tier 2"
            total_price, advance_price = 410.0, 123.0
        elif "Tier 4" in tier_choice:
            selected_tier = "Tier 4"
            total_price, advance_price = 450.0, 135.0
        elif "Tier 5" in tier_choice:
            selected_tier = "Tier 5"
            total_price, advance_price = 400.0, 120.0
            
        modules_desc = f"Full {selected_tier} Bundle"
        
        st.markdown(f"**Total Price:** ${total_price}")
        st.markdown(f"**Required 30% Advance:** <span style='color: #34d399; font-size: 1.2rem; font-weight: bold;'>${advance_price} USD</span>", unsafe_allow_html=True)
        
        pay_url = RAZORPAY_LINKS.get(selected_tier, RAZORPAY_LINKS["Custom"])
        
        if st.button("Proceed to 30% Razorpay Checkout ➔", use_container_width=True):
            if client_email and client_name:
                st.success("Details recorded! Redirecting to secure Razorpay payment gateway...")
                st.markdown(f'<meta http-equiv="refresh" content="2;url={pay_url}">', unsafe_allow_html=True)
                st.markdown(f"If not redirected automatically, [Click Here to Pay]({pay_url})")
            else:
                st.warning("Please fill in your email and name before proceeding.")

    else:
        st.markdown("Select individual custom modules:")
        m1 = st.checkbox("FastQC & Read Trimming ($50)")
        m2 = st.checkbox("Alignment / Mapping ($150)")
        m3 = st.checkbox("Differential Analysis / Clustering ($120)")
        m4 = st.checkbox("Custom Annotation & Report ($100)")
        
        custom_total = (50 if m1 else 0) + (150 if m2 else 0) + (120 if m3 else 0) + (100 if m4 else 0)
        custom_advance = custom_total * 0.30
        
        st.markdown(f"**Calculated Total:** ${custom_total}")
        st.markdown(f"**Required 30% Advance:** <span style='color: #34d399; font-weight: bold;'>${custom_advance:.2f} USD</span>", unsafe_allow_html=True)
        
        chosen_mods = []
        if m1: chosen_mods.append("FastQC")
        if m2: chosen_mods.append("Alignment")
        if m3: chosen_mods.append("Clustering/DE")
        if m4: chosen_mods.append("Annotation")
        modules_desc = ", ".join(chosen_mods) if chosen_mods else "None selected"
        
        if st.button("Submit Custom Intake & Request Payment Link", use_container_width=True):
            if client_email and client_name and chosen_mods:
                payload = {
                    "clientEmail": client_email,
                    "clientName": client_name,
                    "tierSelected": "Custom Modular",
                    "modulesChosen": modules_desc,
                    "totalPrice": custom_total,
                    "advancePrice": custom_advance,
                    "datasetLink": dataset_link,
                    "notes": project_notes,
                    "action": "new_custom_intake"
                }
                try:
                    res = requests.post(WEB_APP_URL, json=payload)
                    st.success("🎉 Intake submitted successfully! We have received your requirements. Your custom 30% payment link will be emailed to you within 6–8 hours.")
                except Exception as e:
                    st.error(f"Error submitting intake: {e}")
            else:
                st.warning("Please provide your email, name, and select at least one module.")

    st.markdown('</div>', unsafe_allow_html=True)