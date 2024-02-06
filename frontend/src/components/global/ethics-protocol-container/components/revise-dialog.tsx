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
import { FaPencil } from 'react-icons/fa6';

export interface ReviseDialogProps {
  id: string;
  disabled?: boolean;
}

export function ReviseDialog({ id, disabled = false }: ReviseDialogProps) {
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

      await update.mutateAsync({ status: 'Revise' });

      toast({
        title: 'Revise Ethics And Protocol Success',
      });

      setOpen(false);
    } catch (error) {
      toast({
        title: 'Revise Ethics And Protocol Failed',
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
        <Button
          className="gap-2 bg-blue-500 hover:bg-blue-500/80"
          disabled={disabled}
        >
          <FaPencil /> <span>Revise</span>
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Revise Ethics And Protocol</DialogTitle>
        </DialogHeader>
        <div>
          <p>Do you want to revise this ethics and protocol?</p>
        </div>
        <DialogFooter>
          <Button onClick={approveHandler} disabled={isSubmitting}>
            {isSubmitting ? (
              <span className="h-fit w-fit animate-spin">
                <BiLoaderAlt />
              </span>
            ) : (
              'Revise'
            )}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
