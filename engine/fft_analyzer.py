"""
Level 3: FFT Signature Detection
ISO 13373-2 Clause 5.4 - Frequency domain analysis
"""

def detect_fft_signatures(data):
    """
    Detect fault signatures from FFT peaks (frequency + amplitude)
    
    Parameters:
    -----------
    data : dict
        Dictionary containing FFT peak data and machine parameters
    
    Returns:
    --------
    list : List of detected faults with confidence scores
    """
    faults = []
    
    # Extract FFT data
    peak1_freq = data.get("peak1_freq", 0)
    peak1_amp = data.get("peak1_amp", 0)
    peak2_freq = data.get("peak2_freq", 0)
    peak2_amp = data.get("peak2_amp", 0)
    peak3_freq = data.get("peak3_freq", 0)
    peak3_amp = data.get("peak3_amp", 0)
    rpm = data.get("motor_rpm", 1500)
    
    # Calculate expected frequencies
    fundamental = rpm / 60          # 1X frequency (Hz)
    second_harmonic = 2 * fundamental  # 2X frequency (Hz)
    third_harmonic = 3 * fundamental   # 3X frequency (Hz)
    line_freq_2x = 100.0             # 2×Line Frequency (50 Hz system)
    
    # Calculate ratios
    total_rms = peak1_amp + peak2_amp + peak3_amp
    peak1_ratio = peak1_amp / total_rms if total_rms > 0 else 0
    peak2_ratio = peak2_amp / peak1_amp if peak1_amp > 0 else 0
    peak3_ratio = peak3_amp / peak1_amp if peak1_amp > 0 else 0
    
    # === DETECTION 1: ELECTRICAL UNBALANCE ===
    # Check if peak3 is near 2×Line Frequency (100 Hz)
    is_2lf_dominant = (abs(peak3_freq - line_freq_2x) < 5.0 and 
                      peak3_amp > 0.5 * peak1_amp)
    
    # Check voltage imbalance
    v_r = data.get("voltage_r", 400)
    v_s = data.get("voltage_s", 400)
    v_t = data.get("voltage_t", 400)
    v_avg = (v_r + v_s + v_t) / 3
    v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
    
    is_v_imbalance = v_imbalance > 2.0
    
    if is_2lf_dominant and is_v_imbalance:
        faults.append({
            "type": "ELECTRICAL_UNBALANCE",
            "confidence": 0.92,
            "primary_evidence": f"2×Line Freq dominant at {peak3_freq:.1f} Hz ({peak3_amp:.1f} mm/s)",
            "secondary_evidence": [
                f"2LF/1X ratio = {peak3_ratio:.2f} > 0.5 threshold",
                f"Voltage imbalance {v_imbalance:.1f}% > 2% limit (IEC 60034-1 §6.3)",
                "Phase instability expected (electrical origin)"
            ],
            "standard": "ISO 13373-2 Clause 5.4.3 + NEMA MG-1 §14.32",
            "severity": "WARNING"
        })
    
    # === DETECTION 2: MECHANICAL UNBALANCE ===
    is_1x_dominant = (abs(peak1_freq - fundamental) < 0.1 * fundamental and
                     peak1_ratio > 0.80)
    
    # Assume phase stability if not electrical unbalance
    is_phase_stable = not is_2lf_dominant
    
    if is_1x_dominant and is_phase_stable and not is_v_imbalance:
        faults.append({
            "type": "MECHANICAL_UNBALANCE",
            "confidence": 0.88,
            "primary_evidence": f"1X dominant at {peak1_freq:.1f} Hz ({peak1_amp:.1f} mm/s, {peak1_ratio*100:.0f}% RMS)",
            "secondary_evidence": [
                f"1X/Total RMS ratio = {peak1_ratio:.2f} > 0.80 threshold",
                "Phase stability confirmed (mechanical origin)",
                f"Fundamental frequency = {fundamental:.2f} Hz (RPM/60)"
            ],
            "standard": "ISO 1940-1:2003 G2.5",
            "severity": "WARNING"
        })
    
    # === DETECTION 3: MISALIGNMENT ===
    is_2x_dominant = (abs(peak2_freq - second_harmonic) < 0.1 * second_harmonic and
                     peak2_ratio > 0.50)
    
    # Check axial vs radial vibration
    pump_a_avr = (data.get("pump_a_de", 0) + data.get("pump_a_nde", 0)) / 2
    pump_v_avr = (data.get("pump_v_de", 0) + data.get("pump_v_nde", 0)) / 2
    is_axial_dominant = pump_a_avr > 0.7 * pump_v_avr
    
    if is_2x_dominant:
        alignment_type = "ANGULAR" if is_axial_dominant else "PARALLEL"
        faults.append({
            "type": f"{alignment_type}_MISALIGNMENT",
            "confidence": 0.85,
            "primary_evidence": f"2X dominant at {peak2_freq:.1f} Hz ({peak2_amp:.1f} mm/s)",
            "secondary_evidence": [
                f"2X/1X ratio = {peak2_ratio:.2f} > 0.5 threshold",
                f"{'Axial' if alignment_type == 'ANGULAR' else 'Radial'} vibration dominant",
                f"2X frequency = {second_harmonic:.2f} Hz (2×RPM/60)"
            ],
            "standard": "API 671 Clause 5.3",
            "severity": "WARNING"
        })
    
    # === DETECTION 4: BEARING DEFECT ===
    hf_pump_de = data.get("hf_pump_de", 0)
    is_hf_high = hf_pump_de > 0.7  # g RMS
    
    # Temperature gradient analysis
    temp_pump_de = data.get("temp_pump_de", 0)
    temp_pump_nde = data.get("temp_pump_nde", 0)
    temp_gradient = abs(temp_pump_de - temp_pump_nde)
    is_temp_gradient_high = temp_gradient > 15  # °C
    
    # Check if peak3 is bearing defect frequency (not harmonic)
    is_bpfo_candidate = (peak3_freq > 50 and 
                        abs(peak3_freq - fundamental) > 0.2 * fundamental and
                        abs(peak3_freq - second_harmonic) > 0.2 * second_harmonic and
                        abs(peak3_freq - third_harmonic) > 0.2 * third_harmonic)
    
    if is_hf_high and (is_bpfo_candidate or is_temp_gradient_high):
        faults.append({
            "type": "BEARING_DEFECT",
            "confidence": 0.87,
            "primary_evidence": f"HF 5-16 kHz = {hf_pump_de:.2f}g > 0.7g threshold",
            "secondary_evidence": [
                f"Peak3 at {peak3_freq:.1f} Hz (BPFO candidate - non-harmonic)",
                f"Temperature gradient DE-NDE = {temp_gradient:.0f}°C >15°C",
                "High frequency bands indicate bearing defect (ISO 15243)"
            ],
            "standard": "ISO 15243:2017 Table 2 (Stage 2 defect)",
            "severity": "WARNING"
        })
    
    # === DETECTION 5: CAVITATION ===
    p_suc = data.get("p_suc", 0)
    p_dis = data.get("p_dis", 0)
    actual_flow = data.get("actual_flow", 0)
    bep_flow = data.get("bep_flow", 100)
    npshr = data.get("npshr", 3.0)
    
    # Calculate NPSHa (simplified for BBM)
    npsha = p_suc + 10.33 - 0.5  # Approximation for BBM
    npsha_margin = npsha - npshr
    
    # Calculate BEP deviation
    bep_deviation = abs(actual_flow - bep_flow) / bep_flow * 100 if bep_flow > 0 else 0
    
    is_cavitation_risk = npsha_margin < 0.6 and bep_deviation > 20
    
    if is_cavitation_risk:
        faults.append({
            "type": "CAVITATION",
            "confidence": 0.80,
            "primary_evidence": f"NPSHa margin = {npsha_margin:.2f}m < 0.6m safety margin",
            "secondary_evidence": [
                f"BEP deviation = {bep_deviation:.0f}% > 20% limit",
                "Operating outside Best Efficiency Point",
                "Cavitation risk increases bearing load"
            ],
            "standard": "API 610 Clause 7.3.2",
            "severity": "WARNING"
        })
    
    # Sort by confidence (highest first)
    faults.sort(key=lambda x: x["confidence"], reverse=True)
    
    return faults


def analyze_bearing_condition(hf_value, temp_rise, demod_value=0):
    """
    Analyze bearing condition based on HF bands and temperature
    
    Parameters:
    -----------
    hf_value : float
        HF 5-16 kHz value in g RMS
    temp_rise : float
        Temperature rise above ambient in °C
    demod_value : float
        Demodulation envelope value in g (optional)
    
    Returns:
    --------
    dict : Bearing condition assessment
    """
    # ISO 15243:2017 bearing defect stages
    if hf_value < 0.3:
        stage = 0
        condition = "NORMAL"
        recommendation = "Continue routine monitoring"
    elif hf_value < 0.7:
        stage = 1
        condition = "EARLY STAGE"
        recommendation = "Monitor closely - defect incipient"
    elif hf_value < 1.5:
        stage = 2
        condition = "MODERATE DEFECT"
        recommendation = "Plan replacement within 30 days"
    else:
        stage = 3
        condition = "SEVERE DEFECT"
        recommendation = "Replace immediately - failure imminent"
    
    # Adjust based on temperature rise
    if temp_rise > 60:
        condition += " + OVERHEATING"
        recommendation = "URGENT: Replace bearing and check lubrication"
    
    # Adjust based on demodulation (if available)
    if demod_value > 0.5:
        condition += " + IMPACT DETECTED"
        recommendation += " - Demodulation confirms defect"
    
    return {
        "stage": stage,
        "condition": condition,
        "hf_value": hf_value,
        "temp_rise": temp_rise,
        "demod_value": demod_value,
        "recommendation": recommendation,
        "standard": "ISO 15243:2017 Table 2"
    }
