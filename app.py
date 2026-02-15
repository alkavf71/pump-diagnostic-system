"""
Pump Diagnostic System - Pertamina Patra Niaga
"""

import streamlit as st
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
    </style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<p class="main-header">🛢️ Pump Diagnostic System - Pertamina Patra Niaga</p>', unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #6c757d; margin-bottom: 30px;'>Sistem Diagnostik Pompa Centrifugal Berbasis Adash Vibrio 4900 | Asset Integrity Management</div>", unsafe_allow_html=True)

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
    bearing_size = st.selectbox("Bearing Size (Estimasi Visual)", [
        "Small Roller (<50mm shaft)",
        "Medium Roller (50-100mm shaft)",
        "Large Roller (>100mm shaft)",
        "Unknown"
    ], help="Perkiraan diameter shaft: jempol=kecil, telapak=medium")
    asset_id = st.text_input("Asset ID", "PPJ-BBM-P-205")
    location = st.text_input("Location", "Plaju Terminal")

# ============================================
# SECTION 2: Vibration Measurements
# ============================================
st.markdown('<p class="section-header">2. Pengukuran Vibrasi (Adash Vibrio 4900)</p>', unsafe_allow_html=True)
st.info("💡 **Petunjuk**: Ukur DE (Drive End) dan NDE (Non-Drive End) untuk setiap arah. Nilai dalam mm/s RMS.")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("#### Motor (Driver)")
    motor_h_de = st.number_input("Motor H - DE (mm/s)", 0.0, 20.0, 1.10, key="m_h_de")
    motor_h_nde = st.number_input("Motor H - NDE (mm/s)", 0.0, 20.0, 1.05, key="m_h_nde")
    motor_v_de = st.number_input("Motor V - DE (mm/s)", 0.0, 20.0, 0.50, key="m_v_de")
    motor_v_nde = st.number_input("Motor V - NDE (mm/s)", 0.0, 20.0, 0.48, key="m_v_nde")
    motor_a_de = st.number_input("Motor A - DE (mm/s)", 0.0, 20.0, 0.30, key="m_a_de")
    motor_a_nde = st.number_input("Motor A - NDE (mm/s)", 0.0, 20.0, 0.35, key="m_a_nde")

with col5:
    st.markdown("#### Pump (Driven)")
    pump_h_de = st.number_input("Pump H - DE (mm/s)", 0.0, 20.0, 1.85, key="p_h_de")
    pump_h_nde = st.number_input("Pump H - NDE (mm/s)", 0.0, 20.0, 1.75, key="p_h_nde")
    pump_v_de = st.number_input("Pump V - DE (mm/s)", 0.0, 20.0, 5.20, key="p_v_de")
    pump_v_nde = st.number_input("Pump V - NDE (mm/s)", 0.0, 20.0, 4.80, key="p_v_nde")
    pump_a_de = st.number_input("Pump A - DE (mm/s)", 0.0, 20.0, 0.85, key="p_a_de")
    pump_a_nde = st.number_input("Pump A - NDE (mm/s)", 0.0, 20.0, 0.90, key="p_a_nde")

with col6:
    st.markdown("#### High Frequency Bands (0.5-16 kHz)")
    st.caption("Diukur di DE saja (sisi beban) - Pump DE untuk bearing defect")
    hf_motor_de = st.number_input("Motor DE HF (g)", 0.0, 10.0, 0.25, key="hf_motor")
    hf_pump_de = st.number_input("Pump DE HF (g)", 0.0, 10.0, 0.95, key="hf_pump")
    
    st.markdown("#### Bearing Temperature (°C)")
    st.caption("Diukur di housing bearing dengan infrared thermometer")
    temp_motor_de = st.number_input("Motor DE Temp", 0, 150, 62, key="tm_de")
    temp_motor_nde = st.number_input("Motor NDE Temp", 0, 150, 64, key="tm_nde")
    temp_pump_de = st.number_input("Pump DE Temp", 0, 150, 88, key="tp_de")
    temp_pump_nde = st.number_input("Pump NDE Temp", 0, 150, 70, key="tp_nde")

# ============================================
# SECTION 3: FFT Spectrum Analysis (REVISED - NO PHASE)
# ============================================
st.markdown('<p class="section-header">3. FFT Spectrum Analysis (Adash Vibrio 4900)</p>', unsafe_allow_html=True)
st.info("""
📍 **LOKASI PENGUKURAN YANG BENAR (ISO 13373-2 Clause 5.4.2):**
• **Diukur di: PUMP DE (Driven End) pada arah HORIZONTAL**
• **Range frekuensi: 1-200 Hz**
• **PENTING**: Vibrio 4900 **TIDAK mengukur phase angle**. 
  Diagnosa electrical vs mechanical unbalance berdasarkan:
  - 2×Line Freq (100 Hz) + voltage imbalance → Electrical Unbalance
  - 1X dominant + voltage normal → Mechanical Unbalance
""")

col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("#### Peak 1 (1X - Fundamental)")
    peak1_freq = st.number_input("Frekuensi Peak 1 (Hz)", 0.0, 200.0, 24.8, key="p1f")
    peak1_amp = st.number_input("Amplitudo Peak 1 (mm/s)", 0.0, 20.0, 3.8, key="p1a")

with col8:
    st.markdown("#### Peak 2 (2X - Harmonik)")
    peak2_freq = st.number_input("Frekuensi Peak 2 (Hz)", 0.0, 200.0, 49.6, key="p2f")
    peak2_amp = st.number_input("Amplitudo Peak 2 (mm/s)", 0.0, 20.0, 1.1, key="p2a")

with col9:
    st.markdown("#### Peak 3 (Bearing/2LF)")
    peak3_freq = st.number_input("Frekuensi Peak 3 (Hz)", 0.0, 200.0, 76.0, key="p3f")
    peak3_amp = st.number_input("Amplitudo Peak 3 (mm/s)", 0.0, 20.0, 0.7, key="p3a")

# Additional parameters (Displacement only - Phase REMOVED)
st.markdown("#### Additional Parameters (Optional)")
displacement_peak = st.number_input("Displacement Peak (μm)", 0, 200, 68,
                                   help="Peak-to-peak 2-100 Hz (optional - untuk looseness detection)")

# ============================================
# SECTION 4: Hydraulic & Electrical Parameters
# ============================================
st.markdown('<p class="section-header">4. Parameter Hydraulic & Electrical</p>', unsafe_allow_html=True)

col12, col13, col14 = st.columns(3)

with col12:
    st.markdown("#### Hydraulic Parameters")
    actual_flow = st.number_input("Actual Flow (m³/hr)", 0.0, 1000.0, 35.0)
    p_suc = st.number_input("Suction Pressure (bar g)", 0.0, 50.0, 2.5)
    p_dis = st.number_input("Discharge Pressure (bar g)", 0.0, 100.0, 10.2)

with col13:
    st.markdown("#### Electrical - Voltage (V)")
    voltage_r = st.number_input("Voltage R", 0.0, 1000.0, 402.0)
    voltage_s = st.number_input("Voltage S", 0.0, 1000.0, 389.0)
    voltage_t = st.number_input("Voltage T", 0.0, 1000.0, 405.0)

with col14:
    st.markdown("#### Electrical - Current (A)")
    current_r = st.number_input("Current R", 0.0, 1000.0, 76.0)
    current_s = st.number_input("Current S", 0.0, 1000.0, 81.0)
    current_t = st.number_input("Current T", 0.0, 1000.0, 78.0)
    actual_rpm = st.number_input("Actual RPM (measured)", 0, 3600, 1472,
                                help="Dari tachometer laser - untuk hitung motor slip")

# ============================================
# SECTION 5: Generate Diagnosis (BOTTOM) - REVISED
# ============================================
st.markdown('<p class="section-header">5. Hasil Diagnosa Komprehensif</p>', unsafe_allow_html=True)

if st.button("🔍 GENERATE DIAGNOSIS", type="primary", use_container_width=True, key="diagnose_btn"):
    with st.spinner("Menganalisis data dengan ISO 10816-3 + API 610 + IEC 60034-1..."):
        # ============================================
        # STEP 1: Calculate ALL Parameters (NO PHASE)
        # ============================================
        # Vibration averages
        motor_h_avr = (motor_h_de + motor_h_nde) / 2
        motor_v_avr = (motor_v_de + motor_v_nde) / 2
        motor_a_avr = (motor_a_de + motor_a_nde) / 2
        pump_h_avr = (pump_h_de + pump_h_nde) / 2
        pump_v_avr = (pump_v_de + pump_v_nde) / 2
        pump_a_avr = (pump_a_de + pump_a_nde) / 2
        
        all_velocities = [motor_h_avr, motor_v_avr, motor_a_avr, pump_h_avr, pump_v_avr, pump_a_avr]
        max_velocity = max(all_velocities)
        directions = ["Motor H", "Motor V", "Motor A", "Pump H", "Pump V", "Pump A"]
        max_direction = directions[all_velocities.index(max_velocity)]
        
        # Electrical calculations (NO PHASE USED)
        v_avg = (voltage_r + voltage_s + voltage_t) / 3
        v_imbalance = max(abs(voltage_r - v_avg), abs(voltage_s - v_avg), abs(voltage_t - v_avg)) / v_avg * 100 if v_avg > 0 else 0
        
        i_avg = (current_r + current_s + current_t) / 3
        i_imbalance = max(abs(current_r - i_avg), abs(current_s - i_avg), abs(current_t - i_avg)) / i_avg * 100 if i_avg > 0 else 0
        
        load_factor = (i_avg / flc) * 100 if flc > 0 else 0
        
        # Motor slip calculation (IEC 60034-1)
        slip_rpm = motor_rpm - actual_rpm if actual_rpm > 0 else 0
        slip_percent = (slip_rpm / motor_rpm) * 100 if motor_rpm > 0 else 0
        
        # Hydraulic calculations (API 610)
        rho_bbm = 850  # kg/m³
        vapor_pressure_m = 0.5  # m (approx for BBM at 35°C)
        friction_loss_m = 0.3  # m (approx suction line loss)
        
        npsha = (p_suc * 10.197) / rho_bbm * 1000 - vapor_pressure_m - friction_loss_m
        npsha_margin = npsha - npshr
        
        # BEP deviation
        bep_deviation = abs(actual_flow - bep_flow) / bep_flow * 100 if bep_flow > 0 else 0
        
        # Temperature analysis
        pump_temp_gradient = abs(temp_pump_de - temp_pump_nde)
        ambient = 35
        temp_rise_pump = temp_pump_de - ambient
        
        # Fundamental frequency
        fundamental = motor_rpm / 60
        
        # ============================================
        # STEP 2: ISO 10816-3 ZONE CLASSIFICATION
        # ============================================
        if group_num == 2:  # Group 2: 15-75 kW
            if foundation_type == "Rigid (Concrete)":
                zone_a_limit = 1.8
                zone_b_limit = 4.5
                zone_c_limit = 7.1
                zone_explanation = "Group 2, Rigid Foundation (ISO 10816-3 Table 2)"
            else:
                zone_a_limit = 2.8
                zone_b_limit = 7.1
                zone_c_limit = 11.2
                zone_explanation = "Group 2, Flexible Foundation (ISO 10816-3 Table 2)"
        else:  # Group 3: >75 kW
            if foundation_type == "Rigid (Concrete)":
                zone_a_limit = 2.8
                zone_b_limit = 7.1
                zone_c_limit = 11.2
                zone_explanation = "Group 3, Rigid Foundation (ISO 10816-3 Table 2)"
            else:
                zone_a_limit = 4.5
                zone_b_limit = 11.2
                zone_c_limit = 18.0
                zone_explanation = "Group 3, Flexible Foundation (ISO 10816-3 Table 2)"
        
        if max_velocity <= zone_a_limit:
            zone = "A"
            zone_status = "New machine condition (ISO 10816-3 Clause 5.1)"
            zone_color = "success"
        elif max_velocity <= zone_b_limit:
            zone = "B"
            zone_status = "Acceptable for unlimited operation (ISO 10816-3 Clause 5.2)"
            zone_color = "info"
        elif max_velocity <= zone_c_limit:
            zone = "C"
            zone_status = "UNSATISFACTORY - Short-term operation only (ISO 10816-3 Clause 5.3)"
            zone_color = "warning"
        else:
            zone = "D"
            zone_status = "UNACCEPTABLE - Vibration causes damage (ISO 10816-3 Clause 5.4)"
            zone_color = "error"
        
        # Calculate ISO 10816-3 compliance status
        iso_10816_3_status = "COMPLIANT" if zone in ["A", "B"] else "WARNING" if zone == "C" else "NON-COMPLIANT"
        iso_10816_3_emoji = "✅" if iso_10816_3_status == "COMPLIANT" else "⚠️" if iso_10816_3_status == "WARNING" else "❌"
        
        # ============================================
        # STEP 3: Multi-Parameter Fault Detection (NO PHASE)
        # ============================================
        faults = []
        hydraulic_issues = []
        electrical_issues = []
        
        # === ELECTRICAL ANALYSIS ===
        if v_imbalance > 5.0:
            electrical_issues.append({
                "parameter": "Voltage Imbalance",
                "value": f"{v_imbalance:.1f}%",
                "threshold": ">5.0%",
                "severity": "CRITICAL",
                "standard": "IEC 60034-1 §6.3"
            })
        elif v_imbalance > 2.0:
            electrical_issues.append({
                "parameter": "Voltage Imbalance",
                "value": f"{v_imbalance:.1f}%",
                "threshold": ">2.0%",
                "severity": "WARNING",
                "standard": "IEC 60034-1 §6.3"
            })
        
        if i_imbalance > 10.0:
            electrical_issues.append({
                "parameter": "Current Imbalance",
                "value": f"{i_imbalance:.1f}%",
                "threshold": ">10.0%",
                "severity": "CRITICAL",
                "standard": "NEMA MG-1 §14.32"
            })
        elif i_imbalance > 5.0:
            electrical_issues.append({
                "parameter": "Current Imbalance",
                "value": f"{i_imbalance:.1f}%",
                "threshold": ">5.0%",
                "severity": "WARNING",
                "standard": "NEMA MG-1 §14.32"
            })
        
        if slip_percent > 3.0:
            electrical_issues.append({
                "parameter": "Motor Slip",
                "value": f"{slip_percent:.1f}%",
                "threshold": ">3.0%",
                "severity": "WARNING",
                "standard": "IEC 60034-1 Clause 5.2"
            })
        
        if load_factor > 110:
            electrical_issues.append({
                "parameter": "Overload",
                "value": f"{load_factor:.0f}%",
                "threshold": ">110%",
                "severity": "CRITICAL",
                "standard": "IEC 60034-1 Table 3"
            })
        elif load_factor < 40:
            electrical_issues.append({
                "parameter": "Underload",
                "value": f"{load_factor:.0f}%",
                "threshold": "<40%",
                "severity": "WARNING",
                "standard": "API 610 Clause 7.3"
            })
        
        # Calculate IEC 60034-1 compliance status
        iec_60034_1_status = "COMPLIANT" if v_imbalance <= 2.0 else "WARNING" if v_imbalance <= 5.0 else "NON-COMPLIANT"
        iec_60034_1_emoji = "✅" if iec_60034_1_status == "COMPLIANT" else "⚠️" if iec_60034_1_status == "WARNING" else "❌"
        
        # === HYDRAULIC ANALYSIS ===
        if npsha_margin < 0.3:
            hydraulic_issues.append({
                "parameter": "NPSHa Margin",
                "value": f"{npsha_margin:.2f}m",
                "threshold": "<0.3m",
                "severity": "CRITICAL",
                "standard": "API 610 Clause 7.3.2"
            })
        elif npsha_margin < 0.6:
            hydraulic_issues.append({
                "parameter": "NPSHa Margin",
                "value": f"{npsha_margin:.2f}m",
                "threshold": "<0.6m",
                "severity": "WARNING",
                "standard": "API 610 Clause 7.3.2"
            })
        
        if bep_deviation > 30:
            hydraulic_issues.append({
                "parameter": "BEP Deviation",
                "value": f"{bep_deviation:.0f}%",
                "threshold": ">30%",
                "severity": "CRITICAL",
                "standard": "API 610 Clause 7.3"
            })
        elif bep_deviation > 20:
            hydraulic_issues.append({
                "parameter": "BEP Deviation",
                "value": f"{bep_deviation:.0f}%",
                "threshold": ">20%",
                "severity": "WARNING",
                "standard": "API 610 Clause 7.3"
            })
        
        # Cavitation risk assessment
        cavitation_risk = "LOW"
        cavitation_evidence = []
        if npsha_margin < 0.6 and bep_deviation > 20:
            cavitation_risk = "HIGH"
            cavitation_evidence.append(f"NPSHa margin {npsha_margin:.2f}m < 0.6m safety margin")
            cavitation_evidence.append(f"BEP deviation {bep_deviation:.0f}% > 20% limit")
        elif npsha_margin < 0.6 or bep_deviation > 20:
            cavitation_risk = "MEDIUM"
            if npsha_margin < 0.6:
                cavitation_evidence.append(f"NPSHa margin {npsha_margin:.2f}m < 0.6m")
            if bep_deviation > 20:
                cavitation_evidence.append(f"BEP deviation {bep_deviation:.0f}% > 20%")
        
        # Calculate API 610 compliance status
        api_610_status = "COMPLIANT" if npsha_margin >= 0.6 else "WARNING" if npsha_margin >= 0.3 else "NON-COMPLIANT"
        api_610_emoji = "✅" if api_610_status == "COMPLIANT" else "⚠️" if api_610_status == "WARNING" else "❌"
        
        # === FFT FAULT DETECTION (NO PHASE USED) ===
        is_2lf_dominant = abs(peak3_freq - 100.0) < 5.0 and peak3_amp > 0.5 * peak1_amp
        is_1x_dominant = abs(peak1_freq - fundamental) < 0.1 * fundamental and peak1_amp > 0.8 * (peak1_amp + peak2_amp + peak3_amp)
        
        # Electrical Unbalance Detection (NO PHASE)
        if is_2lf_dominant and v_imbalance > 2.0:
            faults.append({
                "type": "ELECTRICAL UNBALANCE",
                "confidence": 92,
                "evidence": [
                    f"2×Line Frequency dominant di {peak3_freq:.1f} Hz ({peak3_amp:.1f} mm/s)",
                    f"Voltage imbalance {v_imbalance:.1f}% > 2% limit (IEC 60034-1 §6.3)",
                    "Diagnosis based on 2LF signature + voltage imbalance (phase measurement not available on Vibrio 4900)"
                ],
                "severity": "WARNING",
                "standard": "ISO 13373-2 Clause 5.4.3 + IEC 60034-1 §6.3"
            })
        
        # Mechanical Unbalance Detection (NO PHASE)
        elif is_1x_dominant and v_imbalance < 2.0:
            faults.append({
                "type": "MECHANICAL UNBALANCE",
                "confidence": 88,
                "evidence": [
                    f"1X dominant di {peak1_freq:.1f} Hz ({peak1_amp:.1f} mm/s, {peak1_amp/(peak1_amp+peak2_amp+peak3_amp)*100:.0f}% RMS)",
                    f"Voltage imbalance {v_imbalance:.1f}% < 2% limit",
                    "Diagnosis based on 1X dominance + normal voltage (phase measurement not required for screening)"
                ],
                "severity": "WARNING",
                "standard": "ISO 1940-1:2003 G2.5"
            })
        
        # Misalignment (2X dominant + axial vibration)
        is_2x_dominant = abs(peak2_freq - 2*fundamental) < 0.1 * 2*fundamental and peak2_amp > 0.5 * peak1_amp
        if is_2x_dominant:
            alignment_type = "ANGULAR" if pump_a_avr > pump_v_avr else "PARALLEL"
            faults.append({
                "type": f"{alignment_type} MISALIGNMENT",
                "confidence": 85,
                "evidence": [
                    f"2X dominant di {peak2_freq:.1f} Hz ({peak2_amp:.1f} mm/s)",
                    f"2X/1X ratio = {peak2_amp/peak1_amp:.2f} > 0.5",
                    f"{'Axial' if alignment_type == 'ANGULAR' else 'Radial'} vibration dominant"
                ],
                "severity": "WARNING",
                "standard": "API 671 Clause 5.3"
            })
        
        # Bearing Defect (HF high + temp gradient + BPFO peak)
        is_bearing_defect = hf_pump_de > 0.7 and (pump_temp_gradient > 15 or abs(peak3_freq - 76.0) < 5.0)
        if is_bearing_defect:
            faults.append({
                "type": "BEARING DEFECT (Stage 2)",
                "confidence": 87,
                "evidence": [
                    f"HF 5-16 kHz = {hf_pump_de:.2f}g > 0.7g threshold",
                    f"Temperature gradient DE-NDE = {pump_temp_gradient:.0f}°C >15°C",
                    f"Peak3 di {peak3_freq:.1f} Hz (BPFO candidate - bearing defect frequency)"
                ],
                "severity": "WARNING",
                "standard": "ISO 15243:2017 Table 2"
            })
        
        # Default if no fault detected
        if not faults:
            faults.append({
                "type": "NO SIGNIFICANT FAULT DETECTED",
                "confidence": 95,
                "evidence": ["All vibration parameters within acceptable limits"],
                "severity": "NORMAL",
                "standard": "ISO 10816-3 Clause 5.2"
            })
        
        primary_fault = faults[0]
        
        # Calculate ISO 15243 compliance status
        iso_15243_status = "COMPLIANT" if hf_pump_de <= 0.7 else "STAGE 2" if hf_pump_de <= 1.5 else "STAGE 3"
        iso_15243_emoji = "✅" if iso_15243_status == "COMPLIANT" else "⚠️" if iso_15243_status == "STAGE 2" else "❌"
        
        # ============================================
        # STEP 4: RISK ASSESSMENT (Severity-Based)
        # ============================================
        safety_issues = []
        if max(temp_motor_de, temp_motor_nde, temp_pump_de, temp_pump_nde) > 120:
            safety_issues.append(f"Bearing temperature {max(temp_motor_de, temp_motor_nde, temp_pump_de, temp_pump_nde)}°C >120°C")
        if max_velocity > zone_c_limit:
            safety_issues.append(f"Vibration {max_velocity:.1f} mm/s > Zone C limit ({zone_c_limit:.1f} mm/s)")
        
        if safety_issues:
            risk_level = "CRITICAL"
            timeline = "<4 hours"
            risk_explanation = "Safety hazard detected - immediate shutdown required"
            mtbf_days = 3
        elif zone == "C" or (is_bearing_defect and hf_pump_de > 1.0):
            risk_level = "HIGH"
            timeline = "<72 hours"
            risk_explanation = f"Vibration Zone C ({max_velocity:.1f} mm/s) or bearing defect progression"
            mtbf_days = 14
        elif hydraulic_issues or electrical_issues or is_bearing_defect:
            risk_level = "MEDIUM"
            timeline = "<30 days"
            risk_explanation = "Hydraulic/electrical issues or bearing defect detected"
            mtbf_days = 60
        else:
            risk_level = "LOW"
            timeline = "<90 days"
            risk_explanation = "All parameters within acceptable limits"
            mtbf_days = 180
        
        # ============================================
        # DISPLAY RESULTS - REVISED (NO COMPLIANCE SECTION)
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
            else:
                severity_emoji = "🔴" if primary_fault["severity"] == "CRITICAL" else "🟠" if primary_fault["severity"] == "WARNING" else "🟢"
                st.warning(f"{severity_emoji} **{primary_fault['type']}**")
                st.progress(min(primary_fault.get("confidence", 95), 95))
                st.caption(f"Confidence: {primary_fault.get('confidence', 95)}% | Standard: {primary_fault.get('standard', 'N/A')}")
        
        st.markdown("---")
        
        # Vibration Severity (WITH COMPLIANCE BADGE)
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
            # Compliance badge
            st.markdown(f'<span class="compliance-badge compliance-{iso_10816_3_status.lower()}">{iso_10816_3_emoji} ISO 10816-3: {iso_10816_3_status}</span>', unsafe_allow_html=True)
        with col16:
            st.metric("Max Velocity", f"{max_velocity:.2f} mm/s")
        with col17:
            st.metric("Direction", max_direction)
        
        st.caption(f"Machine Group: {machine_group}")
        st.caption(f"Foundation: {foundation_type}")
        st.caption(f"Zone Limits: A≤{zone_a_limit:.1f} | B≤{zone_b_limit:.1f} | C≤{zone_c_limit:.1f} mm/s")
        st.caption(f"Standard: {zone_explanation}")
        
        st.markdown("---")
        
        # HYDRAULIC ANALYSIS (WITH COMPLIANCE BADGE)
        st.markdown("### 💧 Hydraulic Performance Analysis")
        
        col18, col19, col20 = st.columns(3)
        with col18:
            st.metric("BEP Deviation", f"{bep_deviation:.0f}%", 
                     delta=f"{bep_deviation-20:.0f}%" if bep_deviation > 20 else None,
                     delta_color="inverse")
        with col19:
            st.metric("NPSHa", f"{npsha:.2f} m")
        with col20:
            st.metric("NPSHa Margin", f"{npsha_margin:.2f} m", 
                     delta="-0.6m" if npsha_margin < 0.6 else None,
                     delta_color="inverse")
            # Compliance badge
            st.markdown(f'<span class="compliance-badge compliance-{api_610_status.lower()}">{api_610_emoji} API 610: {api_610_status}</span>', unsafe_allow_html=True)
        
        st.markdown(f"**Cavitation Risk: {'🔴 HIGH' if cavitation_risk == 'HIGH' else '🟠 MEDIUM' if cavitation_risk == 'MEDIUM' else '🟢 LOW'}**")
        if cavitation_evidence:
            for evidence in cavitation_evidence:
                st.write(f"• {evidence}")
        
        # Show calculation details
        with st.expander("🔍 NPSHa Calculation Details (API 610 Clause 7.3.2)"):
            st.markdown(f"""
            <div class="calculation-box">
            NPSHa = (P_suc × 10.197) / ρ - h_vapor - h_friction<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= ({p_suc} bar × 10.197) / 850 kg/m³ × 1000 - 0.5m - 0.3m<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= {npsha:.2f} m<br><br>
            NPSHr (from pump curve) = {npshr} m<br>
            Safety Margin Required = 0.6 m (API 610)<br>
            Actual Margin = {npsha:.2f} - {npshr} = <b>{npsha_margin:.2f} m</b>
            </div>
            """, unsafe_allow_html=True)
        
        if hydraulic_issues:
            st.warning("⚠️ **Hydraulic Issues Detected**")
            for issue in hydraulic_issues[:2]:
                st.write(f"• **{issue['parameter']}**: {issue['value']} (threshold: {issue['threshold']})")
                st.caption(f"Standard: {issue['standard']}")
        
        st.markdown("---")
        
        # ELECTRICAL ANALYSIS (WITH COMPLIANCE BADGE)
        st.markdown("### ⚡ Electrical Performance Analysis")
        
        col21, col22, col23, col24 = st.columns(4)
        with col21:
            st.metric("Voltage Imbalance", f"{v_imbalance:.1f}%", 
                     delta=">2%" if v_imbalance > 2.0 else None,
                     delta_color="inverse")
            # Compliance badge
            st.markdown(f'<span class="compliance-badge compliance-{iec_60034_1_status.lower()}">{iec_60034_1_emoji} IEC 60034-1: {iec_60034_1_status}</span>', unsafe_allow_html=True)
        with col22:
            st.metric("Current Imbalance", f"{i_imbalance:.1f}%", 
                     delta=">5%" if i_imbalance > 5.0 else None,
                     delta_color="inverse")
        with col23:
            st.metric("Load Factor", f"{load_factor:.0f}%", 
                     delta=">110%" if load_factor > 110 else "<40%" if load_factor < 40 else None,
                     delta_color="inverse")
        with col24:
            st.metric("Motor Slip", f"{slip_percent:.1f}%", 
                     delta=">3%" if slip_percent > 3.0 else None,
                     delta_color="inverse")
        
        if electrical_issues:
            severity_map = {"CRITICAL": "🔴", "WARNING": "🟠", "INFO": "🟢"}
            for issue in electrical_issues[:3]:
                emoji = severity_map.get(issue['severity'], "🔵")
                st.write(f"{emoji} **{issue['parameter']}**: {issue['value']} (threshold: {issue['threshold']})")
                st.caption(f"Standard: {issue['standard']}")
        
        # Show calculation details
        with st.expander("🔍 Electrical Calculations Details (IEC 60034-1 §6.3)"):
            st.markdown(f"""
            <div class="calculation-box">
            Voltage Average = ({voltage_r} + {voltage_s} + {voltage_t}) / 3 = {v_avg:.1f} V<br>
            Max Deviation = {max(abs(voltage_r-v_avg), abs(voltage_s-v_avg), abs(voltage_t-v_avg)):.1f} V<br>
            Voltage Imbalance = {max(abs(voltage_r-v_avg), abs(voltage_s-v_avg), abs(voltage_t-v_avg)):.1f} / {v_avg:.1f} × 100% = <b>{v_imbalance:.1f}%</b><br><br>
            
            Current Average = ({current_r} + {current_s} + {current_t}) / 3 = {i_avg:.1f} A<br>
            Load Factor = {i_avg:.1f} / {flc} × 100% = <b>{load_factor:.0f}%</b><br><br>
            
            Motor Slip = ({motor_rpm} - {actual_rpm}) / {motor_rpm} × 100% = <b>{slip_percent:.1f}%</b>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Primary Diagnosis (FFT)
        st.markdown("### 🔍 FFT Signature Analysis")
        
        if primary_fault["type"] != "NO SIGNIFICANT FAULT DETECTED":
            for evidence in primary_fault.get("evidence", []):
                st.write(f"• {evidence}")
            st.caption(f"Standard: {primary_fault.get('standard', 'N/A')}")
        else:
            st.success("✅ No significant fault signatures detected in FFT spectrum")
        
        # Show FFT calculation details
        with st.expander("🔍 FFT Peak Analysis Details"):
            st.markdown(f"""
            <div class="calculation-box">
            Fundamental Frequency (1X) = RPM / 60 = {motor_rpm} / 60 = <b>{fundamental:.2f} Hz</b><br>
            Expected 2X = 2 × {fundamental:.2f} = <b>{2*fundamental:.2f} Hz</b><br><br>
            
            Peak 1: {peak1_freq:.1f} Hz → {peak1_amp:.1f} mm/s ({'✅ matches 1X' if abs(peak1_freq-fundamental) < 0.1*fundamental else '❌ not 1X'})<br>
            Peak 2: {peak2_freq:.1f} Hz → {peak2_amp:.1f} mm/s ({'✅ matches 2X' if abs(peak2_freq-2*fundamental) < 0.1*2*fundamental else '❌ not 2X'})<br>
            Peak 3: {peak3_freq:.1f} Hz → {peak3_amp:.1f} mm/s ({'✅ 2LF (electrical)' if abs(peak3_freq-100) < 5 else '✅ BPFO candidate' if abs(peak3_freq-76) < 5 else '❓ unknown'})
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Bearing Condition (WITH COMPLIANCE BADGE)
        st.markdown("### ⚙️ Bearing Condition (ISO 15243:2017)")
        
        col25, col26, col27 = st.columns(3)
        with col25:
            st.metric("Pump DE HF", f"{hf_pump_de:.2f} g", 
                     delta=">0.7g" if hf_pump_de > 0.7 else None,
                     delta_color="inverse")
            # Compliance badge
            st.markdown(f'<span class="compliance-badge compliance-{iso_15243_status.lower()}">{iso_15243_emoji} ISO 15243: {iso_15243_status}</span>', unsafe_allow_html=True)
        with col26:
            st.metric("Temp Rise", f"{temp_rise_pump:.0f}°C", 
                     delta=">40°C" if temp_rise_pump > 40 else None,
                     delta_color="inverse")
        with col27:
            st.metric("Temp Gradient", f"{pump_temp_gradient:.0f}°C", 
                     delta=">15°C" if pump_temp_gradient > 15 else None,
                     delta_color="inverse")
        
        if hf_pump_de > 1.5:
            st.error("❌ **Stage 3 Defect** - Replacement required immediately (ISO 15243 Table 2)")
        elif hf_pump_de > 0.7:
            st.warning("⚠️ **Stage 2 Defect** - Plan replacement within 30 days (ISO 15243 Table 2)")
        else:
            st.success("✅ **Normal Condition** - Continue routine monitoring")
        
        st.markdown("---")
        
        # Action Plan
        st.markdown("### ✅ Recommended Actions (ISO 45001 Risk-Based)")
        
        col28, col29, col30 = st.columns(3)
        with col28:
            risk_emoji = "🔴" if risk_level == "CRITICAL" else "🟠" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"
            st.metric("Risk Level", f"{risk_emoji} {risk_level}")
        with col29:
            st.metric("MTBF Estimation", f"{mtbf_days} days")
        with col30:
            st.metric("Action Timeline", timeline)
        
        st.caption(f"Risk Basis: {risk_explanation}")
        
        # Prioritized action items
        if safety_issues:
            st.error("🔴 **CRITICAL - <4 hours**")
            st.write("• LAKUKAN SHUTDOWN SEGERA")
            st.write("• Ikuti prosedur LOTO sesuai OSHA 1910.147")
        
        elif zone == "C":
            st.warning("🟠 **HIGH PRIORITY - <72 hours**")
            st.write(f"• Jadwalkan corrective maintenance dalam 72 jam (ISO 10816-3 Clause 5.3)")
            st.write(f"• Vibrasi {max_velocity:.1f} mm/s melebihi Zone B limit ({zone_b_limit:.1f} mm/s)")
            
            if hydraulic_issues:
                st.write("• Perbaiki kondisi hydraulic (NPSHa margin, BEP deviation)")
            if electrical_issues:
                st.write("• Koreksi ketidakseimbangan voltage/current")
        
        elif electrical_issues or hydraulic_issues:
            st.info("🟡 **MEDIUM PRIORITY - <30 days**")
            if electrical_issues:
                st.write(f"• Koreksi voltage imbalance {v_imbalance:.1f}% ke <2% (IEC 60034-1 §6.3)")
            if hydraulic_issues:
                st.write(f"• Optimasi flow ke 70-110% BEP ({bep_flow*0.7:.0f}-{bep_flow*1.1:.0f} m³/hr)")
        
        else:
            st.success("🟢 **ROUTINE MONITORING**")
            st.write(f"• Inspeksi berikutnya: {timeline}")
            st.write("• Lanjutkan pemantauan rutin sesuai jadwal")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export section
        st.markdown("### 📥 Export Report")
        col31, col32 = st.columns(2)
        
        report_text = f"""
PUMP DIAGNOSTIC REPORT - PERTAMINA PATRA NIAGA
===============================================
Asset ID      : {asset_id}
Location      : {location}
Pump Type     : {pump_type}
Machine Group : {machine_group}
Foundation    : {foundation_type}
Date          : {datetime.now().strftime('%d %b %Y %H:%M')}

EXECUTIVE SUMMARY
-----------------
Diagnosis     : {primary_fault['type']}
Confidence    : {primary_fault.get('confidence', 95)}%
Risk Level    : {risk_level}
Timeline      : {timeline}
MTBF Estimate : {mtbf_days} days

VIBRATION SEVERITY (ISO 10816-3:2001)
--------------------------------------
Zone          : {zone} ({iso_10816_3_status})
Max Velocity  : {max_velocity:.2f} mm/s
Direction     : {max_direction}
Machine Group : {machine_group}
Foundation    : {foundation_type}
Zone Limits   : A≤{zone_a_limit:.1f} | B≤{zone_b_limit:.1f} | C≤{zone_c_limit:.1f} mm/s

HYDRAULIC ANALYSIS (API 610 Clause 7.3)
----------------------------------------
BEP Flow      : {bep_flow:.1f} m³/hr
Actual Flow   : {actual_flow:.1f} m³/hr
BEP Deviation : {bep_deviation:.0f}%
NPSHa         : {npsha:.2f} m
NPSHr         : {npshr:.2f} m
NPSHa Margin  : {npsha_margin:.2f} m ({api_610_status})
Cavitation Risk: {cavitation_risk}

ELECTRICAL ANALYSIS (IEC 60034-1)
----------------------------------
Voltage R/S/T : {voltage_r}/{voltage_s}/{voltage_t} V
Voltage Imbalance: {v_imbalance:.1f}% ({iec_60034_1_status})
Current R/S/T : {current_r}/{current_s}/{current_t} A
Current Imbalance: {i_imbalance:.1f}%
Load Factor   : {load_factor:.0f}%
Motor Slip    : {slip_percent:.1f}%
FLC           : {flc} A
Actual RPM    : {actual_rpm} RPM

BEARING CONDITION (ISO 15243:2017)
-----------------------------------
Pump DE HF    : {hf_pump_de:.2f} g ({iso_15243_status})
Temp Rise     : {temp_rise_pump:.0f}°C
Temp Gradient : {pump_temp_gradient:.0f}°C

RECOMMENDED ACTIONS
-------------------
Risk Level    : {risk_level}
Timeline      : {timeline}
MTBF Estimate : {mtbf_days} days

Report Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Standards       : ISO 10816-3:2001, API 610 Ed.11, IEC 60034-1:2017, ISO 15243:2017
        """
        
        with col31:
            st.download_button(
                "📄 Download Full Report",
                report_text,
                file_name=f"pump_diagnostic_{asset_id}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col32:
            st.caption("Report includes compliance status integrated into each section")

# Footer
st.markdown("""
<div class="footer">
    <p>Pump Diagnostic System v2.2 | Pertamina Patra Niaga - Asset Integrity Management</p>
    <p>Standards: ISO 10816-3:2001, API 610 Ed.11, IEC 60034-1:2017, ISO 15243:2017, ISO 45001:2018</p>
    <p>© 2026 Pertamina Patra Niaga. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
