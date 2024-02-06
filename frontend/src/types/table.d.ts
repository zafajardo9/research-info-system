import { RowData } from '@tanstack/react-table';

declare module '@tanstack/react-table' {
  interface TableMeta<TData extends RowData> {
    researchType?: string;

    selected_research_types?: string[];
    changeResearchType?: (value: string) => void;

    isUpdating?: boolean;
    setIsUpdating?: (value: boolean) => void;
  }
}
