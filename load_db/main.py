import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from models.students import Students
from utils import norm_str, norm_title, to_int, to_bool, get_or_create, parse_enum, to_gender, to_float

from models.references import University, Faculty, Specialization, Language
from models.Enum import DegreeLevel

BASE_DIR = Path(__file__).resolve().parent
DB_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/test?client_encoding=utf8"
EXCEL_PATH = "test.xlsx"

def is_empty(session: Session, model) -> bool:
    count = session.execute(
        select(func.count()).select_from(model)
    ).scalar_one()
    print(count)
    return count == 0

def load_students(session: Session, df: pd.DataFrame):
    df = df.where(pd.notna(df), None)
    for _, row in df.iterrows():
        student_id = row["ID"]
        if not student_id:
            continue
        university = (
            get_or_create(session, University, name=norm_str(row["Наименование университета"]))
            if norm_str(row["Наименование университета"]) else None
        )
        faculty = (
            get_or_create(session, Faculty, name=norm_str(row["Факультет"]))
            if norm_str(row["Факультет"]) else None
        )
        specialization = (
            get_or_create(session, Specialization, name=norm_str(row["Направление подготовки/специальность"]))
            if norm_str(row["Направление подготовки/специальность"]) else None
        )
        language = (
            get_or_create(session, Language, name=norm_str(row["Иностранный язык"]))
            if norm_str(row["Иностранный язык"]) else None
        )
        
        student = Students(
            student_id = student_id,
            full_name = norm_title(row["Ф.И.О."]),
            gender = to_gender(row["Пол"]),
            age = to_int(row["Возраст"]),
            adress = norm_title(row["Место проживания"]),
            phone = row["Телефон"],
            mail = row["E-mail"],
            marital_status = norm_str(row["Семейное положение"]),
            university_id = university.id if university else None,
            faculty_id = faculty.id if faculty else None,
            course = to_int(row["Курс"]),
            specialization_id = specialization.id if specialization else None,
            average = to_float(row["Средний балл"]),
            additional = norm_str(row["Другое образование"]),
            is_windows = to_bool(row["Базовые программы / Windows"]),
            is_office = to_bool(row["Базовые программы / MS Office"]),
            is_linux = to_bool(row["Базовые программы / Linux"]),
            is_1c = to_bool(row["Специализированные программы / 1С"]),
            is_sap = to_bool(row["Специализированные программы / SAP"]),
            is_oracle = to_bool(row["Специализированные программы / Oracle"]),
            is_sql = to_bool(row["Специализированные программы / MS SQL"]),
            is_basic = to_bool(row["Языки программирования / Basic"]),
            is_pascal = to_bool(row["Языки программирования / Pascal"]),
            is_c = to_bool(row["Языки программирования / C / C++"]),
            is_assembler = to_bool(row["Языки программирования / Assembler"]),
            other = norm_str(row["Другое"]),
            language_id = language.id if language else None,
            degree = parse_enum(row["Степень владения"], DegreeLevel),
        )
        session.add(student)

    session.flush()

def load(path: str) -> None:
    engine = create_engine(DB_URL)
    xls = pd.ExcelFile(path)
    with Session(engine) as session:
        try:
            if is_empty(session, Students):
                df_students = pd.read_excel(xls, "Студенты", dtype=str)
                load_students(session, df_students)
                print("Student заполнено")
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error {e}")
            raise

if __name__ == "__main__":
    load(EXCEL_PATH)