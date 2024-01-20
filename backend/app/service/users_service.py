from sqlalchemy import desc, distinct, func, or_, outerjoin, select, and_
from app.model import Users


from app.model.student import Class, Student  # Import the Student model
from app.model.faculty import Faculty  # Import the Faculty model
from app.config import db
from app.model.users import Role, UsersRole, Users
from app.model.connected_SPS import SPSStudentClassSubjectGrade, SPSClassSubject, SPSClass, SPSMetadata, SPSCourse, SPSCourseEnrolled, SPSStudentClassGrade, SPSLatestBatchSemester
class UserService:


    # BABAGUTIN
    @staticmethod
    async def get_student_profile(user_id: str):
        query = (
            select(
                Users.id,
                Student.StudentId.label('student_id'),
                Student.Email.label('email'),
                func.concat(Student.FirstName, ' ', Student.MiddleName, ' ', Student.LastName).label('name'),
                Student.DateOfBirth.label('birth'),
                Student.StudentNumber.label('student_number'),
                Student.MobileNumber.label('phone_number'),
                SPSCourse.CourseCode.label('course'),
                #func.concat(SPSMetadata.Year, '-', SPSClass.Section).label('section'),
                SPSClass.ClassId.label('class_id'),
            )
            .select_from(SPSStudentClassSubjectGrade)
            .join(SPSClassSubject, SPSClassSubject.ClassSubjectId == SPSStudentClassSubjectGrade.ClassSubjectId)
            .join(SPSClass, SPSClass.ClassId == SPSClassSubject.ClassId)
            .join(SPSMetadata, SPSMetadata.MetadataId == SPSClass.MetadataId)
            .join(SPSCourse, SPSCourse.CourseId == SPSMetadata.CourseId)
            .join(SPSCourseEnrolled, SPSCourseEnrolled.CourseId == SPSCourse.CourseId)
            .join(Student, SPSCourseEnrolled.StudentId == Student.StudentId)
            .join(Users, Student.StudentId == Users.student_id)
            .where(Users.id == user_id)
            # .order_by(desc(SPSMetadata.Batch), desc(SPSMetadata.Semester))
            # .limit(1)
        )

        
        result = await db.execute(query)
        result = result.mappings().first()
        
        print(result)
        
        section = await db.execute(
            select(SPSClass.Section)
            .join(SPSStudentClassGrade, SPSClass.ClassId == SPSStudentClassGrade.ClassId)
            .filter(SPSStudentClassGrade.StudentId == result.student_id)
            .order_by(SPSClass.Section)
        )
        section_result = section.scalar()

        year = await db.execute(
            select(SPSMetadata.Year)
            .join(SPSClass, SPSMetadata.MetadataId == SPSClass.MetadataId)
            .join(SPSStudentClassGrade, SPSClass.ClassId == SPSStudentClassGrade.ClassId)
            .filter(SPSStudentClassGrade.StudentId == result.student_id)
            .order_by(desc(SPSMetadata.Year))
        )
        year_result = year.scalar()
        
        overall = f"{year_result}-{section_result}"
        
        custom_result = {
            "id": result.id,
            "email": result.email,
            "name": result.name,
            "birth": result.birth,
            "student_number": result.student_number,
            "phone_number": result.phone_number,
            "course": result.course,
            "section": overall
        }

        return custom_result
    
    @staticmethod
    async def get_class_id(user_id: str):
        
        query = (
            select(
                SPSCourse.CourseCode.label('course'), 
                Student.StudentId.label('student_id'),
                )
            .select_from(Users)
            .join(Student, Users.student_id == Student.StudentId)
            .join(SPSCourseEnrolled, Student.StudentId == SPSCourseEnrolled.StudentId)
            .join(SPSCourse, SPSCourseEnrolled.CourseId == SPSCourse.CourseId)
            .where(Users.id == user_id)
        )

        result = await db.execute(query)
        user_class_data = result.mappings().first()
        print(user_class_data)
        
        section = await db.execute(
            select(SPSClass.Section)
            .join(SPSStudentClassGrade, SPSClass.ClassId == SPSStudentClassGrade.ClassId)
            .filter(SPSStudentClassGrade.StudentId == user_class_data.student_id)
            .order_by(SPSClass.Section)
        )
        section_result = section.scalar()
        year = await db.execute(
            select(SPSMetadata.Year)
            .join(SPSClass, SPSMetadata.MetadataId == SPSClass.MetadataId)
            .join(SPSStudentClassGrade, SPSClass.ClassId == SPSStudentClassGrade.ClassId)
            .filter(SPSStudentClassGrade.StudentId == user_class_data.student_id)
            .order_by(desc(SPSMetadata.Year))
        )
        year_result = year.scalar()
        
        overall = f"{year_result}-{section_result}"
    
        result_course = user_class_data.course.upper()
        
        query_class_id_ris = (
            select(
                Class.id,
                Class.section,
                Class.course
            )
            .where(Class.section == overall)
            .where(Class.course == result_course)
        )
        
        result_class_id = await db.execute(query_class_id_ris)
        result_last = result_class_id.scalars().all()
        
        return result_last
    
    @staticmethod
    async def get_faculty_profile(user_id: str):
        query = (
            select(
                Users.id,
                Faculty.Email.label('email'),
                func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),
                Faculty.BirthDate.label('birth'),
                Faculty.MobileNumber.label('phone_number')
            )
            .join_from(Users, Faculty)
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().one()
    
    @staticmethod
    async def get_student_profile_by_ID(user_id: str):
        query = (
            select(
                Users.id,
                Users.username,
                Users.email,
                Student.name,
                Student.birth,
                Student.year,
                Student.student_number,
                Student.phone_number,
                Class.section,
                Class.course
            )
            .join(Student, Users.student_id == Student.id)
            .join(Class, Student.class_id == Class.id)
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().one()
    
    
    @staticmethod
    async def get_faculty_profile_by_ID(user_id: str):
        query = (
            select(
                Users.id,
                Faculty.Email.label('email'),
                func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),
                Faculty.BirthDate.label('birth'),
                Faculty.MobileNumber.label('phone_number'),
            )
            .join_from(Users, Faculty)
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().one()
    
    @staticmethod
    async def faculty_info_needed(user_id: str):
        query = (
            select(
                Users.id,
                func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),
            )
            .join_from(Users, Faculty)
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().one()

    @staticmethod
    async def getprofile(user_id: str):
        query = (
            select(
                Users.id,
                Faculty.Email.label('email'),
                func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),
            )
            .join_from(Users, Faculty)
            .where(Users.id == user_id)
        )
        return (await db.execute(query)).mappings().first()
#asdfasdfadf


#FOR NOW OKS LANG TO
    @staticmethod
    async def get_all_student():
        query = (
            select(
                Users.id,
                Student.Email.label('email'),
                func.concat(Student.FirstName, ' ', Student.MiddleName, ' ', Student.LastName).label('name'),
                Student.DateOfBirth.label('birth'),
                Student.StudentNumber.label('student_number'),
                Student.MobileNumber.label('phone_number')
                # Class.section,
                # Class.course
            )
            .join(Student, Users.student_id == Student.StudentId)
            #.join(Class, Student.class_id == Class.id)
            .where(Role.role_name == "student")
        )

        result = await db.execute(query)
        students_data = result.mappings().all()

        return students_data
    
    

    @staticmethod
    async def get_all_faculty():
        query = (
            select(Users.id, 
                   Faculty.Email.label('email'), 
                   Users.faculty_id, 
                   func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),
                   )
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                or_(
                    Role.role_name == "faculty",
                    Role.role_name == "research professor",
                    Role.role_name == "research adviser",
                    Role.role_name == "admin",
                ),
                ))
            )
        )

        result = await db.execute(query)
        faculty_data = result.mappings().all()

        return faculty_data
    
    @staticmethod
    async def get_all_research_adviser():
        query = (
            select(Users.id, 
                   Faculty.Email.label('email'), 
                   Users.faculty_id, 
                   func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),)
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                    Role.role_name == "research adviser",
                ))
            )
        )

        result = await db.execute(query)
        faculty_data = result.mappings().all()

        return faculty_data

    @staticmethod
    async def get_all_research_prof():
        query = (
            select(Users.id, 
                   Faculty.Email.label('email'), 
                   Users.faculty_id, 
                   func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),)
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                    Role.role_name == "research professor",
                ))
            )
        )

        result = await db.execute(query)
        research_prof_data = result.mappings().all()

        return research_prof_data
    
    @staticmethod
    async def get_all_admin():
        query = (
            select(Users.id, 
                   Faculty.Email.label('email'), 
                   Users.faculty_id, 
                   func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('name'),)
            .select_from(
                outerjoin(Users, Faculty).join(UsersRole).join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                    Role.role_name == "admin",
                ))
            )
        )

        result = await db.execute(query)
        admin_data = result.mappings().all()

        return admin_data


    @staticmethod
    async def get_all_list():
        query = (
            select(Users)
        )

        result = await db.execute(query)
        all_user = result.scalars().all()

        return all_user
    

    @staticmethod
    async def get_all_in_faculty_with_roles():
        query = (
            select(
                Users.id,
                Faculty.Email.label('email'), 
                Users.faculty_id,
                func.concat(Faculty.FirstName, ' ', Faculty.MiddleName, ' ', Faculty.LastName).label('faculty_name'),
                Role.role_name
            )
            .select_from(
                outerjoin(Users, Faculty)
                .join(UsersRole)
                .join(Role, and_(
                    UsersRole.users_id == Users.id,
                    UsersRole.role_id == Role.id,
                ))
            )
            .where(or_(
                Role.role_name == "faculty",
                Role.role_name == "admin",
                Role.role_name == "research professor",
                Role.role_name == "research adviser",
            ))
        )

        result = await db.execute(query)
        faculty_data = result.mappings().all()

        return faculty_data

    @staticmethod
    def format_users_with_roles(users_with_roles):
        formatted_result = {}
        
        for user_role in users_with_roles:
            user_id = user_role["id"]
            
            if user_id not in formatted_result:
                # Initialize user entry if not exists
                formatted_result[user_id] = {
                    "id": user_role["id"],
                    "email": user_role["email"],
                    "faculty_name": user_role["faculty_name"],
                    "role_names": [user_role["role_name"]],
                }
            else:
                # Add role to existing user entry
                formatted_result[user_id]["role_names"].append(user_role["role_name"])

        return list(formatted_result.values())