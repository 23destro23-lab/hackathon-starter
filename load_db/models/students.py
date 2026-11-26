from typing import Optional
from sqlalchemy import String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from models.references import University, Faculty, Specialization, Language
from models.Enum import DegreeLevel

class Students(Base):
    __tablename__ = "students"

    student_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    gender: Mapped[bool] = mapped_column(Boolean, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    adress: Mapped[str] = mapped_column(String(200), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    mail: Mapped[str] = mapped_column(String(100), nullable=True)
    marital_status: Mapped[str] = mapped_column(String(50), nullable=True)
    university_id: Mapped[int] = mapped_column(ForeignKey('university.id', ondelete="RESTRICT"), nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey('faculty.id', ondelete="RESTRICT"), nullable=False)
    course: Mapped[int] = mapped_column(Integer, nullable=False)
    specialization_id: Mapped[int] = mapped_column(ForeignKey('specialization.id', ondelete="RESTRICT"), nullable=False)
    average: Mapped[float] = mapped_column(default=0.0)
    additional: Mapped[str] = mapped_column(String(250), nullable=True)
    is_windows: Mapped[bool] = mapped_column(Boolean, default=False)
    is_office: Mapped[bool] = mapped_column(Boolean, default=False)
    is_linux: Mapped[bool] = mapped_column(Boolean, default=False)
    is_1c: Mapped[bool] = mapped_column(Boolean, default=False)
    is_sap: Mapped[bool] = mapped_column(Boolean, default=False)
    is_oracle: Mapped[bool] = mapped_column(Boolean, default=False)
    is_sql: Mapped[bool] = mapped_column(Boolean, default=False)
    is_basic: Mapped[bool] = mapped_column(Boolean, default=False)
    is_pascal: Mapped[bool] = mapped_column(Boolean, default=False)
    is_c: Mapped[bool] = mapped_column(Boolean, default=False)
    is_assembler: Mapped[bool] = mapped_column(Boolean, default=False)
    other: Mapped[str] = mapped_column(String(250), nullable=True)
    language_id: Mapped[int] = mapped_column(ForeignKey('language.id', ondelete="RESTRICT"), nullable=True)
    degree: Mapped[str] = mapped_column(String(5), nullable=True)
    degree: Mapped[Optional[DegreeLevel]] = mapped_column(Enum(DegreeLevel, name="degree_level_enum", native_enum=False, length=20), nullable=True)

    university: Mapped[Optional["University"]] = relationship()
    faculty: Mapped[Optional["Faculty"]] = relationship()
    specialization: Mapped[Optional["Specialization"]] = relationship()
    language: Mapped[Optional["Language"]] = relationship()
