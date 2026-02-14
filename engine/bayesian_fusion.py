"""
Level 5: Bayesian Fusion
ISO 13381-1 Clause 7 - Probabilistic fault diagnosis
"""

def bayesian_fusion(validated_faults, data):
    """
    Calculate posterior probability using Bayesian inference
    
    Parameters:
    -----------
    validated_faults : list
        List of validated faults from cross-validation
    data : dict
        Dictionary containing all measurement data
    
    Returns:
    --------
    dict : Bayesian fusion result with posterior probabilities
    """
    # Conditional Probability Table (CPT) based on industry data
    # P(Evidence | Fault) - Likelihood of evidence given fault
    cpt = {
        "ELECTRICAL_UNBALANCE": {
            "2lf_dominant": 0.95,
            "v_imbalance>2%": 0.92,
            "phase_unstable": 0.88,
            "hf_normal": 0.85,
            "temp_normal": 0.80,
            "1x_not_dominant": 0.75
        },
        "MECHANICAL_UNBALANCE": {
            "1x_dominant": 0.94,
            "phase_stable": 0.90,
            "v_imbalance<2%": 0.85,
            "hf_normal": 0.80,
            "temp_normal": 0.75,
            "displacement_correlated": 0.70
        },
        "BEARING_DEFECT": {
            "hf>0.7g": 0.96,
            "bpfo_peak": 0.93,
            "temp_rise>40C": 0.90,
            "v_imbalance<2%": 0.85,
            "1x_not_dominant": 0.80,
            "temp_gradient>15C": 0.75
        },
        "MISALIGNMENT": {
            "2x_dominant": 0.92,
            "axial_dominant": 0.88,
            "v_imbalance<2%": 0.85,
            "temp_gradient>10C": 0.80,
            "phase_unstable": 0.75
        }
    }
    
    fault_probabilities = []
    
    for fault in validated_faults:
        fault_type = fault["type"]
        likelihood = 1.0
        evidence_list = []
        
        # === ELECTRICAL UNBALANCE BAYESIAN CALCULATION ===
        if "ELECTRICAL_UNBALANCE" in fault_type:
            # Evidence 1: 2×Line Frequency dominant
            peak3_freq = data.get("peak3_freq", 0)
            peak3_amp = data.get("peak3_amp", 0)
            peak1_amp = data.get("peak1_amp", 0)
            is_2lf = abs(peak3_freq - 100.0) < 5.0
            is_2lf_dominant = is_2lf and peak3_amp > 0.5 * peak1_amp
            
            if is_2lf_dominant:
                likelihood *= cpt["ELECTRICAL_UNBALANCE"]["2lf_dominant"]
                evidence_list.append("2LF dominant")
            
            # Evidence 2: Voltage imbalance >2%
            v_r = data.get("voltage_r", 400)
            v_s = data.get("voltage_s", 400)
            v_t = data.get("voltage_t", 400)
            v_avg = (v_r + v_s + v_t) / 3
            v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
            
            if v_imbalance > 2.0:
                likelihood *= cpt["ELECTRICAL_UNBALANCE"]["v_imbalance>2%"]
                evidence_list.append(f"V imbalance {v_imbalance:.1f}%")
            
            # Evidence 3: Phase instability
            phase_instability = data.get("phase_instability", 30)
            if phase_instability > 20:
                likelihood *= cpt["ELECTRICAL_UNBALANCE"]["phase_unstable"]
                evidence_list.append(f"Phase unstable ±{phase_instability}°")
            
            # Evidence 4: HF bands normal
            hf_pump_de = data.get("hf_pump_de", 0)
            if hf_pump_de < 0.7:
                likelihood *= cpt["ELECTRICAL_UNBALANCE"]["hf_normal"]
                evidence_list.append(f"HF {hf_pump_de:.2f}g normal")
            
            # Evidence 5: Temperature normal
            temp_pump_de = data.get("temp_pump_de", 0)
            ambient = 35
            temp_rise = temp_pump_de - ambient
            if temp_rise < 40:
                likelihood *= cpt["ELECTRICAL_UNBALANCE"]["temp_normal"]
                evidence_list.append(f"Temp rise {temp_rise:.0f}°C normal")
        
        # === MECHANICAL UNBALANCE BAYESIAN CALCULATION ===
        elif "MECHANICAL_UNBALANCE" in fault_type:
            # Evidence 1: 1X dominant
            peak1_freq = data.get("peak1_freq", 0)
            rpm = data.get("motor_rpm", 1500)
            fundamental = rpm / 60
            peak1_amp = data.get("peak1_amp", 0)
            peak2_amp = data.get("peak2_amp", 0)
            peak3_amp = data.get("peak3_amp", 0)
            total_rms = peak1_amp + peak2_amp + peak3_amp
            peak1_ratio = peak1_amp / total_rms if total_rms > 0 else 0
            
            is_1x_dominant = (abs(peak1_freq - fundamental) < 0.1 * fundamental and
                            peak1_ratio > 0.80)
            
            if is_1x_dominant:
                likelihood *= cpt["MECHANICAL_UNBALANCE"]["1x_dominant"]
                evidence_list.append("1X dominant")
            
            # Evidence 2: Phase stable
            phase_instability = data.get("phase_instability", 5)
            if phase_instability < 10:
                likelihood *= cpt["MECHANICAL_UNBALANCE"]["phase_stable"]
                evidence_list.append(f"Phase stable ±{phase_instability}°")
            
            # Evidence 3: Voltage imbalance normal
            v_r = data.get("voltage_r", 400)
            v_s = data.get("voltage_s", 400)
            v_t = data.get("voltage_t", 400)
            v_avg = (v_r + v_s + v_t) / 3
            v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
            
            if v_imbalance < 2.0:
                likelihood *= cpt["MECHANICAL_UNBALANCE"]["v_imbalance<2%"]
                evidence_list.append(f"V imbalance {v_imbalance:.1f}% normal")
            
            # Evidence 4: HF bands normal
            hf_pump_de = data.get("hf_pump_de", 0)
            if hf_pump_de < 0.7:
                likelihood *= cpt["MECHANICAL_UNBALANCE"]["hf_normal"]
                evidence_list.append(f"HF {hf_pump_de:.2f}g normal")
        
        # === BEARING DEFECT BAYESIAN CALCULATION ===
        elif "BEARING_DEFECT" in fault_type:
            # Evidence 1: HF >0.7g
            hf_pump_de = data.get("hf_pump_de", 0)
            if hf_pump_de > 0.7:
                likelihood *= cpt["BEARING_DEFECT"]["hf>0.7g"]
                evidence_list.append(f"HF {hf_pump_de:.2f}g high")
            
            # Evidence 2: BPFO peak (non-harmonic frequency)
            peak3_freq = data.get("peak3_freq", 0)
            rpm = data.get("motor_rpm", 1500)
            fundamental = rpm / 60
            second_harmonic = 2 * fundamental
            third_harmonic = 3 * fundamental
            
            is_bpfo = (peak3_freq > 50 and 
                      abs(peak3_freq - fundamental) > 0.2 * fundamental and
                      abs(peak3_freq - second_harmonic) > 0.2 * second_harmonic)
            
            if is_bpfo:
                likelihood *= cpt["BEARING_DEFECT"]["bpfo_peak"]
                evidence_list.append(f"BPFO peak {peak3_freq:.1f}Hz")
            
            # Evidence 3: Temperature rise >40°C
            temp_pump_de = data.get("temp_pump_de", 0)
            ambient = 35
            temp_rise = temp_pump_de - ambient
            
            if temp_rise > 40:
                likelihood *= cpt["BEARING_DEFECT"]["temp_rise>40C"]
                evidence_list.append(f"Temp rise {temp_rise:.0f}°C")
            
            # Evidence 4: Voltage imbalance normal
            v_r = data.get("voltage_r", 400)
            v_s = data.get("voltage_s", 400)
            v_t = data.get("voltage_t", 400)
            v_avg = (v_r + v_s + v_t) / 3
            v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
            
            if v_imbalance < 2.0:
                likelihood *= cpt["BEARING_DEFECT"]["v_imbalance<2%"]
                evidence_list.append(f"V imbalance {v_imbalance:.1f}% normal")
        
        # Normalize to 0-95% range
        posterior = min(likelihood * 100, 95)
        
        fault_probabilities.append({
            "fault_type": fault_type,
            "posterior_probability": posterior,
            "likelihood": likelihood,
            "evidence_count": len(evidence_list),
            "evidence_list": evidence_list,
            "bayes_explanation": f"Likelihood = {likelihood:.3f} based on {len(evidence_list)} consistent parameters",
            "standard": "ISO 13381-1 Clause 7.3 (Remaining life estimation)"
        })
    
    # Sort by posterior probability (highest first)
    fault_probabilities.sort(key=lambda x: x["posterior_probability"], reverse=True)
    
    # Get primary fault
    primary_fault = fault_probabilities[0] if fault_probabilities else None
    
    return {
        "primary_fault": primary_fault["fault_type"] if primary_fault else "NO_FAULT_DETECTED",
        "primary_confidence": primary_fault["posterior_probability"] if primary_fault else 0,
        "secondary_faults": fault_probabilities[1:] if len(fault_probabilities) > 1 else [],
        "all_probabilities": fault_probabilities,
        "evidence_summary": f"{primary_fault['evidence_count']} consistent parameters" if primary_fault else "No fault detected",
        "standard": "ISO 13381-1:2021 Clause 7 (Prognostics methodology)"
    }
