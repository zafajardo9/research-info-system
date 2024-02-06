import { type SuggestionProps } from '@tiptap/suggestion';
import React from 'react';
import { type Mention, type SuggestionDropdownRef } from '../../types';
import SuggestionDropdown from './suggestion-dropdown';

type MentionListProps = Pick<SuggestionProps, 'command'> & {
  items: Mention[];
};

// eslint-disable-next-line react/display-name
export const HashtagList = React.forwardRef<SuggestionDropdownRef, MentionListProps>(
  ({ items, command }, ref) => {
    return (
      <SuggestionDropdown
        forwardedRef={ref}
        items={items}
        onSelect={command}
        renderItem={({ label }) => <h3 className="name">#{label}</h3>}
      />
    );
  }
);
