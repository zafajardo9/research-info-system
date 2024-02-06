'use client';

import _ from 'lodash';
import { useMemo } from 'react';
import { Chart } from 'react-google-charts';
import { useGetAdminCourseAnalytics } from '../../hooks/use-admin-analytics-query';

export const data = [
  ['Programs', 'Total'],
  ['BSIT', 10],
  ['BBTLEDHE', 6],
  ['BTLEDICT', 2],
  ['BSBAHRM', 1],
  ['Faculty Copyrighted Papers Total', 7],
];

export const options = {
  title: 'Researches per Programs',
  chartArea: { width: '50%' },
  hAxis: {
    title: 'Researches count',
    minValue: 0,
  },
  vAxis: {
    title: 'Programs',
  },
};

export function AdminProgramsBarGraph() {
  const { data: courseData } = useGetAdminCourseAnalytics();

  const courseDataAnalytics = useMemo(() => {
    const graphHead = [
      'Program',
      'Research',
      'Feasibility Study',
      'Capstone',
      'Business Plan',
      'Copyrighted Papers',
    ];

    let programsData: (string | number)[][] = [];

    const facultyCopyrightedTotal =
      courseData?.['Faculty Copyrighted Papers Total'];

    // prettier-ignore
    let facultyData =
      typeof facultyCopyrightedTotal !== 'undefined'
        ? ['Faculty', 0, 0, 0, 0, facultyCopyrightedTotal]
        : [];

    if (typeof courseData !== 'undefined') {
      const filteredData = _.omit(courseData, [
        'Total number across all courses',
        'Faculty Copyrighted Papers Total',
      ]);

      Object.entries(filteredData).forEach(([key, values]) => {
        const temp: Array<string | number> = [key, 0, 0, 0, 0, 0];

        values.forEach(({ research_type, count }) => {
          const researchTypeIndex = graphHead.findIndex(
            (e) => e === research_type
          );

          temp[researchTypeIndex] = count ?? 0;
        });

        programsData.push(temp);
      });
    }

    return [graphHead, ...programsData, facultyData];
  }, [courseData]);

  return (
    <div>
      <Chart
        chartType="BarChart"
        width="100%"
        height="800px"
        data={courseDataAnalytics}
        options={options}
      />
    </div>
  );
}
