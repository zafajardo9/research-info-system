'use client';

import logo13 from '@/assets/images/logo13.png';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';
import { Button } from '@/components/ui/button';
import { ComboboxOptions } from '@/components/ui/combobox';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useId, useMemo } from 'react';
import { BiSolidDashboard } from 'react-icons/bi';
import { BsGraphUpArrow } from 'react-icons/bs';
import { FaChalkboardTeacher, FaCopyright, FaUsersCog } from 'react-icons/fa';
import { FaArrowRotateRight } from 'react-icons/fa6';
import { GiFeather } from 'react-icons/gi';
import { HiMiniUserGroup } from 'react-icons/hi2';
import { IoShieldHalf } from 'react-icons/io5';
import { SlBookOpen } from 'react-icons/sl';
import { TbCalendarStats } from 'react-icons/tb';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../../ui/select';
import { useGetShowFacultyProcess } from '../hooks/use-faculty-process';
import { useFacultyWorkflowContext } from './context/faculty-workflow';
import { ResearchAdvisersDropdowns } from './sidebar-dropdown/research-advisers-dropdowns';
import { ResearchProfessorsDropdowns } from './sidebar-dropdown/research-professors-dropdowns';

const RESEARCH_PROFESSOR = 'research professor';

export function FacultySidebar() {
  const labelId = useId();
  const pathname = usePathname();
  const router = useRouter();

  const {
    researchType,
    setResearchType,
    selectedProcess,
    selectedProcessIndex,
    setSelectedProcess,
  } = useFacultyWorkflowContext();

  const { data: facultyProcess } = useGetShowFacultyProcess();

  const researchTypes = useMemo(() => {
    const collection = facultyProcess?.assigned_sections_as_adviser ?? [];
    return collection.map(({ research_type_name }) => research_type_name);
  }, [facultyProcess]);

  useEffect(() => {
    router.push('/faculty/dashboard');

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [researchType, selectedProcess]);

  return (
    <div
      className={cn(
        'hidden xl:fixed xl:flex xl:flex-col xl:inset-y-0 xl:z-50 xl:w-64 transition-all ease-out duration-500 bg-card border-r'
      )}
    >
      <div className="flex justify-center items-center gap-5 h-28 opacity-100">
        <Image src={logo13} alt="PUPQC RIS logo" height={120} width={120} />
      </div>

      <div className="px-4 pt-5 pb-10 space-y-4">
        <Select
          onValueChange={(e) => {
            setResearchType(e);
            setSelectedProcess(null);
          }}
        >
          <SelectTrigger className="bg-primary text-white [&>svg]:hidden text-center rounded-xl justify-center font-semibold">
            <SelectValue placeholder="Select Role" />
          </SelectTrigger>

          <SelectContent>
            {facultyProcess?.role?.includes(RESEARCH_PROFESSOR) && (
              <SelectItem value={RESEARCH_PROFESSOR} className="capitalize">
                Professor
              </SelectItem>
            )}

            {researchTypes.map((option, idx) => (
              <SelectItem
                key={labelId + idx + 'type'}
                value={option}
                className="capitalize"
              >
                {option} Adviser
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {researchType !== RESEARCH_PROFESSOR && facultyProcess && (
          <ResearchAdvisersDropdowns
            assignedSectionsAsAdviser={
              facultyProcess?.assigned_sections_as_adviser ?? []
            }
          />
        )}

        {researchType === RESEARCH_PROFESSOR && facultyProcess && (
          <ResearchProfessorsDropdowns
            assignedSections={facultyProcess?.assigned_sections_as_prof ?? []}
          />
        )}
      </div>

      <ScrollArea className="flex flex-col flex-1 overflow-y-auto">
        <Link href="/faculty/dashboard">
          <Button
            variant="ghost"
            className={cn(
              'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
              pathname.startsWith('/faculty/dashboard') &&
                'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
            )}
          >
            <BiSolidDashboard className="h-4 w-4" />
            <span className="w-44 truncate text-left">Dashboard</span>
          </Button>
        </Link>

        {researchType === RESEARCH_PROFESSOR && (
          <Accordion type="single" collapsible>
            <AccordionItem value="Faculty Roles">
              <AccordionTrigger
                className={cn('hover:no-underline px-4 text-xs font-medium')}
              >
                Faculty Roles
              </AccordionTrigger>
              <AccordionContent className="p-0">
                <Link href="/faculty/user-and-responsibility">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith('/faculty/user-and-responsibility') &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <FaUsersCog className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      User and responsibility
                    </span>
                  </Button>
                </Link>
                <Link href="/faculty/adviser-and-section-distribution">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith(
                        '/faculty/adviser-and-section-distribution'
                      ) &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <FaChalkboardTeacher className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      Adviser and section distribution
                    </span>
                  </Button>
                </Link>
                <Link href="/faculty/section-and-process-selection">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith(
                        '/faculty/section-and-process-selection'
                      ) &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <FaArrowRotateRight className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      Section and process selection
                    </span>
                  </Button>
                </Link>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        )}

        {Boolean(selectedProcess) && (
          <Accordion type="single" collapsible>
            <AccordionItem value="Students Documents">
              <AccordionTrigger
                className={cn('hover:no-underline px-4 text-xs font-medium')}
              >
                Students Documents
              </AccordionTrigger>
              <AccordionContent className="p-0">
                {selectedProcess?.process[selectedProcessIndex]
                  ?.has_submitted_proposal && (
                  <Link href="/faculty/submitted-proposal">
                    <Button
                      variant="ghost"
                      className={cn(
                        'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                        pathname.startsWith('/faculty/submitted-proposal') &&
                          'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                      )}
                    >
                      <BsGraphUpArrow className="h-4 w-4" />
                      <span className="w-44 truncate text-left">
                        Submitted Proposal
                      </span>
                    </Button>
                  </Link>
                )}

                {selectedProcess?.process[selectedProcessIndex]
                  ?.has_pre_oral_defense_date && (
                  <Link href="/faculty/set-pre-oral-defense">
                    <Button
                      variant="ghost"
                      className={cn(
                        'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                        pathname.startsWith('/faculty/set-pre-oral-defense') &&
                          'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                      )}
                    >
                      <TbCalendarStats className="h-4 w-4" />
                      <span className="w-44 truncate text-left">
                        Set Pre-Oral Defense Date
                      </span>
                    </Button>
                  </Link>
                )}

                {selectedProcess?.process[selectedProcessIndex]
                  ?.has_submitted_ethics_protocol && (
                  <Link href="/faculty/submitted-ethics-protocol">
                    <Button
                      variant="ghost"
                      className={cn(
                        'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                        pathname.startsWith(
                          '/faculty/submitted-ethics-protocol'
                        ) &&
                          'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                      )}
                    >
                      <IoShieldHalf className="h-4 w-4" />
                      <span className="w-44 truncate text-left">
                        Submitted Ethics/Protocol
                      </span>
                    </Button>
                  </Link>
                )}

                {selectedProcess?.process[selectedProcessIndex]
                  ?.has_submitted_full_manuscript && (
                  <Link href="/faculty/submitted-full-manuscript">
                    <Button
                      variant="ghost"
                      className={cn(
                        'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                        pathname.startsWith(
                          '/faculty/submitted-full-manuscript'
                        ) &&
                          'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                      )}
                    >
                      <GiFeather className="h-4 w-4" />
                      <span className="w-44 truncate text-left">
                        Submitted Full Manuscript
                      </span>
                    </Button>
                  </Link>
                )}

                {selectedProcess?.process[selectedProcessIndex]
                  ?.has_set_final_defense_date && (
                  <Link href="/faculty/set-final-defense">
                    <Button
                      variant="ghost"
                      className={cn(
                        'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                        pathname.startsWith('/faculty/set-final-defense') &&
                          'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                      )}
                    >
                      <TbCalendarStats className="h-4 w-4" />
                      <span className="w-44 truncate text-left">
                        Set Final Defense Date
                      </span>
                    </Button>
                  </Link>
                )}

                {selectedProcess?.process[selectedProcessIndex]
                  ?.has_submitted_copyright && (
                  <Link href="/faculty/submitted-copyright-documents">
                    <Button
                      variant="ghost"
                      className={cn(
                        'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                        pathname.startsWith(
                          '/faculty/submitted-copyright-documents'
                        ) &&
                          'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                      )}
                    >
                      <FaCopyright className="h-4 w-4" />
                      <span className="w-44 truncate text-left">
                        Submitted Copyright Documents
                      </span>
                    </Button>
                  </Link>
                )}
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        )}

        <Link href="/faculty/researchers-profile">
          <Button
            variant="ghost"
            className={cn(
              'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
              pathname.startsWith('/faculty/researchers-profile') &&
                'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
            )}
          >
            <HiMiniUserGroup className="h-4 w-4" />
            <span className="w-44 truncate text-left">Researchers Profile</span>
          </Button>
        </Link>

        <Link href="/faculty/repository">
          <Button
            variant="ghost"
            className={cn(
              'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
              pathname.startsWith('/faculty/repository') &&
                'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
            )}
          >
            <SlBookOpen className="h-4 w-4" />
            <span className="w-44 truncate text-left">Repository</span>
          </Button>
        </Link>

        <Link href="/faculty/copyrighted-research-submissions">
          <Button
            variant="ghost"
            className={cn(
              'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
              pathname.startsWith(
                '/faculty/copyrighted-research-submissions'
              ) &&
                'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
            )}
          >
            <FaCopyright className="h-4 w-4" />
            <span className="w-44 truncate text-left">
              Copyrighted research submissions
            </span>
          </Button>
        </Link>
      </ScrollArea>
    </div>
  );
}
