'use client';

import { AnnouncementContainer } from '@/components/global/announcement-container';
import { useGetStudentAnnouncementFundingOpportunity } from '@/hooks/use-announcement-query';

export function FundingSection() {
  const { data: fundingOpportunities = [] } =
    useGetStudentAnnouncementFundingOpportunity();

  return (
    <section>
      <div className="space-y-6">
        {fundingOpportunities.map((announcement) => (
          <AnnouncementContainer
            key={announcement.announcement.id}
            data={announcement}
          />
        ))}
      </div>
    </section>
  );
}
