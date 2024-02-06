import { risApi } from '@/lib/api';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export interface FacultyDefense {
  id: string;
  title: string;
  time: string;
  date: string;
}

export function useGetFacultyDefense({
  course,
  section,
  research_type,
  defense_type,
}: {
  course?: string;
  section?: string;
  defense_type?: string;
  research_type?: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/faculty/adviser/defense/${course}/${section}`;

  return useQuery<FacultyDefense[]>({
    queryKey: [PATH_KEY, research_type, defense_type],
    queryFn: async () => {
      const res = await risApi.get<FacultyDefense[]>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
        params: {
          research_type,
          defense_type,
        },
      });
      return res.data;
    },
    enabled:
      status === 'authenticated' &&
      Boolean(research_type) &&
      Boolean(course) &&
      Boolean(section) &&
      Boolean(defense_type),
  });
}

export interface FacultySetDefenseDate {
  id: string
  created_at: string
  defense_type: string
  time: string
  research_type: string
  modified_at: string
  date: string
  class_id: string
}

export const FACULTY_SET_DEFENSE_DATE_DISPLAY_KEY =
  '/defense/faculty-set-date-display/';

export function useGetFacultyDefenseSetDateDisplay({
  research_type,
  defense_type,
  class_id,
}: {
  research_type?: string;
  defense_type?: string;
  class_id?: string;
}) {
  const { data: session, status } = useSession();

  return useQuery<FacultySetDefenseDate>({
    queryKey: [
      FACULTY_SET_DEFENSE_DATE_DISPLAY_KEY,
      research_type,
      defense_type,
    ],
    queryFn: async () => {
      const res = await risApi.get<FacultySetDefenseDate>(
        FACULTY_SET_DEFENSE_DATE_DISPLAY_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
          params: { research_type, defense_type, class_id },
        }
      );
      return res.data;
    },
    enabled:
      status === 'authenticated' &&
      Boolean(research_type) &&
      Boolean(defense_type) &&
      Boolean(class_id),
    refetchOnMount: true,
  });
}

export interface UploadDefensePayload {
  research_type?: string;
  defense_type: string;
  date: string;
  time: string;
  class_id: string;
}

export function useFacultyDefenseSetDate() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: (payload: UploadDefensePayload) => {
      return risApi.post('/defense/faculty-set-date', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },
  });
}

export interface FacultyDefenseSetClassPayload {
  set_id: string;
  class_id: string;
}

export function useFacultyDefenseSetClass() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: ({ set_id, class_id }: FacultyDefenseSetClassPayload) => {
      return risApi.post(
        `/defense/faculty-set-date/class/${set_id}`,
        { class_id },
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },
  });
}

export interface FacultyUpdateDefensePayload {
  id: string;
  research_type: string;
  defense_type: string;
  date: string;
  time: string;
}

export function useFacultyUpdateDefense() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: ({ id, ...payload }: FacultyUpdateDefensePayload) => {
      return risApi.put(`/defense/faculty-update-date/${id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },
  });
}
