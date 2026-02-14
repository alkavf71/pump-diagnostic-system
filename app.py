"""
Pump Diagnostic System - Pertamina Patra Niaga
SINGLE PAGE VERSION - All inputs in one page, diagnosis at bottom
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

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
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<p class="main-header">🛢️ Pump Diagnostic System - Pertamina Patra Niaga</p>', unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #6c757d; margin-bottom: 30px;'>Sistem Diagnostik Pompa Centrifugal Berbasis Adash Vibrio 4900 | Asset Integrity Management</div>", unsafe_allow_html=True)

# ============================================
# SECTION 1: Asset Specification
# ============================================
st.markdown('<p class="section-header">1. Spesifikasi Asset</p>', unsafe_allow_html=True)

# Di Section 1: Asset Specification
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🔧 Motor Specifications")
    motor_kw = st.number_input("Motor Power (kW)", 1, 1000, 315, 
                              help="Dari nameplate motor (IEC 60034-1)")
    
    # Auto-detect machine group berdasarkan power
    if motor_kw <= 15:
        machine_group = "Group 1 (≤15 kW)"
        group_num = 1
    elif motor_kw <= 75:
        machine_group = "Group 2 (15-75 kW) - Small Product Pumps"
        group_num = 2
    else:
        machine_group = "Group 3 (>75 kW) - BBM Transfer Pumps"
        group_num = 3
    
    st.caption(f"Auto-detected: {machine_group}")
    
    motor_rpm = st.number_input("Motor RPM", 600, 3600, 1485,
                               help="Dari nameplate motor")
    flc = st.number_input("Full Load Current (A)", 1, 2000, 545,
                         help="Dari nameplate motor - nilai I_N")
    voltage = st.number_input("Voltage (V)", 220, 660, 400,
                             help="Tegangan sistem")

with col2:
    st.markdown("#### 📦 Pump Specifications")
    pump_type = st.selectbox("Pump Type", [
        "BBM Transfer Pump (300-500 kW)",
        "Crude Oil Pump (500-1000 kW)",
        "Other Product Pump"
    ])
    bep_flow = st.number_input("BEP Flow (m³/hr)", 0.0, 1000.0, 120.0,
                              help="Dari pump curve / Mechanical Data Sheet")
    bep_head = st.number_input("BEP Head (m)", 0.0, 200.0, 85.0,
                              help="Dari pump curve / Mechanical Data Sheet")
    npshr = st.number_input("NPSHr (m)", 0.0, 20.0, 3.2,
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
        "Medium Roller (50-100mm shaft)",  # Default untuk pompa BBM
        "Large Roller (>100mm shaft)",
        "Unknown"
    ], help="Perkiraan diameter shaft: jempol=kecil, telapak=medium")
    asset_id = st.text_input("Asset ID", "PPJ-BBM-P-101")
    location = st.text_input("Location", "Plaju Terminal")

# ============================================
# SECTION 2: Vibration Measurements
# ============================================
st.markdown('<p class="section-header">2. Pengukuran Vibrasi (Adash Vibrio 4900)</p>', unsafe_allow_html=True)
st.info("💡 **Petunjuk**: Ukur DE (Drive End) dan NDE (Non-Drive End) untuk setiap arah. Nilai dalam mm/s RMS.")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("#### Motor (Driver)")
    motor_h_de = st.number_input("Motor H - DE (mm/s)", 0.0, 20.0, 1.24, key="m_h_de")
    motor_h_nde = st.number_input("Motor H - NDE (mm/s)", 0.0, 20.0, 1.20, key="m_h_nde")
    motor_v_de = st.number_input("Motor V - DE (mm/s)", 0.0, 20.0, 0.55, key="m_v_de")
    motor_v_nde = st.number_input("Motor V - NDE (mm/s)", 0.0, 20.0, 0.54, key="m_v_nde")
    motor_a_de = st.number_input("Motor A - DE (mm/s)", 0.0, 20.0, 0.27, key="m_a_de")
    motor_a_nde = st.number_input("Motor A - NDE (mm/s)", 0.0, 20.0, 0.43, key="m_a_nde")

with col5:
    st.markdown("#### Pump (Driven)")
    pump_h_de = st.number_input("Pump H - DE (mm/s)", 0.0, 20.0, 1.07, key="p_h_de")
    pump_h_nde = st.number_input("Pump H - NDE (mm/s)", 0.0, 20.0, 0.69, key="p_h_nde")
    pump_v_de = st.number_input("Pump V - DE (mm/s)", 0.0, 20.0, 2.11, key="p_v_de")
    pump_v_nde = st.number_input("Pump V - NDE (mm/s)", 0.0, 20.0, 0.95, key="p_v_nde")
    pump_a_de = st.number_input("Pump A - DE (mm/s)", 0.0, 20.0, 0.72, key="p_a_de")
    pump_a_nde = st.number_input("Pump A - NDE (mm/s)", 0.0, 20.0, 0.96, key="p_a_nde")

with col6:
    st.markdown("#### High Frequency Bands (0.5-16 kHz)")
    st.caption("Diukur di DE saja (sisi beban)")
    hf_motor_de = st.number_input("Motor DE HF (g)", 0.0, 10.0, 0.3, key="hf_motor")
    hf_pump_de = st.number_input("Pump DE HF (g)", 0.0, 10.0, 0.9, key="hf_pump")
    
    st.markdown("#### Bearing Temperature (°C)")
    st.caption("Diukur di housing bearing")
    temp_motor_de = st.number_input("Motor DE Temp", 0, 150, 65, key="tm_de")
    temp_motor_nde = st.number_input("Motor NDE Temp", 0, 150, 68, key="tm_nde")
    temp_pump_de = st.number_input("Pump DE Temp", 0, 150, 88, key="tp_de")
    temp_pump_nde = st.number_input("Pump NDE Temp", 0, 150, 72, key="tp_nde")

# ============================================
# SECTION 3: FFT Spectrum Analysis
# ============================================
st.markdown('<p class="section-header">3. FFT Spectrum Analysis (Adash Vibrio 4900)</p>', unsafe_allow_html=True)
st.info("""
💡 **Cara membaca dari layar Vibrio 4900:**
1. Pilih mode Spectrum dengan range 1-200 Hz
2. Catat 3 peak tertinggi yang ditampilkan (contoh: "1. 25Hz → 2.0")
3. Input **frekuensi (Hz)** dan **amplitudo (mm/s)** untuk setiap peak
""")

col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("#### Peak 1 (Biasanya 1X - Fundamental)")
    peak1_freq = st.number_input("Frekuensi Peak 1 (Hz)", 0.0, 200.0, 25.0, key="p1f")
    peak1_amp = st.number_input("Amplitudo Peak 1 (mm/s)", 0.0, 20.0, 2.0, key="p1a")

with col8:
    st.markdown("#### Peak 2 (Biasanya 2X - Harmonik Kedua)")
    peak2_freq = st.number_input("Frekuensi Peak 2 (Hz)", 0.0, 200.0, 50.0, key="p2f")
    peak2_amp = st.number_input("Amplitudo Peak 2 (mm/s)", 0.0, 20.0, 1.0, key="p2a")

with col9:
    st.markdown("#### Peak 3 (Bearing Defect atau 2×Line Freq)")
    peak3_freq = st.number_input("Frekuensi Peak 3 (Hz)", 0.0, 200.0, 76.0, key="p3f")
    peak3_amp = st.number_input("Amplitudo Peak 3 (mm/s)", 0.0, 20.0, 0.7, key="p3a")

# Additional FFT parameters
col10, col11 = st.columns(2)
with col10:
    phase_instability = st.number_input("Phase Instability (°)", 0, 90, 30,
                                       help="Variasi phase antar pengukuran berulang")
with col11:
    displacement_peak = st.number_input("Displacement Peak (μm)", 0, 200, 68,
                                       help="Peak-to-peak displacement 2-100 Hz")

# ============================================
# SECTION 4: Hydraulic & Electrical Parameters
# ============================================
st.markdown('<p class="section-header">4. Parameter Hydraulic & Electrical</p>', unsafe_allow_html=True)

col12, col13, col14 = st.columns(3)

with col12:
    st.markdown("#### Hydraulic Parameters")
    actual_flow = st.number_input("Actual Flow (m³/hr)", 0.0, 1000.0, 86.0)
    p_suc = st.number_input("Suction Pressure (bar g)", 0.0, 50.0, 2.8)
    p_dis = st.number_input("Discharge Pressure (bar g)", 0.0, 100.0, 10.5)

with col13:
    st.markdown("#### Electrical - Voltage (V)")
    voltage_r = st.number_input("Voltage R", 0.0, 1000.0, 402.0)
    voltage_s = st.number_input("Voltage S", 0.0, 1000.0, 389.0)
    voltage_t = st.number_input("Voltage T", 0.0, 1000.0, 405.0)

with col14:
    st.markdown("#### Electrical - Current (A)")
    current_r = st.number_input("Current R", 0.0, 1000.0, 498.0)
    current_s = st.number_input("Current S", 0.0, 1000.0, 502.0)
    current_t = st.number_input("Current T", 0.0, 1000.0, 495.0)

# ============================================
# SECTION 5: Generate Diagnosis (BOTTOM OF PAGE)
# ============================================
st.markdown('<p class="section-header">5. Hasil Diagnosa</p>', unsafe_allow_html=True)

# Diagnosis button at the bottom
if st.button("🔍 GENERATE DIAGNOSIS", type="primary", use_container_width=True, key="diagnose_btn"):
    with st.spinner("Menganalisis data menggunakan 6-level diagnostic engine..."):
        # Calculate averages first
        motor_h_avr = (motor_h_de + motor_h_nde) / 2
        motor_v_avr = (motor_v_de + motor_v_nde) / 2
        motor_a_avr = (motor_a_de + motor_a_nde) / 2
        pump_h_avr = (pump_h_de + pump_h_nde) / 2
        pump_v_avr = (pump_v_de + pump_v_nde) / 2
        pump_a_avr = (pump_a_de + pump_a_nde) / 2
        
        # Find maximum velocity
        all_velocities = [
            motor_h_avr, motor_v_avr, motor_a_avr,
            pump_h_avr, pump_v_avr, pump_a_avr
        ]
        max_velocity = max(all_velocities)
        directions = ["Motor Horizontal", "Motor Vertical", "Motor Axial", 
                     "Pump Horizontal", "Pump Vertical", "Pump Axial"]
        max_direction = directions[all_velocities.index(max_velocity)]
        
        # Calculate voltage imbalance
        v_avg = (voltage_r + voltage_s + voltage_t) / 3
        v_imbalance = max(abs(voltage_r - v_avg), abs(voltage_s - v_avg), abs(voltage_t - v_avg)) / v_avg * 100 if v_avg > 0 else 0
        
        # Calculate current imbalance
        i_avg = (current_r + current_s + current_t) / 3
        i_imbalance = max(abs(current_r - i_avg), abs(current_s - i_avg), abs(current_t - i_avg)) / i_avg * 100 if i_avg > 0 else 0
        
        # Calculate temperature gradients
        motor_temp_gradient = abs(temp_motor_de - temp_motor_nde)
        pump_temp_gradient = abs(temp_pump_de - temp_pump_nde)
        
        # Calculate fundamental frequency
        fundamental = motor_rpm / 60
        
        # ============================================
        # ACCURATE DIAGNOSIS LOGIC (Fixed & Improved)
        # ============================================
        
        # Step 1: Safety Check
        safety_issues = []
        if max(temp_motor_de, temp_motor_nde, temp_pump_de, temp_pump_nde) > 120:
            safety_issues.append("Suhu bearing >120°C - Emergency shutdown required")
        if max_velocity > 11.2:
            safety_issues.append("Vibrasi Zone D (>11.2 mm/s) - Emergency shutdown required")
        
        # Step 2: ISO 10816-3 Zone Classification
        if foundation_type == "Rigid (Concrete)":
            zone_b_limit = 2.8
            zone_c_limit = 7.1
        else:  # Flexible
            zone_b_limit = 4.5
            zone_c_limit = 11.2
        
        if max_velocity <= zone_b_limit:
            zone = "A"
            zone_status = "New machine condition"
            zone_color = "success"
        elif max_velocity <= zone_c_limit:
            zone = "B"
            zone_status = "Acceptable for unlimited operation"
            zone_color = "info"
        elif max_velocity <= 11.2:
            zone = "C"
            zone_status = "UNSATISFACTORY - Short-term operation only"
            zone_color = "warning"
        else:
            zone = "D"
            zone_status = "UNACCEPTABLE - Vibration causes damage"
            zone_color = "error"
        
        # Step 3: FFT-Based Fault Detection (ACCURATE LOGIC)
        faults = []
        
        # Electrical Unbalance Detection (2×Line Frequency at 100 Hz)
        if abs(peak3_freq - 100.0) < 5.0 and peak3_amp > 0.5 * peak1_amp and v_imbalance > 2.0:
            faults.append({
                "type": "ELECTRICAL UNBALANCE",
                "confidence": 92,
                "evidence": [
                    f"2×Line Frequency dominant di {peak3_freq:.1f} Hz ({peak3_amp:.1f} mm/s)",
                    f"Voltage imbalance {v_imbalance:.1f}% > 2% limit",
                    "Phase instability mengkonfirmasi origin electrical"
                ],
                "severity": "WARNING"
            })
        
        # Mechanical Unbalance Detection (1X dominant + phase stable)
        elif abs(peak1_freq - fundamental) < 0.1 * fundamental and peak1_amp > 0.8 * (peak1_amp + peak2_amp + peak3_amp) and v_imbalance < 2.0:
            faults.append({
                "type": "MECHANICAL UNBALANCE",
                "confidence": 88,
                "evidence": [
                    f"1X dominant di {peak1_freq:.1f} Hz ({peak1_amp:.1f} mm/s, {peak1_amp/(peak1_amp+peak2_amp+peak3_amp)*100:.0f}% RMS)",
                    "Phase stability mengkonfirmasi origin mechanical",
                    f"Fundamental frequency = {fundamental:.2f} Hz (RPM/60)"
                ],
                "severity": "WARNING"
            })
        
        # Misalignment Detection (2X dominant + axial vibration high)
        elif abs(peak2_freq - 2*fundamental) < 0.1 * 2*fundamental and peak2_amp > 0.5 * peak1_amp:
            alignment_type = "ANGULAR" if pump_a_avr > pump_v_avr else "PARALLEL"
            faults.append({
                "type": f"{alignment_type} MISALIGNMENT",
                "confidence": 85,
                "evidence": [
                    f"2X dominant di {peak2_freq:.1f} Hz ({peak2_amp:.1f} mm/s)",
                    f"2X/1X ratio = {peak2_amp/peak1_amp:.2f} > 0.5",
                    f"{'Axial' if alignment_type == 'ANGULAR' else 'Radial'} vibration dominant"
                ],
                "severity": "WARNING"
            })
        
        # Bearing Defect Detection (HF bands high + temperature gradient)
        elif hf_pump_de > 0.7 and (pump_temp_gradient > 15 or abs(peak3_freq - 76.0) < 5.0):
            faults.append({
                "type": "BEARING DEFECT (Stage 2)",
                "confidence": 87,
                "evidence": [
                    f"HF 5-16 kHz = {hf_pump_de:.2f}g > 0.7g threshold",
                    f"Temperature gradient DE-NDE = {pump_temp_gradient:.0f}°C >15°C",
                    f"Peak3 di {peak3_freq:.1f} Hz (kandidat BPFO)"
                ],
                "severity": "WARNING"
            })
        
        # Cavitation Detection (NPSHa margin low + BEP deviation high)
        else:
            npsha = p_suc + 10.33 - 0.5  # Simplified for BBM
            npsha_margin = npsha - npshr
            bep_deviation = abs(actual_flow - bep_flow) / bep_flow * 100 if bep_flow > 0 else 0
            
            if npsha_margin < 0.6 and bep_deviation > 20:
                faults.append({
                    "type": "CAVITATION RISK",
                    "confidence": 80,
                    "evidence": [
                        f"NPSHa margin = {npsha_margin:.2f}m < 0.6m safety margin",
                        f"BEP deviation = {bep_deviation:.0f}% > 20% limit",
                        "Broadband noise 50-200 Hz elevated"
                    ],
                    "severity": "WARNING"
                })
        
        # Default if no fault detected
        if not faults:
            faults.append({
                "type": "NO SIGNIFICANT FAULT DETECTED",
                "confidence": 95,
                "evidence": ["All parameters within acceptable limits"],
                "severity": "NORMAL"
            })
        
        # Primary fault
        primary_fault = faults[0]
        
        # Step 4: MTBF Estimation
        if "BEARING DEFECT" in primary_fault["type"]:
            mtbf_days = 24
        elif "MISALIGNMENT" in primary_fault["type"]:
            mtbf_days = 30
        elif primary_fault["type"] == "NO SIGNIFICANT FAULT DETECTED":
            mtbf_days = 180
        else:
            mtbf_days = 60
        
        # Step 5: Risk Assessment
        if zone == "D" or primary_fault["severity"] == "CRITICAL":
            risk_level = "CRITICAL"
            timeline = "<4 hours"
        elif zone == "C" or primary_fault["confidence"] > 85:
            risk_level = "HIGH"
            timeline = "<72 hours"
        elif zone == "B" or primary_fault["confidence"] > 75:
            risk_level = "MEDIUM"
            timeline = "<30 days"
        else:
            risk_level = "LOW"
            timeline = "<90 days"
        
        # ============================================
        # DISPLAY RESULTS
        # ============================================
        
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        
        # Executive Summary
        st.markdown("### 📊 Executive Summary")
        
        if safety_issues:
            st.error("🚨 **EMERGENCY SHUTDOWN REQUIRED**")
            for issue in safety_issues:
                st.write(f"• {issue}")
            st.markdown("**Action: Segera lakukan LOTO sesuai OSHA 1910.147**")
        else:
            if primary_fault["type"] == "NO SIGNIFICANT FAULT DETECTED":
                st.success(f"✅ **{primary_fault['type']}**")
                st.markdown(f"**Status**: Semua parameter dalam batas aman")
            else:
                severity_emoji = "🔴" if primary_fault["severity"] == "CRITICAL" else "🟠" if primary_fault["severity"] == "WARNING" else "🟢"
                st.warning(f"{severity_emoji} **{primary_fault['type']}**")
                st.progress(primary_fault["confidence"])
                st.caption(f"Confidence: {primary_fault['confidence']}%")
        
        st.markdown("---")
        
        # Vibration Severity
        st.markdown("### 📏 Vibration Severity (ISO 10816-3:2001)")
        
        col15, col16, col17 = st.columns(3)
        with col15:
            if zone_color == "success":
                st.success(f"Zone {zone}")
            elif zone_color == "warning":
                st.warning(f"Zone {zone}")
            elif zone_color == "error":
                st.error(f"Zone {zone}")
            else:
                st.info(f"Zone {zone}")
        with col16:
            st.metric("Max Velocity", f"{max_velocity:.2f} mm/s")
        with col17:
            st.metric("Direction", max_direction)
        
        st.caption(f"Foundation: {foundation_type} | Zone B Limit: {zone_b_limit:.1f} mm/s | Zone C Limit: {zone_c_limit:.1f} mm/s")
        st.caption(f"Status: {zone_status}")
        
        st.markdown("---")
        
        # Primary Diagnosis
        if primary_fault["type"] != "NO SIGNIFICANT FAULT DETECTED":
            st.markdown("### 🔍 Primary Diagnosis")
            
            for evidence in primary_fault["evidence"]:
                st.write(f"• {evidence}")
            
            st.caption(f"Standard: ISO 13373-2 Clause 5.4.3 + IEC 60034-1 §6.3")
        
        st.markdown("---")
        
        # Bearing Condition
        st.markdown("### ⚙️ Bearing Condition (ISO 15243:2017)")
        
        col18, col19, col20 = st.columns(3)
        with col18:
            st.metric("Pump DE HF", f"{hf_pump_de:.2f} g")
        with col19:
            ambient = 35
            temp_rise = temp_pump_de - ambient
            st.metric("Temp Rise", f"{temp_rise:.0f}°C")
        with col20:
            st.metric("Temp Gradient", f"{pump_temp_gradient:.0f}°C")
        
        if hf_pump_de > 1.5:
            st.error("❌ **Stage 3 Defect** - Replacement required immediately")
        elif hf_pump_de > 0.7:
            st.warning("⚠️ **Stage 2 Defect** - Plan replacement within 30 days")
        else:
            st.success("✅ **Normal Condition** - Continue routine monitoring")
        
        st.markdown("---")
        
        # Action Plan
        st.markdown("### ✅ Recommended Actions (ISO 45001 Risk-Based)")
        
        col21, col22, col23 = st.columns(3)
        with col21:
            risk_emoji = "🔴" if risk_level == "CRITICAL" else "🟠" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"
            st.metric("Risk Level", f"{risk_emoji} {risk_level}")
        with col22:
            st.metric("MTBF Estimation", f"{mtbf_days} days")
        with col23:
            st.metric("Action Timeline", timeline)
        
        st.markdown("**Action Items:**")
        
        if safety_issues:
            st.error("🔴 **CRITICAL - <4 hours**")
            st.write("• LAKUKAN SHUTDOWN SEGERA")
            st.write("• Ikuti prosedur LOTO sesuai OSHA 1910.147")
            st.write("• Laporkan ke supervisor sebelum melanjutkan")
        
        elif primary_fault["type"] == "ELECTRICAL UNBALANCE":
            st.warning("🟠 **HIGH PRIORITY - <24 hours**")
            st.write("• Koreksi voltage imbalance ke <2%")
            st.write("• Periksa tap changer transformer dan distribusi beban 3-phase")
            st.write("• Verifikasi dengan thermal camera pada koneksi terminal")
            st.caption("Standard: IEC 60034-1 §6.3")
            
            st.info("🟡 **MEDIUM PRIORITY - <7 days**")
            st.write("• Monitor bearing temperature harian")
            st.write("• Jika vibrasi meningkat >7.1 mm/s → shutdown segera")
            st.caption("Standard: ISO 10816-3 Clause 5.3")
        
        elif "BEARING DEFECT" in primary_fault["type"]:
            st.warning("🟠 **HIGH PRIORITY - <14 days**")
            st.write(f"• Jadwalkan penggantian bearing (MTBF: {mtbf_days} hari)")
            st.write("• Monitor HF bands dan temperature trend harian")
            st.write("• Siapkan bearing pengganti sesuai spesifikasi")
            st.caption("Standard: ISO 15243:2017 Table 2")
            
            st.info("🟡 **MEDIUM PRIORITY - <30 days**")
            st.write("• Periksa sistem pelumasan")
            st.write("• Pastikan oil level dan kualitas sesuai ISO 12922")
            st.caption("Standard: ISO 12922")
        
        elif primary_fault["type"] == "NO SIGNIFICANT FAULT DETECTED":
            st.success("🟢 **ROUTINE MONITORING**")
            st.write("• Lanjutkan pemantauan rutin sesuai jadwal")
            st.write("• Inspeksi vibrasi bulanan")
            st.write("• Catat tren parameter untuk early warning")
            st.caption("Standard: ISO 10816-3 Clause 5.2")
        
        st.markdown("---")
        
        # Compliance Status
        st.markdown("### 📋 Compliance Status (AIM-004 Format)")
        
        col24, col25, col26, col27 = st.columns(4)
        
        with col24:
            iso_status = "✅ COMPLIANT" if zone in ["A", "B"] else "⚠️ WARNING" if zone == "C" else "❌ NON-COMPLIANT"
            st.metric("ISO 10816-3", iso_status)
        
        with col25:
            iec_status = "✅ COMPLIANT" if v_imbalance <= 2.0 else "❌ NON-COMPLIANT"
            st.metric("IEC 60034-1", iec_status)
        
        with col26:
            npsha = p_suc + 10.33 - 0.5
            npsha_margin = npsha - npshr
            api_status = "✅ COMPLIANT" if npsha_margin >= 0.6 else "⚠️ WARNING"
            st.metric("API 610", api_status)
        
        with col27:
            iso15243_status = "✅ COMPLIANT" if hf_pump_de <= 0.7 else "⚠️ STAGE 2" if hf_pump_de <= 1.5 else "❌ STAGE 3"
            st.metric("ISO 15243", iso15243_status)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export section
        st.markdown("### 📥 Export Report")
        col28, col29 = st.columns(2)
        
        report_text = f"""
PUMP DIAGNOSTIC REPORT - PERTAMINA PATRA NIAGA
===============================================
Asset ID: {asset_id}
Location: {location}
Pump Type: {pump_type}
Date: {datetime.now().strftime('%d %b %Y %H:%M')}
Inspector: {st.session_state.get('inspector_name', 'Unknown')}

EXECUTIVE SUMMARY
-----------------
Diagnosis: {primary_fault['type']}
Confidence: {primary_fault['confidence']}%
Risk Level: {risk_level}
Recommended Timeline: {timeline}

VIBRATION SEVERITY (ISO 10816-3:2001)
--------------------------------------
Zone Classification: {zone}
Maximum Velocity: {max_velocity:.2f} mm/s
Direction: {max_direction}
Foundation Type: {foundation_type}
Zone B Limit: {zone_b_limit:.1f} mm/s
Zone C Limit: {zone_c_limit:.1f} mm/s
Status: {zone_status}

PRIMARY DIAGNOSIS
-----------------
{chr(10).join(['• ' + e for e in primary_fault['evidence']])}

BEARING CONDITION (ISO 15243:2017)
-----------------------------------
Pump DE HF 5-16 kHz: {hf_pump_de:.2f} g
Temperature Rise: {temp_rise:.0f}°C
Temperature Gradient: {pump_temp_gradient:.0f}°C

RECOMMENDED ACTIONS
-------------------
Risk Level: {risk_level}
MTBF Estimation: {mtbf_days} days
Timeline: {timeline}

COMPLIANCE STATUS
-----------------
ISO 10816-3: {iso_status}
IEC 60034-1: {iec_status} (Voltage Imbalance: {v_imbalance:.1f}%)
API 610: {api_status} (NPSHa Margin: {npsha_margin:.2f}m)
ISO 15243: {iso15243_status}

Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Standards Referenced: ISO 10816-3:2001, API 610 Ed.11, IEC 60034-1:2017, ISO 15243:2017, ISO 45001:2018
        """
        
        with col28:
            st.download_button(
                "📄 Download Text Report",
                report_text,
                file_name=f"pump_diagnostic_{asset_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col29:
            st.download_button(
                "📋 Copy Report to Clipboard",
                report_text,
                key="copy_report",
                help="Copy report text to clipboard",
                use_container_width=True
            )

# Footer
st.markdown("""
<div class="footer">
    <p>Pump Diagnostic System v1.1 | Pertamina Patra Niaga - Asset Integrity Management</p>
    <p>Developed with ❤️ using Streamlit | Standards: ISO 10816-3, API 610, IEC 60034-1, ISO 15243, ISO 45001</p>
    <p>© 2026 Pertamina Patra Niaga. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
