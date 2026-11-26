from datetime import date, datetime
import re
import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

def norm_str(value) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    s = str(value).strip()
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s)
    return s.lower() if s else None

def norm_title(value) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)) or value == "—":
        return None
    s = str(value).strip().replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s)
    return s or None

def get_year(value) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)) or value == "—":
        return None
    s = str(value)
    res = re.search(r"\b(20\d{2})\b", s)
    return int(res.group(1)) or None

def to_int(value) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None
    
def to_bool(value) -> bool | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, bool):
        return value
    s = str(value).strip()
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).lower()

    true_values = {'1', 'true', 'yes', 'y', 'да', 'истина', 't', '+', '1.0'}
    false_values = {'0', 'false', 'no', 'n', 'нет', 'ложь', 'f', '-', '0.0'}

    if s in true_values:
        return True
    if s in false_values:
        return False

    return None

def to_gender(value) -> bool | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    if isinstance(value, bool):
        return value
    s = str(value).strip()
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).lower()

    true_values = {'1', 'мужской', 'м', 'm', 'male'}
    false_values = {'0', 'женский', 'ж', 'f', 'female'}

    if s in true_values:
        return True
    if s in false_values:
        return False

    return None

def to_date(value) -> date | None:
    if value is None or pd.isna(value):
        return None
    if isinstance(value, (datetime, pd.Timestamp)):
        return value.date()
    s = str(value).strip().replace("\xa0", " ").replace("T", " ").split(" ")[0]
    if not s:
        return None
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except (ValueError, TypeError) as e:
            continue
    return None
        
def get_or_create(session: Session, model, defaults: dict | None = None, **kwargs):
    instance = session.execute(
        select(model).filter_by(**kwargs)
    ).scalar_one_or_none()
    if instance:
        return instance
    instance = model(**{**kwargs, **(defaults or {})})
    session.add(instance)
    session.flush()
    return instance

def parse_fio(value) -> tuple[str | None, str | None, str | None]:
    if not value or not isinstance(value, str):
        return None, None, None
    s = value.replace("\xa0", " ").strip()
    s = re.sub(r"\s+", " ", s)
    parts = s.split()
    if len(parts) >=3:
        return parts[0], parts[1], parts[2]
    if len(parts) == 2:
        return parts[0], parts[1], None
    return None, None, None
    
def parse_enum(value, enum_class, default=None):
    if value is None or (isinstance(value,float)):
        return default
    key = str(value).strip().lower()
    key = " ".join(key.split())
    for member in enum_class:
        member_value = str(member.value).strip().lower()
        member_value = " ".join(member_value.split())
        if member_value == key:
            return member
        
    return default

def to_float(value) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    s = str(value).strip().replace("\xa0", " ").replace(",", ".")
    try:
        return round(float(s), 2)
    except (ValueError, TypeError):
        return None