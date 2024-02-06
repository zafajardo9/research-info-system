import { risApi } from '@/lib/api';
import {
  ADVISER_KEY,
  ADVISER_WITH_ASSIGNED_KEY,
  FACULTY_ADVISER_KEY,
  FACULTY_LIST_KEY,
  USER_FACULTY_WITH_ROLES_KEY,
} from '@/lib/constants';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useGetFacultyAdviser() {
  const { data: session, status } = useSession();

  return useQuery<Research[]>({
    queryKey: [FACULTY_ADVISER_KEY],
    queryFn: async () => {
      const res = await risApi.get<Research[]>(FACULTY_ADVISER_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: true,
  });
}

export function useGetFaculties() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<Faculty[]>>({
    queryKey: [FACULTY_LIST_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<Faculty[]>>(
        FACULTY_LIST_KEY,
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
  });
}

export function useGetAdviserAssigned(user_id: string) {
  const { data: session, status } = useSession();

  return useQuery<AdviserData>({
    queryKey: [ADVISER_KEY, user_id],
    queryFn: async () => {
      const res = await risApi.get<AdviserData>(
        `${ADVISER_KEY}/${user_id}/assigned`,
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export function useGetAdviserWithAssignedList() {
  const { data: session, status } = useSession();

  return useQuery<AdviserData[]>({
    queryKey: [ADVISER_WITH_ASSIGNED_KEY],
    queryFn: async () => {
      const res = await risApi.get<AdviserData[]>(ADVISER_WITH_ASSIGNED_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated',
  });
}

export function useGetAdviserById({
  user_id,
  research_type,
  enabled = false,
}: {
  user_id: string;
  research_type: string;
  enabled?: boolean;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/researchprof/adviser/${user_id}/assigned`;

  return useQuery<AdviserData>({
    queryKey: [PATH_KEY, research_type],
    queryFn: async () => {
      const res = await risApi.get<AdviserData>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated' && enabled,
  });
}

export function useGetAdviserListByResearchType({
  research_type,
}: {
  research_type: string;
}) {
  const { data: session, status } = useSession();

  const PATH_KEY = `/researchprof/adviser/${research_type}/list`;

  return useQuery<ResearchTypeData[]>({
    queryKey: [PATH_KEY],
    queryFn: async () => {
      const res = await risApi.get<ResearchTypeData[]>(PATH_KEY, {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
      });
      return res.data;
    },
    enabled: status === 'authenticated' && Boolean(research_type),
  });
}

export function useAdminAssignResearchAdviserRole() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: ({ user_id }: { user_id: string; research_type: string }) => {
      return risApi.post(
        `/researchprof/assign-adviser/${user_id}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },
  });
}

export function useAdminAssignResearchAdviser() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: { user_id: string; research_type_name: string }) => {
      return risApi.post('/researchprof/assign-adviser-type/', payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { research_type_name }) {
      // cancel any outgoing refetches
      await queryClient.cancelQueries({
        queryKey: [ADVISER_WITH_ASSIGNED_KEY],
      });

      await queryClient.cancelQueries({
        queryKey: [USER_FACULTY_WITH_ROLES_KEY],
      });

      await queryClient.cancelQueries({
        queryKey: [`/researchprof/adviser/${research_type_name}/list`],
      });

      // validate
      await queryClient.invalidateQueries({
        queryKey: [ADVISER_WITH_ASSIGNED_KEY],
      });

      await queryClient.invalidateQueries({
        queryKey: [USER_FACULTY_WITH_ROLES_KEY],
      });

      await queryClient.invalidateQueries({
        queryKey: [`/researchprof/adviser/${research_type_name}/list`],
      });
    },
  });
}

export function useAdminRemoveAssignResearchAdviserRole() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ user_id }: { user_id: string; research_type: string }) => {
      return risApi.delete(`/researchprof/remove-adviser-role/${user_id}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess(_, { research_type }) {
      // cancel any outgoing refetches
      await queryClient.cancelQueries({
        queryKey: [ADVISER_WITH_ASSIGNED_KEY],
      });

      await queryClient.cancelQueries({
        queryKey: [USER_FACULTY_WITH_ROLES_KEY],
      });

      await queryClient.cancelQueries({
        queryKey: [`/researchprof/adviser/${research_type}/list`],
      });

      // validate
      await queryClient.invalidateQueries({
        queryKey: [ADVISER_WITH_ASSIGNED_KEY],
      });

      await queryClient.invalidateQueries({
        queryKey: [USER_FACULTY_WITH_ROLES_KEY],
      });

      await queryClient.invalidateQueries({
        queryKey: [`/researchprof/adviser/${research_type}/list`],
      });
    },
  });
}

export function useAdminRemoveAssignResearchAdviser() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      user_id,
      research_type
    }: {
      user_id: string;
      research_type: string;
    }) => {
      return risApi.delete(
        `/researchprof/delete-type-and-role/${user_id}/${research_type}`,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    async onSuccess(_, { research_type }) {
      // cancel any outgoing refetches
      await queryClient.cancelQueries({
        queryKey: [ADVISER_WITH_ASSIGNED_KEY],
      });

      await queryClient.cancelQueries({
        queryKey: [USER_FACULTY_WITH_ROLES_KEY],
      });

      await queryClient.cancelQueries({
        queryKey: [`/researchprof/adviser/${research_type}/list`],
      });

      // validate
      await queryClient.invalidateQueries({
        queryKey: [ADVISER_WITH_ASSIGNED_KEY],
      });

      await queryClient.invalidateQueries({
        queryKey: [USER_FACULTY_WITH_ROLES_KEY],
      });

      await queryClient.invalidateQueries({
        queryKey: [`/researchprof/adviser/${research_type}/list`],
      });
    },
  });
}

export interface AssignAdviserSectionPayload {
  research_type: string;
  research_type_id: string;
  user_id: string;
  assignment: Array<{
    class_id: string;
  }>;
}

export function useAssignAdviserSection() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      research_type_id,
      assignment,
    }: AssignAdviserSectionPayload) => {
      return risApi.post(
        `/researchprof/assign-adviser-section/${research_type_id}/`,
        assignment,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    async onSuccess(_, { user_id, research_type }) {
      await queryClient.invalidateQueries({
        queryKey: [`/researchprof/adviser/${user_id}/assigned`, research_type],
      });
    },
  });
}

export function useRemoveAdviserSection() {
  const { data: session } = useSession();

  return useMutation({
    mutationFn: ({ section_id }: { section_id: string }) => {
      return risApi.delete(
        `/researchprof/delete-assigned-sections/${section_id}`,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },
  });
}

export interface UpdateAdviserSectionPayload {
  research_type_id: string;
  user_id: string;
  new_class_id: string;
}

export function useUpdateAdviserSection() {
  const { data: session } = useSession();
  // const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      research_type_id,
      user_id,
      new_class_id,
    }: UpdateAdviserSectionPayload) => {
      return risApi.put(
        `/researchprof/update-assign-adviser-section/${research_type_id}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
          params: { user_id, new_class_id },
        }
      );
    },
  });
}
