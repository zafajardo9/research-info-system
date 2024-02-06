'use client';

import { AnnouncementContainer } from '@/components/global/announcement-container';
import { Card, CardContent } from '@/components/ui/card';
import {
  useGetFacultyAnnouncementFundingOpportunity,
  useGetFacultyAnnouncementTrainingAndWorkshop,
} from '@/hooks/use-announcement-query';
import { useId } from 'react';
import { IoCloudUploadOutline } from 'react-icons/io5';
import { LuCheckCircle, LuShield, LuXCircle } from 'react-icons/lu';
import { MdOutlinePending } from 'react-icons/md';
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

  const analyticId = useId();

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
                <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-primary bg-primary-foreground text-4xl text-primary">
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

          {ethics && (
            <Card className="w-full max-w-[260px] p-0">
              <CardContent className="flex items-center gap-3 p-5">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-primary bg-primary-foreground text-4xl text-primary">
                  <LuShield />
                </div>
                <div className="space-y-1">
                  <div className="text-4xl font-semibold">
                    {ethics['Approved Ethics']}
                  </div>
                  <div className="text-xs font-semibold">Ethics</div>
                </div>
              </CardContent>
            </Card>
          )}

          {proposal && <Card className="w-full max-w-[260px] p-0">
            <CardContent className="flex items-center gap-3 p-5">
              <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-primary bg-primary-foreground text-4xl text-primary">
                <IoCloudUploadOutline />
              </div>
              <div className="space-y-1">
                <div className="text-4xl font-semibold">{proposal['Approved Proposal']}</div>
                <div className="text-xs font-semibold">Approved Researches</div>
              </div>
            </CardContent>
          </Card>}

          {/* <Card className="w-full max-w-[260px] p-0">
            <CardContent className="flex items-center gap-3 p-5">
              <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-green-500 bg-[#f7f8f8] text-4xl text-green-500">
                <LuCheckCircle />
              </div>
              <div className="space-y-1">
                <div className="text-4xl font-semibold">80</div>
                <div className="text-xs font-semibold">Approved Researches</div>
              </div>
            </CardContent>
          </Card>

          <Card className="w-full max-w-[260px] p-0">
            <CardContent className="flex items-center gap-3 p-5">
              <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-red-500 bg-[#faf9f9] text-4xl text-red-500">
                <LuXCircle />
              </div>
              <div className="space-y-1">
                <div className="text-4xl font-semibold">80</div>
                <div className="text-xs font-semibold">Rejected Researches</div>
              </div>
            </CardContent>
          </Card> */}

          {/* <Card className="w-full max-w-[260px] p-0">
            <CardContent className="flex items-center gap-3 p-5">
              <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-yellow-500 bg-[#f9f9f8] text-4xl text-yellow-500">
                <MdOutlinePending />
              </div>
              <div className="space-y-1">
                <div className="text-4xl font-semibold">80</div>
                <div className="text-xs font-semibold">Pending Researches</div>
              </div>
            </CardContent>
          </Card> */}
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
