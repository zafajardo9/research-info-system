'use client';

import { cn } from '@/lib/utils';
import Placeholder from '@tiptap/extension-placeholder';
import { EditorContent, useEditor } from '@tiptap/react';
import { useEffect } from 'react';
import { extensions } from '../constants';
import type { TiptapProps } from '../types';
import { Toolbar } from './toolbar';

export const TiptapEditor = ({
  value,
  onChange = () => {},
  className,
  containerClassName,
  children,
  placeholder = 'Write here...',
  disabled
}: TiptapProps) => {
  const editor = useEditor({
    extensions: [
      ...extensions,
      Placeholder.configure({
        placeholder,
      }),
    ],
    editable: true,
    editorProps: {
      attributes: {
        class: cn('tiptap-editor', className),
      },
    },

    onUpdate: ({ editor }) => {
      const html = editor.getHTML();
      onChange(html);
    },
  });

  useEffect(() => {
    if (!editor) return;

    if (!editor.isFocused) {
      editor.commands.setContent(value, false);
    }
  }, [editor, value]);

  if (!editor) {
    return <div className="min-h-[24px] w-full" />;
  }

  return (
    <>
      <div
        className={cn(
          'tiptap-container overflow-hidden shadow-sm',
          'focus-within:outline-none focus-within:text-blue-500 focus-within:ring-1 focus-within:ring-ring',
          containerClassName
        )}
      >
        <Toolbar editor={editor} />
        <EditorContent editor={editor} className="bg-card" disabled />
      </div>
      {children}
    </>
  );
};
