'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import parse from 'html-react-parser';
import { useRouter } from 'next/navigation';
import { useId } from 'react';
import { BsFillPersonFill } from 'react-icons/bs';
import { CgProfile } from 'react-icons/cg';
import { IoChevronBackSharp } from 'react-icons/io5';
import {
  Paper,
  useGetResearcherProfileById,
} from '../hooks/use-researcher-profle-query';

export interface ResearcherProfileContainerProps {
  id: string;
}

export function ResearcherProfileContainer({
  id,
}: ResearcherProfileContainerProps) {
  const router = useRouter();
  const paperId = useId();

  const { data: researchProfile } = useGetResearcherProfileById({ id });

  return (
    <section>
      <div className="p-6">
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

      <div className="p-6 flex items-center gap-2">
        <div className="text-[90px]">
          <CgProfile />
        </div>
        <div>
          <div className="text-3xl font-semibold flex items-center gap-2">
            <span>{researchProfile?.name}</span>
            <Badge>{researchProfile?.status}</Badge>
          </div>

          <div className="text-sm">{researchProfile?.student_number}</div>

          <div className="text-xs text-gray-500">
            {researchProfile?.course} {researchProfile?.section}
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {(researchProfile?.papers ?? []).map((props, idx) => (
          <ResearchPaper key={paperId + idx} {...props} />
        ))}
      </div>
    </section>
  );
}

function ResearchPaper({ research_paper, authors }: Paper) {
  const authorId = useId();

  return (
    <div className="border rounded shadow p-6">
      <div className="space-y-6 ">
        <div className="space-y-1">
          <div className="text-3xl font-semibold">
            {research_paper.title} <Badge>{research_paper.research_type}</Badge>
          </div>
        </div>

        <div className="flex flex-1 flex-wrap gap-3">
          {authors &&
            authors.map(({ name, course, year_section }, idx) => (
              <div key={authorId + idx} className="flex items-center gap-3">
                <div className="text-3xl">
                  <BsFillPersonFill />
                </div>

                <div className="space-y-1">
                  <div className="capitalize text-sm">{name}</div>
                  <div className="capitalize text-xs">
                    {course} {year_section}
                  </div>
                </div>
              </div>
            ))}
        </div>

        {research_paper.content && (
          <div className="space-y-1 text-sm">
            <div className="font-semibold">Content</div>
            <div className="prose prose-sm max-w-none">
              {parse(research_paper.content)}
            </div>
          </div>
        )}

        {research_paper.abstract && (
          <div className="space-y-1 text-sm">
            <div className="font-semibold">Abstract</div>
            <div className="prose prose-sm max-w-none">
              {parse(research_paper.abstract)}
            </div>
          </div>
        )}

        <div className="space-y-1 text-sm">
          <div className="font-semibold">Keywords</div>
          <div>{research_paper.keywords}</div>
        </div>

        {/* {file_path && (
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
        )} */}

        <div className="space-y-1 text-sm">
          <div className="font-semibold">Date Publish</div>
          <div>{research_paper.date_publish}</div>
        </div>
      </div>
    </div>
  );
}
