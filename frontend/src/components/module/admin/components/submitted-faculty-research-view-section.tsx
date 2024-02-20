'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { useToast } from '@/components/ui/use-toast';
import { risApi } from '@/lib/api';
import DocViewer, { DocViewerRenderers } from '@cyntler/react-doc-viewer';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import parse from 'html-react-parser';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { BiLoaderAlt } from 'react-icons/bi';
import { FaCheck, FaXmark } from 'react-icons/fa6';
import { IoChevronBackSharp } from 'react-icons/io5';
import { useGetFacultyResearchPaperById } from '../hooks/use-faculty-research-papers';

export interface SubmittedFacultyResearchViewSectionProps {
  id: string;
}

export function SubmittedFacultyResearchViewSection({
  id,
}: SubmittedFacultyResearchViewSectionProps) {
  const { toast } = useToast();
  const [openReject, setOpenReject] = useState<boolean>(false);

  const router = useRouter();

  const { data: researchPaper, isLoading } = useGetFacultyResearchPaperById({
    research_paper_id: id,
  });

  const docs = [
    {
      uri: researchPaper?.file_path ?? '',
    },
  ];

  return (
    <section className="p-6">
      <div className="mb-10 flex items-center justify-between">
        <Button
          type="button"
          variant="secondary"
          className="gap-2"
          onClick={() => router.back()}
        >
          <IoChevronBackSharp />
          <span>Back</span>
        </Button>

        <div className="space-x-3">
          <ApproveDialog
            id={id}
            disabled={researchPaper?.status === 'Approved'}
          />
          <RejectDialog
            id={id}
            disabled={researchPaper?.status === 'Rejected'}
          />
        </div>
      </div>
      <Card>
        <CardContent className="py-6 space-y-10">
          {Boolean(researchPaper) && (
            <div className="space-y-6">
              <div className="space-y-1 text-sm">
                <div className="font-semibold">Title</div>
                <div>{researchPaper?.title}</div>
              </div>

              <div className="space-y-1 text-sm">
                <div className="font-semibold">Category</div>
                <div>{researchPaper?.category}</div>
              </div>

              <div className="space-y-1 text-sm">
                <div className="font-semibold">Publisher</div>
                <div>{researchPaper?.publisher}</div>
              </div>

              {researchPaper?.content && (
                <div className="space-y-1 text-sm">
                  <div className="font-semibold">Content</div>
                  <div className="prose prose-sm max-w-none">
                    {parse(researchPaper?.content)}
                  </div>
                </div>
              )}

              {researchPaper?.abstract && (
                <div className="space-y-1 text-sm">
                  <div className="font-semibold">Abstract</div>
                  <div className="prose prose-sm max-w-none">
                    {parse(researchPaper?.abstract)}
                  </div>
                </div>
              )}

              {researchPaper?.keywords && (
                <div className="space-y-1 text-sm">
                  <div className="font-semibold">Keywords</div>
                  <div className="prose prose-sm max-w-none">
                    {parse(researchPaper?.keywords)}
                  </div>
                </div>
              )}

              {researchPaper?.file_path && (
                <div className="mt-10">
                  <DocViewer
                    documents={docs}
                    pluginRenderers={DocViewerRenderers}
                    theme={{
                      primary: '#f4f4f4',
                      textPrimary: '#000000',
                    }}
                  />
                </div>
              )}

              <div className="space-y-1 text-sm">
                <div className="font-semibold">Date Publish</div>
                <div>{researchPaper?.date_publish}</div>
              </div>
            </div>
          )}

          {isLoading && (
            <div className="w-full h-40 relative flex items-center justify-center">
              <div className="flex items-center gap-2 font-semibold">
                The table is currently loading. Please wait for a moment.
                <span className="h-fit w-fit text-2xl animate-spin">
                  <BiLoaderAlt />
                </span>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </section>
  );
}

function ApproveDialog({
  id,
  disabled = false,
}: {
  id: string;
  disabled?: boolean;
}) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const { toast } = useToast();

  const update = useMutation({
    mutationFn: (payload: { status: string }) => {
      return risApi.put(`/admin/approve-faculty-paper/${id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
        params: { id },
      });
    },

    onSuccess() {
      // prettier-ignore
      queryClient.invalidateQueries({ queryKey: [`/admin/faculty-paper-view/${id}`] });
    },
  });

  async function approveHandler() {
    try {
      setIsSubmitting(true);

      await update.mutateAsync({ status: 'Approved' });

      toast({
        title: 'Approve Copyrighted Research Success',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Approve Copyrighted Research Failed',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Dialog
      open={open}
      defaultOpen={open}
      onOpenChange={() => setOpen((prev) => !prev)}
    >
      <DialogTrigger asChild>
        <Button className="gap-2" disabled={disabled}>
          <FaCheck /> <span>Approve</span>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Approve Copyrighted Research</DialogTitle>
        </DialogHeader>
        <div>
          <p>Do you want to approve this Copyrighted Research?</p>
        </div>
        <DialogFooter>
          <Button onClick={approveHandler} disabled={isSubmitting}>
            {isSubmitting ? (
              <span className="h-fit w-fit animate-spin">
                <BiLoaderAlt />
              </span>
            ) : (
              'Approve'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function RejectDialog({
  id,
  disabled = false,
}: {
  id: string;
  disabled?: boolean;
}) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const { toast } = useToast();

  const update = useMutation({
    mutationFn: (payload: { status: string }) => {
      return risApi.put(`/admin/approve-faculty-paper/${id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
        params: { id },
      });
    },

    onSuccess() {
      // prettier-ignore
      queryClient.invalidateQueries({ queryKey: [`/admin/faculty-paper-view/${id}`] });
    },
  });

  async function rejectHandler() {
    try {
      setIsSubmitting(true);

      await update.mutateAsync({ status: 'Rejected' });

      toast({
        title: 'Reject Copyrighted Research Success',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Reject Copyrighted Research Failed',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <Dialog
      open={open}
      defaultOpen={open}
      onOpenChange={() => setOpen((prev) => !prev)}
    >
      <DialogTrigger asChild>
        <Button variant="destructive" className="gap-2" disabled={disabled}>
          <FaXmark /> <span>Reject</span>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Reject Copyrighted Research</DialogTitle>
        </DialogHeader>
        <div>
          <p>Do you want to reject this Copyrighted Research?</p>
        </div>
        <DialogFooter>
          <Button
            variant="destructive"
            onClick={rejectHandler}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <span className="h-fit w-fit animate-spin">
                <BiLoaderAlt />
              </span>
            ) : (
              'Reject'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
