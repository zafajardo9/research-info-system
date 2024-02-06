'use client';

import _ from 'lodash';
import { useId, useState } from 'react';
import { Control } from 'react-hook-form';
import { FaRegTrashAlt } from 'react-icons/fa';
import { FaRegFileImage, FaRegFilePdf } from 'react-icons/fa6';
import { ViewFileDialog } from '../global/view-file-dialog';
import { Button } from './button';
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from './form';

export interface FileUploadInputProps {
  control: Control<any>;
  name: string;
  label?: string;
  placeholder?: string;
  description?: string;
  accept?: string;
  defaultFile?: string;
  defaultFileName?: string;
  hideDeleteButton?: boolean;
  isImage?: boolean;
}

export function FileUploadInput({
  control,
  name,
  label = 'File input',
  placeholder = 'Upload File',
  accept = '.pdf, .doc, .docx',
  description,
  defaultFile,
  defaultFileName,
  hideDeleteButton = false,
  isImage = false,
}: FileUploadInputProps) {
  const fileUploadId = useId();
  const [file, setFile] = useState<string>(defaultFile ?? '');

  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem className="col-span-2">
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <div className="flex items-center gap-3">
              {field?.value ?? file ? (
                <>
                  <ViewFileDialog
                    uri={field.value ? URL.createObjectURL(field.value) : file}
                    fileName={field.value ? field.value.name : defaultFileName}
                    label={_.truncate(
                      field.value ? field.value.name : defaultFileName,
                      {
                        length: 30,
                      }
                    )}
                    className="flex flex-1"
                  />
                  {!hideDeleteButton && (
                    <Button
                      variant="destructive"
                      type="button"
                      onClick={() => {
                        field.onChange(null);
                        setFile('');
                      }}
                    >
                      <FaRegTrashAlt />
                    </Button>
                  )}
                </>
              ) : (
                <label
                  htmlFor={fileUploadId}
                  className="flex flex-1 border rounded cursor-pointer gap-2 items-center text-base justify-center bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80 h-9 px-4 py-2"
                >
                  {isImage ? <FaRegFileImage /> : <FaRegFilePdf />}
                  <span>{placeholder}</span>

                  <input
                    type="file"
                    id={fileUploadId}
                    className="hidden"
                    onChange={(e) =>
                      field.onChange(e.target.files ? e.target.files[0] : null)
                    }
                    accept={isImage ? 'image/*' : accept}
                  />
                </label>
              )}
            </div>
          </FormControl>
          {description && <FormDescription>{description}</FormDescription>}
          <FormMessage />
        </FormItem>
      )}
    />
  );
}
