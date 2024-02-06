'use client';

import logo13 from '@/assets/images/logo13.png';
import { cn } from '@/lib/utils';
import { SidebarData } from '@/types/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useId } from 'react';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '../../../ui/accordion';
import { Button } from '../../../ui/button';
import { ScrollArea } from '../../../ui/scroll-area';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../../ui/select';
import { useStudentWorkflowContext } from './context/student-workflow';

export interface StudentSidebarProps {
  className?: string;
  sidebars?: SidebarData[];
}

export function StudentSidebar({
  className,
  sidebars = [],
}: StudentSidebarProps) {
  const parentId = useId();
  const childrenId = useId();
  const labelId = useId();
  const pathname = usePathname();
  const router = useRouter();

  const { researchType, setResearchType, workflowId, setWorkflowId } =
    useStudentWorkflowContext();

  const options = sidebars.map(({ label }) => label);

  const currentSidebar = sidebars.find(({ label }) => label === researchType);

  useEffect(() => {
    router.push('/student/progress');

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [researchType, workflowId]);

  return (
    <div
      className={cn(
        'hidden xl:fixed xl:flex xl:flex-col xl:inset-y-0 xl:z-50 xl:w-64 transition-all ease-out duration-500 bg-card border-r',
        className
      )}
    >
      <div className="flex justify-center items-center gap-5 h-28 opacity-100">
        <Image src={logo13} alt="PUPQC RIS logo" height={120} width={120} />
      </div>

      <div className="px-4 pt-5 pb-10">
        {currentSidebar && (
          <Select
            defaultValue={currentSidebar.label}
            onValueChange={(value) => {
              const data = sidebars.find(({ label }) => label === value);

              if (data) {
                setResearchType(data.label);
                setWorkflowId(data.key);
              }
            }}
          >
            <SelectTrigger className="bg-primary text-white [&>svg]:hidden text-center rounded-xl justify-center font-semibold">
              <SelectValue placeholder="Select a type" />
            </SelectTrigger>
            <SelectContent className="z-50">
              <SelectGroup>
                {options.map((option, idx) => (
                  <SelectItem key={labelId + idx} value={option}>
                    {option}
                  </SelectItem>
                ))}
              </SelectGroup>
            </SelectContent>
          </Select>
        )}
      </div>

      <ScrollArea className="flex flex-col flex-1 overflow-y-auto">
        {currentSidebar?.navigations.map((n, parentIdx) => {
          if ('nodeList' in n) {
            const { label, nodeList } = n;

            const hasActiveNav = nodeList.some(({ href }) =>
              pathname.startsWith(href)
            );

            return (
              <Accordion
                key={parentId + parentIdx}
                type="single"
                defaultValue={hasActiveNav ? label : undefined}
                collapsible
              >
                <AccordionItem value={label}>
                  <AccordionTrigger
                    className={cn(
                      'hover:no-underline px-4 text-xs font-medium',
                      hasActiveNav && 'text-primary text-center'
                    )}
                  >
                    {label}
                  </AccordionTrigger>
                  <AccordionContent className="p-0">
                    {nodeList.map(
                      (
                        { href, label, Icon, className, isHidden },
                        childrenIdx
                      ) => (
                        <Link key={childrenId + childrenIdx} href={href}>
                          <Button
                            variant="ghost"
                            className={cn(
                              'border-bd relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                              pathname.startsWith(href) &&
                                'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0',
                              isHidden && 'hidden',
                              className
                            )}
                          >
                            <Icon className="h-4 w-4" />
                            <span className="w-44 truncate text-left">
                              {label}
                            </span>
                          </Button>
                        </Link>
                      )
                    )}
                  </AccordionContent>
                </AccordionItem>
              </Accordion>
            );
          } else {
            const { href, Icon, label, isHidden } = n;
            return (
              <Link key={childrenId + parentIdx} href={href}>
                <Button
                  variant="ghost"
                  className={cn(
                    'relative justify-start w-full gap-6 text-[11px] py-6 hover:bg-blue-50 transition-colors hover:text-primary',
                    pathname.startsWith(href) &&
                      'bg-blue-50 text-primary after:absolute after:h-full after:w-1 after:bg-primary after:right-0',
                    isHidden && 'hidden',
                    className
                  )}
                >
                  <Icon className="h-4 w-4" />
                  <span className="w-44 truncate text-left">{label}</span>
                </Button>
              </Link>
            );
          }
        })}
      </ScrollArea>
    </div>
  );
}
