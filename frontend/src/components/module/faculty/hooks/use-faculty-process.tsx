import { risApi } from '@/lib/api';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface ShowFacultyProcess {
  role: string[];
  assigned_sections_as_prof: Assignsection[];
  assigned_sections_as_adviser: AssignedSectionsAsAdviser[];
}

export interface AssignedSectionsAsAdviser {
  assigned_type_id: string;
  research_type_name: string;
  assignsection: Assignsection[];
}

export interface Assignsection {
  id: string;
  class_id: string;
  course: string;
  section: string;
  process: Process[];
}

export interface Process {
  role: string;
  type: string;
  has_submitted_proposal: boolean;
  has_pre_oral_defense_date: boolean;
  has_submitted_ethics_protocol: boolean;
  has_submitted_full_manuscript: boolean;
  has_set_final_defense_date: boolean;
  has_submitted_copyright: boolean;
}

export const SHOW_FACULTY_PROCESS_KEY =
  '/show-faculty-process/process-of-current-user/';

export function useGetShowFacultyProcess() {
  const { data: session, status } = useSession();

  return useQuery<ShowFacultyProcess>({
    queryKey: [SHOW_FACULTY_PROCESS_KEY],
    queryFn: async () => {
      const res = await risApi.get<ShowFacultyProcess>(
        SHOW_FACULTY_PROCESS_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: true,
  });
}
