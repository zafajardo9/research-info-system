'use client';

import { Skeleton } from '@/components/ui/skeleton';
import { useId } from 'react';
import { useGetAdminResearchTypeAnalytics } from '../../hooks/use-admin-analytics-query';

export interface UserAnalytics {
  Students: number;
  'Research Adviser': number;
  'Research Professor': number;
}

export interface ProposalAnalytics {
  'Approved Proposal': number;
  'For Revision Proposal': number;
}

export interface EthicsAnalytics {
  'Approved Ethics': number;
  'For Revision Ethics': number;
}

export interface ManuscriptAnalytics {
  'Approved Full Manuscript': number;
  'For Revision Full Manuscript': number;
}

export interface CopyrightAnalytics {
  'Approved Copyright': number;
  'For Revision Copyright': number;
}

export interface AdminResearchTypeAnalyticProps {
  type: string;
}

export function AdminResearchTypeAnalytic({
  type,
}: AdminResearchTypeAnalyticProps) {
  const skeletonId = useId();

  const { data = [], isLoading } = useGetAdminResearchTypeAnalytics({ type });

  const userAnalytics = data.find((e) => 'Students' in e) as UserAnalytics;

  const proposalAnalytics = data.find(
    (e) => 'Approved Proposal' in e
  ) as ProposalAnalytics;

  const ethicsAnalytics = data.find(
    (e) => 'Approved Ethics' in e
  ) as EthicsAnalytics;

  const manuscriptAnalytics = data.find(
    (e) => 'Approved Full Manuscript' in e
  ) as ManuscriptAnalytics;

  const copyrightAnalytics = data.find(
    (e) => 'Approved Copyright' in e
  ) as CopyrightAnalytics;

  return (
    <div>
      {isLoading && (
        <div className="flex flex-wrap gap-6 items-center">
          {Array.from({ length: 11 }).map((_, idx) => (
            <Skeleton
              key={skeletonId + idx}
              className="h-20 max-w-[300px] w-full rounded-xl"
            />
          ))}
        </div>
      )}

      {!isLoading && data ? (
        <div className="flex flex-wrap gap-6 items-center">
          {userAnalytics ? (
            <>
              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">Professor</div>
                <div className="text-4xl font-bold text-primary">
                  {userAnalytics?.['Research Professor']}
                </div>
              </div>

              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">Adviser</div>
                <div className="text-4xl font-bold text-primary">
                  {userAnalytics?.['Research Adviser']}
                </div>
              </div>

              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">Student</div>
                <div className="text-4xl font-bold text-primary">
                  {userAnalytics?.Students}
                </div>
              </div>
            </>
          ) : null}

          {proposalAnalytics ? (
            <>
              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">Approved Proposal</div>
                <div className="text-4xl font-bold text-primary">
                  {proposalAnalytics?.['Approved Proposal']}
                </div>
              </div>

              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">For Revision Proposal</div>
                <div className="text-4xl font-bold text-primary">
                  {proposalAnalytics?.['For Revision Proposal']}
                </div>
              </div>
            </>
          ) : null}

          {ethicsAnalytics ? (
            <>
              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">Approved Ethics</div>
                <div className="text-4xl font-bold text-primary">
                  {ethicsAnalytics?.['Approved Ethics']}
                </div>
              </div>

              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">For Revision Ethics</div>
                <div className="text-4xl font-bold text-primary">
                  {ethicsAnalytics?.['For Revision Ethics']}
                </div>
              </div>
            </>
          ) : null}

          {manuscriptAnalytics ? (
            <>
              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">
                  Approved Full Manuscript
                </div>
                <div className="text-4xl font-bold text-primary">
                  {manuscriptAnalytics?.['Approved Full Manuscript']}
                </div>
              </div>

              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">
                  For Revision Full Manuscript
                </div>
                <div className="text-4xl font-bold text-primary">
                  {manuscriptAnalytics?.['For Revision Full Manuscript']}
                </div>
              </div>
            </>
          ) : null}

          {copyrightAnalytics ? (
            <>
              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">Approved Copyright</div>
                <div className="text-4xl font-bold text-primary">
                  {copyrightAnalytics?.['Approved Copyright']}
                </div>
              </div>

              <div className="flex gap-3 items-end justify-between p-6 border max-w-[300px] w-full rounded-xl shadow">
                <div className="text-xl font-medium">
                  For Revision Copyright
                </div>
                <div className="text-4xl font-bold text-primary">
                  {copyrightAnalytics?.['For Revision Copyright']}
                </div>
              </div>
            </>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
