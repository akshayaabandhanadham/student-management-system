
from typing import Dict, Tuple, Optional

def validate_student_payload(payload: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate incoming student payload.
    Returns (is_valid, error_message_or_None).
    Expected minimal fields:
      - enrollment_no (non-empty string)
      - first_name (non-empty string)
    Optional:
      - last_name, email, course
    """
    if not isinstance(payload, dict):
        return False, "Payload must be a JSON object."

    enrollment_no = payload.get("enrollment_no")
    first_name = payload.get("first_name")

    if not enrollment_no or not isinstance(enrollment_no, str):
        return False, "enrollment_no is required and must be a string."
    if not first_name or not isinstance(first_name, str):
        return False, "first_name is required and must be a string."

    email = payload.get("email")
    if email is not None and ("@" not in email or len(email) > 120):
        return False, "email must be a valid email-like string (<120 chars)."

    return True, None
