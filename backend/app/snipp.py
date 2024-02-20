@router.get("/myflow", response_model=List[WorkflowDetail])
async def read_workflow(credentials: HTTPAuthorizationCredentials = Security(JWTBearer())):
    token = JWTRepo.extract_token(credentials)
    user_id = token['user_id']
    roles = token.get('role', [])

    if "student" not in roles:
        raise HTTPException(status_code=403, detail="Access forbidden. Only research professors are allowed to create workflows.")

    result = await UserService.get_class_id(user_id)
    
    user_class = result[0] if result else None
 
    workflow = await WorkflowService.get_my_workflow(user_class)
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow
    
class UserService:
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
    
    
    
class WorkflowService:
    @staticmethod
    async def get_my_workflow(user_class: str):
        query = (
            select(Workflow, Class.course, Class.section)
            .join(WorkflowClass, Workflow.id == WorkflowClass.workflow_id)
            .join(Class, WorkflowClass.class_id == Class.id)
            .where(WorkflowClass.class_id == user_class)
        )

        result = await db.execute(query)
        rows = result.mappings().all()

        if not rows:
            return [] 

        workflows_with_steps = []
        for row in rows:
            workflow = row[Workflow]
            course = row[Class.course]
            section = row[Class.section]

            steps_query = select(WorkflowStep).where(WorkflowStep.workflow_id == workflow.id)
            steps = await db.execute(steps_query)
            steps = steps.scalars().all()


            workflow_detail = WorkflowDetail(
                id=workflow.id,
                class_id=user_class,
                type=workflow.type,
                user_id=workflow.user_id,
                course=course,
                section=section,
                steps=steps,
            )
            workflows_with_steps.append(workflow_detail)

        return workflows_with_steps