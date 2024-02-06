'use client';

import { useMemo } from 'react';
import { Chart } from 'react-google-charts';
import { useGetAdminAllCollabMetrics } from '../../hooks/use-admin-analytics-query';

export const options = {
  title: '',
};

export function AdminProgramsPieGraph() {
  const { data: collabMetrics, isLoading } = useGetAdminAllCollabMetrics();

  const averageCollabCount =
    collabMetrics?.all_metrics?.['Average Collaboration Count'] ?? 0;
  const averagePercentOfAuthors =
    collabMetrics?.all_metrics?.['Average Percentage of Authors'] ?? 0;

  const collabMetricsPieGraph = useMemo(() => {
    let pieGraphHead = ['Research Type', 'Collaboration'];
    let research = ['Research', 0];
    let feasibilityStudy = ['Feasibility Study', 0];
    let capstone = ['Capstone', 0];
    let businessPlan = ['Business Plan', 0];

    if (typeof collabMetrics !== 'undefined') {
      const values = collabMetrics?.all_metrics?.['Pie Chart Values'] ?? [];

      for (const { research_type, count } of values) {
        if (research_type === 'Research') {
          research = ['Research', count];
        }

        if (research_type === 'Feasibility Study') {
          feasibilityStudy = ['Feasibility Study', count];
        }

        if (research_type === 'Capstone') {
          capstone = ['Capstone', count];
        }

        if (research_type === 'Business Plan') {
          businessPlan = ['Business Plan', count];
        }
      }
    }

    return [pieGraphHead, research, feasibilityStudy, capstone, businessPlan];
  }, [collabMetrics]);

  return (
    <div>
      {!isLoading && collabMetrics ? (
        <div className="space-y-3">
          <div>
            <div className="text-sm">
              Avg. authors per research: {averageCollabCount}
            </div>
            <div className="text-sm">
              Collaboration metrics in Whole: {averagePercentOfAuthors}
            </div>
          </div>
          <Chart
            chartType="PieChart"
            data={collabMetricsPieGraph}
            options={options}
            width={'100%'}
            height={'400px'}
          />
        </div>
      ) : null}
    </div>
  );
}
