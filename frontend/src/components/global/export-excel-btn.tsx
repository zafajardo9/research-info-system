'use client';

import { risApi } from '@/lib/api';
import FileSaver from 'file-saver';
import { useSession } from 'next-auth/react';
import { useState } from 'react';
import { AiOutlineLoading3Quarters } from 'react-icons/ai';
import { TiExportOutline } from 'react-icons/ti';
import { Button } from '../ui/button';

export interface ExportExcelBtnProps {
  type: string;
  section?: string;
}

const ExportExcelBtn = ({ type, section }: ExportExcelBtnProps) => {
  const { data: session } = useSession();
  const [isFetching, setIsFetching] = useState<boolean>(false);

  async function exportHandler() {
    try {
      setIsFetching(true);

      const response = await risApi.get('/info/print/print-all-research', {
        headers: {
          Authorization: `Bearer ${session?.user?.authToken}`,
        },
        params: { type, section },
      });

      const file_link = response.data?.file_link;

      if (file_link) {
        let name = type;

        if (section) name += `-${section}`;

        name += `-${Date.now()}.xlsx`;

        FileSaver.saveAs(file_link, name);
      }
    } catch (error) {
      console.log(error);
    } finally {
      setIsFetching(false);
    }
  }

  return (
    <Button
      type="button"
      variant="secondary"
      className="flex items-center gap-2 uppercase"
      onClick={exportHandler}
      disabled={isFetching}
    >
      {isFetching ? (
        <AiOutlineLoading3Quarters className="h-4 w-4 animate-spin" />
      ) : (
        <>
          <TiExportOutline className="h-5 w-5" />
          <span>Export</span>
        </>
      )}
    </Button>
  );
};

export default ExportExcelBtn;
