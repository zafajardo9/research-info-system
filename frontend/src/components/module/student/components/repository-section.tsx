'use client';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Skeleton } from '@/components/ui/skeleton';
import { Toggle } from '@/components/ui/toggle';
import { ToggleGroup, ToggleGroupItem } from '@/components/ui/toggle-group';
import { useGetAllResearchPapersWithAuthors } from '@/hooks/use-research-query';
import { useGetCourseList } from '@/hooks/use-user-query';
import DocViewer, { DocViewerRenderers } from '@cyntler/react-doc-viewer';
import parse from 'html-react-parser';
import moment from 'moment';
import { useId, useMemo, useRef, useState } from 'react';
import { BsFillPersonFill } from 'react-icons/bs';
import { HiOutlineBookOpen } from 'react-icons/hi2';
import {
  FacultyResearchPaperData,
  useGetFacultyResearchPapers,
} from '../../admin/hooks/use-faculty-research-papers';

const PROPOSAL_TYPES = [
  'Research',
  'Capstone',
  'Feasibility Study',
  'Business Plan',
];

const SORT_BY = [
  {
    label: 'By Title',
    value: 'title',
  },
  {
    label: 'By Issue Date',
    value: 'submitted_date',
  },
];

const CHARACTERS = Array.from({ length: 26 }, function (_, idx) {
  return String.fromCharCode('A'.charCodeAt(0) + idx);
});

export function RepositorySection() {
  const [activeCourses, setActiveCourses] = useState<string[]>([]);
  const [activeProposalTypes, setActiveProposalTypes] = useState<string[]>([]);
  const [activeChars, setActiveChars] = useState<string[]>([]);
  const [sortBy, setSortBy] = useState<string>('');
  const [search, setSearch] = useState<string>('');
  const [selectedResearch, setSelectedResearch] = useState<ResearchPaperV2>();
  const inputRef = useRef<HTMLInputElement>(null);

  const { data: courseList, isLoading: courseListLoading } = useGetCourseList();
  const { data: researches, isLoading } = useGetAllResearchPapersWithAuthors();

  const { data: facultyResearches = [] } = useGetFacultyResearchPapers();

  const facultyResearchApprovedList = facultyResearches.filter(
    ({ FacultyResearchPaper: { status } }) => status === 'Approved'
  );

  const coursesId = useId();
  const proposalTypesId = useId();
  const characterId = useId();
  const researchId = useId();
  const courseId = useId();

  const filteredResearches = useMemo<FacultyResearchPaperData[]>(() => {
    let filter: FacultyResearchPaperData[] = Array.from(
      facultyResearchApprovedList
    );

    // if (activeCourses.length > 0) {
    //   filter = filter.filter(({ authors }) =>
    //     authors.some(({ course }) => activeCourses.includes(course))
    //   );
    // }

    // if (activeProposalTypes.length > 0) {
    //   filter = filter.filter(({ FacultyResearchPaper: {} }) =>
    //     activeProposalTypes.some((v) =>
    //       research_paper.research_type.toLowerCase().startsWith(v.toLowerCase())
    //     )
    //   );
    // }

    if (activeChars.length > 0) {
      filter = filter.filter(({ FacultyResearchPaper: { title } }) =>
        activeChars.some((v) => title.toLowerCase().startsWith(v.toLowerCase()))
      );
    }

    if (search) {
      const regex = new RegExp(search.toLowerCase());

      filter = filter.filter(({ FacultyResearchPaper: { title } }) =>
        title.toLowerCase().match(regex)
      );
    }

    if (Boolean(sortBy) && sortBy === 'title') {
      filter = filter.sort((a, b) =>
        a.FacultyResearchPaper.title.localeCompare(b.FacultyResearchPaper.title)
      );
    }

    if (Boolean(sortBy) && sortBy === 'submitted_date') {
      filter = filter.sort((a, b) => {
        const bDate = Date.parse(b.FacultyResearchPaper.created_at);
        const aDate = Date.parse(a.FacultyResearchPaper.created_at);

        return bDate - aDate;
      });
    }

    return filter;
  }, [facultyResearchApprovedList, activeChars, search, sortBy]);

  function toggleHandler(prev: string[], value: string) {
    const cloned = [...prev];

    const index = cloned.indexOf(value);

    if (index > -1) {
      cloned.splice(index, 1);
    } else {
      cloned.push(value);
    }

    return cloned;
  }

  function searchHandler() {
    const input = inputRef.current;

    if (input) {
      setSearch(input.value);
    }
  }

  return (
    <section className="space-y-10 px-1">
      <div className="space-y-5">
        {/* {courseList && (
          <div className="flex items-center gap-3 flex-wrap">
            {courseList.courses.map((course, idx) => (
              <Toggle
                key={coursesId + idx}
                size="sm"
                variant="outline"
                className="capitalize data-[state=on]:bg-primary data-[state=on]:text-white rounded-2xl"
                onClick={() => {
                  setActiveCourses((prev) => toggleHandler(prev, course));
                }}
              >
                {course}
              </Toggle>
            ))}
          </div>
        )} */}

        {/* <div className="flex items-center gap-3 flex-wrap">
          {PROPOSAL_TYPES.map((type) => (
            <Toggle
              key={proposalTypesId + type}
              size="sm"
              variant="outline"
              className="uppercase data-[state=on]:bg-primary data-[state=on]:text-white rounded-2xl"
              onClick={() => {
                setActiveProposalTypes((prev) => toggleHandler(prev, type));
              }}
            >
              {type}
            </Toggle>
          ))}
        </div> */}

        <div className="flex items-center flex-wrap">
          <ToggleGroup type="single" className="gap-0">
            {SORT_BY.map(({ label, value }) => (
              <ToggleGroupItem
                key={proposalTypesId + value}
                size="sm"
                variant="outline"
                value={value}
                className="capitalize data-[state=on]:bg-primary data-[state=on]:text-white rounded-none"
                onClick={() => {
                  setSortBy((prev) => (prev === value ? '' : value));
                }}
                unselectable="on"
              >
                {label}
              </ToggleGroupItem>
            ))}
          </ToggleGroup>
        </div>

        <div className="flex flex-wrap items-center gap-1">
          {CHARACTERS.map((char) => (
            <Toggle
              key={characterId + char}
              size="sm"
              variant="outline"
              className="capitalize font-bold data-[state=on]:bg-white data-[state=on]:text-primary"
              onClick={() => {
                setActiveChars((prev) => toggleHandler(prev, char));
              }}
            >
              {char}
            </Toggle>
          ))}
        </div>

        <div className="relative h-fit max-w-lg">
          <Input
            ref={inputRef}
            placeholder="Search research title..."
            className="pr-28"
            onChange={(e) => {
              if (!Boolean(e.target.value)) {
                setSearch('');
              }
            }}
            onKeyDown={(e) => {
              if (e.code === 'Enter') {
                setSearch(e.currentTarget.value);
              }
            }}
          />
          <Button
            type="button"
            className="gap-2 rounded-l-none absolute bottom-0 right-0"
            onClick={searchHandler}
          >
            <HiOutlineBookOpen />
            <span>Browse</span>
          </Button>
        </div>
      </div>

      <div className="space-y-6 p-6 border rounded">
        {isLoading &&
          Array.from({ length: 10 }).map((_, idx) => (
            <Skeleton key={researchId + idx} className="rounded h-32 w-full" />
          ))}

        {filteredResearches &&
          !isLoading &&
          filteredResearches.map(
            (
              {
                FacultyResearchPaper: {
                  created_at,
                  id,
                  content,
                  file_path,
                  category,
                  user_id,
                  title,
                  modified_at,
                  abstract,
                  date_publish,
                  publisher,
                  status,
                },
                name,
              },
              idx
            ) => {
              // const courses = authors
              //   ? authors.map(
              //       ({ course, year_section }) => `${course} ${year_section}`
              //     )
              //   : [];

              // const filteredCourses = Array.from(new Set(courses));
              const docs = [
                {
                  uri: file_path ?? '',
                },
              ];

              return (
                <Dialog key={researchId + idx}>
                  <DialogTrigger asChild>
                    <div
                      role="button"
                      className="border bg-card rounded p-3 transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-1"
                      // onClick={() => {
                      //   setSelectedResearch(research_paper);
                      // }}
                    >
                      <h2 className="font-bold">{title}</h2>
                      <div className="flex items-center gap-2 text-sm my-4">
                        {/* {filteredCourses.map((course, idx) => (
                        <Badge key={courseId + idx} variant="outline">
                          {course}
                        </Badge>
                      ))} */}

                        <div>{moment(created_at).format('LL')}</div>
                      </div>

                      <div className="flex items-center gap-4">
                        <div className="flex flex-1 flex-wrap gap-3">
                          {/* {authors &&
                          authors.map(({ id, name }) => ( */}
                          <div
                            // key={id}
                            className="flex items-center gap-2 capitalize text-sm"
                          >
                            <BsFillPersonFill />
                            <span>{name}</span>
                          </div>
                          {/* ))} */}
                        </div>
                      </div>
                    </div>
                  </DialogTrigger>
                  <DialogContent className="max-w-4xl">
                    <div>
                      <DialogHeader>
                        <DialogTitle>{title}</DialogTitle>
                      </DialogHeader>
                      <ScrollArea className="h-96 py-10">
                        <div className="space-y-6 ">
                          <div className="space-y-1 text-sm">
                            <div className="font-semibold">Category</div>
                            <div>{category}</div>
                          </div>

                          <div className="space-y-1 text-sm">
                            <div className="font-semibold">Publisher</div>
                            <div>{publisher}</div>
                          </div>

                          {content && (
                            <div className="space-y-1 text-sm">
                              <div className="font-semibold">Content</div>
                              <div className="prose prose-sm max-w-none">
                                {parse(content)}
                              </div>
                            </div>
                          )}

                          {abstract && (
                            <div className="space-y-1 text-sm">
                              <div className="font-semibold">Abstract</div>
                              <div className="prose prose-sm max-w-none">
                                {parse(abstract)}
                              </div>
                            </div>
                          )}

                          {file_path && (
                            <div className="mt-10">
                              <DocViewer
                                documents={docs}
                                pluginRenderers={DocViewerRenderers}
                                theme={{
                                  primary: '#f4f4f4',
                                  textPrimary: '#000000',
                                }}
                              />
                            </div>
                          )}

                          <div className="space-y-1 text-sm">
                            <div className="font-semibold">Date Publish</div>
                            <div>{date_publish}</div>
                          </div>
                        </div>
                      </ScrollArea>
                    </div>
                  </DialogContent>
                </Dialog>
              );
            }
          )}

        {filteredResearches.length < 1 && (
          <div className="text-muted-foreground text-center">No results.</div>
        )}
      </div>
    </section>
  );
}
