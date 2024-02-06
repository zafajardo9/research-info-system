'use client';

import profileImage from '@/assets/images/profile.png';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';
import { useSidebarStore } from '@/store/sidebar-store';
import { ChevronDownIcon } from '@radix-ui/react-icons';
import { signOut, useSession } from 'next-auth/react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Badge } from '../ui/badge';

export interface ProfileGearProps {
  role: string;
}

export function ProfileGear({ role }: ProfileGearProps) {
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const router = useRouter();

  const { data: session } = useSession();

  const { selectSidebar } = useSidebarStore();

  const profile =
    session?.user?.studentProfile ?? session?.user?.facultyProfile;

  const profileHasStudentNumber =
    typeof profile !== 'undefined' && 'student_number' in profile;

  async function logOutHandler() {
    await signOut({ redirect: false });

    router.push('/');

    selectSidebar(null);
  }

  return (
    <>
      {profile && (
        <DropdownMenu
          defaultOpen={isOpen}
          onOpenChange={() => setIsOpen((prev) => !prev)}
        >
          <DropdownMenuTrigger className="flex items-center gap-2 hover:bg-muted py-4 px-5 focus:outline-none">
            <div>
              <Image
                src={profileImage}
                alt="User profile placeholder"
                height={40}
                width={40}
              />
            </div>

            <div className="leading-none space-y-1 text-left">
              <div className="text-xs font-semibold max-w-[150px] truncate">
                {profile?.name}
              </div>

              {profileHasStudentNumber ? (
                <Badge className="text-[10px] font-semibold">
                  {profile.status ?? 'Student'}
                </Badge>
              ) : (
                <Badge className="text-[10px] font-semibold">{role}</Badge>
              )}
            </div>

            <ChevronDownIcon
              className={cn(
                'h-5 w-5 transition-transform',
                isOpen && '-rotate-180'
              )}
            />
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56" align="end">
            {/* <DropdownMenuGroup>
              <DropdownMenuItem>Profile</DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator /> */}
            <DropdownMenuItem
              onClick={logOutHandler}
              className="justify-center"
            >
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )}
    </>
  );
}
