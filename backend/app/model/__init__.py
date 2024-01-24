from .mixins import TimeMixin

from .users import Users
from .users import UsersRole
from .users import Role
from .workflowprocess import Workflow
from .workflowprocess import WorkflowStep



from .student import Class

from .student import Student
from .faculty import Faculty


from .research_paper import ResearchPaper
from .research_paper import Author
from .research_paper import FacultyResearchPaper

from .research_status import Comment


from .researchdef import ResearchDefense
from .researchdef import SetDefense
# from .researchdef import SetDefenseClass

from .ethics import Ethics
from .full_manuscript import FullManuscript
from .copyright import CopyRight


#Announcement and Notifications
from .notification import Notification
from .announcements import Announcement

from .assignedTo import AssignedResearchType
from .assignedTo import AssignedSections
#from .assignedTo import AssignedResearchTypeToProf
from .assignedTo import AssignedSectionsToProf

from .workflowprocess import NavigationTab
from .workflowprocess import NavigationClass


#integrated tables:

from .connected_SPS import SPSStudentClassSubjectGrade, SPSClassSubject, SPSClass, SPSMetadata, SPSCourse, SPSCourseEnrolled, SPSLatestBatchSemester



