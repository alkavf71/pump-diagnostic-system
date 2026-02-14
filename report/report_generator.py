"""
Report Generator - AIM-004 Compliant Format
"""

import json
from datetime import datetime


def generate_text_report(diagnosis_result, asset_info):
    """
    Generate comprehensive text report
    
    Parameters:
    -----------
    diagnosis_result : dict
        Complete diagnosis result from engine
    asset_info : dict
        Asset information
    
    Returns:
    --------
    str : Formatted text report
    """
    report_lines = []
    
    # Header
    report_lines.append("=" * 80)
    report_lines.append("🛢️  PUMP DIAGNOSTIC REPORT - PERTAMINA PATRA NIAGA")
    report_lines.append("=" * 80)
    report_lines.append(f"Asset ID: {asset_info.get('asset_id', 'UNKNOWN')}")
    report_lines.append(f"Location: {asset_info.get('location', 'UNKNOWN')}")
    report_lines.append(f"Pump Type: {asset_info.get('pump_type', 'UNKNOWN')}")
    report_lines.append(f"Date: {datetime.now().strftime('%d %b %Y')}")
    report_lines.append(f"Report ID: DIAG-{datetime.now().strftime('%Y%m%d')}-{asset_info.get('asset_id', 'XXX')}")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Executive Summary
    report_lines.append("EXECUTIVE SUMMARY")
    report_lines.append("-" * 80)
    report_lines.append(f"Diagnosis: {diagnosis_result['summary']}")
    report_lines.append(f"Confidence: {diagnosis_result['audit_trail']['confidence_score']:.0f}%")
    report_lines.append(f"Risk Level: {diagnosis_result['level_6_risk']['risk_level']}")
    report_lines.append(f"Recommended Timeline: {diagnosis_result['level_6_risk']['action_timeline']}")
    report_lines.append("")
    
    # Level 2: Severity Classification
    if "level_2_severity" in diagnosis_result:
        zone_result = diagnosis_result["level_2_severity"]
        report_lines.append("VIBRATION SEVERITY (ISO 10816-3:2001)")
        report_lines.append("-" * 80)
        report_lines.append(f"Zone Classification: {zone_result['zone']}")
        report_lines.append(f"Maximum Velocity: {zone_result['max_velocity']:.2f} mm/s")
        report_lines.append(f"Direction: {diagnosis_result['averages']['max_direction']}")
        report_lines.append(f"Zone B Limit: {zone_result['limit_b']:.1f} mm/s")
        report_lines.append(f"Zone C Limit: {zone_result['limit_c']:.1f} mm/s")
        report_lines.append(f"Foundation Type: {zone_result['foundation_type']}")
        report_lines.append(f"Status: {zone_result['remark']}")
        report_lines.append(f"Action: {zone_result['action']}")
        report_lines.append(f"Standard: {zone_result['standard']}")
        report_lines.append("")
    
    # Level 5: Primary Diagnosis
    if "level_5_bayesian" in diagnosis_result:
        bayesian = diagnosis_result["level_5_bayesian"]
        report_lines.append("PRIMARY DIAGNOSIS (Bayesian Fusion)")
        report_lines.append("-" * 80)
        report_lines.append(f"Fault Type: {bayesian['primary_fault']}")
        report_lines.append(f"Confidence: {bayesian['primary_confidence']:.0f}%")
        report_lines.append(f"Evidence: {bayesian['evidence_summary']}")
        report_lines.append("")
        
        if bayesian["secondary_faults"]:
            report_lines.append("Secondary Faults:")
            for fault in bayesian["secondary_faults"][:2]:  # Top 2
                report_lines.append(f"  • {fault['fault_type']} ({fault['posterior_probability']:.0f}% confidence)")
            report_lines.append("")
    
    # Bearing Condition
    if "bearing_condition" in diagnosis_result:
        bearing = diagnosis_result["bearing_condition"]
        report_lines.append("BEARING CONDITION (ISO 15243:2017)")
        report_lines.append("-" * 80)
        report_lines.append(f"Stage: {bearing['stage']}")
        report_lines.append(f"Condition: {bearing['condition']}")
        report_lines.append(f"HF 5-16 kHz: {bearing['hf_value']:.2f} g")
        report_lines.append(f"Temperature Rise: {bearing['temp_rise']:.0f}°C")
        report_lines.append(f"Recommendation: {bearing['recommendation']}")
        report_lines.append("")
    
    # Level 6: Action Plan
    if "level_6_risk" in diagnosis_result:
        risk = diagnosis_result["level_6_risk"]
        report_lines.append("RECOMMENDED ACTIONS (ISO 45001 Risk-Based)")
        report_lines.append("-" * 80)
        report_lines.append(f"Risk Level: {risk['risk_level']}")
        report_lines.append(f"Severity: {risk['severity_level']} - {risk['severity_description']}")
        report_lines.append(f"Probability: {risk['probability_level']} - {risk['probability_description']}")
        report_lines.append(f"MTBF Estimation: {risk['mtbf_days']} days")
        report_lines.append("")
        
        report_lines.append("Action Items:")
        for i, rec in enumerate(risk["recommendations"], 1):
            report_lines.append(f"{i}. [{rec['priority']}] {rec['timeline']}")
            report_lines.append(f"   Action: {rec['action']}")
            report_lines.append(f"   Details: {rec['details']}")
            report_lines.append(f"   Standard: {rec['standard']}")
            report_lines.append("")
    
    # Compliance Status
    if "compliance" in diagnosis_result:
        comp = diagnosis_result["compliance"]
        report_lines.append("COMPLIANCE STATUS (AIM-004 Format)")
        report_lines.append("-" * 80)
        report_lines.append(f"ISO 10816-3: {comp['iso_10816_3']}")
        report_lines.append(f"IEC 60034-1: {comp['iec_60034_1']}")
        report_lines.append(f"API 610: {comp['api_610']}")
        report_lines.append(f"ISO 15243: {comp['iso_15243']}")
        report_lines.append(f"Overall Status: {comp['overall_status']}")
        report_lines.append("")
    
    # Footer
    report_lines.append("=" * 80)
    report_lines.append("END OF REPORT")
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


def generate_json_report(diagnosis_result, asset_info):
    """
    Generate JSON format report
    
    Parameters:
    -----------
    diagnosis_result : dict
        Complete diagnosis result
    asset_info : dict
        Asset information
    
    Returns:
    --------
    str : JSON formatted report
    """
    report = {
        "report_metadata": {
            "report_type": "Pump Diagnostic Report",
            "generated_date": datetime.now().isoformat(),
            "asset_info": asset_info,
            "report_id": f"DIAG-{datetime.now().strftime('%Y%m%d')}-{asset_info.get('asset_id', 'XXX')}"
        },
        "diagnosis_result": diagnosis_result,
        "audit_trail": {
            "standards_used": diagnosis_result.get("audit_trail", {}).get("standards_referenced", []),
            "confidence_score": diagnosis_result.get("audit_trail", {}).get("confidence_score", 0),
            "analysis_engine": "6-Level Hierarchical Diagnostic Engine"
        }
    }
    
    return json.dumps(report, indent=2)


def save_report(report_text, filename):
    """
    Save report to file
    
    Parameters:
    -----------
    report_text : str
        Report text content
    filename : str
        Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_text)
