import { useFacultyWorkflowContext } from '@/components/module/faculty/components/context/faculty-workflow';
import { Button } from '@/components/ui/button';
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
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';
import { useState } from 'react';
import { BiLoaderAlt } from 'react-icons/bi';
import { FaCheck } from 'react-icons/fa6';

export interface ApproveDialogProps {
  id: string;
  disabled?: boolean;
}

export function ApproveDialog({ id, disabled = false }: ApproveDialogProps) {
  const { data: session } = useSession();
  const queryClient = useQueryClient();
  const [open, setOpen] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const { toast } = useToast();


  const update = useMutation({
    mutationFn: (payload: { status: string }) => {
      return risApi.put(`/faculty/approve_ethics/${id}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: [`/ethics/get-ethics/${id}`],
      });
    },
  });

  async function approveHandler() {
    try {
      setIsSubmitting(true);

      await update.mutateAsync({ status: 'Approved' });

      toast({
        title: 'Approve Ethics And Protocol Success',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Approve Ethics And Protocol Failed',
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
          <DialogTitle>Approve ethics and protocol</DialogTitle>
        </DialogHeader>
        <div>
          <p>Do you want to approve this ethics and protocol?</p>
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
