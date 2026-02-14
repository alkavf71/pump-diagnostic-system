"""
Level 1: Safety Gates
API 670 Annex G Table G.1 + OSHA 1910.147
Hard shutdown criteria - no probabilistic assessment
"""

def safety_gates_check(data):
    """
    Check for critical safety hazards requiring immediate shutdown
    
    Parameters:
    -----------
    data : dict
        Dictionary containing all input measurements
    
    Returns:
    --------
    dict : Safety check result with shutdown triggers
    """
    shutdown_triggers = []
    
    # Trigger 1: Bearing temperature critical (>120°C)
    temp_motor_max = max(data.get("temp_motor_de", 0), data.get("temp_motor_nde", 0))
    temp_pump_max = max(data.get("temp_pump_de", 0), data.get("temp_pump_nde", 0))
    
    if temp_motor_max > 120:
        shutdown_triggers.append({
            "parameter": "Motor Bearing Temperature",
            "component": "Motor",
            "value": temp_motor_max,
            "threshold": "120°C",
            "unit": "°C",
            "standard": "API 610 Table 8.4.3-1",
            "action": "IMMEDIATE SHUTDOWN - LOTO required",
            "severity": "CRITICAL"
        })
    
    if temp_pump_max > 120:
        shutdown_triggers.append({
            "parameter": "Pump Bearing Temperature",
            "component": "Pump",
            "value": temp_pump_max,
            "threshold": "120°C",
            "unit": "°C",
            "standard": "API 610 Table 8.4.3-1",
            "action": "IMMEDIATE SHUTDOWN - LOTO required",
            "severity": "CRITICAL"
        })
    
    # Trigger 2: Vibration Zone D (>11.2 mm/s for Group 3)
    vibration_max = data.get("vibration_max_avr", 0)
    if vibration_max > 11.2:
        shutdown_triggers.append({
            "parameter": "Vibration Velocity",
            "component": "Overall",
            "value": vibration_max,
            "threshold": "11.2 mm/s",
            "unit": "mm/s",
            "standard": "ISO 10816-3:2001 Clause 5.4",
            "action": "IMMEDIATE SHUTDOWN - bearing damage imminent",
            "severity": "CRITICAL"
        })
    
    # Trigger 3: Hydraulic surge (>15% pressure fluctuation)
    p_dis_fluct = data.get("p_dis_fluctuation", 0)
    if p_dis_fluct > 15:
        shutdown_triggers.append({
            "parameter": "Discharge Pressure Fluctuation",
            "component": "Hydraulic",
            "value": p_dis_fluct,
            "threshold": "15%",
            "unit": "%",
            "standard": "API 610 Clause 7.3.4",
            "action": "IMMEDIATE SHUTDOWN - surge protection required",
            "severity": "CRITICAL"
        })
    
    # Trigger 4: Overload (>110% FLC)
    flc = data.get("flc", 500)
    current_avg = (data.get("current_r", 0) + data.get("current_s", 0) + data.get("current_t", 0)) / 3
    load_factor = (current_avg / flc) * 100 if flc > 0 else 0
    
    if load_factor > 110:
        shutdown_triggers.append({
            "parameter": "Motor Load Factor",
            "component": "Electrical",
            "value": load_factor,
            "threshold": "110%",
            "unit": "%",
            "standard": "IEC 60034-1 Table 3",
            "action": "IMMEDIATE SHUTDOWN - overload protection",
            "severity": "CRITICAL"
        })
    
    return {
        "shutdown_required": len(shutdown_triggers) > 0,
        "triggers": shutdown_triggers,
        "trigger_count": len(shutdown_triggers),
        "standard": "API 670 Annex G Table G.1 + OSHA 1910.147",
        "safety_status": "CRITICAL" if len(shutdown_triggers) > 0 else "SAFE"
    }
