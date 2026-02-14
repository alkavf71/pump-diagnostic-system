"""
Level 4: Cross-Validation
Multi-parameter consistency check to avoid false positives
"""

def cross_validate_faults(primary_faults, data):
    """
    Validate fault consistency across multiple parameters
    
    Parameters:
    -----------
    primary_faults : list
        List of primary faults from FFT analysis
    data : dict
        Dictionary containing all measurement data
    
    Returns:
    --------
    list : Validated faults with consistency scores
    """
    validated_faults = []
    
    for fault in primary_faults:
        consistency_score = 0
        consistency_evidence = []
        inconsistencies = []
        
        fault_type = fault["type"]
        
        # === VALIDATION FOR ELECTRICAL UNBALANCE ===
        if "ELECTRICAL_UNBALANCE" in fault_type:
            # Validation 1: Voltage imbalance must be present
            v_r = data.get("voltage_r", 400)
            v_s = data.get("voltage_s", 400)
            v_t = data.get("voltage_t", 400)
            v_avg = (v_r + v_s + v_t) / 3
            v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
            
            if v_imbalance > 2.0:
                consistency_score += 0.4
                consistency_evidence.append(f"✓ Voltage imbalance {v_imbalance:.1f}% confirmed (>2% limit)")
            else:
                inconsistencies.append(f"✗ Voltage imbalance only {v_imbalance:.1f}% (<2% limit)")
            
            # Validation 2: Temperature gradient should be normal (not bearing defect)
            temp_pump_de = data.get("temp_pump_de", 0)
            temp_pump_nde = data.get("temp_pump_nde", 0)
            temp_gradient = abs(temp_pump_de - temp_pump_nde)
            
            if temp_gradient < 15:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Temperature gradient {temp_gradient:.0f}°C normal (<15°C)")
            else:
                inconsistencies.append(f"✗ Temperature gradient {temp_gradient:.0f}°C high - possible bearing defect")
            
            # Validation 3: Phase instability should be present
            phase_instability = data.get("phase_instability", 30)
            if phase_instability > 20:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Phase instability ±{phase_instability:.0f}° confirmed")
            else:
                inconsistencies.append(f"✗ Phase stability ±{phase_instability:.0f}° - unexpected for electrical fault")
        
        # === VALIDATION FOR MECHANICAL UNBALANCE ===
        elif "MECHANICAL_UNBALANCE" in fault_type:
            # Validation 1: Voltage imbalance should be normal
            v_r = data.get("voltage_r", 400)
            v_s = data.get("voltage_s", 400)
            v_t = data.get("voltage_t", 400)
            v_avg = (v_r + v_s + v_t) / 3
            v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
            
            if v_imbalance < 2.0:
                consistency_score += 0.4
                consistency_evidence.append(f"✓ Voltage imbalance {v_imbalance:.1f}% normal (<2% limit)")
            else:
                inconsistencies.append(f"✗ Voltage imbalance {v_imbalance:.1f}% high - possible electrical fault")
            
            # Validation 2: Phase should be stable
            phase_instability = data.get("phase_instability", 5)
            if phase_instability < 10:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Phase stability ±{phase_instability:.0f}° confirmed")
            else:
                inconsistencies.append(f"✗ Phase instability ±{phase_instability:.0f}° - unexpected for mechanical fault")
            
            # Validation 3: Displacement should correlate with velocity
            pump_v_avr = (data.get("pump_v_de", 0) + data.get("pump_v_nde", 0)) / 2
            displacement_peak = data.get("displacement_peak", 0)
            
            # Rough correlation check (displacement ≈ velocity / (2πf))
            rpm = data.get("motor_rpm", 1500)
            freq_hz = rpm / 60
            expected_displacement = pump_v_avr / (2 * 3.1416 * freq_hz) * 1000  # μm
            
            if abs(displacement_peak - expected_displacement) < expected_displacement * 0.5:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Displacement {displacement_peak:.0f}μm correlates with velocity")
            else:
                inconsistencies.append(f"✗ Displacement {displacement_peak:.0f}μm doesn't correlate with velocity")
        
        # === VALIDATION FOR BEARING DEFECT ===
        elif "BEARING_DEFECT" in fault_type:
            # Validation 1: HF bands must be high
            hf_pump_de = data.get("hf_pump_de", 0)
            if hf_pump_de > 0.7:
                consistency_score += 0.4
                consistency_evidence.append(f"✓ HF 5-16 kHz = {hf_pump_de:.2f}g > 0.7g threshold")
            else:
                inconsistencies.append(f"✗ HF 5-16 kHz = {hf_pump_de:.2f}g normal (<0.7g)")
            
            # Validation 2: Temperature rise should be present
            ambient = 35  # Assume ambient temperature for BBM terminal
            temp_pump_de = data.get("temp_pump_de", 0)
            temp_rise = temp_pump_de - ambient
            
            if temp_rise > 40:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Bearing temp rise {temp_rise:.0f}°C >40°C limit")
            else:
                consistency_evidence.append(f"○ Bearing temp rise {temp_rise:.0f}°C normal")
            
            # Validation 3: Voltage imbalance should be normal
            v_r = data.get("voltage_r", 400)
            v_s = data.get("voltage_s", 400)
            v_t = data.get("voltage_t", 400)
            v_avg = (v_r + v_s + v_t) / 3
            v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
            
            if v_imbalance < 2.0:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Voltage imbalance {v_imbalance:.1f}% normal")
            else:
                inconsistencies.append(f"✗ Voltage imbalance {v_imbalance:.1f}% high")
        
        # === VALIDATION FOR MISALIGNMENT ===
        elif "MISALIGNMENT" in fault_type:
            # Validation 1: 2X should be dominant
            peak2_amp = data.get("peak2_amp", 0)
            peak1_amp = data.get("peak1_amp", 0)
            peak2_ratio = peak2_amp / peak1_amp if peak1_amp > 0 else 0
            
            if peak2_ratio > 0.5:
                consistency_score += 0.4
                consistency_evidence.append(f"✓ 2X/1X ratio = {peak2_ratio:.2f} > 0.5 threshold")
            else:
                inconsistencies.append(f"✗ 2X/1X ratio = {peak2_ratio:.2f} < 0.5 threshold")
            
            # Validation 2: Axial vibration should be high for angular misalignment
            pump_a_avr = (data.get("pump_a_de", 0) + data.get("pump_a_nde", 0)) / 2
            pump_v_avr = (data.get("pump_v_de", 0) + data.get("pump_v_nde", 0)) / 2
            
            if "ANGULAR" in fault_type and pump_a_avr > pump_v_avr:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Axial vibration {pump_a_avr:.2f} mm/s > radial {pump_v_avr:.2f} mm/s")
            elif "PARALLEL" in fault_type and pump_a_avr < pump_v_avr:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Radial vibration dominant (parallel misalignment)")
            else:
                inconsistencies.append(f"✗ Vibration pattern doesn't match misalignment type")
            
            # Validation 3: Temperature gradient may be present
            temp_pump_de = data.get("temp_pump_de", 0)
            temp_pump_nde = data.get("temp_pump_nde", 0)
            temp_gradient = abs(temp_pump_de - temp_pump_nde)
            
            if temp_gradient > 10:
                consistency_score += 0.3
                consistency_evidence.append(f"✓ Temperature gradient {temp_gradient:.0f}°C present")
            else:
                consistency_evidence.append(f"○ Temperature gradient {temp_gradient:.0f}°C normal")
        
        # Calculate final confidence with consistency adjustment
        original_confidence = fault["confidence"]
        adjusted_confidence = original_confidence * (0.7 + consistency_score * 0.3)
        
        validated_faults.append({
            "type": fault_type,
            "original_confidence": original_confidence,
            "consistency_score": consistency_score,
            "final_confidence": min(adjusted_confidence, 0.95),  # Cap at 95%
            "consistency_evidence": consistency_evidence,
            "inconsistencies": inconsistencies,
            "is_validated": consistency_score >= 0.6,
            "standard": fault["standard"],
            "severity": fault["severity"]
        })
    
    # Sort by final confidence (highest first)
    validated_faults.sort(key=lambda x: x["final_confidence"], reverse=True)
    
    return validated_faults
