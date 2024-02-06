import { type SuggestionProps } from '@tiptap/suggestion';
import Image from 'next/image';
import React from 'react';
import { type Mention, type SuggestionDropdownRef } from '../../types';
import SuggestionDropdown from './suggestion-dropdown';

type MentionListProps = Pick<SuggestionProps, 'command'> & {
  items: Mention[];
};

// eslint-disable-next-line react/display-name
export const MentionList = React.forwardRef<SuggestionDropdownRef, MentionListProps>(
  ({ items, command }, ref) => {
    return (
      <SuggestionDropdown
        forwardedRef={ref}
        items={items}
        onSelect={command}
        renderItem={({ label }) => (
          <div className="mention-item">
            <Image
              className="avatar"
              src={`/thirteen.svg`}
              alt={`${label}'s Avatar`}
              title={`${label}'s Avatar`}
              width={30}
              height={30}
            />
            <span className="name">{label}</span>
          </div>
        )}
      />
    );
  }
);
