import { risApi } from '@/lib/api';
import { COPYRIGHT_DOCUMENTS_KEY } from '@/lib/constants';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useUploadCopyrightDocument({
  workflowId,
}: {
  workflowId: string;
}) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (payload: UploadCopyrightDocumentsPayload) => {
      return risApi.post(`${COPYRIGHT_DOCUMENTS_KEY}/upload`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    async onSuccess() {
      await queryClient.invalidateQueries({
        queryKey: [`/student/flow-info-status/${workflowId}`],
      });
    },
  });
}

export interface UpdateCopyrightDocumentPayload {
  copyright_id: string;
  co_authorship: string;
  affidavit_co_ownership: string;
  joint_authorship: string;
  approval_sheet: string;
  receipt_payment: string;
  recordal_slip: string;
  acknowledgement_receipt: string;
  certificate_copyright: string;
  recordal_template: string;
  ureb_18: string;
  journal_publication: string;
  copyright_manuscript: string;
}

export function useUpdateCopyrightDocument({
  workflowId,
}: {
  workflowId: string;
}) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      copyright_id,
      ...payload
    }: UpdateCopyrightDocumentPayload) => {
      return risApi.put(
        `${COPYRIGHT_DOCUMENTS_KEY}/update/${copyright_id}`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    async onSuccess() {
      await queryClient.invalidateQueries({
        queryKey: [`/student/flow-info-status/${workflowId}`],
      });
    },
  });
}

export function useDeleteCopyrightDocuments() {
  const { data: session } = useSession();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ copyright_id }: { copyright_id: string }) => {
      return risApi.delete(
        `${COPYRIGHT_DOCUMENTS_KEY}/delete_copyright/${copyright_id}`,
        {
          headers: {
            Authorization: `Bearer ${session?.user.authToken}`,
          },
        }
      );
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [COPYRIGHT_DOCUMENTS_KEY] });
    },
  });
}

export function useGetUserUserCopyrightDocuments() {
  const { data: session, status } = useSession();

  return useQuery<CopyrightDocument[]>({
    queryKey: [COPYRIGHT_DOCUMENTS_KEY],
    queryFn: async () => {
      const res = await risApi.get<CopyrightDocument[]>(
        COPYRIGHT_DOCUMENTS_KEY + '/user',
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
