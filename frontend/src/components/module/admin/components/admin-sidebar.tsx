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
import { useEffect, useId } from 'react';
import { BiSolidDashboard } from 'react-icons/bi';
import { BsGraphUpArrow } from 'react-icons/bs';
import {
  FaChalkboardTeacher,
  FaCopyright,
  FaFolder,
  FaUsersCog,
} from 'react-icons/fa';
import { GiFeather } from 'react-icons/gi';
import { HiMiniUserGroup } from 'react-icons/hi2';
import { IoMdMegaphone } from 'react-icons/io';
import { IoShieldHalf } from 'react-icons/io5';
import { SlBookOpen } from 'react-icons/sl';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../../ui/select';
import { useAdminWorkflowContext } from './context/process';

const ADMIN = 'Admin';

const SIDEBAR_OPTIONS: ComboboxOptions[] = [
  {
    label: 'Admin',
    value: 'Admin',
  },
  {
    label: 'Research',
    value: 'Research',
  },
  {
    label: 'Feasibility Study',
    value: 'Feasibility Study',
  },
  {
    label: 'Capstone',
    value: 'Capstone',
  },
  {
    label: 'Business Plan',
    value: 'Business Plan',
  },
];

export function AdminSidebar() {
  const labelId = useId();
  const pathname = usePathname();
  const router = useRouter();

  const { researchType = 'Admin', setResearchType } = useAdminWorkflowContext();

  useEffect(() => {
    router.push('/admin/dashboard');

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [researchType]);

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
          defaultValue="Admin"
          onValueChange={(e) => {
            setResearchType(e);
          }}
        >
          <SelectTrigger className="bg-primary text-white [&>svg]:hidden text-center rounded-xl justify-center font-semibold">
            <SelectValue placeholder="Select Role" />
          </SelectTrigger>

          <SelectContent>
            {SIDEBAR_OPTIONS.map(({ label, value }, idx) => (
              <SelectItem
                key={labelId + idx}
                value={value}
                className="capitalize"
              >
                {label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <ScrollArea className="flex flex-col flex-1 overflow-y-auto">
        <Link href="/admin/dashboard">
          <Button
            variant="ghost"
            className={cn(
              'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
              pathname.startsWith('/admin/dashboard') &&
                'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
            )}
          >
            <BiSolidDashboard className="h-4 w-4" />
            <span className="w-44 truncate text-left">Dashboard</span>
          </Button>
        </Link>

        {researchType == ADMIN && (
          <Accordion type="single" collapsible>
            <AccordionItem value="Admin Roles">
              <AccordionTrigger
                className={cn('hover:no-underline px-4 text-xs font-medium')}
              >
                User Responsibility
              </AccordionTrigger>
              <AccordionContent className="p-0">
                <Link href="/admin/user-and-responsibility">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith('/admin/user-and-responsibility') &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <FaUsersCog className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      User and responsibility
                    </span>
                  </Button>
                </Link>
                <Link href="/admin/professor-and-section-distribution">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith(
                        '/admin/professor-and-section-distribution'
                      ) &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <FaChalkboardTeacher className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      Professor and section distribution
                    </span>
                  </Button>
                </Link>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        )}

        {researchType !== ADMIN && (
          <Accordion type="single" collapsible>
            <AccordionItem value="Students Documents">
              <AccordionTrigger
                className={cn('hover:no-underline px-4 text-xs font-medium')}
              >
                Students Documents
              </AccordionTrigger>
              <AccordionContent className="p-0">
                <Link href="/admin/submitted-proposal">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith('/admin/submitted-proposal') &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <BsGraphUpArrow className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      Submitted Proposal
                    </span>
                  </Button>
                </Link>

                <Link href="/admin/submitted-ethics-protocol">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith('/admin/submitted-ethics-protocol') &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <IoShieldHalf className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      Submitted Ethics/Protocol
                    </span>
                  </Button>
                </Link>

                <Link href="/admin/submitted-full-manuscript">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith('/admin/submitted-full-manuscript') &&
                        'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
                    )}
                  >
                    <GiFeather className="h-4 w-4" />
                    <span className="w-44 truncate text-left">
                      Submitted Full Manuscript
                    </span>
                  </Button>
                </Link>

                <Link href="/admin/submitted-copyright-documents">
                  <Button
                    variant="ghost"
                    className={cn(
                      'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                      pathname.startsWith(
                        '/admin/submitted-copyright-documents'
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
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        )}

        {researchType === ADMIN && (
          <Link href="/admin/researchers-profile">
            <Button
              variant="ghost"
              className={cn(
                'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                pathname.startsWith('/admin/researchers-profile') &&
                  'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
              )}
            >
              <HiMiniUserGroup className="h-4 w-4" />
              <span className="w-44 truncate text-left">
                Researchers Profile
              </span>
            </Button>
          </Link>
        )}
        {researchType === ADMIN && (
          <Link href="/admin/submitted-faculty-research">
            <Button
              variant="ghost"
              className={cn(
                'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                pathname.startsWith('/admin/submitted-faculty-research') &&
                  'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
              )}
            >
              <FaFolder className="h-4 w-4" />
              <span className="w-44 truncate text-left">
                Submitted faculty research
              </span>
            </Button>
          </Link>
        )}
        {researchType === ADMIN && (
          <Link href="/admin/announcement">
            <Button
              variant="ghost"
              className={cn(
                'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                pathname.startsWith('/admin/announcement') &&
                  'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
              )}
            >
              <IoMdMegaphone className="h-4 w-4" />
              <span className="w-44 truncate text-left">Announcement</span>
            </Button>
          </Link>
        )}
        {researchType === ADMIN && (
          <Link href="/admin/repository">
            <Button
              variant="ghost"
              className={cn(
                'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                pathname.startsWith('/admin/repository') &&
                  'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0'
              )}
            >
              <SlBookOpen className="h-4 w-4" />
              <span className="w-44 truncate text-left">Repository</span>
            </Button>
          </Link>
        )}
      </ScrollArea>
    </div>
  );
}
