import enum

class DegreeLevel(str, enum.Enum):
    BEGINNER = "A1"
    ELEMENTARY  = "A2"
    INTERMEDIATE = "B1"
    UPPER_INTERMEDIATE  = "B2"
    ADVANCED = "C1"
    PROFICIENCY = "C2"