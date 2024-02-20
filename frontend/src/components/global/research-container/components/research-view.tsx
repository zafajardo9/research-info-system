'use client';

import UpdateResearchSheet from '@/components/module/student/components/update-research-sheet';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { risApi } from '@/lib/api';
import { RESEARCH_KEY } from '@/lib/constants';
import { cn, isURL } from '@/lib/utils';
import DocViewer, { DocViewerRenderers } from '@cyntler/react-doc-viewer';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { BsFillPersonFill } from 'react-icons/bs';
import { IoChevronBackSharp } from 'react-icons/io5';
import Cooldown from '../../cooldown';
import { ApproveDialog } from './approve-dialog';
import { CommentSection } from './comment-section';
import { ExtensionDropdown } from './extension-dropdown';
import { RejectDialog } from './reject-dialog';
import { ReviseDialog } from './revise-dialog';

export interface ResearchPaperDetails {
  research_paper: ResearchPaper[];
  authors: Author[];
}

export interface ResearchPaper {
  id: string;
  title: string;
  submitted_date: string;
  status: string;
  file_path: string;
  research_adviser: string;
  faculty_name: string;
  research_type: string;
  extension: string | null;
  modified_at: string;
}

export interface Author {
  id: string;
  name: string;
  student_number: string;
  section: string;
  course: string;
}

export interface ResearchViewProps {
  id: string;
  showUpdateSheet?: boolean;
  showApproveDialog?: boolean;
  showReviseDialog?: boolean;
  showRejectDialog?: boolean;
  showBackButton?: boolean;
  hideExtensionDropdown?: boolean;
  hasCooldown?: boolean;
}

export function ResearchView({
  id,
  showUpdateSheet = false,
  showApproveDialog = false,
  showReviseDialog = false,
  showRejectDialog = false,
  showBackButton = false,
  hideExtensionDropdown = false,
  hasCooldown = false,
}: ResearchViewProps) {
  const router = useRouter();
  const [isCooldown, setIsCooldown] = useState<boolean>(false);

  const { data: session, status } = useSession();

  const { data: researchWithAuthors, isLoading } =
    useQuery<ResearchPaperDetails>({
      queryKey: [RESEARCH_KEY, id],
      queryFn: async () => {
        const res = await risApi.get<ResearchPaperDetails>(
          `${RESEARCH_KEY}/${id}`,
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

  const research = researchWithAuthors?.research_paper?.[0];

  const authors = researchWithAuthors?.authors ?? [];

  const docs = [
    {
      uri: research?.file_path ?? '',
    },
  ];

  return (
    <>
      {hasCooldown && (
        <Cooldown
          modified_at={research?.modified_at ?? ''}
          isCooldown={isCooldown}
          setIsCooldown={(value) => setIsCooldown(value)}
        />
      )}

      <div className="flex items-start">
        {showBackButton && (
          <div>
            <Button
              type="button"
              variant="secondary"
              className="gap-2"
              onClick={() => router.back()}
            >
              <IoChevronBackSharp />
              <span>Back</span>
            </Button>
          </div>
        )}

        {research && (
          <div className="flex items-start ml-auto gap-2">
            {showUpdateSheet && <UpdateResearchSheet research={research} />}

            {!hideExtensionDropdown && (
              <ExtensionDropdown
                id={research.id}
                extension={research?.extension ?? ''}
                disabled={isCooldown}
              />
            )}

            {showApproveDialog && (
              <ApproveDialog
                id={id}
                disabled={
                  research.status === 'Approved' ||
                  // research.status === 'Revise' ||
                  isCooldown
                }
              />
            )}

            {showReviseDialog && (
              <ReviseDialog
                id={id}
                disabled={research.status === 'Revise' || isCooldown}
              />
            )}

            {showRejectDialog && (
              <RejectDialog
                id={id}
                disabled={research.status === 'Rejected' || isCooldown}
              />
            )}
          </div>
        )}
      </div>

      {isLoading && (
        <div className="space-y-4">
          <Skeleton className="h-4 w-20" />

          <Skeleton className="h-12 w-full" />

          <div className="flex items-center gap-3">
            <Skeleton className="h-5 w-28" />
            <Skeleton className="h-5 w-28" />
          </div>

          <div className="flex items-center gap-3">
            <Skeleton className="h-5 w-40" />
            <Skeleton className="h-5 w-40" />
            <Skeleton className="h-5 w-40" />
          </div>

          <Skeleton className="h-96 w-full" />
        </div>
      )}

      {research && (
        <article className="prose max-w-none">
          <div className="text-xs pb-5 text-muted-foreground uppercase">
            {research.submitted_date}
          </div>

          <h1>{research.title}</h1>

          <div className="flex items-center gap-2">
            <Badge>{research.research_type}</Badge>
            <Badge
              className={cn(
                research.status === 'Pending' &&
                  'bg-yellow-500 hover:bg-yellow-500/80',
                research.status === 'Approved' &&
                  'bg-green-500 hover:bg-green-500/80',
                research.status === 'Rejected' &&
                  'bg-red-500 hover:bg-red-500/80'
              )}
            >
              {research.status}
            </Badge>
          </div>
          {authors && (
            <div className="mt-5 flex items-center gap-3">
              {authors.map(({ id, name }) => (
                <div key={id} className="flex items-center gap-2 capitalize">
                  <BsFillPersonFill /> <span>{name}</span>
                </div>
              ))}
            </div>
          )}
        </article>
      )}

      {research?.file_path && isURL(research.file_path) && (
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

      {research && <CommentSection id={id} />}
    </>
  );
}
