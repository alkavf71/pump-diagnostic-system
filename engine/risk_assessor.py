"""
Level 6: Risk Assessment & Action Plan
ISO 45001 Annex A + API 581 RBI Methodology
"""

def assess_risk_and_generate_plan(diagnosis, data):
    """
    Assess risk level and generate action plan with timeline
    
    Parameters:
    -----------
    diagnosis : dict
        Bayesian fusion diagnosis result
    data : dict
        Dictionary containing all measurement data
    
    Returns:
    --------
    dict : Risk assessment and action plan
    """
    # Extract key parameters
    primary_fault = diagnosis.get("primary_fault", "NO_FAULT_DETECTED")
    confidence = diagnosis.get("primary_confidence", 0)
    
    # Get severity zone
    vibration_max = data.get("vibration_max_avr", 0)
    if vibration_max > 11.2:
        severity_zone = "D"
    elif vibration_max > 7.1:
        severity_zone = "C"
    elif vibration_max > 2.8:
        severity_zone = "B"
    else:
        severity_zone = "A"
    
    # Calculate severity based on ISO 45001 Annex A
    if confidence > 90 and severity_zone == "C":
        severity_level = "HIGH"
        severity_description = "Major damage potential - bearing failure imminent"
    elif confidence > 80 and severity_zone in ["B", "C"]:
        severity_level = "MEDIUM"
        severity_description = "Moderate damage potential - requires attention"
    else:
        severity_level = "LOW"
        severity_description = "Minor issue - routine monitoring acceptable"
    
    # Calculate probability based on MTBF estimation
    mtbf_days = estimate_mtbf(primary_fault, data)
    
    if mtbf_days < 7:
        probability_level = "HIGH"
        probability_description = "Failure likely within 7 days"
    elif mtbf_days < 30:
        probability_level = "MEDIUM"
        probability_description = "Failure likely within 30 days"
    else:
        probability_level = "LOW"
        probability_description = "Failure unlikely within 90 days"
    
    # Risk matrix (ISO 45001 Annex A)
    risk_matrix = {
        ("HIGH", "HIGH"): ("CRITICAL", "<4 hours", "IMMEDIATE SHUTDOWN"),
        ("HIGH", "MEDIUM"): ("HIGH", "<24 hours", "CORRECTIVE MAINTENANCE"),
        ("HIGH", "LOW"): ("MEDIUM", "<72 hours", "SCHEDULED MAINTENANCE"),
        ("MEDIUM", "HIGH"): ("HIGH", "<24 hours", "CORRECTIVE MAINTENANCE"),
        ("MEDIUM", "MEDIUM"): ("MEDIUM", "<7 days", "PLANNED MAINTENANCE"),
        ("MEDIUM", "LOW"): ("LOW", "<30 days", "ROUTINE MONITORING"),
        ("LOW", "HIGH"): ("MEDIUM", "<7 days", "PLANNED MAINTENANCE"),
        ("LOW", "MEDIUM"): ("LOW", "<30 days", "ROUTINE MONITORING"),
        ("LOW", "LOW"): ("LOW", "<90 days", "ROUTINE MONITORING")
    }
    
    risk_level, timeline, action_priority = risk_matrix.get(
        (severity_level, probability_level),
        ("MEDIUM", "<7 days", "PLANNED MAINTENANCE")
    )
    
    # Generate specific recommendations based on fault type
    recommendations = generate_recommendations(primary_fault, data, mtbf_days, risk_level)
    
    return {
        "risk_level": risk_level,
        "severity_level": severity_level,
        "probability_level": probability_level,
        "severity_description": severity_description,
        "probability_description": probability_description,
        "action_timeline": timeline,
        "action_priority": action_priority,
        "mtbf_days": mtbf_days,
        "recommendations": recommendations,
        "standard": "ISO 45001:2018 Annex A + API 581 RBI Methodology"
    }


def estimate_mtbf(fault_type, data):
    """
    Estimate Mean Time Between Failures based on fault type and severity
    
    Parameters:
    -----------
    fault_type : str
        Type of detected fault
    data : dict
        Measurement data
    
    Returns:
    --------
    int : Estimated MTBF in days
    """
    # Base MTBF values
    base_mtbf = {
        "ELECTRICAL_UNBALANCE": 45,
        "MECHANICAL_UNBALANCE": 60,
        "MISALIGNMENT": 30,
        "BEARING_DEFECT": 21,
        "CAVITATION": 14,
        "NO_FAULT_DETECTED": 365
    }
    
    mtbf = base_mtbf.get(fault_type, 90)
    
    # Adjust based on severity
    vibration_max = data.get("vibration_max_avr", 0)
    if vibration_max > 7.1:  # Zone C
        mtbf = max(mtbf // 3, 3)  # Reduce to 1/3
    elif vibration_max > 4.5:  # High Zone B
        mtbf = max(mtbf // 2, 7)  # Reduce to 1/2
    
    # Adjust for bearing defect severity
    if "BEARING_DEFECT" in fault_type:
        hf_value = data.get("hf_pump_de", 0)
        if hf_value > 1.5:
            mtbf = 3  # Stage 3 - immediate failure
        elif hf_value > 1.0:
            mtbf = 7  # Stage 2+ - within a week
    
    # Adjust for temperature
    temp_pump_de = data.get("temp_pump_de", 0)
    ambient = 35
    temp_rise = temp_pump_de - ambient
    
    if temp_rise > 60:
        mtbf = max(mtbf // 2, 2)  # Halve MTBF for overheating
    elif temp_rise > 50:
        mtbf = max(mtbf * 2 // 3, 3)  # Reduce to 2/3
    
    return mtbf


def generate_recommendations(fault_type, data, mtbf_days, risk_level):
    """
    Generate specific recommendations based on fault type
    
    Parameters:
    -----------
    fault_type : str
        Type of detected fault
    data : dict
        Measurement data
    mtbf_days : int
        Estimated MTBF in days
    risk_level : str
        Risk level (CRITICAL/HIGH/MEDIUM/LOW)
    
    Returns:
    --------
    list : List of recommendations
    """
    recommendations = []
    
    # Common monitoring recommendation
    recommendations.append({
        "priority": "MONITOR",
        "timeline": "Daily" if risk_level in ["CRITICAL", "HIGH"] else "Weekly",
        "action": "Monitor vibration and temperature trends",
        "details": "Record FFT spectrum and bearing temperatures daily until resolved",
        "standard": "ISO 13373-3 Clause 7.2"
    })
    
    # Fault-specific recommendations
    if "ELECTRICAL_UNBALANCE" in fault_type:
        recommendations.insert(0, {
            "priority": "CRITICAL" if risk_level == "CRITICAL" else "HIGH",
            "timeline": "<4 hours" if risk_level == "CRITICAL" else "<24 hours",
            "action": "Correct voltage imbalance to <2%",
            "details": "Check tap changer transformer and balance 3-phase load distribution",
            "standard": "IEC 60034-1 §6.3"
        })
        
        recommendations.append({
            "priority": "MEDIUM",
            "timeline": "<7 days",
            "action": "Verify motor terminal connections",
            "details": "Check for loose connections or corrosion at motor terminals",
            "standard": "NEMA MG-1 §14.32"
        })
    
    elif "MECHANICAL_UNBALANCE" in fault_type:
        recommendations.insert(0, {
            "priority": "HIGH",
            "timeline": "<72 hours",
            "action": "Schedule dynamic balancing",
            "details": "Perform dynamic balancing to ISO 1940-1 G2.5 grade",
            "standard": "ISO 1940-1:2003 G2.5"
        })
        
        recommendations.append({
            "priority": "MEDIUM",
            "timeline": "<7 days",
            "action": "Inspect impeller for fouling or damage",
            "details": "Check impeller for product buildup or erosion damage",
            "standard": "API 610 Clause 8.4.3"
        })
    
    elif "MISALIGNMENT" in fault_type:
        recommendations.insert(0, {
            "priority": "HIGH",
            "timeline": "<72 hours",
            "action": "Re-align coupling",
            "details": "Perform laser alignment to API 671 tolerances (±0.05 mm)",
            "standard": "API 671 Clause 5.3"
        })
        
        recommendations.append({
            "priority": "MEDIUM",
            "timeline": "<7 days",
            "action": "Inspect coupling and foundation bolts",
            "details": "Check for loose foundation bolts or coupling wear",
            "standard": "API 686 Chapter 4"
        })
    
    elif "BEARING_DEFECT" in fault_type:
        recommendations.insert(0, {
            "priority": "CRITICAL" if mtbf_days < 7 else "HIGH",
            "timeline": f"<{min(mtbf_days, 14)} days",
            "action": "Schedule bearing replacement",
            "details": f"MTBF estimation: {mtbf_days} days. Replace before Stage 3 progression.",
            "standard": "ISO 15243:2017 Table 2"
        })
        
        recommendations.append({
            "priority": "MEDIUM",
            "timeline": "<30 days",
            "action": "Check lubrication system",
            "details": "Verify oil level, quality, and contamination level (ISO 4406)",
            "standard": "ISO 12922"
        })
    
    elif "CAVITATION" in fault_type:
        recommendations.insert(0, {
            "priority": "HIGH",
            "timeline": "<24 hours",
            "action": "Adjust flow control valve",
            "details": "Operate within 70-110% BEP to prevent cavitation damage",
            "standard": "API 610 Clause 7.3.2"
        })
        
        recommendations.append({
            "priority": "MEDIUM",
            "timeline": "<7 days",
            "action": "Check NPSHa margin",
            "details": "Verify suction pressure and vapor pressure margin",
            "standard": "API 610 Clause 7.3.2"
        })
    
    return recommendations
