import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { columns } from '../adviser-and-section-distribution-section-table/columns';
import { DataTable } from '../adviser-and-section-distribution-section-table/data-table';

export interface SectionDistributionCardProps {
  data: AdviserDataGroup;
}

export default function SectionDistributionCard({
  data,
}: SectionDistributionCardProps) {
  const { research_type_name, list } = data;

  return (
    <Card>
      <CardHeader>
        <CardTitle>Adviser and Section Distribution</CardTitle>
        <CardDescription>You can select multiple section</CardDescription>
      </CardHeader>
      <CardContent className="py-5 space-y-10">
        <div className="text-primary text-lg font-semibold">
          {research_type_name}
        </div>

        <DataTable
          columns={columns}
          data={list}
          researchType={research_type_name}
        />
      </CardContent>
    </Card>
  );
}
