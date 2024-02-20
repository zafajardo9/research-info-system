'use client';

import { AnnouncementContainer } from '@/components/global/announcement-container';
import { Card, CardContent } from '@/components/ui/card';
import {
  useGetFacultyAnnouncementFundingOpportunity,
  useGetFacultyAnnouncementTrainingAndWorkshop,
} from '@/hooks/use-announcement-query';
import { FaCheck } from 'react-icons/fa6';
import { FiEdit3 } from 'react-icons/fi';
import { PiChalkboardTeacherLight } from 'react-icons/pi';
import { useGetFacultyAnalytics } from '../hooks/use-analytics-query';
import { useFacultyWorkflowContext } from './context/faculty-workflow';

export interface SectionData {
  Students: number;
  'Research Adviser': number;
  'Research Professor': number;
}

export interface AdviseeData {
  Advisee: number;
}

export interface ProposalData {
  'Approved Proposal': number;
  'For Revision Proposal': number;
}

export interface EthicsData {
  'Approved Ethics': number;
  'For Revision Ethics': number;
}

export interface CopyrightData {
  'Approved Copyright': number;
  'For Revision Copyright': number;
}

export interface ManuscriptData {
  'Approved Full Manuscript': number;
  'For Revision Full Manuscript': number;
}

export function FacultyDashboardSection() {
  const { data: fundingOpportunities } =
    useGetFacultyAnnouncementFundingOpportunity();

  const { data: trainingAndWorkshops } =
    useGetFacultyAnnouncementTrainingAndWorkshop();

  const { selectedProcess, selectedProcessIndex } = useFacultyWorkflowContext();

  const process = selectedProcess?.process?.[selectedProcessIndex];

  const { data: facultyAnalytics = [] } = useGetFacultyAnalytics({
    type: process?.type,
  });

  const advisee = facultyAnalytics?.find(
    (data) => 'Advisee' in data
  ) as AdviseeData;

  const proposal = facultyAnalytics?.find(
    (data) => 'Approved Proposal' in data
  ) as ProposalData;

  const ethics = facultyAnalytics?.find(
    (data) => 'Approved Ethics' in data
  ) as EthicsData;

  const copyright = facultyAnalytics?.find(
    (data) => 'Approved Copyright' in data
  ) as CopyrightData;

  const manuscript = facultyAnalytics?.find(
    (data) => 'Approved Full Manuscript' in data
  ) as ManuscriptData;

  return (
    <section className="space-y-10">
      {facultyAnalytics && (
        <div className="flex flex-wrap items-center gap-4">
          {advisee && (
            <Card className="w-full max-w-[260px] p-0">
              <CardContent className="flex items-center gap-3 p-5">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl border text-4xl">
                  <PiChalkboardTeacherLight />
                </div>
                <div className="space-y-1">
                  <div className="text-4xl font-semibold">
                    {advisee.Advisee}
                  </div>
                  <div className="text-xs font-semibold">Advisee</div>
                </div>
              </CardContent>
            </Card>
          )}

          {proposal && (
            <>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-green-500 bg-green-50 text-4xl text-green-500">
                    <FaCheck />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {proposal['Approved Proposal']}
                    </div>
                    <div className="text-xs font-semibold">
                      Approved Proposal
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-primary bg-primary-foreground text-4xl text-primary">
                    <FiEdit3 />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {proposal['For Revision Proposal']}
                    </div>
                    <div className="text-xs font-semibold">
                      For Revision Proposal
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}

          {ethics && (
            <>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-green-500 bg-green-50 text-4xl text-green-500">
                    <FaCheck />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {ethics['Approved Ethics']}
                    </div>
                    <div className="text-xs font-semibold">Approved Ethics</div>
                  </div>
                </CardContent>
              </Card>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-primary bg-primary-foreground text-4xl text-primary">
                    <FiEdit3 />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {ethics['For Revision Ethics']}
                    </div>
                    <div className="text-xs font-semibold">
                      For Revision Ethics
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}

          {manuscript && (
            <>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-green-500 bg-green-50 text-4xl text-green-500">
                    <FaCheck />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {manuscript['Approved Full Manuscript']}
                    </div>
                    <div className="text-xs font-semibold">
                      Approved Full Manuscript
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-primary bg-primary-foreground text-4xl text-primary">
                    <FiEdit3 />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {manuscript['For Revision Full Manuscript']}
                    </div>
                    <div className="text-xs font-semibold">
                      For Revision Full Manuscript
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}

          {copyright && (
            <>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-green-500 bg-green-50 text-4xl text-green-500">
                    <FaCheck />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {copyright['Approved Copyright']}
                    </div>
                    <div className="text-xs font-semibold">
                      Approved Full Manuscript
                    </div>
                  </div>
                </CardContent>
              </Card>
              <Card className="w-full max-w-[260px] p-0">
                <CardContent className="flex items-center gap-3 p-5">
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-primary bg-primary-foreground text-4xl text-primary">
                    <FiEdit3 />
                  </div>
                  <div className="space-y-1">
                    <div className="text-4xl font-semibold">
                      {copyright['For Revision Copyright']}
                    </div>
                    <div className="text-xs font-semibold">
                      For Revision Copyright
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </div>
      )}

      <div className="space-y-10">
        {fundingOpportunities instanceof Array && (
          <>
            <h2 className="text-xl font-semibold mb-6 text-center">
              Funding And Opportunity
            </h2>

            <div className="space-y-6">
              {fundingOpportunities.map((announcement) => (
                <AnnouncementContainer
                  key={announcement.announcement.id}
                  data={announcement}
                />
              ))}
            </div>
          </>
        )}

        {trainingAndWorkshops instanceof Array && (
          <>
            <h2 className="text-xl font-semibold mb-6 text-center">
              Training And Workshops
            </h2>

            <div className="space-y-6">
              {trainingAndWorkshops.map((announcement) => (
                <AnnouncementContainer
                  key={announcement.announcement.id}
                  data={announcement}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </section>
  );
}
