"""
Pump Diagnostic System - Pertamina Patra Niaga
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from engine.diagnostic_engine import PumpDiagnosticEngine
from report.report_generator import generate_text_report, generate_json_report, save_report

# Page configuration
st.set_page_config(
    page_title="🛢️ Pump Diagnostic System - Pertamina",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #262730;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize diagnostic engine
@st.cache_resource
def get_engine():
    return PumpDiagnosticEngine()

engine = get_engine()

# Main header
st.markdown('<p class="main-header">🛢️ Pump Diagnostic System</p>', unsafe_allow_html=True)
st.markdown("**Pertamina Patra Niaga - Asset Integrity Management**")
st.markdown("---")

# Sidebar for asset information
with st.sidebar:
    st.header("Asset Information")
    
    asset_id = st.text_input("Asset ID", "PPJ-BBM-P-101")
    location = st.text_input("Location", "Plaju Terminal")
    pump_type = st.selectbox("Pump Type", [
        "BBM Transfer Pump (300-500 kW)",
        "Crude Oil Pump (500-1000 kW)",
        "Other Product Pump"
    ])
    
    st.markdown("---")
    st.markdown("**Inspector Information**")
    inspector_name = st.text_input("Inspector Name", "Budi Santoso")
    inspector_id = st.text_input("Inspector ID", "INS-789")
    
    st.markdown("---")
    st.markdown("**Report Date**")
    report_date = st.date_input("Inspection Date", datetime.now())

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 Asset Specification", "📊 Field Measurements", 
                                    "📈 FFT Spectrum", "🔍 Diagnosis & Report"])

# ============================================
# TAB 1: Asset Specification
# ============================================
with tab1:
    st.markdown('<p class="sub-header">Motor Specifications</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        motor_kw = st.number_input("Motor Power (kW)", 1, 1000, 315, 
                                  help="From motor nameplate (IEC 60034-1)")
        motor_rpm = st.number_input("Motor RPM", 600, 3600, 1485,
                                   help="From motor nameplate")
        flc = st.number_input("Full Load Current (A)", 1, 2000, 545,
                             help="From motor nameplate - I_N value")
    
    with col2:
        voltage = st.number_input("Voltage (V)", 220, 660, 400,
                                 help="From motor nameplate")
        frequency = st.selectbox("Frequency (Hz)", [50, 60], index=0)
        foundation_type = st.radio(
            "**Foundation Type**",
            ["Rigid (Concrete)", "Flexible (Steel Structure)"],
            help="Rigid = concrete foundation, Flexible = steel structure"
        )
    
    st.markdown("---")
    st.markdown('<p class="sub-header">Pump Specifications</p>', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        bep_flow = st.number_input("BEP Flow (m³/hr)", 0.0, 1000.0, 120.0,
                                  help="From pump curve / MDS")
        bep_head = st.number_input("BEP Head (m)", 0.0, 200.0, 85.0,
                                  help="From pump curve / MDS")
    
    with col4:
        npshr = st.number_input("NPSHr (m)", 0.0, 20.0, 3.2,
                               help="From pump curve / MDS")
        bearing_size = st.selectbox("Bearing Size (Estimate)", [
            "Small Roller (<50mm shaft)",
            "Medium Roller (50-100mm shaft)",
            "Large Roller (>100mm shaft)",
            "Unknown (use default)"
        ], help="Visual estimate of shaft diameter")
    
    # Store in session state
    st.session_state.asset_spec = {
        "asset_id": asset_id,
        "location": location,
        "pump_type": pump_type,
        "motor_kw": motor_kw,
        "motor_rpm": motor_rpm,
        "flc": flc,
        "voltage": voltage,
        "frequency": frequency,
        "foundation_type": foundation_type,
        "bep_flow": bep_flow,
        "bep_head": bep_head,
        "npshr": npshr,
        "bearing_size": bearing_size
    }

# ============================================
# TAB 2: Field Measurements
# ============================================
with tab2:
    st.markdown('<p class="sub-header">Vibration Measurements (Adash Vibrio 4900)</p>', unsafe_allow_html=True)
    st.info("💡 **Note**: Measure DE (Drive End) and NDE (Non-Drive End) for each direction")
    
    # Motor vibration
    st.markdown("### Motor (Driver)")
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.markdown("**Horizontal**")
        motor_h_de = st.number_input("Motor H - DE (mm/s)", 0.0, 20.0, 1.24, key="m_h_de")
        motor_h_nde = st.number_input("Motor H - NDE (mm/s)", 0.0, 20.0, 1.20, key="m_h_nde")
    
    with col6:
        st.markdown("**Vertical**")
        motor_v_de = st.number_input("Motor V - DE (mm/s)", 0.0, 20.0, 0.55, key="m_v_de")
        motor_v_nde = st.number_input("Motor V - NDE (mm/s)", 0.0, 20.0, 0.54, key="m_v_nde")
    
    with col7:
        st.markdown("**Axial**")
        motor_a_de = st.number_input("Motor A - DE (mm/s)", 0.0, 20.0, 0.27, key="m_a_de")
        motor_a_nde = st.number_input("Motor A - NDE (mm/s)", 0.0, 20.0, 0.43, key="m_a_nde")
    
    # Pump vibration
    st.markdown("### Pump (Driven)")
    col8, col9, col10 = st.columns(3)
    
    with col8:
        st.markdown("**Horizontal**")
        pump_h_de = st.number_input("Pump H - DE (mm/s)", 0.0, 20.0, 1.07, key="p_h_de")
        pump_h_nde = st.number_input("Pump H - NDE (mm/s)", 0.0, 20.0, 0.69, key="p_h_nde")
    
    with col9:
        st.markdown("**Vertical**")
        pump_v_de = st.number_input("Pump V - DE (mm/s)", 0.0, 20.0, 2.11, key="p_v_de")
        pump_v_nde = st.number_input("Pump V - NDE (mm/s)", 0.0, 20.0, 0.95, key="p_v_nde")
    
    with col10:
        st.markdown("**Axial**")
        pump_a_de = st.number_input("Pump A - DE (mm/s)", 0.0, 20.0, 0.72, key="p_a_de")
        pump_a_nde = st.number_input("Pump A - NDE (mm/s)", 0.0, 20.0, 0.96, key="p_a_nde")
    
    st.markdown("---")
    st.markdown('<p class="sub-header">High Frequency Bands & Temperature</p>', unsafe_allow_html=True)
    
    col11, col12 = st.columns(2)
    
    with col11:
        st.markdown("### HF Bands 0.5-16 kHz (g)")
        hf_motor_de = st.number_input("Motor DE HF (g)", 0.0, 10.0, 0.3, key="hf_motor")
        hf_pump_de = st.number_input("Pump DE HF (g)", 0.0, 10.0, 0.9, key="hf_pump")
    
    with col12:
        st.markdown("### Bearing Temperature (°C)")
        temp_motor_de = st.number_input("Motor DE Temp", 0, 150, 65, key="tm_de")
        temp_motor_nde = st.number_input("Motor NDE Temp", 0, 150, 68, key="tm_nde")
        temp_pump_de = st.number_input("Pump DE Temp", 0, 150, 88, key="tp_de")
        temp_pump_nde = st.number_input("Pump NDE Temp", 0, 150, 72, key="tp_nde")
    
    st.markdown("---")
    st.markdown('<p class="sub-header">Hydraulic & Electrical Parameters</p>', unsafe_allow_html=True)
    
    col13, col14, col15 = st.columns(3)
    
    with col13:
        st.markdown("### Hydraulic")
        actual_flow = st.number_input("Actual Flow (m³/hr)", 0.0, 1000.0, 86.0)
        p_suc = st.number_input("Suction Pressure (bar g)", 0.0, 50.0, 2.8)
        p_dis = st.number_input("Discharge Pressure (bar g)", 0.0, 100.0, 10.5)
    
    with col14:
        st.markdown("### Electrical - Voltage (V)")
        voltage_r = st.number_input("Voltage R", 0.0, 1000.0, 402.0)
        voltage_s = st.number_input("Voltage S", 0.0, 1000.0, 389.0)
        voltage_t = st.number_input("Voltage T", 0.0, 1000.0, 405.0)
    
    with col15:
        st.markdown("### Electrical - Current (A)")
        current_r = st.number_input("Current R", 0.0, 1000.0, 498.0)
        current_s = st.number_input("Current S", 0.0, 1000.0, 502.0)
        current_t = st.number_input("Current T", 0.0, 1000.0, 495.0)
    
    # Store in session state
    st.session_state.field_data = {
        "motor_h_de": motor_h_de, "motor_h_nde": motor_h_nde,
        "motor_v_de": motor_v_de, "motor_v_nde": motor_v_nde,
        "motor_a_de": motor_a_de, "motor_a_nde": motor_a_nde,
        "pump_h_de": pump_h_de, "pump_h_nde": pump_h_nde,
        "pump_v_de": pump_v_de, "pump_v_nde": pump_v_nde,
        "pump_a_de": pump_a_de, "pump_a_nde": pump_a_nde,
        "hf_motor_de": hf_motor_de, "hf_pump_de": hf_pump_de,
        "temp_motor_de": temp_motor_de, "temp_motor_nde": temp_motor_nde,
        "temp_pump_de": temp_pump_de, "temp_pump_nde": temp_pump_nde,
        "actual_flow": actual_flow, "p_suc": p_suc, "p_dis": p_dis,
        "voltage_r": voltage_r, "voltage_s": voltage_s, "voltage_t": voltage_t,
        "current_r": current_r, "current_s": current_s, "current_t": current_t
    }

# ============================================
# TAB 3: FFT Spectrum
# ============================================
with tab3:
    st.markdown('<p class="sub-header">FFT Spectrum Analysis (Adash Vibrio 4900)</p>', unsafe_allow_html=True)
    
    st.info("""
    💡 **How to read from Vibrio 4900:**
    1. Set frequency range to 1-200 Hz
    2. Note the 3 top peaks shown on screen (e.g., "1. 25Hz → 2.0")
    3. Input both frequency (Hz) and amplitude (mm/s) for each peak
    """)
    
    col16, col17 = st.columns(2)
    
    with col16:
        st.markdown("### 1st Peak (Usually 1X)")
        peak1_freq = st.number_input("1st Peak Frequency (Hz)", 0.0, 200.0, 25.0, key="p1f")
        peak1_amp = st.number_input("1st Peak Amplitude (mm/s)", 0.0, 20.0, 2.0, key="p1a")
    
    with col17:
        st.markdown("### 2nd Peak (Usually 2X)")
        peak2_freq = st.number_input("2nd Peak Frequency (Hz)", 0.0, 200.0, 50.0, key="p2f")
        peak2_amp = st.number_input("2nd Peak Amplitude (mm/s)", 0.0, 20.0, 1.0, key="p2a")
    
    col18, col19 = st.columns(2)
    
    with col18:
        st.markdown("### 3rd Peak (Bearing Defect or 2LF)")
        peak3_freq = st.number_input("3rd Peak Frequency (Hz)", 0.0, 200.0, 76.0, key="p3f")
        peak3_amp = st.number_input("3rd Peak Amplitude (mm/s)", 0.0, 20.0, 0.7, key="p3a")
    
    with col19:
        st.markdown("### Additional Parameters")
        phase_instability = st.number_input("Phase Instability (°)", 0, 90, 30,
                                           help="Phase variation between measurements")
        displacement_peak = st.number_input("Displacement Peak (μm)", 0, 200, 68,
                                           help="Peak-to-peak displacement 2-100 Hz")
        demod_pump_de = st.number_input("Demodulation Pump DE (g)", 0.0, 10.0, 0.0,
                                       help="Optional: Only if HF >0.5g")
    
    # Store in session state
    st.session_state.fft_data = {
        "peak1_freq": peak1_freq, "peak1_amp": peak1_amp,
        "peak2_freq": peak2_freq, "peak2_amp": peak2_amp,
        "peak3_freq": peak3_freq, "peak3_amp": peak3_amp,
        "phase_instability": phase_instability,
        "displacement_peak": displacement_peak,
        "demod_pump_de": demod_pump_de
    }

# ============================================
# TAB 4: Diagnosis & Report
# ============================================
with tab4:
    st.markdown('<p class="sub-header">Diagnosis Results</p>', unsafe_allow_html=True)
    
    # Check if all data is available
    if 'asset_spec' not in st.session_state or 'field_data' not in st.session_state or 'fft_data' not in st.session_state:
        st.warning("⚠️ Please fill in all tabs (Asset Specification, Field Measurements, FFT Spectrum) before generating diagnosis.")
    else:
        # Combine all data
        input_data = {
            **st.session_state.asset_spec,
            **st.session_state.field_data,
            **st.session_state.fft_data
        }
        
        # Add calculated fields
        input_data["vibration_max_avr"] = max(
            (input_data["motor_h_de"] + input_data["motor_h_nde"]) / 2,
            (input_data["motor_v_de"] + input_data["motor_v_nde"]) / 2,
            (input_data["motor_a_de"] + input_data["motor_a_nde"]) / 2,
            (input_data["pump_h_de"] + input_data["pump_h_nde"]) / 2,
            (input_data["pump_v_de"] + input_data["pump_v_nde"]) / 2,
            (input_data["pump_a_de"] + input_data["pump_a_nde"]) / 2
        )
        
        # Run diagnosis
        if st.button("🔍 Generate Diagnosis", type="primary", use_container_width=True):
            with st.spinner("Analyzing data using 6-level diagnostic engine..."):
                diagnosis_result = engine.run_diagnosis(input_data)
            
            # Display results
            st.markdown("### 📊 Executive Summary")
            
            # Report type and summary
            report_type = diagnosis_result["report_type"]
            summary = diagnosis_result["summary"]
            
            if report_type == "EMERGENCY_SHUTDOWN":
                st.error(f"🚨 **{summary}**")
                st.markdown("**IMMEDIATE ACTION REQUIRED**")
            elif report_type == "COMPREHENSIVE_DIAGNOSIS":
                st.success(f"✅ **{summary}**")
                st.markdown(f"**Confidence: {diagnosis_result['audit_trail']['confidence_score']:.0f}%**")
            else:
                st.info(f"ℹ️ **{summary}**")
            
            st.markdown("---")
            
            # Level 2: Severity Classification
            if "level_2_severity" in diagnosis_result:
                zone_result = diagnosis_result["level_2_severity"]
                averages = diagnosis_result.get("averages", {})
                
                st.markdown("### 📏 Vibration Severity (ISO 10816-3:2001)")
                
                col20, col21, col22 = st.columns(3)
                
                with col20:
                    zone_color = zone_result.get("status_color", "info")
                    if zone_color == "success":
                        st.success(f"Zone {zone_result['zone']}")
                    elif zone_color == "warning":
                        st.warning(f"Zone {zone_result['zone']}")
                    elif zone_color == "error":
                        st.error(f"Zone {zone_result['zone']}")
                    else:
                        st.info(f"Zone {zone_result['zone']}")
                
                with col21:
                    max_velocity = averages.get("max_velocity", 0)
                    st.metric("Max Velocity", f"{max_velocity:.2f} mm/s")
                
                with col22:
                    max_direction = averages.get("max_direction", "Unknown")
                    st.metric("Direction", max_direction)
                
                st.caption(f"Foundation: {zone_result.get('foundation_type', 'Unknown')}")
                st.caption(f"Zone B Limit: {zone_result.get('limit_b', 0):.1f} mm/s | Zone C Limit: {zone_result.get('limit_c', 0):.1f} mm/s")
                st.caption(f"Standard: {zone_result.get('standard', 'Unknown')}")
            
            st.markdown("---")
            
            # Level 5: Primary Diagnosis
            if "level_5_bayesian" in diagnosis_result:
                bayesian = diagnosis_result["level_5_bayesian"]
                
                st.markdown("### 🔍 Primary Diagnosis (Bayesian Fusion)")
                
                st.success(f"**{bayesian.get('primary_fault', 'Unknown')}**")
                confidence = bayesian.get('primary_confidence', 0)
                st.progress(int(confidence))
                st.caption(f"Confidence: {confidence:.0f}%")
                st.caption(f"Evidence: {bayesian.get('evidence_summary', 'No evidence available')}")
                
                if bayesian.get("secondary_faults"):
                    with st.expander("Secondary Faults"):
                        for fault in bayesian["secondary_faults"][:2]:
                            fault_type = fault.get('fault_type', 'Unknown')
                            posterior_prob = fault.get('posterior_probability', 0)
                            st.write(f"• {fault_type} ({posterior_prob:.0f}% confidence)")
            
            st.markdown("---")
            
            # Bearing Condition
            if "bearing_condition" in diagnosis_result:
                bearing = diagnosis_result["bearing_condition"]
                
                st.markdown("### ⚙️ Bearing Condition (ISO 15243:2017)")
                
                col23, col24, col25 = st.columns(3)
                
                with col23:
                    stage = bearing.get('stage', 0)
                    st.metric("Stage", f"{stage}")
                
                with col24:
                    hf_value = bearing.get('hf_value', 0)
                    st.metric("HF 5-16 kHz", f"{hf_value:.2f} g")
                
                with col25:
                    temp_rise = bearing.get('temp_rise', 0)
                    st.metric("Temp Rise", f"{temp_rise:.0f}°C")
                
                condition = bearing.get('condition', 'Unknown')
                st.info(f"**Condition**: {condition}")
                recommendation = bearing.get('recommendation', 'No recommendation')
                st.caption(f"Recommendation: {recommendation}")
            
            st.markdown("---")
            
            # Level 6: Action Plan
            if "level_6_risk" in diagnosis_result:
                risk = diagnosis_result["level_6_risk"]
                
                st.markdown("### ✅ Recommended Actions (ISO 45001 Risk-Based)")
                
                col26, col27, col28 = st.columns(3)
                
                with col26:
                    risk_level = risk.get('risk_level', 'Unknown')
                    risk_color = "🔴" if risk_level == "CRITICAL" else "🟠" if risk_level == "HIGH" else "🟡" if risk_level == "MEDIUM" else "🟢"
                    st.metric("Risk Level", f"{risk_color} {risk_level}")
                
                with col27:
                    mtbf_days = risk.get('mtbf_days', 0)
                    st.metric("MTBF Estimation", f"{mtbf_days} days")
                
                with col28:
                    action_timeline = risk.get('action_timeline', 'Unknown')
                    st.metric("Timeline", action_timeline)
                
                st.markdown("**Action Items:**")
                recommendations = risk.get("recommendations", [])
                for i, rec in enumerate(recommendations, 1):
                    priority = rec.get('priority', 'Unknown')
                    priority_emoji = "🔴" if priority == "CRITICAL" else "🟠" if priority == "HIGH" else "🟡" if priority == "MEDIUM" else "🟢" if priority == "LOW" else "🔵"
                    action = rec.get('action', 'No action')
                    timeline = rec.get('timeline', 'Unknown')
                    
                    with st.expander(f"{priority_emoji} {i}. {action} ({timeline})"):
                        details = rec.get('details', 'No details')
                        st.write(f"**Details:** {details}")
                        standard = rec.get('standard', 'No standard')
                        st.write(f"**Standard:** {standard}")
            
            st.markdown("---")
            
            # Compliance Status
            if "compliance" in diagnosis_result:
                comp = diagnosis_result["compliance"]
                
                st.markdown("### 📋 Compliance Status (AIM-004 Format)")
                
                col29, col30, col31, col32 = st.columns(4)
                
                with col29:
                    iso_10816_3 = comp.get('iso_10816_3', 'Unknown')
                    iso_status = "✅" if iso_10816_3 == "COMPLIANT" else "⚠️" if iso_10816_3 == "WARNING" else "❌"
                    st.metric("ISO 10816-3", f"{iso_status} {iso_10816_3}")
                
                with col30:
                    iec_60034_1 = comp.get('iec_60034_1', 'Unknown')
                    iec_status = "✅" if iec_60034_1 == "COMPLIANT" else "❌"
                    st.metric("IEC 60034-1", f"{iec_status} {iec_60034_1}")
                
                with col31:
                    api_610 = comp.get('api_610', 'Unknown')
                    api_status = "✅" if api_610 == "COMPLIANT" else "⚠️" if api_610 == "WARNING" else "❌"
                    st.metric("API 610", f"{api_status} {api_610}")
                
                with col32:
                    iso_15243 = comp.get('iso_15243', 'Unknown')
                    iso15243_status = "✅" if iso_15243 == "COMPLIANT" else "⚠️" if iso_15243 == "WARNING" else "❌"
                    st.metric("ISO 15243", f"{iso15243_status} {iso_15243}")
                
                overall_status = comp.get('overall_status', 'Unknown')
                overall_emoji = "✅ COMPLIANT" if overall_status == "COMPLIANT" else "❌ NON-COMPLIANT"
                st.metric("Overall Status", overall_emoji)
            
            st.markdown("---")
            
            # Export Report
            st.markdown("### 📥 Export Report")
            
            col33, col34 = st.columns(2)
            
            with col33:
                if st.button("📄 Generate Text Report"):
                    asset_info = st.session_state.asset_spec
                    report_text = generate_text_report(diagnosis_result, asset_info)
                    
                    st.download_button(
                        label="⬇️ Download Text Report",
                        data=report_text,
                        file_name=f"pump_diagnostic_{asset_info.get('asset_id', 'UNKNOWN')}_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
            
            with col34:
                if st.button("📊 Generate JSON Report"):
                    asset_info = st.session_state.asset_spec
                    report_json = generate_json_report(diagnosis_result, asset_info)
                    
                    st.download_button(
                        label="⬇️ Download JSON Report",
                        data=report_json,
                        file_name=f"pump_diagnostic_{asset_info.get('asset_id', 'UNKNOWN')}_{datetime.now().strftime('%Y%m%d')}.json",
                        mime="application/json"
                    )
            
            # Store diagnosis result in session state
            st.session_state.diagnosis_result = diagnosis_result

# Footer
st.markdown("---")
st.markdown("**Pump Diagnostic System v1.0** | Pertamina Patra Niaga - Asset Integrity Management")
st.markdown("Developed with ❤️ using Streamlit | Standards: ISO 10816-3, API 610, IEC 60034-1, ISO 15243, ISO 45001")
