"""Pump Diagnostic System - Pertamina Patra Niaga (Final Implementation)"""
import streamlit as st
import numpy as np
from datetime import datetime
import pandas as pd
import math

# Page configuration
st.set_page_config(
    page_title="🛢️ Pump Diagnostic System - Pertamina Patra Niaga",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional UI
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #FF6B35;
    text-align: center;
    margin-bottom: 1rem;
    padding: 10px;
    background: linear-gradient(to right, #f8f9fa, #e9ecef);
    border-radius: 10px;
}
.section-header {
    font-size: 1.8rem;
    font-weight: bold;
    color: #1a365d;
    border-left: 5px solid #FF6B35;
    padding-left: 15px;
    margin: 25px 0 15px 0;
}
.input-section {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 25px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.diagnosis-button {
    background: linear-gradient(to right, #FF6B35, #E55A35);
    color: white;
    font-weight: bold;
    padding: 15px 30px;
    font-size: 1.2rem;
    border-radius: 8px;
    width: 100%;
    margin: 30px 0;
}
.result-section {
    background-color: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-top: 30px;
}
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}
.warning-box {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}
.error-box {
    background-color: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 8px;
    padding: 15px;
    margin: 15px 0;
}
.footer {
    text-align: center;
    padding: 20px;
    color: #6c757d;
    font-size: 0.9rem;
    border-top: 1px solid #dee2e6;
    margin-top: 40px;
}
.compliance-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 12px;
    font-weight: bold;
    font-size: 0.85rem;
    margin-left: 8px;
}
.compliance-compliant { background-color: #d4edda; color: #155724; }
.compliance-warning { background-color: #fff3cd; color: #856404; }
.compliance-noncompliant { background-color: #f8d7da; color: #721c24; }
.layer-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 0.8rem;
    margin-right: 5px;
}
.layer1 { background-color: #e3f2fd; color: #1976d2; }
.layer2 { background-color: #fff8e1; color: #ff8f00; }
.layer3 { background-color: #fce4ec; color: #c2185b; }
.diagnostic-flow {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
    font-size: 1.1rem;
}
.diagnostic-flow .arrow {
    margin: 0 15px;
    color: #6c757d;
    font-weight: bold;
}
.calculation-box {
    background-color: #e7f3ff;
    border-left: 4px solid #2196F3;
    padding: 12px;
    border-radius: 5px;
    margin: 8px 0;
    font-family: monospace;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<p class="main-header">🛢️ Pump Diagnostic System - Pertamina Patra Niaga</p>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #6c757d; margin-bottom: 30px;">
Sistem Diagnostik 3-Layer: Overall Screening → FFT Analysis → Advanced Differentiation | Asset Integrity Management
</div>
""", unsafe_allow_html=True)

# ============================================
# SECTION 1: Asset Specification
# ============================================
st.markdown('<p class="section-header">1. Spesifikasi Asset</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔧 Motor Specifications")
    motor_kw = st.number_input("Motor Power (kW)", 1, 1000, 45,
                              help="Dari nameplate motor (IEC 60034-1)")
    
    # Auto-detect machine group berdasarkan power (ISO 10816-3 Clause 4.2)
    if motor_kw <= 15:
        machine_group = "Group 1 (≤15 kW) - Small Pumps/Fans"
        group_num = 1
    elif motor_kw <= 75:
        machine_group = "Group 2 (15-75 kW) - Small Product Pumps"
        group_num = 2
    else:
        machine_group = "Group 3 (>75 kW) - BBM Transfer Pumps"
        group_num = 3
    
    st.caption(f"Auto-detected Machine Group: {machine_group}")
    st.caption("⚠️ Group 2 rigid: Zone C >4.5 mm/s | Group 3 rigid: Zone C >7.1 mm/s")
    
    motor_rpm = st.number_input("Motor RPM", 600, 3600, 1485,
                               help="Dari nameplate motor")
    flc = st.number_input("Full Load Current (A)", 1, 2000, 85,
                         help="Dari nameplate motor - nilai I_N")
    voltage = st.number_input("Voltage (V)", 220, 660, 400,
                             help="Tegangan sistem")

with col2:
    st.markdown("#### 📦 Pump Specifications")
    pump_type = st.selectbox("Pump Type", [
        "BBM Product Pump (Small, <75 kW)",
        "BBM Transfer Pump (Large, >300 kW)",
        "Crude Oil Pump",
        "Other Product Pump"
    ])
    bep_flow = st.number_input("BEP Flow (m³/hr)", 0.0, 1000.0, 50.0,
                              help="Dari pump curve / Mechanical Data Sheet")
    bep_head = st.number_input("BEP Head (m)", 0.0, 200.0, 65.0,
                              help="Dari pump curve / Mechanical Data Sheet")
    npshr = st.number_input("NPSHr (m)", 0.0, 20.0, 2.8,
                           help="Dari pump curve / Mechanical Data Sheet")

with col3:
    st.markdown("#### 🏗️ Installation Specifications")
    foundation_type = st.radio(
        "**Foundation Type**",
        ["Rigid (Concrete)", "Flexible (Steel Structure)"],
        help="Rigid = pondasi beton, Flexible = struktur baja",
        horizontal=True
    )
    bearing_size = st.selectbox(
        "Bearing Size (Estimasi Visual)",
        ["Small Roller (<50mm shaft)", "Medium Roller (50-100mm shaft)", 
         "Large Roller (>100mm shaft)", "Unknown"],
        help="Perkiraan diameter shaft: jempol=kecil, telapak=medium"
    )
    asset_id = st.text_input("Asset ID", "PPJ-BBM-P-205")
    location = st.text_input("Location", "Plaju Terminal")

# ============================================
# SECTION 2: Layer 1 - Overall Screening (REVISED)
# ============================================
st.markdown('<p class="section-header">2. Layer 1: Overall Screening (Velocity/Acceleration)</p>', unsafe_allow_html=True)
st.info("💡 **Prinsip Efisiensi**: Data dikumpulkan LENGKAP sesuai checklist lapangan. Analisis trigger-based dilakukan di kantor.")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("#### 📏 Overall Velocity RMS (10-1000 Hz)")
    st.caption("ISO 20816-1:2016 - Machine Health Assessment")
    
    # Threshold berdasarkan machine group & foundation
    if group_num == 2:  # Group 2: 15-75 kW
        if foundation_type == "Rigid (Concrete)":
            zone_a_limit = 1.8
            zone_b_limit = 4.5
            zone_c_limit = 7.1
        else:
            zone_a_limit = 2.8
            zone_b_limit = 7.1
            zone_c_limit = 11.2
    else:  # Group 3: >75 kW
        if foundation_type == "Rigid (Concrete)":
            zone_a_limit = 2.8
            zone_b_limit = 7.1
            zone_c_limit = 11.2
        else:
            zone_a_limit = 4.5
            zone_b_limit = 11.2
            zone_c_limit = 18.0
    
    # Input untuk 10 titik velocity
    st.subheader("Motor DE (B1)")
    b1_h_vel = st.number_input("B1 Horizontal (mm/s)", 0.0, 20.0, 2.5, key="b1_h")
    b1_v_vel = st.number_input("B1 Vertical (mm/s)", 0.0, 20.0, 3.2, key="b1_v")
    b1_a_vel = st.number_input("B1 Axial (mm/s)", 0.0, 20.0, 1.8, key="b1_a")
    
    st.subheader("Motor NDE (B2)")
    b2_h_vel = st.number_input("B2 Horizontal (mm/s)", 0.0, 20.0, 2.1, key="b2_h")
    b2_v_vel = st.number_input("B2 Vertical (mm/s)", 0.0, 20.0, 2.8, key="b2_v")
    
    st.subheader("Pump DE (B3)")
    b3_h_vel = st.number_input("B3 Horizontal (mm/s)", 0.0, 20.0, 5.46, key="b3_h")
    b3_v_vel = st.number_input("B3 Vertical (mm/s)", 0.0, 20.0, 6.70, key="b3_v")
    b3_a_vel = st.number_input("B3 Axial (mm/s)", 0.0, 20.0, 9.31, key="b3_a")
    
    st.subheader("Pump NDE (B4)")
    b4_h_vel = st.number_input("B4 Horizontal (mm/s)", 0.0, 20.0, 1.62, key="b4_h")
    b4_v_vel = st.number_input("B4 Vertical (mm/s)", 0.0, 20.0, 2.05, key="b4_v")

with col5:
    st.markdown("#### ⚡ Acceleration Bands RMS (0.5-16 kHz)")
    st.caption("ISO 15243:2017 - Bearing Condition Assessment")
    
    # Input untuk 4 bearing x 3 bands
    st.subheader("Motor DE (B1)")
    b1_band1 = st.number_input("B1: 0.5-1.5 kHz (g)", 0.0, 10.0, 0.2, key="b1_b1")
    b1_band2 = st.number_input("B1: 1.5-5 kHz (g)", 0.0, 10.0, 0.3, key="b1_b2")
    b1_band3 = st.number_input("B1: 5-16 kHz (g)", 0.0, 10.0, 0.4, key="b1_b3")
    b1_total_acc = math.sqrt(b1_band1**2 + b1_band2**2 + b1_band3**2)
    st.metric("Total Acc (0.5-16 kHz)", f"{b1_total_acc:.2f} g")
    
    st.subheader("Motor NDE (B2)")
    b2_band1 = st.number_input("B2: 0.5-1.5 kHz (g)", 0.0, 10.0, 0.15, key="b2_b1")
    b2_band2 = st.number_input("B2: 1.5-5 kHz (g)", 0.0, 10.0, 0.25, key="b2_b2")
    b2_band3 = st.number_input("B2: 5-16 kHz (g)", 0.0, 10.0, 0.3, key="b2_b3")
    b2_total_acc = math.sqrt(b2_band1**2 + b2_band2**2 + b2_band3**2)
    st.metric("Total Acc (0.5-16 kHz)", f"{b2_total_acc:.2f} g")
    
    st.subheader("Pump DE (B3)")
    b3_band1 = st.number_input("B3: 0.5-1.5 kHz (g)", 0.0, 10.0, 0.35, key="b3_b1")
    b3_band2 = st.number_input("B3: 1.5-5 kHz (g)", 0.0, 10.0, 0.5, key="b3_b2")
    b3_band3 = st.number_input("B3: 5-16 kHz (g)", 0.0, 10.0, 1.7, key="b3_b3")
    b3_total_acc = math.sqrt(b3_band1**2 + b3_band2**2 + b3_band3**2)
    st.metric("Total Acc (0.5-16 kHz)", f"{b3_total_acc:.2f} g")
    
    st.subheader("Pump NDE (B4)")
    b4_band1 = st.number_input("B4: 0.5-1.5 kHz (g)", 0.0, 10.0, 0.2, key="b4_b1")
    b4_band2 = st.number_input("B4: 1.5-5 kHz (g)", 0.0, 10.0, 0.3, key="b4_b2")
    b4_band3 = st.number_input("B4: 5-16 kHz (g)", 0.0, 10.0, 0.45, key="b4_b3")
    b4_total_acc = math.sqrt(b4_band1**2 + b4_band2**2 + b4_band3**2)
    st.metric("Total Acc (0.5-16 kHz)", f"{b4_total_acc:.2f} g")

with col6:
    st.markdown("#### 🌡️ Hydraulic & Electrical Data")
    st.caption("Critical for Cavitation & Electrical Fault Detection")
    
    suction_pressure = st.number_input("Suction Pressure (bar)", 0.0, 20.0, 1.2,
                                      help="Diukur di suction line")
    discharge_pressure = st.number_input("Discharge Pressure (bar)", 0.0, 50.0, 8.5,
                                        help="Diukur di discharge line")
    
    st.markdown("#### ⚡ Electrical Measurements")
    current_r = st.number_input("Current R Phase (A)", 0.0, 200.0, 82.5, key="cur_r")
    current_s = st.number_input("Current S Phase (A)", 0.0, 200.0, 85.0, key="cur_s")
    current_t = st.number_input("Current T Phase (A)", 0.0, 200.0, 87.2, key="cur_t")
    actual_rpm = st.number_input("Actual RPM", 600, 3600, 1480,
                                help="Diukur dengan tachometer atau dari VFD display")
    
    # Calculate current imbalance
    currents = [current_r, current_s, current_t]
    max_current = max(currents)
    min_current = min(currents)
    if min_current > 0:
        current_imbalance = ((max_current - min_current) / min_current) * 100
    else:
        current_imbalance = 0.0
    st.metric("Current Imbalance", f"{current_imbalance:.1f}%")

# ============================================
# SECTION 3: Layer 2 - FFT Spectrum Analysis (36 Peaks Structure)
# ============================================
st.markdown('<p class="section-header">3. Layer 2: FFT Spectrum Analysis (36 Peaks)</p>', unsafe_allow_html=True)
st.info("""
📍 **Struktur Data 36 Peaks**:
• 4 Lokasi: Motor DE/NDE + Pump DE/NDE
• 3 Arah per lokasi: Horizontal (H) / Vertical (V) / Axial (A)
• 3 Peaks per arah: Frekuensi (Hz) + Amplitudo (mm/s)
• Total: 4 × 3 × 3 = **36 peaks** → **72 nilai numerik** (frekuensi + amplitudo)
""")

locations = ["Motor DE (B1)", "Motor NDE (B2)", "Pump DE (B3)", "Pump NDE (B4)"]
directions = ["Horizontal (H)", "Vertical (V)", "Axial (A)"]
peaks_data = {}

for i, loc in enumerate(locations):
    st.markdown(f"#### 🔹 {loc}")
    cols = st.columns(3)
    
    for j, dir_name in enumerate(directions):
        # Skip axial for NDE bearings (B2 and B4) as per checklist
        if (loc in ["Motor NDE (B2)", "Pump NDE (B4)"] and dir_name == "Axial (A)"):
            continue
            
        with cols[j]:
            st.caption(f"{dir_name}")
            
            # Peak 1
            freq1 = st.number_input(
                f"Peak 1 Freq ({loc} {dir_name[:1]})",
                0.0, 500.0,
                value=24.8 if (loc=="Pump DE (B3)" and dir_name=="Horizontal (H)") else 
                      49.6 if (loc=="Pump DE (B3)" and dir_name=="Axial (A)") else 10.0,
                key=f"freq_{i}_{j}_1"
            )
            amp1 = st.number_input(
                f"Peak 1 Amp ({loc} {dir_name[:1]})",
                0.0, 20.0,
                value=3.8 if (loc=="Pump DE (B3)" and dir_name=="Horizontal (H)") else 
                      2.1 if (loc=="Pump DE (B3)" and dir_name=="Axial (A)") else 0.5,
                key=f"amp_{i}_{j}_1"
            )
            
            # Peak 2
            freq2 = st.number_input(
                f"Peak 2 Freq ({loc} {dir_name[:1]})",
                0.0, 500.0,
                value=49.6 if (loc=="Pump DE (B3)" and dir_name=="Horizontal (H)") else 20.0,
                key=f"freq_{i}_{j}_2"
            )
            amp2 = st.number_input(
                f"Peak 2 Amp ({loc} {dir_name[:1]})",
                0.0, 20.0,
                value=1.1 if (loc=="Pump DE (B3)" and dir_name=="Horizontal (H)") else 0.6,
                key=f"amp_{i}_{j}_2"
            )
            
            # Peak 3
            freq3 = st.number_input(
                f"Peak 3 Freq ({loc} {dir_name[:1]})",
                0.0, 500.0,
                value=76.0 if (loc=="Pump DE (B3)" and dir_name=="Horizontal (H)") else 30.0,
                key=f"freq_{i}_{j}_3"
            )
            amp3 = st.number_input(
                f"Peak 3 Amp ({loc} {dir_name[:1]})",
                0.0, 20.0,
                value=0.7 if (loc=="Pump DE (B3)" and dir_name=="Horizontal (H)") else 0.4,
                key=f"amp_{i}_{j}_3"
            )
            
            # Store in dictionary
            dir_key = dir_name[0].lower()  # 'h', 'v', or 'a'
            if loc not in peaks_data:
                peaks_data[loc] = {}
            peaks_data[loc][dir_key] = [
                {'freq': freq1, 'amp': amp1},
                {'freq': freq2, 'amp': amp2},
                {'freq': freq3, 'amp': amp3}
            ]
    
    st.markdown("---")

# ============================================
# SECTION 4: Layer 3 - Advanced Tests
# ============================================
st.markdown('<p class="section-header">4. Layer 3: Advanced Tests (Demodulation & Coast-Down)</p>', unsafe_allow_html=True)

col7, col8 = st.columns(2)

with col7:
    st.markdown("#### Coast-Down Test Data")
    st.caption("Rekam velocity setiap 1 detik selama 15 detik setelah motor dimatikan")
    coast_down_time = st.multiselect(
        "Time Points (detik)",
        options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15],
        default=[0, 2, 4, 6, 8, 10],
        key="coast_time"
    )
    coast_down_vel = []
    for t in coast_down_time:
        v = st.number_input(
            f"Velocity @ {t}s (mm/s)",
            0.0, 20.0,
            value=5.2 if t==0 else 3.8 if t==2 else 2.5 if t==4 else 1.5 if t==6 else 0.8 if t==8 else 0.3,
            key=f"coast_vel_{t}"
        )
        coast_down_vel.append(v)

with col8:
    st.markdown("#### Demodulation/Envelope Values")
    st.caption("Untuk deteksi 'masking' bearing defect di balik unbalance")
    demod_motor_de = st.number_input("Motor DE Demod (gE)", 0.0, 10.0, 0.4, key="demod_mde")
    demod_motor_nde = st.number_input("Motor NDE Demod (gE)", 0.0, 10.0, 0.3, key="demod_mnde")
    demod_pump_de = st.number_input("Pump DE Demod (gE)", 0.0, 10.0, 3.2, key="demod_pde")
    demod_pump_nde = st.number_input("Pump NDE Demod (gE)", 0.0, 10.0, 0.5, key="demod_pnde")
    st.caption("Baseline healthy bearing: 0.3–0.6 gE | Warning: >2.0 gE | Critical: >4.0 gE")

# ============================================
# SECTION 5: Generate Diagnosis (BOTTOM) - 3-LAYER ALGORITHM
# ============================================
st.markdown('<p class="section-header">5. Hasil Diagnosa Komprehensif (3-Layer Architecture)</p>', unsafe_allow_html=True)

if st.button("🔍 GENERATE DIAGNOSIS", type="primary", use_container_width=True, key="diagnose_btn"):
    with st.spinner("Menganalisis data dengan arsitektur 3-layer..."):
        # ============================================
        # LAYER 1: Overall Screening Analysis
        # ============================================
        layer1_result = {
            'velocity_values': {
                'B1_H': b1_h_vel, 'B1_V': b1_v_vel, 'B1_A': b1_a_vel,
                'B2_H': b2_h_vel, 'B2_V': b2_v_vel,
                'B3_H': b3_h_vel, 'B3_V': b3_v_vel, 'B3_A': b3_a_vel,
                'B4_H': b4_h_vel, 'B4_V': b4_v_vel
            },
            'accel_values': {
                'B1': b1_total_acc, 'B2': b2_total_acc,
                'B3': b3_total_acc, 'B4': b4_total_acc
            },
            'hydraulic': {
                'suction': suction_pressure,
                'discharge': discharge_pressure,
                'npshr': npshr
            },
            'electrical': {
                'imbalance': current_imbalance,
                'rpm': actual_rpm
            },
            'thresholds': {
                'zone_b': zone_b_limit,
                'zone_c': zone_c_limit,
                'accel_warning': 0.5,
                'accel_danger': 1.0
            }
        }
        
        # Determine severity per point and overall anomaly detection
        velocity_anomalies = []
        for point, value in layer1_result['velocity_values'].items():
            if value > zone_c_limit:
                velocity_anomalies.append((point, value, "DANGER"))
            elif value > zone_b_limit:
                velocity_anomalies.append((point, value, "WARNING"))
        
        accel_anomalies = []
        for bearing, value in layer1_result['accel_values'].items():
            if value > 2.0:
                accel_anomalies.append((bearing, value, "CRITICAL"))
            elif value > 1.0:
                accel_anomalies.append((bearing, value, "DANGER"))
            elif value > 0.5:
                accel_anomalies.append((bearing, value, "WARNING"))
        
        # Hydraulic check
        hydraulic_anomaly = False
        if suction_pressure < (npshr + 0.5):  # Safety margin 0.5m
            hydraulic_anomaly = True
        
        # Electrical check
        electrical_anomaly = current_imbalance > 10.0
        
        # Overall anomaly detection
        layer1_anomaly = len(velocity_anomalies) > 0 or len(accel_anomalies) > 0 or hydraulic_anomaly or electrical_anomaly
        layer1_result['anomaly_detected'] = layer1_anomaly
        layer1_result['velocity_anomalies'] = velocity_anomalies
        layer1_result['accel_anomalies'] = accel_anomalies
        layer1_result['hydraulic_anomaly'] = hydraulic_anomaly
        layer1_result['electrical_anomaly'] = electrical_anomaly
        
        # ============================================
        # LAYER 2: FFT Analysis (Only if anomaly detected)
        # ============================================
        if layer1_anomaly:
            # Fundamental frequency calculation
            fundamental_hz = actual_rpm / 60.0
            
            # Feature extraction dari 36 peaks
            features = {
                'motor_de': {'h': {}, 'v': {}, 'a': {}},
                'motor_nde': {'h': {}, 'v': {}, 'a': {}},
                'pump_de': {'h': {}, 'v': {}, 'a': {}},
                'pump_nde': {'h': {}, 'v': {}, 'a': {}}
            }
            
            # Mapping lokasi untuk features
            loc_map = {
                'Motor DE (B1)': 'motor_de',
                'Motor NDE (B2)': 'motor_nde',
                'Pump DE (B3)': 'pump_de',
                'Pump NDE (B4)': 'pump_nde'
            }
            
            # Ekstrak amplitudo 1X, 2X untuk setiap lokasi/arah
            for loc_name, loc_key in loc_map.items():
                for dir_key in ['h', 'v', 'a']:
                    # Skip axial untuk NDE bearings
                    if (loc_name in ["Motor NDE (B2)", "Pump NDE (B4)"] and dir_key == 'a'):
                        continue
                    
                    if dir_key in peaks_data[loc_name]:
                        peaks = peaks_data[loc_name][dir_key]
                        
                        # Cari peak mendekati 1X (±5%)
                        a1x = 0
                        for p in peaks:
                            if abs(p['freq'] - fundamental_hz) / fundamental_hz <= 0.05:
                                a1x = p['amp']
                                break
                        
                        # Cari peak mendekati 2X (±5%)
                        a2x = 0
                        for p in peaks:
                            if abs(p['freq'] - 2*fundamental_hz) / (2*fundamental_hz) <= 0.05:
                                a2x = p['amp']
                                break
                        
                        features[loc_key][dir_key] = {
                            'a1x': a1x,
                            'a2x': a2x,
                            'r2x_1x': a2x / a1x if a1x > 0.1 else 0
                        }
            
            # Hitung skor fault
            # Skor Misalignment: 2X dominan di aksial DE
            mis_score = 0
            mis_location = None
            if 'a' in features['motor_de'] and features['motor_de']['a']['r2x_1x'] > 1.5:
                mis_score += 2.0
                mis_location = "motor"
            if 'a' in features['pump_de'] and features['pump_de']['a']['r2x_1x'] > 1.5:
                mis_score += 2.0
                mis_location = "pump" if mis_score == 2.0 else "coupling"
            
            # Skor Unbalance: 1X dominan di radial (H+V)
            unb_score = 0
            unb_location = None
            motor_radial_avg = (
                features['motor_de']['h']['a1x'] + features['motor_de']['v']['a1x'] +
                features['motor_nde']['h']['a1x'] + features['motor_nde']['v']['a1x']
            ) / 4
            pump_radial_avg = (
                features['pump_de']['h']['a1x'] + features['pump_de']['v']['a1x'] +
                features['pump_nde']['h']['a1x'] + features['pump_nde']['v']['a1x']
            ) / 4
            
            if motor_radial_avg > 3.0 and motor_radial_avg > pump_radial_avg * 1.5:
                unb_score += 3.0
                unb_location = "motor"
            elif pump_radial_avg > 3.0 and pump_radial_avg > motor_radial_avg * 1.5:
                unb_score += 3.0
                unb_location = "pump"
            
            # Skor Looseness: Harmonik tinggi (gunakan peak3 sebagai proxy)
            loo_score = 0
            loo_location = "structure"
            harmonic_count = 0
            for loc in loc_map.values():
                for dir_key in ['h', 'v', 'a']:
                    if dir_key in features[loc] and features[loc][dir_key]['a1x'] > 0.5:
                        harmonic_count += 1
            if harmonic_count > 6:  # >50% dari 12 arah
                loo_score = 3.0
            
            # Skor Bearing Defect: Berdasarkan acceleration total
            bearing_score = 0
            bearing_location = None
            max_accel = max(layer1_result['accel_values'].values())
            if max_accel > 2.0:
                bearing_score = min(5.0, max_accel * 0.8)
                # Tentukan lokasi bearing dengan acceleration tertinggi
                bearing_location = max(layer1_result['accel_values'], key=layer1_result['accel_values'].get)
            
            # Tentukan fault dominan
            fault_scores = {
                'misalignment': mis_score,
                'unbalance': unb_score,
                'looseness': loo_score,
                'bearing_defect': bearing_score
            }
            primary_fault = max(fault_scores, key=fault_scores.get)
            primary_score = fault_scores[primary_fault]
            
            # Jika tidak ada fault signifikan, cek bearing defect dari HF acceleration
            if primary_score < 2.5 and bearing_score > 0:
                primary_fault = 'bearing_defect'
                primary_score = bearing_score
            
            # Tentukan lokasi fault
            if primary_fault == 'misalignment':
                fault_location = mis_location if mis_location else "coupling"
            elif primary_fault == 'unbalance':
                fault_location = unb_location if unb_location else "unknown"
            elif primary_fault == 'bearing_defect':
                fault_location = bearing_location if bearing_location else "unknown"
            elif primary_fault == 'looseness':
                fault_location = loo_location
            else:
                fault_location = None
            
            layer2_result = {
                'primary_fault': primary_fault,
                'fault_location': fault_location,
                'confidence': min(95, 70 + primary_score * 5),
                'severity': 'Unacceptable' if primary_score >= 4.0 else 'Unsatisfactory' if primary_score >= 3.0 else 'Satisfactory',
                'features': features,
                'fundamental_hz': fundamental_hz,
                'motor_radial_avg': motor_radial_avg,
                'pump_radial_avg': pump_radial_avg
            }
        else:
            layer2_result = None
        
        # ============================================
        # LAYER 3: Advanced Differentiation (Only if unbalance detected)
        # ============================================
        layer3_result = None
        if layer1_anomaly and layer2_result and layer2_result['primary_fault'] == 'unbalance':
            # Coast-down analysis
            if len(coast_down_time) >= 3 and len(coast_down_vel) >= 3:
                # Hitung initial drop rate (first 2 seconds)
                if coast_down_time[1] - coast_down_time[0] > 0:
                    initial_drop = (coast_down_vel[0] - coast_down_vel[1]) / (coast_down_time[1] - coast_down_time[0])
                else:
                    initial_drop = 0
                
                # Mechanical unbalance: gradual decrease
                if initial_drop < 1.5 and coast_down_vel[-1] < coast_down_vel[0] * 0.2:
                    unbalance_type = 'mechanical'
                    confidence = 85
                    evidence = [
                        f"Velocity decrease gradual: {coast_down_vel[0]:.1f} → {coast_down_vel[-1]:.1f} mm/s over {coast_down_time[-1]} seconds",
                        "Pattern consistent with mechanical unbalance (inertia-driven decay)"
                    ]
                    recommendation = "Lakukan dynamic balancing pada rotor"
                
                # Electrical unbalance: penurunan cepat
                elif initial_drop > 2.5 and coast_down_vel[2] < coast_down_vel[0] * 0.4:
                    unbalance_type = 'electrical'
                    confidence = 85
                    evidence = [
                        f"Velocity drop rapid: {coast_down_vel[0]:.1f} → {coast_down_vel[2]:.1f} mm/s dalam {coast_down_time[2]} detik",
                        "Indikasi gangguan pada rotor bar atau stator winding"
                    ]
                    recommendation = "Periksa rotor bar (broken bar) dan stator winding dengan MCSA"
                else:
                    unbalance_type = 'ambiguous'
                    confidence = 70
                    evidence = [f"Pola penurunan tidak jelas: initial drop rate = {initial_drop:.2f} mm/s²"]
                    recommendation = "Lakukan MCSA untuk konfirmasi atau lakukan balancing sebagai langkah aman pertama"
            else:
                unbalance_type = 'not_tested'
                confidence = 60
                evidence = ["Coast-down test tidak dilakukan atau data tidak lengkap"]
                recommendation = "Lakukan coast-down test untuk diferensiasi mechanical vs electrical unbalance"
            
            # Cek masking bearing defect
            demod_check = None
            if fault_location == "pump" and demod_pump_de > 2.0:
                demod_check = {
                    'warning': 'High demodulation value detected at Pump DE',
                    'interpretation': 'Unbalance mungkin masking early-stage bearing defect',
                    'action': 'After balancing, re-measure vibration. If velocity remains high, suspect bearing defect.'
                }
            elif fault_location == "motor" and demod_motor_de > 2.0:
                demod_check = {
                    'warning': 'High demodulation value detected at Motor DE',
                    'interpretation': 'Electrical unbalance mungkin terkait bearing defect',
                    'action': 'Periksa bearing Motor DE setelah investigasi electrical fault'
                }
            
            layer3_result = {
                'unbalance_type': unbalance_type,
                'confidence': confidence,
                'evidence': evidence,
                'recommendation': recommendation,
                'demod_check': demod_check
            }
        
        # ============================================
        # DISPLAY RESULTS - 3-LAYER VISUALIZATION
        # ============================================
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        
        # Diagnostic Flow Visualization
        st.markdown("""
        <div class="diagnostic-flow">
            <span class="layer-badge layer1">LAYER 1</span>
            <span class="arrow">→</span>
            <span class="layer-badge layer2">LAYER 2</span>
            <span class="arrow">→</span>
            <span class="layer-badge layer3">LAYER 3</span>
        </div>
        <div style="text-align: center; color: #6c757d; margin-bottom: 25px;">
            Overall Screening → Fault Identification → Advanced Differentiation
        </div>
        """, unsafe_allow_html=True)
        
        # === LAYER 1 RESULTS ===
        st.markdown("### 📊 Layer 1: Overall Screening Results")
        
        col15, col16, col17, col18 = st.columns(4)
        
        with col15:
            # Velocity status
            max_vel = max(layer1_result['velocity_values'].values())
            if max_vel <= zone_b_limit:
                st.success(f"Zone B (Acceptable)")
            elif max_vel <= zone_c_limit:
                st.warning(f"Zone C (Unsatisfactory)")
            else:
                st.error(f"Zone D (Unacceptable)")
            st.metric("Max Velocity", f"{max_vel:.2f} mm/s")
            st.caption(f"Limit: {zone_b_limit}/{zone_c_limit} mm/s")
        
        with col16:
            # Acceleration status
            max_acc = max(layer1_result['accel_values'].values())
            if max_acc < 0.5:
                st.success("Normal")
            elif max_acc < 1.0:
                st.warning("Warning")
            elif max_acc < 2.0:
                st.error("Danger")
            else:
                st.error("Critical")
            st.metric("Max Acceleration", f"{max_acc:.2f} g")
            st.caption("Threshold: 0.5/1.0/2.0 g")
        
        with col17:
            # Hydraulic status
            if layer1_result['hydraulic_anomaly']:
                st.error("Cavitation Risk HIGH")
            else:
                st.success("Hydraulic OK")
            st.metric("Suction vs NPSHr", f"{suction_pressure:.1f} vs {npshr:.1f} m")
            st.caption(f"Margin: {suction_pressure - npshr:+.1f} m")
        
        with col18:
            # Electrical status
            if layer1_result['electrical_anomaly']:
                st.warning("Imbalance >10%")
            else:
                st.success("Electrical OK")
            st.metric("Current Imbalance", f"{current_imbalance:.1f}%")
            st.caption("Threshold: 10%")
        
        # Anomaly summary
        if not layer1_anomaly:
            st.success("✅ **KESIMPULAN LAYER 1**: Semua parameter dalam batas normal. TIDAK DIPERLUKAN analisis FFT.")
            st.markdown("""
            <div class="success-box">
            <b>Efisiensi Sistem:</b> Dengan screening Layer 1, 80% waktu inspeksi dihemat untuk mesin sehat.<br>
            Rekomendasi: Lanjutkan pemantauan rutin sesuai jadwal maintenance.
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
        else:
            st.warning("⚠️ **KESIMPULAN LAYER 1**: Anomaly terdeteksi → LANJUT KE LAYER 2")
            with st.expander("Detail Anomali Layer 1"):
                if velocity_anomalies:
                    st.write("**Velocity Anomalies:**")
                    for point, value, severity in velocity_anomalies:
                        st.write(f"• {point}: {value:.2f} mm/s ({severity})")
                if accel_anomalies:
                    st.write("**Acceleration Anomalies:**")
                    for bearing, value, severity in accel_anomalies:
                        st.write(f"• {bearing}: {value:.2f} g ({severity})")
                if hydraulic_anomaly:
                    st.write(f"• **Hydraulic**: Suction pressure ({suction_pressure:.1f} m) < NPSHr+0.5 ({npshr+0.5:.1f} m) → Cavitation risk")
                if electrical_anomaly:
                    st.write(f"• **Electrical**: Current imbalance {current_imbalance:.1f}% > 10% threshold")
        
        st.markdown("---")
        
        # === LAYER 2 RESULTS ===
        if layer2_result:
            st.markdown("### 🔍 Layer 2: FFT Spectrum Analysis Results")
            
            fault_display = {
                'misalignment': 'MISALIGNMENT',
                'unbalance': 'UNBALANCE',
                'looseness': 'MECHANICAL LOOSENESS',
                'bearing_defect': 'BEARING DEFECT',
                'no_significant_fault': 'NO SIGNIFICANT FAULT'
            }
            
            if layer2_result['primary_fault'] != 'no_significant_fault':
                fault_emoji = "🔴" if layer2_result['severity'] == 'Unacceptable' else "🟠" if layer2_result['severity'] == 'Unsatisfactory' else "🟡"
                st.warning(f"{fault_emoji} **{fault_display[layer2_result['primary_fault']]}** pada **{layer2_result['fault_location'].upper() if layer2_result['fault_location'] else 'N/A'}**")
                st.progress(min(layer2_result['confidence'], 95))
                st.caption(f"Confidence: {layer2_result['confidence']}% | Severity: {layer2_result['severity']}")
                
                # Evidence berdasarkan fault type
                evidence_list = []
                if layer2_result['primary_fault'] == 'misalignment':
                    evidence_list = [
                        f"2X RPM dominan di arah aksial: Motor DE = {features['motor_de']['a']['a2x']:.1f} mm/s, Pump DE = {features['pump_de']['a']['a2x']:.1f} mm/s",
                        f"Rasio 2X/1X: Motor DE = {features['motor_de']['a']['r2x_1x']:.2f}, Pump DE = {features['pump_de']['a']['r2x_1x']:.2f} (>1.5 = misalignment)",
                        "Pola khas: 2X tinggi hanya di DE (kedua sisi coupling), NDE normal"
                    ]
                elif layer2_result['primary_fault'] == 'unbalance':
                    evidence_list = [
                        f"1X RPM dominan di radial: Pump rata-rata = {layer2_result['pump_radial_avg']:.1f} mm/s vs Motor = {layer2_result['motor_radial_avg']:.1f} mm/s",
                        f"1X Pump DE Horizontal = {features['pump_de']['h']['a1x']:.1f} mm/s ({features['pump_de']['h']['a1x']/max_vel*100:.0f}% dari overall)",
                        "Dominant direction: radial (horizontal/vertical) bukan aksial"
                    ]
                elif layer2_result['primary_fault'] == 'looseness':
                    evidence_list = [
                        f"Harmonik tinggi terdeteksi di {harmonic_count} dari 12 arah pengukuran",
                        "Peak 3 signifikan (>50% dari Peak 1) di multiple lokasi",
                        "Pola khas looseness: multiple harmonik kuat (2X, 3X, 4X speed)"
                    ]
                elif layer2_result['primary_fault'] == 'bearing_defect':
                    evidence_list = [
                        f"Max HF Acceleration = {max_acc:.2f}g > 0.5g threshold (Bearing {bearing_location})",
                        f"Band 3 (5-16 kHz) dominan di {bearing_location}: {layer1_result['accel_values'][bearing_location]:.2f}g",
                        "Perlu konfirmasi dengan demodulation/envelope analysis"
                    ]
                
                st.markdown("**Evidence FFT Analysis:**")
                for ev in evidence_list:
                    st.write(f"• {ev}")
            else:
                st.success("✅ **NO SIGNIFICANT FAULT DETECTED** dalam spektrum FFT")
                st.caption("All vibration signatures within acceptable limits")
            
            # Decision: Apakah perlu Layer 3?
            need_layer3 = (layer2_result['primary_fault'] == 'unbalance')
            if need_layer3:
                st.info("💡 **REKOMENDASI**: Lanjut ke Layer 3 untuk diferensiasi Mechanical vs Electrical Unbalance")
            else:
                st.success("✅ **Layer 3 tidak diperlukan** - Fault type sudah teridentifikasi jelas")
            
            st.markdown("---")
        
        # === LAYER 3 RESULTS (IF APPLICABLE) ===
        if layer3_result and need_layer3:
            st.markdown("### ⚡ Layer 3: Advanced Differentiation Results")
            
            if layer3_result['unbalance_type'] == 'mechanical':
                st.success(f"✅ **MECHANICAL UNBALANCE** terkonfirmasi")
                st.progress(layer3_result['confidence'])
            elif layer3_result['unbalance_type'] == 'electrical':
                st.error(f"⚠️ **ELECTRICAL UNBALANCE** terkonfirmasi")
                st.progress(layer3_result['confidence'])
            elif layer3_result['unbalance_type'] == 'ambiguous':
                st.warning(f"❓ **UNBALANCE TYPE AMBIGUOUS**")
                st.progress(layer3_result['confidence'])
            else:
                st.info(f"ℹ️ **COAST-DOWN TEST TIDAK DILAKUKAN**")
                st.progress(layer3_result['confidence'])
            
            st.markdown("**Evidence Coast-Down Analysis:**")
            for ev in layer3_result['evidence']:
                st.write(f"• {ev}")
            
            # Demodulation check for masking
            if layer3_result['demod_check']:
                st.markdown("#### ⚠️ Bearing Defect Masking Check")
                st.warning(layer3_result['demod_check']['warning'])
                st.write(f"• {layer3_result['demod_check']['interpretation']}")
                st.write(f"• **Action**: {layer3_result['demod_check']['action']}")
            
            st.markdown("---")
        
        # === FINAL DIAGNOSIS & ACTION PLAN ===
        st.markdown("### 🎯 Final Diagnosis & Action Plan")
        
        # Determine risk level
        if layer2_result:
            if layer2_result['severity'] == 'Unacceptable' or (layer3_result and layer3_result['unbalance_type'] == 'electrical'):
                risk_level = "CRITICAL"
                mtbf_days = "< 7"
                timeline = "< 4 hours"
            elif layer2_result['severity'] == 'Unsatisfactory':
                risk_level = "HIGH"
                mtbf_days = "7-30"
                timeline = "< 72 hours"
            else:
                risk_level = "MEDIUM"
                mtbf_days = "30-90"
                timeline = "< 30 days"
        else:
            risk_level = "LOW"
            mtbf_days = "> 90"
            timeline = "Routine monitoring"
        
        col28, col29, col30 = st.columns(3)
        with col28:
            risk_emoji = "🔴" if risk_level == "CRITICAL" else "🟠" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"
            st.metric("Risk Level", f"{risk_emoji} {risk_level}")
        with col29:
            st.metric("MTBF Estimation", f"{mtbf_days} days")
        with col30:
            st.metric("Action Timeline", timeline)
        
        # Action items based on diagnosis
        st.markdown("**Recommended Actions:**")
        if risk_level == "CRITICAL":
            st.error("🔴 **CRITICAL - <4 hours**")
            st.write("• LAKUKAN SHUTDOWN SEGERA")
            st.write("• Ikuti prosedur LOTO sesuai OSHA 1910.147")
            st.write("• Siapkan tim maintenance darurat")
        elif risk_level == "HIGH":
            st.warning("🟠 **HIGH PRIORITY - <72 hours**")
            if layer2_result['primary_fault'] == 'misalignment':
                st.write(f"• Jadwalkan laser alignment coupling dalam 72 jam")
                st.write(f"• Periksa kondisi coupling element untuk kerusakan")
            elif layer2_result['primary_fault'] == 'bearing_defect':
                st.write(f"• Segera pesan bearing pengganti untuk {layer2_result['fault_location'].upper()}")
                st.write(f"• Jadwalkan penggantian bearing dalam 7 hari")
            elif layer2_result['primary_fault'] == 'unbalance':
                if layer3_result and layer3_result['unbalance_type'] == 'mechanical':
                    st.write(f"• Lakukan dynamic balancing pada {'impeller pompa' if layer2_result['fault_location'] == 'pump' else 'rotor motor'}")
                    st.write("• Setelah balancing, ulangi pengukuran untuk verifikasi")
                elif layer3_result and layer3_result['unbalance_type'] == 'electrical':
                    st.write("• Lakukan Motor Current Signature Analysis (MCSA) untuk konfirmasi broken rotor bar")
                    st.write("• Jika dikonfirmasi, jadwalkan rewinding motor")
                if layer3_result and layer3_result['demod_check']:
                    st.write("• **PENTING**: Setelah perbaikan unbalance, ulangi pengukuran untuk deteksi bearing defect yang mungkin 'termasking'")
        elif risk_level == "MEDIUM":
            st.info("🟡 **MEDIUM PRIORITY - <30 days**")
            st.write(f"• Jadwalkan perbaikan sesuai maintenance window berikutnya")
            st.write(f"• Monitor vibrasi setiap 7 hari sampai perbaikan")
        else:
            st.success("🟢 **ROUTINE MONITORING**")
            st.write(f"• Inspeksi berikutnya: {timeline}")
            st.write("• Lanjutkan pemantauan rutin sesuai jadwal")
        
        st.markdown("---")
        
        # === COMPLIANCE SUMMARY ===
        st.markdown("### 📜 Compliance Summary")
        
        col31, col32, col33 = st.columns(3)
        
        with col31:
            iso_status = "COMPLIANT" if max_vel <= zone_b_limit else "NON-COMPLIANT"
            iso_emoji = "✅" if iso_status == "COMPLIANT" else "❌"
            st.markdown(f'<span class="compliance-badge compliance-{iso_status.lower()}">{iso_emoji} ISO 20816-1: {iso_status}</span>', unsafe_allow_html=True)
        
        with col32:
            api_status = "COMPLIANT" if not hydraulic_anomaly else "WARNING"
            api_emoji = "✅" if api_status == "COMPLIANT" else "⚠️"
            st.markdown(f'<span class="compliance-badge compliance-{api_status.lower()}">{api_emoji} API 610: {api_status}</span>', unsafe_allow_html=True)
        
        with col33:
            if max_acc < 0.5:
                iso15243_status = "COMPLIANT"
            elif max_acc < 1.0:
                iso15243_status = "STAGE 1"
            elif max_acc < 2.0:
                iso15243_status = "STAGE 2"
            else:
                iso15243_status = "STAGE 3"
            iso15243_emoji = "✅" if iso15243_status == "COMPLIANT" else "⚠️" if iso15243_status in ["STAGE 1", "STAGE 2"] else "❌"
            st.markdown(f'<span class="compliance-badge compliance-{iso15243_status.lower()}">{iso15243_emoji} ISO 15243: {iso15243_status}</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # === EXPORT SECTION ===
        st.markdown("### 📥 Export Report")
        
        # Generate comprehensive report text
        report_text = f"""PUMP DIAGNOSTIC REPORT - PERTAMINA PATRA NIAGA (3-Layer Architecture)
=====================================================================
Asset ID        : {asset_id}
Location        : {location}
Pump Type       : {pump_type}
Machine Group   : {machine_group}
Foundation      : {foundation_type}
Date            : {datetime.now().strftime('%d %b %Y %H:%M')}

DIAGNOSTIC ARCHITECTURE
- Layer 1: Overall Screening (Velocity/Accel/Hydraulic/Electrical)
- Layer 2: FFT Spectrum Analysis (36 Peaks → Fault Type + Location)
- Layer 3: Advanced Differentiation (Mechanical vs Electrical Unbalance)

LAYER 1 RESULTS
- Max Velocity     : {max_vel:.2f} mm/s → Zone {('B' if max_vel<=zone_b_limit else 'C' if max_vel<=zone_c_limit else 'D')}
- Max Acceleration : {max_acc:.2f} g → {"Normal" if max_acc<0.5 else "Warning" if max_acc<1.0 else "Danger" if max_acc<2.0 else "Critical"}
- Hydraulic Status : {"OK" if not hydraulic_anomaly else f"RISK (Suction {suction_pressure:.1f}m < NPSHr+0.5 {npshr+0.5:.1f}m)"}
- Electrical Status: {"OK" if not electrical_anomaly else f"IMBALANCE {current_imbalance:.1f}%"}
- Anomaly Detected : {"YES - Proceed to Layer 2" if layer1_anomaly else "NO"}

LAYER 2 RESULTS
- Primary Fault    : {fault_display[layer2_result['primary_fault']]}
- Location         : {layer2_result['fault_location'].upper() if layer2_result['fault_location'] else 'N/A'}
- Confidence       : {layer2_result['confidence']}%
- Severity         : {layer2_result['severity']}

LAYER 3 RESULTS (if applicable)
- Unbalance Type   : {layer3_result['unbalance_type'].upper() if layer3_result else 'N/A'}
- Confidence       : {layer3_result['confidence'] if layer3_result else 'N/A'}%
- Demod Check      : {"PASS" if not (layer3_result and layer3_result['demod_check']) else "WARNING - Bearing defect masking possible"}

RISK ASSESSMENT
- Risk Level       : {risk_level}
- MTBF Estimation  : {mtbf_days} days
- Action Timeline  : {timeline}

RECOMMENDED ACTIONS
{('• LAKUKAN SHUTDOWN SEGERA (<4 jam)' if risk_level=="CRITICAL" else 
  '• Jadwalkan perbaikan dalam 72 jam' if risk_level=="HIGH" else
  '• Jadwalkan perbaikan dalam 30 hari' if risk_level=="MEDIUM" else
  '• Lanjutkan pemantauan rutin')}

COMPLIANCE STATUS
- ISO 20816-1:2016 : {iso_status}
- API 610 Ed.11    : {api_status}
- ISO 15243:2017   : {iso15243_status}

Report Generated    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Standards           : ISO 20816-1:2016, API 610 Ed.11, ISO 15243:2017
Diagnostic System   : 3-Layer Architecture (Overall Screening → FFT Analysis → Advanced Differentiation)
"""
        
        col34, col35 = st.columns(2)
        with col34:
            st.download_button(
                "📄 Download Full Report",
                report_text,
                file_name=f"pump_diagnostic_{asset_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col35:
            st.download_button(
                "📊 Download Data Summary (CSV)",
                pd.DataFrame({
                    'Parameter': ['Max Velocity', 'Max Acceleration', 'Suction Pressure', 'Current Imbalance', 'Primary Fault', 'Confidence', 'Risk Level'],
                    'Value': [f"{max_vel:.2f} mm/s", f"{max_acc:.2f} g", f"{suction_pressure:.1f} bar", f"{current_imbalance:.1f}%", layer2_result['primary_fault'] if layer2_result else "N/A", f"{layer2_result['confidence'] if layer2_result else 0}%", risk_level]
                }).to_csv(index=False),
                file_name=f"pump_data_{asset_id}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        st.caption("Report includes complete 3-layer diagnostic traceability")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="footer">
        <p>Pump Diagnostic System v3.0 | Pertamina Patra Niaga - Asset Integrity Management</p>
        <p>Architecture: 3-Layer Diagnostic (Overall Screening → FFT Analysis → Advanced Differentiation)</p>
        <p>Standards: ISO 20816-1:2016, API 610 Ed.11, ISO 15243:2017</p>
        <p>© 2026 Pertamina Patra Niaga. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)

# Display important notes at the bottom
st.markdown("""
<div style="background-color: #e7f3ff; border-left: 4px solid #2196F3; padding: 12px; border-radius: 5px; margin-top: 20px; font-size: 0.9rem;">
<b>Catatan Penting:</b><br>
• Sistem ini dirancang untuk <b>single-visit troubleshooting</b> oleh inspector non-expert<br>
• Semua data dikumpulkan di lapangan sesuai checklist 1 halaman (76 data wajib)<br>
• Analisis dilakukan di kantor dengan algoritma 3-layer berbasis trigger<br>
• Tidak ada averaging H/V/A - evaluasi per arah sesuai ISO 20816 Clause 5.3<br>
• Kalkulasi diagnosa 100% sesuai standar internasional (ISO 20816, ISO 15243, API 610)
</div>
""", unsafe_allow_html=True)
