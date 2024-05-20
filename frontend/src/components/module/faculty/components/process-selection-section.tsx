"use client";
import { Unauthorized } from "@/components/global";
import { useGetAdviserWithAssignedList } from "@/hooks/use-faculty-query";
import { useGetFacultyProfile } from "@/hooks/use-user-query";
import React, { useMemo } from "react";
import { WorkflowCard } from "./card/workflow-card";

const AUTHORIZE_ROLES = ["research professor"];

export function ProcessSelectionSection() {
  // Assuming useGetAdviserWithAssignedList and useGetFacultyProfile are custom hooks returning data and loading states
  const { data: adviserAssignedList } = useGetAdviserWithAssignedList();
  const { data: facultyProfile, isLoading: facultyProfileIsLoading } =
    useGetFacultyProfile();

  const isAuthorized = useMemo(() => {
    const profile = facultyProfile?.result;
    return Boolean(
      profile && profile.roles.some((role) => AUTHORIZE_ROLES.includes(role))
    );
  }, [facultyProfile]);

  const adviserAssignedListGroup = useMemo(() => {
    if (!adviserAssignedList) return [];

    const groupings: { [key: string]: AdviserDataGroup } = {}; // Define the type of groupings

    adviserAssignedList.forEach((data) => {
      (data.assignments || []).forEach(
        ({ research_type_name, research_type_id }) => {
          if (!groupings[research_type_name]) {
            groupings[research_type_name] = {
              research_type_name,
              id: research_type_id,
              list: [],
            };
          }
          groupings[research_type_name].list.push(data);
        }
      );
    });

    return Object.values(groupings);
  }, [adviserAssignedList]);

  return (
    <>
      {!facultyProfileIsLoading && (
        <section>
          {isAuthorized ? (
            <div className="space-y-10">
              {adviserAssignedListGroup.map(({ research_type_name }, idx) => (
                <WorkflowCard key={idx} research_type={research_type_name} />
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
