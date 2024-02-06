'use client';

import { type ComboboxOptions } from '@/components/ui/combobox';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { useId } from 'react';
import { type Assignsection } from '../../hooks/use-faculty-process';
import { useFacultyWorkflowContext } from '../context/faculty-workflow';

const RESEARCH_PROFESSOR = 'research professor';

export interface ResearchProfessorsDropdownsProps {
  assignedSections: Assignsection[];
}

export function ResearchProfessorsDropdowns({
  assignedSections = [],
}: ResearchProfessorsDropdownsProps) {
  const sectionId = useId();
  const sectionResearchTypeId = useId();

  const {
    researchType,
    selectedProcess,
    setSelectedProcess,
    setSelectedProcessIndex,
  } = useFacultyWorkflowContext();

  const sections: ComboboxOptions[] = assignedSections.reduce(
    (collection, { id, class_id, course, section }) => {
      const isExist = collection.some(({ value }) => value === class_id);

      if (!isExist) {
        collection.push({
          value: id,
          label: `${course} - ${section}`,
        });
      }

      return collection;
    },
    [] as ComboboxOptions[]
  );

  // const sectionsResearchTypes = useMemo<ComboboxOptions[]>(() => {
  //   const researchTypes: ComboboxOptions[] = [];

  //   if (Boolean(selectedProcess)) {
  //     const process = selectedProcess?.process ?? [];

  //     process.forEach(({ type }, idx) => {
  //       researchTypes.push({ value: idx.toString(), label: type });
  //     });
  //   }

  //   return researchTypes;
  // }, [selectedProcess]);

  const sectionsResearchTypes: ComboboxOptions[] = (
    selectedProcess?.process ?? []
  ).map(({ type }, idx) => {
    return { value: idx.toString(), label: type };
  });

  return (
    <div className="space-y-4">
      <Select
        defaultValue=""
        disabled={sections.length < 1}
        onValueChange={(e) => {
          const assigned = assignedSections.find(({ id }) => id === e);
          setSelectedProcess(assigned ?? null);
        }}
      >
        <SelectTrigger className="bg-primary text-white [&>svg]:hidden text-center rounded-xl justify-center font-semibold">
          <SelectValue placeholder="Select Section" />
        </SelectTrigger>

        <SelectContent>
          {sections.map((option, idx) => (
            <SelectItem
              key={sectionId + idx}
              value={option.value}
              className="capitalize"
            >
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select
      defaultValue=''
        disabled={sectionsResearchTypes.length < 1}
        onValueChange={(e) => {
          if (researchType === RESEARCH_PROFESSOR) {
            setSelectedProcessIndex(parseInt(e));
          }
        }}
      >
        <SelectTrigger className="bg-primary text-white [&>svg]:hidden text-center rounded-xl justify-center font-semibold">
          <SelectValue placeholder="Select Research Type" />
        </SelectTrigger>

        <SelectContent>
          {sectionsResearchTypes.map((option, idx) => (
            <SelectItem
              key={sectionResearchTypeId + idx}
              value={option.value}
              className="capitalize"
            >
              {option.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
