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
import { AssignedSectionsAsAdviser } from '../../hooks/use-faculty-process';
import { useFacultyWorkflowContext } from '../context/faculty-workflow';

const RESEARCH_PROFESSOR = 'research professor';

export interface ResearchAdvisersDropdownsProps {
  assignedSectionsAsAdviser: AssignedSectionsAsAdviser[];
}

export function ResearchAdvisersDropdowns({
  assignedSectionsAsAdviser = [],
}: ResearchAdvisersDropdownsProps) {
  const sectionId = useId();

  const {
    researchType,
    setSelectedProcess,
    selectedProcessIndex,
    setSelectedProcessIndex,
  } = useFacultyWorkflowContext();

  const process =
    researchType !== RESEARCH_PROFESSOR
      ? assignedSectionsAsAdviser.find(
          ({ research_type_name }) => research_type_name === researchType
        )
      : undefined;

  const sections: ComboboxOptions[] = (process?.assignsection ?? []).reduce(
    (collection, { id, class_id, course, section }) => {
      const isExist = collection.some(({ value }) => value === class_id);

      if (!isExist) {
        collection.push({ value: id, label: `${course} - ${section}` });
      }

      return collection;
    },
    [] as ComboboxOptions[]
  );

  return (
    <div className="space-y-4">
      <Select
        defaultValue=""
        disabled={sections.length < 1}
        onValueChange={(e) => {
          if (researchType !== RESEARCH_PROFESSOR) {
            const assigned = process?.assignsection?.find(({ id }) => id === e);
            setSelectedProcess(assigned ?? null);
            setSelectedProcessIndex(0);
          }
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
    </div>
  );
}
