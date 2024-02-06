'use client';

import profilePicture from '@/assets/images/profile-v2.png';
import { Button } from '@/components/ui/button';
import { useGetStudents } from '@/hooks/use-student-query';
import { useSession } from 'next-auth/react';
import Image from 'next/image';
import Link from 'next/link';
import { useMemo } from 'react';
import { v4 as uuidv4 } from 'uuid';

export interface CollaborationSectionProps {
  showMyProfileLink?: boolean;
  profilePath?: string;
}

export function CollaborationSection({
  showMyProfileLink = false,
  profilePath = '/student/researchers-profile',
}: CollaborationSectionProps) {
  const { data: studentData } = useGetStudents();
  const { data: session } = useSession();

  const studentList = useMemo(() => {
    if (!studentData?.result) return [];

    return studentData.result
      .reduce<ProfileCardsContainer[]>((collection, profile) => {
        const courseIndex = collection.findIndex(
          (value) => value.course === profile.course
        );

        if (courseIndex > -1) {
          const prevData = collection[courseIndex];

          prevData.students.push(profile);
        } else {
          collection.push({
            id: uuidv4(),
            course: profile.course,
            students: [profile],
          });
        }

        return collection;
      }, [])
      .sort((a, b) => b.students.length - a.students.length);
  }, [studentData]);

  return (
    <>
      <div className="prose dark:prose-h1:text-white prose-h1:m-0 max-w-none flex justify-between items-center">
        <h1>Researchers Profile</h1>

        {showMyProfileLink && (
          <Link
            href={`${profilePath}/${session?.user?.studentProfile?.id}`}
            className="text-lg font-bold text-muted-foreground underline"
          >
            View My Profile
          </Link>
        )}
      </div>

      <section>
        <p className="text-muted-foreground">
          Find researchers and keep up with their work.
        </p>

        <div className="grid grid-cols-2 gap-10 mt-10">
          {studentList.length > 0 &&
            studentList.map(({ id, course, students }) => (
              <div key={id} className="grid gap-4 h-auto">
                <div className="space-y-4">
                  <h3 className="font-bold text-xl text-[#44465B]">
                    People you may know from {course}
                  </h3>
                  {students.map(({ user_id, name, year_section, course }) => (
                    <div
                      key={id}
                      className="bg-[#F1F5F9] flex items-end gap-4 border-2 p-4"
                    >
                      <Image
                        src={profilePicture}
                        alt={name}
                        height={105}
                        width={105}
                      />

                      <div>
                        <h4 className="text-xl font-bold text-[#44465B]">
                          {name}
                        </h4>
                        <p className="text-xl font-normal text-[#44465B]">
                          {course} {year_section}
                        </p>

                        <Link href={`${profilePath}/${user_id}`}>
                          <Button className="gap-2 h-6 rounded-2xl mt-3">
                            <span>Information</span>
                          </Button>
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
        </div>
      </section>
    </>
  );
}
