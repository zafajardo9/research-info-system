'use client';

import profileImage from '@/assets/images/profile.png';
import { TiptapEditor } from '@/components/module/tiptap';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Form, FormControl, FormField, FormItem } from '@/components/ui/form';
import { useToast } from '@/components/ui/use-toast';
import { risApi } from '@/lib/api';
import { COMMENT_KEY, USERS_KEY, USER_ROLE } from '@/lib/constants';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { DotsHorizontalIcon, PaperPlaneIcon } from '@radix-ui/react-icons';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import parse from 'html-react-parser';
import moment from 'moment';
import { useSession } from 'next-auth/react';
import Image from 'next/image';
import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { BiLoaderAlt } from 'react-icons/bi';
import * as z from 'zod';
import { messageFormSchema } from '../validation';

export type GetCommentsQueryResponse = ProposalComment[];

export interface CommentSectionProps {
  id: string;
  className?: string;
}

export function CommentSection({ id, className }: CommentSectionProps) {
  const queryClient = useQueryClient();
  const { toast } = useToast();
  const [profileEndPoint, setProfileEndPoint] = useState<string>();

  const { data: session, status } = useSession();

  useEffect(() => {
    const role = session?.user.role as keyof typeof USER_ROLE;

    setProfileEndPoint(() => {
      switch (role) {
        case 'STUDENT':
          return '/profile/student';

        case 'FACULTY':
          return '/profile/faculty';

        case 'ADMIN':
          return '/profile/admin';
      }
    });
  }, [session]);

  const { data: profile } = useQuery<DefaultApiResponse<Profile>>({
    queryKey: [USERS_KEY, 'COMMENT', profileEndPoint],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<Profile>>(
        USERS_KEY + profileEndPoint,
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

  const {
    data: comments = [],
    isFetching,
    isLoading,
    isRefetching,
  } = useQuery<GetCommentsQueryResponse>({
    queryKey: [COMMENT_KEY, id],
    queryFn: async () => {
      const res = await risApi.get<GetCommentsQueryResponse>(
        `${COMMENT_KEY}/${id}`,
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

  const create = useMutation({
    mutationFn: (payload: PostCommentPayload) => {
      return risApi.post(`${COMMENT_KEY}`, payload, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [COMMENT_KEY] });
    },
  });

  const remove = useMutation({
    mutationFn: (commentId: string) => {
      return risApi.delete(`${COMMENT_KEY}/${commentId}`, {
        headers: {
          Authorization: `Bearer ${session?.user.authToken}`,
        },
      });
    },

    onSuccess() {
      queryClient.invalidateQueries({ queryKey: [COMMENT_KEY] });
    },
  });

  const form = useForm<z.infer<typeof messageFormSchema>>({
    resolver: zodResolver(messageFormSchema),
    shouldFocusError: false,
  });

  const {
    watch,
    formState: { isSubmitting },
    reset,
  } = form;

  const watchMessage = watch('message');

  async function deleteCommentHandler(commentId: string) {
    try {
      await remove.mutateAsync(commentId);
    } catch (error: any) {
      toast({
        title: 'Delete Comment Failed',
        variant: 'destructive',
        description: error?.message,
      });
    }
  }

  async function onSubmitMessage(values: z.infer<typeof messageFormSchema>) {
    try {
      await create.mutateAsync({ text: values.message, research_id: id });
      reset({ message: '' });
    } catch (error) {
      toast({
        title: 'Comment Failed',
        variant: 'destructive',
      });
    }
  }

  return (
    <div className={cn('border-t', className)}>
      <div className="text-sm font-bold py-6">Comments</div>
      <div>
        {comments && comments.length > 0 ? (
          comments
            .sort(
              (a, b) =>
                new Date(a.created_at).valueOf() -
                new Date(b.created_at).valueOf()
            )
            .map(
              ({
                id: commentId,
                text,
                user_id,
                created_at,
                user_info: { name },
              }) => (
                <div key={commentId} className="space-y-1 py-3 relative">
                  <div className="flex gap-2">
                    <div>
                      <Image
                        src={profileImage}
                        alt="User profile placeholder"
                        height={40}
                        width={40}
                      />
                    </div>
                    <div className="flex flex-col gap-1 w-fit max-w-2xl">
                      <div className="rounded-2xl p-3 prose prose-sm w-fit max-w-none bg-muted">
                        <h4>{name}</h4>
                        {parse(text)}
                      </div>
                      <div className="text-[9px] font-medium text-muted-foreground">
                        {moment(moment.utc(created_at).toDate())
                          .local(true)
                          .fromNow()}
                      </div>
                    </div>
                    {user_id === profile?.result.id && (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button
                            variant="ghost"
                            className="flex h-8 w-8 p-0 data-[state=open]:bg-muted rounded-full"
                          >
                            <DotsHorizontalIcon className="h-4 w-4" />
                            <span className="sr-only">Open menu</span>
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent
                          align="start"
                          side="right"
                          className="w-[160px] h-fit"
                        >
                          <DropdownMenuItem
                            onClick={() => deleteCommentHandler(commentId)}
                          >
                            Delete
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    )}
                  </div>
                </div>
              )
            )
        ) : (
          <div className="text-sm text-muted-foreground text-center">
            No comments found.
          </div>
        )}
      </div>

      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmitMessage)}
          className="space-y-5 py-6 px-1"
        >
          <FormField
            control={form.control}
            name="message"
            render={({ field }) => (
              <FormItem className="flex flex-col flex-1">
                <FormControl>
                  <TiptapEditor
                    value={field.value}
                    onChange={field.onChange}
                    placeholder="Write a comment..."
                  />
                </FormControl>
              </FormItem>
            )}
          />

          <Button
            className="w-52 gap-2"
            disabled={!Boolean(watchMessage) || isSubmitting}
          >
            {isSubmitting ? (
              <span className="h-fit w-fit animate-spin">
                <BiLoaderAlt />
              </span>
            ) : (
              <>
                <span>Comment</span> <PaperPlaneIcon />
              </>
            )}
          </Button>
        </form>
      </Form>
    </div>
  );
}
