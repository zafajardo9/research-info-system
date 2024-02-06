'use client';

import { Unauthorized } from '@/components/global';
import { useGetAdviserWithAssignedList } from '@/hooks/use-faculty-query';
import { useGetFacultyProfile } from '@/hooks/use-user-query';
import { useId, useMemo, useState } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { UserAndResponsibilityCard } from './card/user-and-responsibility-card';

const AUTHORIZE_ROLES = ['research professor'];

const PROPOSAL_TYPES = [
  'Research',
  'Capstone',
  'Feasibility Study',
  'Business Plan',
];

export function UserAndResponsibilitySection() {
  const cardId = useId();

  const { data: facultyProfile, isLoading: facultyProfileIsLoading } =
    useGetFacultyProfile();

  const [addMore, setAddMore] = useState<AdviserDataGroup[]>([]);

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

    setAddMore([]);

    return Object.values(Object.fromEntries(groupingsEntries));
  }, [adviserAssignedList]);

  const profile = facultyProfile?.result;

  const isAuthorized = useMemo<boolean>(() => {
    return Boolean(
      profile && profile.roles.some((role) => AUTHORIZE_ROLES.includes(role))
    );
  }, [profile]);

  const adviserAssignedListGroupMerged = useMemo(
    () => [...adviserAssignedListGroup, ...addMore],
    [addMore, adviserAssignedListGroup]
  );

  const selected_research_types = adviserAssignedListGroupMerged
    .map(({ research_type_name }) => research_type_name)
    .filter((v) => PROPOSAL_TYPES.includes(v));

  return (
    <>
      {profile && !facultyProfileIsLoading && (
        <section>
          {isAuthorized ? (
            <div className="space-y-10">
              {adviserAssignedListGroupMerged.length > 0 ? (
                adviserAssignedListGroupMerged.map(
                  ({ research_type_name, list }, idx) => {
                    const isValidType = PROPOSAL_TYPES.some(
                      (value) =>
                        value.toLowerCase() ===
                        research_type_name?.toLowerCase()
                    );

                    return (
                      <UserAndResponsibilityCard
                        key={cardId + idx}
                        research_type_name={research_type_name}
                        selected_research_types={selected_research_types}
                        advisers={list}
                        addMoreCallback={() => {
                          const key = uuidv4();

                          const cloned = [
                            ...addMore,
                            { research_type_name: key, id: '', list: [] },
                          ];

                          setAddMore(cloned);
                        }}
                        removeCallback={(key) => {
                          const filtered = [...addMore].filter(
                            ({ research_type_name }) =>
                              research_type_name !== key
                          );

                          setAddMore(filtered);
                        }}
                        hideAddMore={
                          adviserAssignedListGroupMerged.length !== idx + 1 ||
                          adviserAssignedListGroupMerged.length === 4 ||
                          !isValidType
                        }
                      />
                    );
                  }
                )
              ) : (
                <UserAndResponsibilityCard
                  research_type_name=""
                  advisers={[]}
                  addMoreCallback={() => {
                    const key = uuidv4();

                    const cloned = [
                      ...addMore,
                      { research_type_name: key, id: '', list: [] },
                    ];

                    setAddMore(cloned);
                  }}
                  hideAddMore
                />
              )}
            </div>
          ) : (
            <Unauthorized />
          )}
        </section>
      )}
    </>
  );
}
