"""
Level 2: ISO 10816-3 Zone Classification
ISO 10816-3:2001 Table 2 with foundation type consideration
"""

def classify_iso_10816_3_zone(velocity_rms, rpm, power_kw, foundation_type):
    """
    Classify vibration severity according to ISO 10816-3:2001 Table 2
    
    Parameters:
    -----------
    velocity_rms : float
        Vibration velocity in mm/s RMS
    rpm : int
        Machine rotational speed
    power_kw : float
        Motor power in kW
    foundation_type : str
        "Rigid (Concrete)" or "Flexible (Steel Structure)"
    
    Returns:
    --------
    dict : Zone classification result
    """
    # Determine machine group based on power
    if power_kw <= 15:
        group = 1
    elif power_kw <= 75:
        group = 2
    else:
        group = 3  # Pompa BBM >75 kW
    
    # Determine zone limits based on foundation type (CRITICAL!)
    is_rigid = (foundation_type == "Rigid (Concrete)")
    
    # Group 3 machines (pompa BBM) - 1200-3600 RPM range
    if group == 3 and 1200 < rpm <= 3600:
        if is_rigid:
            # RIGID FOUNDATION (concrete) - stricter limits
            zone_b_limit = 2.8   # mm/s
            zone_c_limit = 7.1
            zone_d_limit = 11.2
            foundation_note = "Rigid foundation (concrete) - stricter limits apply"
        else:
            # FLEXIBLE FOUNDATION (steel) - more lenient limits
            zone_b_limit = 4.5   # mm/s (60% higher than rigid!)
            zone_c_limit = 11.2
            zone_d_limit = 18.0
            foundation_note = "Flexible foundation (steel structure) - more lenient limits apply"
    else:
        # Other RPM ranges or groups (fallback)
        zone_b_limit = 4.5
        zone_c_limit = 7.1
        zone_d_limit = 11.2
        foundation_note = "Default limits applied"
    
    # Classify zone based on velocity
    if velocity_rms <= zone_b_limit:
        zone = "A"
        remark = "New machine condition or after repair"
        action = "Continue normal operation"
        clause = "ISO 10816-3 Clause 5.1"
        status_color = "success"
    elif velocity_rms <= zone_c_limit:
        zone = "B"
        remark = "Acceptable for unlimited operation"
        action = "Routine monitoring (monthly)"
        clause = "ISO 10816-3 Clause 5.2"
        status_color = "info"
    elif velocity_rms <= zone_d_limit:
        zone = "C"
        remark = "UNSATISFACTORY - Short-term operation only"
        action = "Schedule corrective maintenance within 72 hours"
        clause = "ISO 10816-3 Clause 5.3"
        status_color = "warning"
    else:
        zone = "D"
        remark = "UNACCEPTABLE - Vibration causes damage"
        action = "IMMEDIATE SHUTDOWN REQUIRED"
        clause = "ISO 10816-3 Clause 5.4"
        status_color = "error"
    
    return {
        "zone": zone,
        "velocity_rms": velocity_rms,
        "limit_b": zone_b_limit,
        "limit_c": zone_c_limit,
        "limit_d": zone_d_limit,
        "remark": remark,
        "action": action,
        "clause": clause,
        "status_color": status_color,
        "foundation_type": foundation_type,
        "foundation_note": foundation_note,
        "standard": f"ISO 10816-3:2001 Table 2 (Group {group}, {foundation_type})",
        "group": group
    }


def calculate_direction_averages(data):
    """
    Calculate DE/NDE averages for each direction (H/V/A)
    
    Parameters:
    -----------
    data : dict
        Dictionary containing DE/NDE measurements for motor and pump
    
    Returns:
    --------
    dict : Averages for each direction and component
    """
    # Motor averages
    motor_h_avr = (data.get("motor_h_de", 0) + data.get("motor_h_nde", 0)) / 2
    motor_v_avr = (data.get("motor_v_de", 0) + data.get("motor_v_nde", 0)) / 2
    motor_a_avr = (data.get("motor_a_de", 0) + data.get("motor_a_nde", 0)) / 2
    
    # Pump averages
    pump_h_avr = (data.get("pump_h_de", 0) + data.get("pump_h_nde", 0)) / 2
    pump_v_avr = (data.get("pump_v_de", 0) + data.get("pump_v_nde", 0)) / 2
    pump_a_avr = (data.get("pump_a_de", 0) + data.get("pump_a_nde", 0)) / 2
    
    # Find maximum velocity across all directions
    all_velocities = [
        motor_h_avr, motor_v_avr, motor_a_avr,
        pump_h_avr, pump_v_avr, pump_a_avr
    ]
    max_velocity = max(all_velocities)
    
    # Determine which direction has maximum
    directions = ["Motor H", "Motor V", "Motor A", "Pump H", "Pump V", "Pump A"]
    max_direction = directions[all_velocities.index(max_velocity)]
    
    return {
        "motor_h_avr": motor_h_avr,
        "motor_v_avr": motor_v_avr,
        "motor_a_avr": motor_a_avr,
        "pump_h_avr": pump_h_avr,
        "pump_v_avr": pump_v_avr,
        "pump_a_avr": pump_a_avr,
        "max_velocity": max_velocity,
        "max_direction": max_direction,
        "all_velocities": all_velocities
    }
