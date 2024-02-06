'use client';

import { Unauthorized } from '@/components/global';
import { useGetAdviserWithAssignedList } from '@/hooks/use-faculty-query';
import { useGetFacultyProfile } from '@/hooks/use-user-query';
import { useId, useMemo } from 'react';
import { WorkflowCard } from './card/workflow-card';

const AUTHORIZE_ROLES = ['research professor'];

// function reduceCB(cache, value) {
//   const key = value.course.toLowerCase();

//   if (cache.has(key)) {
//     const previous = cache.get(key);

//     cache.set(key, [...previous, value]);
//   } else {
//     cache.set(key, [value]);
//   }

//   return cache;
// }

// const grouping = Object.fromEntries(items.reduce(reduceCB, new Map()));

export function ProcessSelectionSection() {
  const cardId = useId();

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

  const { data: facultyProfile, isLoading: facultyProfileIsLoading } =
    useGetFacultyProfile();

  const profile = facultyProfile?.result;

  const isAuthorized = useMemo<boolean>(() => {
    return Boolean(
      profile && profile.roles.some((role) => AUTHORIZE_ROLES.includes(role))
    );
  }, [profile]);

  return (
    <>
      {profile && !facultyProfileIsLoading && (
        <section>
          {isAuthorized ? (
            <div className="space-y-10">
              {adviserAssignedListGroup.map(({ research_type_name }, idx) => (
                <WorkflowCard
                  key={cardId + idx}
                  research_type={research_type_name}
                />
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
