import type { SuggestionKeyDownProps } from '@tiptap/suggestion';
import type { PropsWithChildren } from 'react';

export type Mention = {
  id: number;
  label: string;
};

export type SuggestionDropdownRef = {
  onKeyDown: (props: SuggestionKeyDownProps) => boolean;
};

export type SuggestionDropdownProps<TItem> = {
  forwardedRef: React.ForwardedRef<SuggestionDropdownRef>;
  items: TItem[];
  onSelect: (item: TItem) => void;
  renderItem: (item: TItem) => JSX.Element;
};

export type TiptapProps = PropsWithChildren & {
  className?: string;
  containerClassName?: string
  value: string;
  onChange?: (...event: any[]) => void;
  placeholder?: string
  disabled?: boolean
};
