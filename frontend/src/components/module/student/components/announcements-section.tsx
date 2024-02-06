'use client';

import { AnnouncementContainer } from '@/components/global/announcement-container';
import {
  useGetStudentAnnouncementFundingOpportunity,
  useGetStudentAnnouncementTrainingAndWorkshop,
} from '@/hooks/use-announcement-query';

export function AnnouncementsSection() {
  const { data: fundingOpportunities = [] } =
    useGetStudentAnnouncementFundingOpportunity();

  const { data: trainingAndWorkshops = [] } =
    useGetStudentAnnouncementTrainingAndWorkshop();

  return (
    <section className="space-y-10">
      {fundingOpportunities.length > 0 && (
        <div>
          <div className="text-xl font-semibold mb-6 text-center">
            Funding And Opportunity
          </div>
          <div className="space-y-6">
            {fundingOpportunities.map((announcement) => (
              <AnnouncementContainer
                key={announcement.announcement.id}
                data={announcement}
              />
            ))}
          </div>
        </div>
      )}

      {trainingAndWorkshops.length > 0 && (
        <div>
          <div className="text-xl font-semibold mb-6 text-center">
            Training And Workshops
          </div>
          <div className="space-y-6">
            {trainingAndWorkshops.map((announcement) => (
              <AnnouncementContainer
                key={announcement.announcement.id}
                data={announcement}
              />
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
