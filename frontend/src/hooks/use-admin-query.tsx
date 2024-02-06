import { risApi } from '@/lib/api';
import {
  ADMIN_FACULTY_WITH_ROLES_KEY,
  ASSIGN_PROF_TO_SECTION_KEY,
} from '@/lib/constants';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useGetFacultyWithRoles() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<AdminFacultyWithRoles[]>>({
    queryKey: [ADMIN_FACULTY_WITH_ROLES_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<AdminFacultyWithRoles[]>>(
        ADMIN_FACULTY_WITH_ROLES_KEY,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: false,
    refetchOnWindowFocus: false,
  });
}

export function useAdminAssignResearchProf() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ user_id }: { user_id: string }) => {
      return risApi.post(
        `/admin/assign-research-professor/${user_id}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [ADMIN_FACULTY_WITH_ROLES_KEY],
      });
    },
  });
}

export function useAdminRemoveAssignResearchProf() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ user_id }: { user_id: string }) => {
      return risApi.delete(`/admin/remove-professor-role/${user_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [ADMIN_FACULTY_WITH_ROLES_KEY],
      });
    },
  });
}

export function useAdminAssignAdmin() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ user_id }: { user_id: string }) => {
      return risApi.post(
        `/admin/assign-admin/${user_id}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [ADMIN_FACULTY_WITH_ROLES_KEY],
      });
    },
  });
}

export function useAdminRemoveAssignAdmin() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ user_id }: { user_id: string }) => {
      return risApi.delete(`/admin/remove-admin-role/${user_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [ADMIN_FACULTY_WITH_ROLES_KEY],
      });
    },
  });
}

export interface AssignProfessorTypeSectionPayload {
  user_id: string;
  assignment: Array<{
    class_id: string;
  }>;
}

export function useAdminAssignProfessorTypeSection() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: ({
      user_id,
      assignment,
    }: AssignProfessorTypeSectionPayload) => {
      return risApi.post(`/admin/assign-section/${user_id}`, assignment, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },
  });
}

export function useAdminDeleteAssignment() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: ({ assigned_id }: { assigned_id: string }) => {
      return risApi.delete(`/admin/delete-assigned-sections/${assigned_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },
  });
}

export function useGetAssignProfToSection() {
  const { data: session, status } = useSession();

  return useQuery<ProfWithAssign[]>({
    queryKey: [ASSIGN_PROF_TO_SECTION_KEY],
    queryFn: async () => {
      const res = await risApi.get<ProfWithAssign[]>(
        ASSIGN_PROF_TO_SECTION_KEY,
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
