'use client';

import parse from 'html-react-parser';
import moment from 'moment';
import Image from 'next/image';
import { CgProfile } from 'react-icons/cg';

export interface AnnouncementContainerProps {
  data: AnnouncementList;
}

export function AnnouncementContainer({
  data: { faculty_name, announcement },
}: AnnouncementContainerProps) {
  return (
    <div className="overflow-hidden rounded-xl bg-gray-50">
      <div className="flex items-center gap-2 p-6">
        <div className="text-6xl">
          <CgProfile />
        </div>

        <div>
          <div className="text-xl font-semibold">{faculty_name}</div>
          <div className="text-xs text-gray-700">
            {moment(moment.utc(announcement?.created_at).toDate())
              .local(true)
              .fromNow()}
          </div>
        </div>
      </div>

      {announcement?.title && (
        <div className="text-xl font-semibold px-6 py-3">
          {announcement?.title}
        </div>
      )}

      {announcement?.content && (
        <div className="prose max-w-none p-6">
          {parse(announcement?.content)}
        </div>
      )}

      {announcement?.image && (
        <div className="h-96 relative bg-gray-200">
          <Image
            src={announcement?.image}
            alt={announcement?.title}
            fill
            quality={100}
            className="object-contain"
          />
        </div>
      )}

      {announcement?.other_details && (
        <div className="prose max-w-none p-6">
          {parse(announcement?.other_details)}
        </div>
      )}
    </div>
  );
}
