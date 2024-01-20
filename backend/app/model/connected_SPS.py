from datetime import datetime
from typing import List, Optional
from app.model.mixins import TimeMixin
from sqlalchemy import Column, String, Integer
from sqlmodel import SQLModel, Field, Relationship



class SPSStudentClassSubjectGrade(SQLModel,table=True):
    __tablename__= "SPSStudentClassSubjectGrade"
    
    ClassSubjectId: int = Field(primary_key=True, nullable=False)
    StudentId: int
    created_at: datetime
    updated_at: datetime



class SPSClassSubject(SQLModel,table=True):
    __tablename__= "SPSClassSubject"
    
    ClassSubjectId: int = Field(primary_key=True, nullable=False)
    ClassId: int

class SPSClass(SQLModel,table=True):
    __tablename__= "SPSClass"

    ClassId: int = Field(primary_key=True, nullable=False)
    MetadataId: int
    Section: int


#= Field(foreign_key="SPSMetadata.MetadataId")
class SPSMetadata(SQLModel,table=True):
    __tablename__= "SPSMetadata"
    MetadataId: int = Field(primary_key=True, nullable=False)
    CourseId: int
    Batch: str
    Semester: str
    updated_at: datetime
    created_at: datetime
    Year: int

class SPSCourse(SQLModel,table=True):
    __tablename__= "SPSCourse"
    CourseId: int = Field(primary_key=True, nullable=False)
    CourseCode: str
    Name: str

class SPSCourseEnrolled(SQLModel,table=True):
    __tablename__= "SPSCourseEnrolled"
    
    CourseId: int = Field(primary_key=True, nullable=False)
    StudentId: int


class SPSStudentClassGrade(SQLModel,table=True):
    __tablename__= "SPSStudentClassGrade"
    
    StudentId: int = Field(primary_key=True, nullable=False)
    ClassId: int

class SPSLatestBatchSemester(SQLModel,table=True):
    __tablename__= "SPSLatestBatchSemester"
    
    LatestBatchSemesterId: int = Field(primary_key=True, nullable=False)
    Batch: int
    Semester: int
    isEnrollmentStarted: bool
    isGradeFinalized: bool


