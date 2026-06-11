"""Heuristic rules for flagging clinically significant values."""
from __future__ import annotations

REFERENCE_RANGES: dict[str, tuple[float, float, str]] = {
    "hemoglobin": (12.0, 17.5, "g/dL"),
    "glucose": (70.0, 100.0, "mg/dL"),
    "hba1c": (4.0, 5.6, "%"),
    "cholesterol": (0.0, 200.0, "mg/dL"),
    "ldl": (0.0, 100.0, "mg/dL"),
    "hdl_male": (40.0, 60.0, "mg/dL"),
    "hdl_female": (50.0, 60.0, "mg/dL"),
    "triglycerides": (0.0, 150.0, "mg/dL"),
    "systolic_bp": (90.0, 120.0, "mmHg"),
    "diastolic_bp": (60.0, 80.0, "mmHg"),
    "creatinine": (0.7, 1.3, "mg/dL"),
    "tsh": (0.4, 4.0, "mIU/L"),
}


def check_value(test_name: str, value: float) -> dict:
    """Return status and message for a given lab test value."""
    key = test_name.lower().replace(" ", "_")
    if key not in REFERENCE_RANGES:
        return {"status": "unknown", "message": f"No reference range for {test_name}"}

    low, high, unit = REFERENCE_RANGES[key]
    if value < low:
        return {
            "status": "LOW",
            "message": f"{test_name} = {value} {unit} (below normal range {low}–{high})",
        }
    if value > high:
        return {
            "status": "HIGH",
            "message": f"{test_name} = {value} {unit} (above normal range {low}–{high})",
        }
    return {
        "status": "NORMAL",
        "message": f"{test_name} = {value} {unit} (within normal range)",
    }
