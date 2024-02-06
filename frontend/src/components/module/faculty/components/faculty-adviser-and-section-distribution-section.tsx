'use client';

import { Unauthorized } from '@/components/global';
import { useGetAdviserWithAssignedList } from '@/hooks/use-faculty-query';
import { useGetFacultyProfile } from '@/hooks/use-user-query';
import { useId, useMemo } from 'react';
import SectionDistributionCard from './card/section-distribution-card';

const AUTHORIZE_ROLES = ['research professor'];

export function FacultyAdviserAndSectionDistributionSection() {
  const cardId = useId();

  const { data: facultyProfile, isLoading: facultyProfileIsLoading } =
    useGetFacultyProfile();

  const profile = facultyProfile?.result;

  const isAuthorized = useMemo<boolean>(() => {
    return Boolean(
      profile && profile.roles.some((role) => AUTHORIZE_ROLES.includes(role))
    );
  }, [profile]);

  const { data: adviserAssignedList } = useGetAdviserWithAssignedList();

  const adviserAssignedListGroup = useMemo<AdviserDataGroup[]>(() => {
    const list = adviserAssignedList ?? [];

    const groupingsEntries = list.reduce((cache, data) => {
      const assignments = data?.assignments ?? [];

      for (const { research_type_name, research_type_id } of assignments) {
        const hasResearchType = cache.has(research_type_name);
        const previousData = cache.get(research_type_name);

        if (hasResearchType && previousData) {
          cache.set(research_type_name, {
            research_type_name,
            id: research_type_id,
            list: [...previousData.list, data],
          });
        } else {
          cache.set(research_type_name, {
            research_type_name,
            id: research_type_id,
            list: [data],
          });
        }
      }

      return cache;
    }, new Map<string, AdviserDataGroup>());

    return Object.values(Object.fromEntries(groupingsEntries));
  }, [adviserAssignedList]);

  return (
    <>
      {profile && !facultyProfileIsLoading && (
        <section>
          {isAuthorized ? (
            <div className="space-y-10">
              {adviserAssignedListGroup.map((data, idx) => (
                <SectionDistributionCard key={cardId + idx} data={data} />
              ))}
            </div>
          ) : (
            <Unauthorized />
          )}
        </section>
      )}
    </>
  );
}
