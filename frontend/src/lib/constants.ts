import type {
  CustomStep,
  Navigation,
  NavigationParent,
} from '@/types/navigation';
import { BiSolidDashboard } from 'react-icons/bi';
import {
  FaBalanceScaleLeft,
  FaBook,
  FaCalendar,
  FaChalkboardTeacher,
  FaCoins,
  FaCopyright,
  FaFileAlt,
  FaFolder,
  FaScroll,
  FaUsersCog,
} from 'react-icons/fa';
import { FaRegCircleCheck } from 'react-icons/fa6';
import { HiMiniUserGroup } from 'react-icons/hi2';
import { IoMdMegaphone } from 'react-icons/io';
import { SlBookOpen } from 'react-icons/sl';

export const STUDENT_NAVIGATION1: NavigationParent = [
  {
    label: 'Progress',
    Icon: FaRegCircleCheck,
    href: '/student/progress',
  },
  // {
  //   label: 'Submissions',
  //   nodeList: [
  //     {
  //       label: 'Proposal',
  //       Icon: BsGraphUpArrow,
  //       href: '/student/proposal',
  //     },
  //     {
  //       label: 'Ethics/Protocol',
  //       Icon: IoShieldHalf,
  //       href: '/student/ethics-protocol',
  //     },
  //     {
  //       label: 'Full Manuscript',
  //       Icon: GiFeather,
  //       href: '/student/full-manuscript',
  //     },
  //     {
  //       label: 'Copyright Documents',
  //       Icon: FaCopyright,
  //       href: '/student/copyright-documents',
  //     },
  //   ],
  // },
  // {
  //   label: 'Pages',
  //   nodeList: [
  //     {
  //       label: 'Collaboration',
  //       Icon: HiMiniUserGroup,
  //       href: '/student/collaboration',
  //     },
  //     {
  //       label: 'Research Manual',
  //       Icon: FaFolder,
  //       href: '/student/research-manual',
  //     },
  //     {
  //       label: 'Ethics and Compliance',
  //       Icon: FaBalanceScaleLeft,
  //       href: '/student/ethics-and-compliance',
  //     },
  //     {
  //       label: 'Repository',
  //       Icon: SlBookOpen,
  //       href: '/student/repository',
  //     },
  //   ],
  // },
  {
    label: 'Researchers Profile',
    Icon: HiMiniUserGroup,
    href: '/student/researchers-profile',
  },
  {
    label: 'Research Manual',
    Icon: FaFolder,
    href: '/student/research-manual',
  },
  {
    label: 'Ethics and Compliance',
    Icon: FaBalanceScaleLeft,
    href: '/student/ethics-and-compliance',
  },
  {
    label: 'Repository',
    Icon: SlBookOpen,
    href: '/student/repository',
  },
  {
    label: 'Announcements',
    Icon: IoMdMegaphone,
    href: '/student/announcements',
  },
  // {
  //   label: 'Announcement',
  //   nodeList: [
  //     {
  //       label: 'Funding',
  //       Icon: FaCoins,
  //       href: '/student/funding-opportunities',
  //     },
  //     {
  //       label: 'Training and Workshops',
  //       Icon: FaCalendar,
  //       href: '/student/training-and-workshop',
  //     },
  //   ],
  // },
];

export const FACULTY_NAVIGATION: NavigationParent = [
  {
    label: 'Pages',
    nodeList: [
      {
        label: 'Dashboard',
        Icon: BiSolidDashboard,
        href: '/faculty/dashboard',
      },
      {
        label: 'Research Submissions',
        Icon: FaFolder,
        href: '/faculty/research-submissions',
      },
    ],
  },
];

export const ADMIN_NAVIGATION: NavigationParent = [
  {
    label: 'Dashboard',
    Icon: BiSolidDashboard,
    href: '/admin/dashboard',
  },
  {
    label: 'User Responsibility',
    nodeList: [
      {
        label: 'User and responsibility',
        Icon: FaUsersCog,
        href: '/admin/user-and-responsibility',
      },
      {
        label: 'Professor and section distribution',
        Icon: FaChalkboardTeacher,
        href: '/admin/professor-and-section-distribution',
      },
    ],
  },
  {
    label: 'Researchers Profile',
    Icon: HiMiniUserGroup,
    href: '/admin/researchers-profile',
  },
  {
    label: 'Submitted faculty research',
    Icon: FaFolder,
    href: '/admin/submitted-faculty-research',
  },
  {
    label: 'Announcement',
    Icon: IoMdMegaphone,
    href: '/admin/announcement',
  },
  {
    label: 'Repository',
    Icon: SlBookOpen,
    href: '/admin/repository',
  },
];

export const STUDENT_NAVIGATION: Navigation[] = [
  {
    label: 'Dashboard',
    Icon: BiSolidDashboard,
    href: '/student/dashboard',
  },
  {
    label: 'Research Manual',
    Icon: FaFolder,
    href: '/student/research-manual',
  },
  {
    label: 'Collaboration',
    Icon: HiMiniUserGroup,
    href: '/student/collaboration',
  },
  {
    label: 'Ethics and Compliance',
    Icon: FaBalanceScaleLeft,
    href: '/student/ethics-and-compliance',
  },
  {
    label: 'Funding Opportunities',
    Icon: FaCoins,
    href: '/student/funding-opportunities',
  },
  {
    label: 'Training and Workshops',
    Icon: FaCalendar,
    href: '/student/training-and-workshop',
  },
];

export const NAVIGATION: Navigation[] = [
  {
    label: 'Dashboard',
    Icon: BiSolidDashboard,
    href: '/dashboard',
  },
  {
    label: 'Research Manual',
    Icon: FaFolder,
    href: '/research-manual',
  },
  {
    label: 'Collaboration',
    Icon: HiMiniUserGroup,
    href: '/collaboration',
  },
  {
    label: 'Ethics and Compliance',
    Icon: FaBalanceScaleLeft,
    href: '/ethics-and-compliance',
  },
  {
    label: 'Funding Opportunities',
    Icon: FaCoins,
    href: '/funding-opportunities',
  },
  {
    label: 'Training and Workshops',
    Icon: FaCalendar,
    href: '/training-and-workshop',
  },
];

export const DEFAULT_STEPPER_STYLE_CONFIG = {
  activeBgColor: '#FFA500',
  activeTextColor: '#FFFFFF',
  completedBgColor: '#008000',
  completedTextColor: '#FFFFFF',
  inactiveBgColor: '#808080',
  inactiveTextColor: '#FFFFFF',
  size: '2.5em',
  circleFontSize: '1.5rem',
  labelFontSize: '12px',
  borderRadius: '50%',
  fontWeight: 600,
};

export const DASHBOARD_STEPS: CustomStep[] = [
  {
    label: 'PROPOSAL',
    Icon: FaBook,
  },
  {
    label: 'RESEARCH PROTOCOL',
    Icon: FaFileAlt,
  },
  {
    label: 'FULL MANUSCRIPT',
    Icon: FaScroll,
  },
  {
    label: 'COPYRIGHT',
    Icon: FaCopyright,
  },
];

export const USER_ROLE = {
  STUDENT: 'STUDENT',
  FACULTY: 'FACULTY',
  ADMIN: 'ADMIN',
};

export const USERS_KEY = '/users';
export const ALL_USER_KEY = '/users/all_user';
export const FACULTY_WITH_ROLES_KEY = '/users/users_faculty_with_roles';
export const ADMIN_FACULTY_WITH_ROLES_KEY = '/admin/users_faculty_with_roles';
export const USER_FACULTY_WITH_ROLES_KEY = '/users/users_faculty_with_roles';
export const COURSE_WITH_YEAR_LIST_KEY = '/users/course_with_year_list';
export const RESEARCH_KEY = '/research';
export const STUDENT_LIST_KEY = '/users/student_list';
export const FACULTY_LIST_KEY = '/users/faculty_list';
export const COMMENT_KEY = '/comments';
export const FACULTY_ADVISER_KEY = '/faculty/adviser';
export const ETHICS_KEY = '/ethics';
export const FULL_MANUSCRIPT_KEY = '/fullmanuscript';
export const COPYRIGHT_DOCUMENTS_KEY = '/copyright';
export const RESEARCH_PROF_LIST_KEY = '/users/research_prof_list';
export const ANNOUNCEMENT_LIST_KEY =
  '/announcement/announcements_with_user_names/';
export const ANNOUNCEMENT_KEY = '/announcement/announcement';
export const COURSE_LIST_KEY = '/users/course_list';
export const ASSIGN_PROF_TO_SECTION_KEY = '/admin/prof-with-assigned';
export const STUDENT_PROFILE_KEY = '/users/profile/student';
export const FACULTY_PROFILE_KEY = '/users/profile/faculty';
export const ADVISER_KEY = '/researchprof/adviser';
export const ADVISER_WITH_ASSIGNED_KEY = '/researchprof/adviser-with-assigned';
export const SUBMITTED_WORKFLOWS_KEY = '/researchprof/workflows/all-list';
export const DISPLAY_ALL_PROCESS_KEY = '/researchprof/display-process-all/';
export const SECTION_KEY = '/sections';

export const STUDENT_ANNOUNCEMENTS_FUNDING_OPPORTUNITY =
  '/announcement/announcements_for-student/FundingOpportunity';

export const STUDENT_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP =
  '/announcement/announcements_for-student/Training&Workshop';

export const FACULTY_ANNOUNCEMENTS_FUNDING_OPPORTUNITY =
  '/announcement/announcements_for-faculty/FundingOpportunity';

export const FACULTY_ANNOUNCEMENTS_TRAINING_AND_WORKSHOP =
  '/announcement/announcements_for-faculty/Training&Workshop';

export const WORKFLOW_LIST_NAME_PROCESS_STUDENT =
  '/workflow/workflows-list-name-process-student';

export const STUDENT_MY_WORKFLOW = '/student/myflow';

export const STATUS_STYLE = {
  pending: 'bg-[#ffff00] text-black hover:bg-[#ffff00]/90',
  approved: 'bg-[#008000] text-white hover:bg-[#008000]/90',
  rejected: 'bg-[#ff0000] text-white hover:bg-[#ff0000]/90',
};

export const STANDARD_STATUS_STYLE = {
  pending: 'text-yellow-500',
  approved: 'text-green-500',
  rejected: 'text-red-500',
};

export const USER_TYPES = {
  STUDENT: 'student',
  FACULTY: 'faculty',
  ADMIN: 'admin',
  RESEARCH_ADVISER: 'research adviser',
  RESEARCH_PROFESSOR: 'research professor',
};

export const STUDENT_TYPES = {
  STUDENT: 'student',
};

export const FACULTY_TYPES = {
  FACULTY: 'faculty',
  ADMIN: 'admin',
  RESEARCH_ADVISER: 'research adviser',
  RESEARCH_PROFESSOR: 'research professor',
};

export const ADMIN_TYPES = {
  ADMIN: 'admin',
};
