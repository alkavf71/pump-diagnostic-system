"""
Main Diagnostic Engine - Orchestrates all 6 levels
"""

from .safety_gates import safety_gates_check
from .iso_10816_3_classifier import classify_iso_10816_3_zone, calculate_direction_averages
from .fft_analyzer import detect_fft_signatures, analyze_bearing_condition
from .cross_validator import cross_validate_faults
from .bayesian_fusion import bayesian_fusion
from .risk_assessor import assess_risk_and_generate_plan


class PumpDiagnosticEngine:
    """Main engine for pump diagnostic analysis"""
    
    def __init__(self):
        self.results = {}
    
    def run_diagnosis(self, input_data):
        """
        Run complete 6-level diagnostic analysis
        
        Parameters:
        -----------
        input_data : dict
            Dictionary containing all input measurements
        
        Returns:
        --------
        dict : Complete diagnosis report
        """
        # Store input data
        self.input_data = input_data
        
        # === LEVEL 1: SAFETY GATES ===
        safety_result = safety_gates_check(input_data)
        self.results["level_1_safety"] = safety_result
        
        # If safety shutdown required, skip to final report
        if safety_result["shutdown_required"]:
            return self._generate_emergency_report(safety_result)
        
        # === LEVEL 2: SEVERITY CLASSIFICATION ===
        # Calculate direction averages
        averages = calculate_direction_averages(input_data)
        self.results["averages"] = averages
        
        # Classify zone for maximum velocity
        zone_result = classify_iso_10816_3_zone(
            velocity_rms=averages["max_velocity"],
            rpm=input_data.get("motor_rpm", 1500),
            power_kw=input_data.get("motor_kw", 315),
            foundation_type=input_data.get("foundation_type", "Rigid (Concrete)")
        )
        self.results["level_2_severity"] = zone_result
        
        # Add averages to input data for next levels
        input_data["vibration_max_avr"] = averages["max_velocity"]
        
        # === LEVEL 3: PRIMARY FAULT DETECTION ===
        fft_faults = detect_fft_signatures(input_data)
        self.results["level_3_fft"] = {
            "faults": fft_faults,
            "fault_count": len(fft_faults)
        }
        
        # If no faults detected, return basic report
        if not fft_faults:
            return self._generate_basic_report(zone_result)
        
        # === LEVEL 4: CROSS-VALIDATION ===
        validated_faults = cross_validate_faults(fft_faults, input_data)
        self.results["level_4_validation"] = {
            "faults": validated_faults,
            "validated_count": len([f for f in validated_faults if f["is_validated"]])
        }
        
        # Filter only validated faults
        validated_only = [f for f in validated_faults if f["is_validated"]]
        if not validated_only:
            return self._generate_basic_report(zone_result)
        
        # === LEVEL 5: BAYESIAN FUSION ===
        bayesian_result = bayesian_fusion(validated_only, input_data)
        self.results["level_5_bayesian"] = bayesian_result
        
        # === LEVEL 6: RISK ASSESSMENT & ACTION PLAN ===
        risk_result = assess_risk_and_generate_plan(bayesian_result, input_data)
        self.results["level_6_risk"] = risk_result
        
        # === BEARING CONDITION ANALYSIS (Additional) ===
        hf_pump_de = input_data.get("hf_pump_de", 0)
        temp_pump_de = input_data.get("temp_pump_de", 0)
        ambient = 35
        temp_rise = temp_pump_de - ambient
        demod_value = input_data.get("demod_pump_de", 0)
        
        bearing_condition = analyze_bearing_condition(hf_pump_de, temp_rise, demod_value)
        self.results["bearing_condition"] = bearing_condition
        
        # === GENERATE FINAL REPORT ===
        return self._generate_comprehensive_report()
    
    def _generate_emergency_report(self, safety_result):
        """Generate emergency shutdown report"""
        return {
            "report_type": "EMERGENCY_SHUTDOWN",
            "summary": "CRITICAL SAFETY HAZARD DETECTED",
            "level_1_safety": safety_result,
            "recommendations": [{
                "priority": "CRITICAL",
                "timeline": "IMMEDIATE",
                "action": "SHUTDOWN MACHINE NOW",
                "details": "Follow LOTO procedure per OSHA 1910.147",
                "standard": "OSHA 1910.147 + API 670 Annex G"
            }],
            "compliance": {
                "status": "NON-COMPLIANT",
                "reason": "Critical safety hazard detected",
                "required_action": "Immediate shutdown and investigation"
            }
        }
    
    def _generate_basic_report(self, zone_result):
        """Generate basic report when no faults detected"""
        return {
            "report_type": "ROUTINE_MONITORING",
            "summary": "NO SIGNIFICANT FAULTS DETECTED",
            "level_2_severity": zone_result,
            "recommendations": [{
                "priority": "ROUTINE",
                "timeline": "Monthly",
                "action": "Continue routine monitoring",
                "details": f"Vibration Zone {zone_result['zone']} - within acceptable limits",
                "standard": "ISO 10816-3 Clause 5.2"
            }],
            "compliance": {
                "status": "COMPLIANT",
                "reason": "All parameters within acceptable limits",
                "required_action": "Routine monitoring per schedule"
            }
        }
    
    def _generate_comprehensive_report(self):
        """Generate comprehensive diagnostic report"""
        # Extract key results
        zone_result = self.results["level_2_severity"]
        bayesian_result = self.results["level_5_bayesian"]
        risk_result = self.results["level_6_risk"]
        bearing_condition = self.results["bearing_condition"]
        
        # Build compliance status
        compliance = self._assess_compliance()
        
        return {
            "report_type": "COMPREHENSIVE_DIAGNOSIS",
            "summary": bayesian_result["primary_fault"],
            "level_1_safety": self.results["level_1_safety"],
            "level_2_severity": zone_result,
            "level_3_fft": self.results["level_3_fft"],
            "level_4_validation": self.results["level_4_validation"],
            "level_5_bayesian": bayesian_result,
            "level_6_risk": risk_result,
            "bearing_condition": bearing_condition,
            "averages": self.results["averages"],
            "recommendations": risk_result["recommendations"],
            "compliance": compliance,
            "audit_trail": {
                "analysis_timestamp": "Auto-generated",
                "standards_referenced": [
                    "ISO 10816-3:2001",
                    "ISO 13373-2:2012",
                    "IEC 60034-1:2017",
                    "API 610 Ed.11",
                    "ISO 15243:2017",
                    "ISO 45001:2018"
                ],
                "confidence_score": bayesian_result["primary_confidence"]
            }
        }
    
    def _assess_compliance(self):
        """Assess compliance with various standards"""
        input_data = self.input_data
        
        # ISO 10816-3 compliance
        zone = self.results["level_2_severity"]["zone"]
        iso_10816_3_status = "COMPLIANT" if zone in ["A", "B"] else "WARNING" if zone == "C" else "NON-COMPLIANT"
        
        # IEC 60034-1 compliance (voltage imbalance)
        v_r = input_data.get("voltage_r", 400)
        v_s = input_data.get("voltage_s", 400)
        v_t = input_data.get("voltage_t", 400)
        v_avg = (v_r + v_s + v_t) / 3
        v_imbalance = max(abs(v_r-v_avg), abs(v_s-v_avg), abs(v_t-v_avg)) / v_avg * 100
        iec_60034_status = "COMPLIANT" if v_imbalance <= 2.0 else "NON-COMPLIANT"
        
        # API 610 compliance (NPSHa margin)
        p_suc = input_data.get("p_suc", 0)
        npshr = input_data.get("npshr", 3.0)
        npsha = p_suc + 10.33 - 0.5
        npsha_margin = npsha - npshr
        api_610_status = "COMPLIANT" if npsha_margin >= 0.6 else "WARNING"
        
        # ISO 15243 compliance (bearing condition)
        bearing_stage = self.results["bearing_condition"]["stage"]
        iso_15243_status = "COMPLIANT" if bearing_stage == 0 else "WARNING" if bearing_stage == 1 else "NON-COMPLIANT"
        
        return {
            "iso_10816_3": iso_10816_3_status,
            "iec_60034_1": iec_60034_status,
            "api_610": api_610_status,
            "iso_15243": iso_15243_status,
            "overall_status": "COMPLIANT" if all([
                iso_10816_3_status == "COMPLIANT",
                iec_60034_status == "COMPLIANT",
                api_610_status == "COMPLIANT",
                iso_15243_status == "COMPLIANT"
            ]) else "NON-COMPLIANT"
        }
