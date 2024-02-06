import { Toggle } from '@/components/ui/toggle';
import {
  FontBoldIcon,
  FontItalicIcon,
  ListBulletIcon,
  StrikethroughIcon,
  UnderlineIcon,
} from '@radix-ui/react-icons';
import type { Editor } from '@tiptap/react';

type ToolbarProps = {
  editor: Editor;
};

export const Toolbar = ({ editor }: ToolbarProps) => {
  return (
    <div className="flex items-center gap-x-1 rounded-lg rounded-b-none px-3 py-2">
      <Toggle
        onClick={() => editor.chain().focus().toggleBold().run()}
        disabled={!editor.can().chain().focus().toggleBold().run()}
        aria-label="Toggle bold"
        className="text-current data-[state=on]:bg-blue-50 data-[state=on]:text-blue-500 hover:bg-blue-50 hover:text-blue-400"
      >
        <FontBoldIcon className="h-4 w-4" />
      </Toggle>

      <Toggle
        onClick={() => editor.chain().focus().toggleItalic().run()}
        disabled={!editor.can().chain().focus().toggleItalic().run()}
        aria-label="Toggle italic"
        className="text-current data-[state=on]:bg-blue-50 data-[state=on]:text-blue-500 hover:bg-blue-50 hover:text-blue-400"
      >
        <FontItalicIcon className="h-4 w-4" />
      </Toggle>

      <Toggle
        onClick={() => editor.chain().focus().toggleUnderline().run()}
        disabled={!editor.can().chain().focus().toggleUnderline().run()}
        aria-label="Toggle underline"
        className="text-current data-[state=on]:bg-blue-50 data-[state=on]:text-blue-500 hover:bg-blue-50 hover:text-blue-400"
      >
        <UnderlineIcon className="h-4 w-4" />
      </Toggle>

      <Toggle
        onClick={() => editor.chain().focus().toggleStrike().run()}
        disabled={!editor.can().chain().focus().toggleStrike().run()}
        aria-label="Toggle strikethrough"
        className="text-current data-[state=on]:bg-blue-50 data-[state=on]:text-blue-500 hover:bg-blue-50 hover:text-blue-400"
      >
        <StrikethroughIcon className="h-4 w-4" />
      </Toggle>

      <div className="toolabar-divider" />

      <Toggle
        onClick={() => editor.chain().focus().toggleBulletList().run()}
        aria-label="Toggle list"
        className="text-current data-[state=on]:bg-blue-50 data-[state=on]:text-blue-500 hover:bg-blue-50 hover:text-blue-400"
      >
        <ListBulletIcon className="h-4 w-4" />
      </Toggle>
    </div>
  );
};
