VITAL_FIELDS = ("bp", "hr", "temp_f", "spo2")
MEDICATION_FIELDS = ("name", "dose", "frequency", "route")
DIAGNOSIS_FIELDS = ("description", "icd10")
FOLLOW_UP_FIELDS = ("interval_days", "reason")


def empty_clinical_note() -> dict:
    return {
        "chief_complaint": None,
        "vitals": {field: None for field in VITAL_FIELDS},
        "medications": [],
        "diagnoses": [],
        "plan": [],
        "follow_up": {field: None for field in FOLLOW_UP_FIELDS},
    }


def _clean_scalar(value):
    if value in ("", [], {}):
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def _clean_string(value):
    value = _clean_scalar(value)
    return None if value is None else str(value)


def _clean_list(value) -> list:
    if value in (None, "", {}, []):
        return []
    return value if isinstance(value, list) else [value]


def _clean_vitals(value) -> dict:
    vitals = {field: None for field in VITAL_FIELDS}
    if not isinstance(value, dict):
        return vitals

    for field in VITAL_FIELDS:
        vitals[field] = _clean_scalar(value.get(field))
    return vitals


def _clean_medications(value) -> list[dict]:
    medications = []
    for item in _clean_list(value):
        medication = {field: None for field in MEDICATION_FIELDS}
        if isinstance(item, dict):
            for field in MEDICATION_FIELDS:
                medication[field] = _clean_string(item.get(field))
        else:
            medication["name"] = _clean_string(item)
        medications.append(medication)
    return medications


def _clean_diagnoses(value) -> list[dict]:
    diagnoses = []
    for item in _clean_list(value):
        diagnosis = {field: None for field in DIAGNOSIS_FIELDS}
        if isinstance(item, dict):
            for field in DIAGNOSIS_FIELDS:
                diagnosis[field] = _clean_string(item.get(field))
        else:
            diagnosis["description"] = _clean_string(item)
        diagnoses.append(diagnosis)
    return diagnoses


def _clean_plan(value) -> list[str]:
    plan = []
    for item in _clean_list(value):
        item = _clean_string(item)
        if item:
            plan.append(item)
    return plan


def _clean_follow_up(value) -> dict:
    follow_up = {field: None for field in FOLLOW_UP_FIELDS}
    if isinstance(value, dict):
        follow_up["interval_days"] = _clean_scalar(value.get("interval_days"))
        follow_up["reason"] = _clean_string(value.get("reason"))
    elif value:
        follow_up["reason"] = _clean_string(value)
    return follow_up


def validate_output(data) -> dict:
    note = empty_clinical_note()
    if not isinstance(data, dict):
        return note

    note["chief_complaint"] = _clean_string(data.get("chief_complaint"))
    note["vitals"] = _clean_vitals(data.get("vitals"))
    note["medications"] = _clean_medications(data.get("medications"))
    note["diagnoses"] = _clean_diagnoses(data.get("diagnoses"))
    note["plan"] = _clean_plan(data.get("plan"))
    note["follow_up"] = _clean_follow_up(data.get("follow_up"))
    return note
