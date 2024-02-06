'use client';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { cn } from '@/lib/utils';
import DocViewer, { DocViewerRenderers } from '@cyntler/react-doc-viewer';
import { FaRegFilePdf } from 'react-icons/fa6';

export interface ViewFileDialogProps {
  label?: string;
  uri: string;
  fileName?: string;
  className?: string;
  disable?: boolean;
}

export function ViewFileDialog({
  label,
  uri,
  fileName = 'preview',
  className,
  disable = false,
}: ViewFileDialogProps) {
  const docs = [{ uri, fileName }];

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button className={cn('gap-3', className)} disabled={disable || !Boolean(uri)}>
          <FaRegFilePdf /> {label && <span>{label}</span>}
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-4xl">
        <DialogHeader>
          <DialogTitle>Preview</DialogTitle>
        </DialogHeader>
        <div className="py-4 h-[500px]">
          <DocViewer
            documents={docs}
            pluginRenderers={DocViewerRenderers}
            theme={{
              primary: '#f4f4f4',
              textPrimary: '#000000',
            }}
            style={{
              height: '100%',
            }}
          />
        </div>
      </DialogContent>
    </Dialog>
  );
}
