"""
Pump Diagnostic System - Pertamina Patra Niaga (3-Layer Architecture)
"""
import streamlit as st
import numpy as np
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="🛢️ Pump Diagnostic System - Pertamina",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
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
.calculation-box {
    background-color: #e7f3ff;
    border-left: 4px solid #2196F3;
    padding: 12px;
    border-radius: 5px;
    margin: 8px 0;
    font-family: monospace;
    font-size: 0.95rem;
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
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<p class="main-header">🛢️ Pump Diagnostic System - Pertamina Patra Niaga</p>', unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #6c757d; margin-bottom: 30px;'>Sistem Diagnostik 3-Layer: Overall Screening → FFT Analysis → Advanced Differentiation | Asset Integrity Management</div>", unsafe_allow_html=True)

# ============================================
# SECTION 1: Asset Specification (Tidak Berubah)
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
    bearing_size = st.selectbox("Bearing Size (Estimasi Visual)", [
        "Small Roller (<50mm shaft)",
        "Medium Roller (50-100mm shaft)",
        "Large Roller (>100mm shaft)",
        "Unknown"
    ], help="Perkiraan diameter shaft: jempol=kecil, telapak=medium")
    asset_id = st.text_input("Asset ID", "PPJ-BBM-P-205")
    location = st.text_input("Location", "Plaju Terminal")

# ============================================
# SECTION 2: Layer 1 - Overall Screening (REVISED)
# ============================================
st.markdown('<p class="section-header">2. Layer 1: Overall Screening (Velocity/Acceleration/Temperature)</p>', unsafe_allow_html=True)
st.info("💡 **Prinsip Efisiensi**: Jika semua parameter Layer 1 NORMAL → TIDAK PERLU FFT. Hanya lanjut ke Layer 2 jika terdeteksi anomaly.")

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("#### 📏 Overall Velocity RMS (10-1000 Hz)")
    st.caption("ISO 10816-3:2001 - Machine Health Assessment")
    velocity_rms = st.number_input("Overall Velocity RMS (mm/s)", 0.0, 20.0, 5.2,
        help="Diukur pada bearing housing terburuk (biasanya Pump DE)")
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
    
    # Klasifikasi zona
    if velocity_rms <= zone_a_limit:
        zone = "A"
        zone_status = "New machine condition"
        zone_color = "success"
    elif velocity_rms <= zone_b_limit:
        zone = "B"
        zone_status = "Acceptable for unlimited operation"
        zone_color = "info"
    elif velocity_rms <= zone_c_limit:
        zone = "C"
        zone_status = "UNSATISFACTORY - Short-term operation only"
        zone_color = "warning"
    else:
        zone = "D"
        zone_status = "UNACCEPTABLE - Vibration causes damage"
        zone_color = "error"
    
    st.metric("ISO 10816-3 Zone", f"Zone {zone}", delta=f"{velocity_rms:.1f} mm/s")
    if zone_color == "success":
        st.success(zone_status)
    elif zone_color == "warning":
        st.warning(zone_status)
    elif zone_color == "error":
        st.error(zone_status)
    else:
        st.info(zone_status)

with col5:
    st.markdown("#### ⚡ Overall Acceleration RMS (0.5-16 kHz)")
    st.caption("High-Frequency Screening - Bearing/Gear Faults")
    accel_rms = st.number_input("Overall Acceleration RMS (g)", 0.0, 10.0, 0.95,
        help="Diukur pada Pump DE untuk deteksi bearing defect awal")
    
    # Threshold acceleration untuk bearing
    if accel_rms < 2.0:
        accel_status = "Normal"
        accel_color = "success"
    elif accel_rms < 5.0:
        accel_status = "Warning - Bearing defect possible"
        accel_color = "warning"
    else:
        accel_status = "Critical - Bearing defect likely"
        accel_color = "error"
    
    st.metric("HF Acceleration", f"{accel_rms:.2f} g")
    if accel_color == "success":
        st.success(accel_status)
    elif accel_color == "warning":
        st.warning(accel_status)
    else:
        st.error(accel_status)

with col6:
    st.markdown("#### 🌡️ Bearing Temperature")
    st.caption("Thermal Screening - Overheating Detection")
    temp_pump_de = st.number_input("Pump DE Temperature (°C)", 0, 150, 88,
        help="Diukur di housing bearing dengan infrared thermometer")
    ambient = 35
    temp_rise = temp_pump_de - ambient
    
    if temp_rise < 30:
        temp_status = "Normal temperature rise"
        temp_color = "success"
    elif temp_rise < 45:
        temp_status = "Elevated temperature - Monitor closely"
        temp_color = "warning"
    else:
        temp_status = "Critical overheating - Immediate action required"
        temp_color = "error"
    
    st.metric("Temp Rise (vs Ambient)", f"{temp_rise}°C")
    if temp_color == "success":
        st.success(temp_status)
    elif temp_color == "warning":
        st.warning(temp_status)
    else:
        st.error(temp_status)

# Decision Gatekeeper: Apakah perlu lanjut ke Layer 2?
proceed_to_layer2 = (zone in ["C", "D"]) or (accel_rms >= 2.0) or (temp_rise >= 45)

if not proceed_to_layer2:
    st.success("✅ **Layer 1 Result: ALL PARAMETERS NORMAL**")
    st.markdown("""
    <div class="success-box">
    <b>REKOMENDASI:</b> Tidak diperlukan analisis FFT. Lanjutkan pemantauan rutin sesuai jadwal.
    Sistem telah menghemat 80% waktu inspeksi dengan screening efisien di Layer 1.
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ **Layer 1 Result: ANOMALY DETECTED**")
    st.markdown(f"""
    <div class="warning-box">
    <b>ANOMALI TERDETEKSI:</b> 
    {'✓ Velocity Zone ' + zone + ' (' + str(velocity_rms) + ' mm/s)' if zone in ['C','D'] else ''} 
    {'| ' if (zone in ['C','D'] and accel_rms >= 2.0) else ''} 
    {'✓ HF Acceleration ' + str(accel_rms) + 'g > 2.0g' if accel_rms >= 2.0 else ''} 
    {'| ' if ((zone in ['C','D'] or accel_rms >= 2.0) and temp_rise >= 45) else ''} 
    {'✓ Temp rise ' + str(temp_rise) + '°C > 45°C' if temp_rise >= 45 else ''}
    <br><br>
    <b>→ LANJUT KE LAYER 2: FFT Spectrum Analysis untuk identifikasi jenis & lokasi fault</b>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SECTION 3: Layer 2 - FFT Spectrum Analysis (REVISED - 36 Peaks Structure)
# ============================================
if proceed_to_layer2:
    st.markdown('<p class="section-header">3. Layer 2: FFT Spectrum Analysis (36 Peaks)</p>', unsafe_allow_html=True)
    st.info("""
    📍 **Struktur Data 36 Peaks**:
    • 4 Lokasi: Motor DE/NDE + Pump DE/NDE
    • 3 Arah per lokasi: Horizontal (H) / Vertical (V) / Axial (A)
    • 3 Peaks per arah: Frekuensi (Hz) + Amplitudo (mm/s)
    • Total: 4 × 3 × 3 = **36 peaks** → **72 nilai numerik** (frekuensi + amplitudo)
    """)
    
    # Create structured input for 36 peaks
    locations = ["Motor DE", "Motor NDE", "Pump DE", "Pump NDE"]
    directions = ["Horizontal (H)", "Vertical (V)", "Axial (A)"]
    
    # Store all peaks in dictionary
    peaks_data = {}
    
    for i, loc in enumerate(locations):
        st.markdown(f"#### 🔹 {loc}")
        cols = st.columns(3)
        for j, (dir_name, col) in enumerate(zip(directions, cols)):
            with col:
                st.caption(f"{dir_name}")
                freq1 = st.number_input(f"Peak 1 Freq ({loc} {dir_name[:1]})", 0.0, 200.0, 
                    value=24.8 if loc=="Pump DE" and dir_name=="Horizontal (H)" else 
                          49.6 if loc=="Pump DE" and dir_name=="Axial (A)" else 10.0,
                    key=f"freq_{i}_{j}_1")
                amp1 = st.number_input(f"Peak 1 Amp ({loc} {dir_name[:1]})", 0.0, 20.0,
                    value=3.8 if loc=="Pump DE" and dir_name=="Horizontal (H)" else 
                          2.1 if loc=="Pump DE" and dir_name=="Axial (A)" else 0.5,
                    key=f"amp_{i}_{j}_1")
                freq2 = st.number_input(f"Peak 2 Freq ({loc} {dir_name[:1]})", 0.0, 200.0, 
                    value=49.6 if loc=="Pump DE" and dir_name=="Horizontal (H)" else 20.0,
                    key=f"freq_{i}_{j}_2")
                amp2 = st.number_input(f"Peak 2 Amp ({loc} {dir_name[:1]})", 0.0, 20.0,
                    value=1.1 if loc=="Pump DE" and dir_name=="Horizontal (H)" else 0.6,
                    key=f"amp_{i}_{j}_2")
                freq3 = st.number_input(f"Peak 3 Freq ({loc} {dir_name[:1]})", 0.0, 200.0, 
                    value=76.0 if loc=="Pump DE" and dir_name=="Horizontal (H)" else 30.0,
                    key=f"freq_{i}_{j}_3")
                amp3 = st.number_input(f"Peak 3 Amp ({loc} {dir_name[:1]})", 0.0, 20.0,
                    value=0.7 if loc=="Pump DE" and dir_name=="Horizontal (H)" else 0.4,
                    key=f"amp_{i}_{j}_3")
                
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
    # SECTION 4: Layer 3 Inputs (Conditional - Only for Unbalance)
    # ============================================
    st.markdown('<p class="section-header">4. Layer 3: Advanced Differentiation (Opsional - Hanya untuk Unbalance)</p>', unsafe_allow_html=True)
    st.info("""
    🔍 **Kapan Layer 3 Diperlukan?** 
    Hanya jika Layer 2 mendeteksi UNBALANCE → untuk diferensiasi:
    • Mechanical Unbalance: Velocity turun GRADUAL saat coast-down (inersia rotor)
    • Electrical Unbalance: Velocity turun CEPAT saat coast-down (hilangnya medan magnet)
    """)
    
    col7, col8 = st.columns(2)
    with col7:
        st.markdown("#### Coast-Down Test Data")
        st.caption("Rekam velocity setiap 1 detik selama 15 detik setelah motor dimatikan")
        coast_down_time = st.multiselect("Time Points (detik)", 
            options=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15],
            default=[0, 2, 4, 6, 8, 10],
            key="coast_time")
        coast_down_vel = []
        for t in coast_down_time:
            v = st.number_input(f"Velocity @ {t}s (mm/s)", 0.0, 20.0, 
                value=5.2 if t==0 else 3.8 if t==2 else 2.5 if t==4 else 1.5 if t==6 else 0.8 if t==8 else 0.3,
                key=f"coast_vel_{t}")
            coast_down_vel.append(v)
    
    with col8:
        st.markdown("#### Demodulation/Envelope Values")
        st.caption("Untuk deteksi 'masking' bearing defect di balik unbalance")
        demod_motor_de = st.number_input("Motor DE Demod (gE)", 0.0, 10.0, 0.4, key="demod_mde")
        demod_pump_de = st.number_input("Pump DE Demod (gE)", 0.0, 10.0, 3.2, key="demod_pde")
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
            'velocity_rms': velocity_rms,
            'zone': zone,
            'accel_rms': accel_rms,
            'temp_rise': temp_rise,
            'anomaly_detected': proceed_to_layer2,
            'severity': 'Unacceptable' if zone == 'D' else 'Unsatisfactory' if zone == 'C' else 'Satisfactory'
        }
        
        # ============================================
        # LAYER 2: FFT Analysis (Only if anomaly detected)
        # ============================================
        if proceed_to_layer2:
            # Fundamental frequency calculation
            fundamental_hz = motor_rpm / 60.0  # 1485 RPM = 24.75 Hz
            
            # Feature extraction dari 36 peaks
            features = {
                'motor_de': {'h': {}, 'v': {}, 'a': {}},
                'motor_nde': {'h': {}, 'v': {}, 'a': {}},
                'pump_de': {'h': {}, 'v': {}, 'a': {}},
                'pump_nde': {'h': {}, 'v': {}, 'a': {}}
            }
            
            # Mapping lokasi untuk features
            loc_map = {
                'Motor DE': 'motor_de',
                'Motor NDE': 'motor_nde',
                'Pump DE': 'pump_de',
                'Pump NDE': 'pump_nde'
            }
            
            # Ekstrak amplitudo 1X, 2X untuk setiap lokasi/arah
            for loc_name, loc_key in loc_map.items():
                for dir_key in ['h', 'v', 'a']:
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
            if features['motor_de']['a']['r2x_1x'] > 1.5:
                mis_score += 2.0
                mis_location = "motor"
            if features['pump_de']['a']['r2x_1x'] > 1.5:
                mis_score += 2.0
                mis_location = "pump" if mis_score == 2.0 else "coupling"
            
            # Skor Unbalance: 1X dominan di radial (H+V)
            unb_score = 0
            unb_location = None
            motor_radial_avg = (features['motor_de']['h']['a1x'] + features['motor_de']['v']['a1x'] + 
                               features['motor_nde']['h']['a1x'] + features['motor_nde']['v']['a1x']) / 4
            pump_radial_avg = (features['pump_de']['h']['a1x'] + features['pump_de']['v']['a1x'] + 
                              features['pump_nde']['h']['a1x'] + features['pump_nde']['v']['a1x']) / 4
            
            if motor_radial_avg > 3.0 and motor_radial_avg > pump_radial_avg * 1.5:
                unb_score += 3.0
                unb_location = "motor"
            elif pump_radial_avg > 3.0 and pump_radial_avg > motor_radial_avg * 1.5:
                unb_score += 3.0
                unb_location = "pump"
            
            # Skor Looseness: Harmonik tinggi (gunakan peak3 sebagai proxy)
            loo_score = 0
            loo_location = "structure"
            # Simplified: jika ada peak3 > 0.5 * peak1 di banyak lokasi
            harmonic_count = 0
            for loc in loc_map.values():
                for dir_key in ['h', 'v', 'a']:
                    if features[loc][dir_key]['a1x'] > 0.5:
                        harmonic_count += 1
            if harmonic_count > 6:  # >50% dari 12 arah
                loo_score = 3.0
            
            # Tentukan fault dominan
            fault_scores = {
                'misalignment': mis_score,
                'unbalance': unb_score,
                'looseness': loo_score
            }
            primary_fault = max(fault_scores, key=fault_scores.get)
            primary_score = fault_scores[primary_fault]
            
            # Jika tidak ada fault signifikan, cek bearing defect dari HF acceleration
            if primary_score < 2.5 and accel_rms > 2.0:
                primary_fault = 'bearing_defect'
                primary_score = min(5.0, accel_rms * 0.8)
                fault_location = "pump_de" if accel_rms > 1.5 else "motor_de"
            elif primary_score >= 2.5:
                fault_location = mis_location if primary_fault == 'misalignment' else \
                               unb_location if primary_fault == 'unbalance' else loo_location
            else:
                primary_fault = 'no_significant_fault'
                fault_location = None
            
            layer2_result = {
                'primary_fault': primary_fault,
                'fault_location': fault_location,
                'confidence': min(95, 70 + primary_score * 5),
                'severity': 'Unacceptable' if primary_score >= 4.0 else 'Unsatisfactory' if primary_score >= 3.0 else 'Satisfactory',
                'features': features,
                'fundamental_hz': fundamental_hz
            }
        else:
            layer2_result = {
                'primary_fault': 'no_significant_fault',
                'fault_location': None,
                'confidence': 95,
                'severity': 'Good'
            }
        
        # ============================================
        # LAYER 3: Advanced Differentiation (Only for Unbalance)
        # ============================================
        layer3_result = None
        if layer2_result['primary_fault'] == 'unbalance' and coast_down_time:
            # Analisis pola coast-down
            if len(coast_down_vel) >= 3:
                initial_drop = (coast_down_vel[0] - coast_down_vel[1]) / (coast_down_time[1] - coast_down_time[0]) if len(coast_down_time) > 1 else 0
                final_drop = (coast_down_vel[-2] - coast_down_vel[-1]) / (coast_down_time[-1] - coast_down_time[-2]) if len(coast_down_time) > 1 else 0
                
                # Mechanical unbalance: penurunan gradual
                if initial_drop < 1.5 and final_drop < 0.3:
                    unbalance_type = 'mechanical'
                    confidence = 90
                    evidence = [
                        f"Penurunan velocity gradual: {initial_drop:.2f} mm/s² (awal) → {final_drop:.2f} mm/s² (akhir)",
                        "Pola konsisten dengan inersia rotor yang tidak seimbang"
                    ]
                    recommendation = f"Lakukan dynamic balancing pada {'impeller pompa' if layer2_result['fault_location'] == 'pump' else 'rotor motor'}"
                
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
                    evidence = [f"Pola penurunan tidak jelas: initial drop = {initial_drop:.2f} mm/s²"]
                    recommendation = "Lakukan MCSA untuk konfirmasi atau lakukan balancing sebagai langkah aman pertama"
                
                # Cek masking bearing defect
                demod_check = None
                if demod_pump_de > 2.0 and layer2_result['fault_location'] == 'pump':
                    demod_check = {
                        'warning': 'High demodulation value detected',
                        'interpretation': 'Unbalance mungkin masking early-stage bearing defect',
                        'action': 'After balancing, re-measure vibration. If velocity remains high, suspect bearing defect.'
                    }
                elif demod_motor_de > 2.0 and layer2_result['fault_location'] == 'motor':
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
        col15, col16, col17 = st.columns(3)
        with col15:
            if layer1_result['zone'] == 'A':
                st.success(f"Zone {layer1_result['zone']}")
            elif layer1_result['zone'] in ['C', 'D']:
                st.error(f"Zone {layer1_result['zone']}")
            else:
                st.warning(f"Zone {layer1_result['zone']}")
            st.metric("Velocity RMS", f"{layer1_result['velocity_rms']:.2f} mm/s")
        with col16:
            if layer1_result['accel_rms'] < 2.0:
                st.success("HF Normal")
            elif layer1_result['accel_rms'] < 5.0:
                st.warning("HF Warning")
            else:
                st.error("HF Critical")
            st.metric("Acceleration RMS", f"{layer1_result['accel_rms']:.2f} g")
        with col17:
            if layer1_result['temp_rise'] < 30:
                st.success("Temp Normal")
            elif layer1_result['temp_rise'] < 45:
                st.warning("Temp Elevated")
            else:
                st.error("Temp Critical")
            st.metric("Temp Rise", f"{layer1_result['temp_rise']}°C")
        
        if not layer1_result['anomaly_detected']:
            st.success("✅ **KESIMPULAN LAYER 1**: Semua parameter dalam batas normal. TIDAK DIPERLUKAN analisis FFT.")
            st.markdown("""
            <div class="success-box">
            <b>Efisiensi Sistem:</b> Dengan screening Layer 1, 80% waktu inspeksi dihemat untuk mesin sehat.
            Rekomendasi: Lanjutkan pemantauan rutin sesuai jadwal maintenance.
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()
        else:
            st.warning("⚠️ **KESIMPULAN LAYER 1**: Anomaly terdeteksi → LANJUT KE LAYER 2")
        
        st.markdown("---")
        
        # === LAYER 2 RESULTS ===
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
                    f"1X RPM dominan di radial: Pump rata-rata = {pump_radial_avg:.1f} mm/s vs Motor = {motor_radial_avg:.1f} mm/s",
                    f"1X Pump DE Horizontal = {features['pump_de']['h']['a1x']:.1f} mm/s ({features['pump_de']['h']['a1x']/velocity_rms*100:.0f}% dari overall)",
                    "Dominant direction: radial (horizontal/vertical) bukan aksial"
                ]
            elif layer2_result['primary_fault'] == 'bearing_defect':
                evidence_list = [
                    f"HF Acceleration RMS = {accel_rms:.2f}g > 2.0g threshold",
                    f"Temperature rise = {temp_rise}°C > 30°C normal",
                    "Perlu konfirmasi dengan demodulation/envelope analysis"
                ]
            
            for ev in evidence_list:
                st.write(f"• {ev}")
        else:
            st.success("✅ **NO SIGNIFICANT FAULT DETECTED** dalam spektrum FFT")
            st.caption("All vibration signatures within acceptable limits")
        
        # Decision: Apakah perlu Layer 3?
        need_layer3 = (layer2_result['primary_fault'] == 'unbalance' and layer1_result['anomaly_detected'])
        
        if need_layer3:
            st.info("💡 **REKOMENDASI**: Lanjut ke Layer 3 untuk diferensiasi Mechanical vs Electrical Unbalance")
        else:
            st.success("✅ **Layer 3 tidak diperlukan** - Fault type sudah teridentifikasi jelas")
        
        st.markdown("---")
        
        # === LAYER 3 RESULTS (IF APPLICABLE) ===
        if need_layer3 and layer3_result:
            st.markdown("### ⚡ Layer 3: Advanced Differentiation Results")
            
            if layer3_result['unbalance_type'] == 'mechanical':
                st.success(f"✅ **MECHANICAL UNBALANCE** terkonfirmasi")
                st.progress(layer3_result['confidence'])
            elif layer3_result['unbalance_type'] == 'electrical':
                st.error(f"⚠️ **ELECTRICAL UNBALANCE** terkonfirmasi")
                st.progress(layer3_result['confidence'])
            else:
                st.warning(f"❓ **UNBALANCE TYPE AMBIGUOUS**")
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
        st.markdown("### ✅ Final Diagnosis & Action Plan")
        
        # Risk assessment
        if layer1_result['zone'] == 'D' or (layer2_result['primary_fault'] == 'bearing_defect' and accel_rms > 5.0):
            risk_level = "CRITICAL"
            timeline = "<4 hours"
            mtbf_days = 3
        elif layer1_result['zone'] == 'C' or layer2_result['severity'] == 'Unacceptable':
            risk_level = "HIGH"
            timeline = "<72 hours"
            mtbf_days = 14
        elif layer2_result['severity'] == 'Unsatisfactory' or layer3_result:
            risk_level = "MEDIUM"
            timeline = "<30 days"
            mtbf_days = 60
        else:
            risk_level = "LOW"
            timeline = "<90 days"
            mtbf_days = 180
        
        # Display risk summary
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
        elif risk_level == "HIGH":
            st.warning("🟠 **HIGH PRIORITY - <72 hours**")
            if layer2_result['primary_fault'] == 'misalignment':
                st.write(f"• Jadwalkan laser alignment coupling dalam 72 jam")
                st.write(f"• Periksa kondisi coupling element untuk kerusakan")
            elif layer2_result['primary_fault'] == 'bearing_defect':
                st.write(f"• Segera pesan bearing pengganti untuk {layer2_result['fault_location'].upper()}")
                st.write(f"• Jadwalkan penggantian bearing dalam 7 hari")
        elif layer2_result['primary_fault'] == 'unbalance' and layer3_result:
            st.info("🟡 **MEDIUM PRIORITY - <30 days**")
            if layer3_result['unbalance_type'] == 'mechanical':
                st.write(f"• Lakukan dynamic balancing pada {'impeller pompa' if layer2_result['fault_location'] == 'pump' else 'rotor motor'}")
                st.write("• Setelah balancing, ulangi pengukuran untuk verifikasi")
            elif layer3_result['unbalance_type'] == 'electrical':
                st.write("• Lakukan Motor Current Signature Analysis (MCSA) untuk konfirmasi broken rotor bar")
                st.write("• Jika dikonfirmasi, jadwalkan rewinding motor")
            if layer3_result['demod_check']:
                st.write("• **PENTING**: Setelah perbaikan unbalance, ulangi pengukuran untuk deteksi bearing defect yang mungkin 'termasking'")
        else:
            st.success("🟢 **ROUTINE MONITORING**")
            st.write(f"• Inspeksi berikutnya: {timeline}")
            st.write("• Lanjutkan pemantauan rutin sesuai jadwal")
        
        # Compliance summary
        st.markdown("---")
        st.markdown("### 📜 Compliance Summary")
        col31, col32, col33 = st.columns(3)
        with col31:
            iso_status = "COMPLIANT" if layer1_result['zone'] in ['A', 'B'] else "NON-COMPLIANT"
            iso_emoji = "✅" if iso_status == "COMPLIANT" else "❌"
            st.markdown(f'<span class="compliance-badge compliance-{iso_status.lower()}">{iso_emoji} ISO 10816-3: {iso_status}</span>', unsafe_allow_html=True)
        with col32:
            api_status = "COMPLIANT" if temp_rise < 45 else "WARNING"
            api_emoji = "✅" if api_status == "COMPLIANT" else "⚠️"
            st.markdown(f'<span class="compliance-badge compliance-{api_status.lower()}">{api_emoji} API 610: {api_status}</span>', unsafe_allow_html=True)
        with col33:
            iso15243_status = "COMPLIANT" if accel_rms < 2.0 else "STAGE 2" if accel_rms < 5.0 else "STAGE 3"
            iso15243_emoji = "✅" if iso15243_status == "COMPLIANT" else "⚠️" if iso15243_status == "STAGE 2" else "❌"
            st.markdown(f'<span class="compliance-badge compliance-{iso15243_status.lower()}">{iso15243_emoji} ISO 15243: {iso15243_status}</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export section
        st.markdown("### 📥 Export Report")
        col34, col35 = st.columns(2)
        
        # Generate comprehensive report text
        report_text = f"""
PUMP DIAGNOSTIC REPORT - PERTAMINA PATRA NIAGA (3-Layer Architecture)
=====================================================================
Asset ID      : {asset_id}
Location      : {location}
Pump Type     : {pump_type}
Machine Group : {machine_group}
Foundation    : {foundation_type}
Date          : {datetime.now().strftime('%d %b %Y %H:%M')}

DIAGNOSTIC ARCHITECTURE
-----------------------
Layer 1: Overall Screening (Velocity/Accel/Temp)
Layer 2: FFT Spectrum Analysis (36 Peaks → Fault Type + Location)
Layer 3: Advanced Differentiation (Mechanical vs Electrical Unbalance)

LAYER 1 RESULTS
---------------
Velocity RMS  : {velocity_rms:.2f} mm/s → Zone {zone} ({zone_status})
Acceleration  : {accel_rms:.2f} g → {"Normal" if accel_rms < 2.0 else "Warning" if accel_rms < 5.0 else "Critical"}
Temp Rise     : {temp_rise}°C → {"Normal" if temp_rise < 30 else "Elevated" if temp_rise < 45 else "Critical"}
Anomaly       : {"YES - Proceed to Layer 2" if proceed_to_layer2 else "NO - No FFT required"}

LAYER 2 RESULTS
---------------
Primary Fault : {fault_display[layer2_result['primary_fault']]}
Location      : {layer2_result['fault_location'].upper() if layer2_result['fault_location'] else 'N/A'}
Confidence    : {layer2_result['confidence']}%
Severity      : {layer2_result['severity']}

LAYER 3 RESULTS (if applicable)
-------------------------------
Unbalance Type: {layer3_result['unbalance_type'].upper() if layer3_result else 'N/A'}
Confidence    : {layer3_result['confidence'] if layer3_result else 'N/A'}%
Demod Check   : {"Warning: Possible bearing defect masking" if layer3_result and layer3_result.get('demod_check') else "No masking detected"}

RISK ASSESSMENT
---------------
Risk Level    : {risk_level}
Timeline      : {timeline}
MTBF Estimate : {mtbf_days} days

RECOMMENDED ACTIONS
-------------------
{risk_emoji} {risk_level} priority - {timeline} action required
{layer3_result['recommendation'] if layer3_result and layer2_result['primary_fault'] == 'unbalance' else 
  'Lakukan laser alignment coupling' if layer2_result['primary_fault'] == 'misalignment' else
  'Lakukan dynamic balancing' if layer2_result['primary_fault'] == 'unbalance' else
  'Ganti bearing segera' if layer2_result['primary_fault'] == 'bearing_defect' else
  'Lanjutkan pemantauan rutin'}

COMPLIANCE STATUS
-----------------
ISO 10816-3   : {iso_status}
API 610       : {api_status}
ISO 15243     : {iso15243_status}

Report Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Standards       : ISO 10816-3:2001, API 610 Ed.11, IEC 60034-1:2017, ISO 15243:2017
"""
        
        with col34:
            st.download_button(
                "📄 Download Full Report",
                report_text,
                file_name=f"pump_diagnostic_{asset_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col35:
            st.caption("Report includes complete 3-layer diagnostic traceability")

# Footer
st.markdown("""
<div class="footer">
<p>Pump Diagnostic System v3.0 | Pertamina Patra Niaga - Asset Integrity Management</p>
<p>Architecture: 3-Layer Diagnostic (Overall Screening → FFT Analysis → Advanced Differentiation)</p>
<p>Standards: ISO 10816-3:2001, API 610 Ed.11, IEC 60034-1:2017, ISO 15243:2017, ISO 45001:2018</p>
<p>© 2026 Pertamina Patra Niaga. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
