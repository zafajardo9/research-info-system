import {
  OverlayScrollbarsComponent,
  type OverlayScrollbarsComponentRef,
} from 'overlayscrollbars-react';
import React from 'react';

import 'overlayscrollbars/overlayscrollbars.css';

import { cn } from '@/lib/utils';
import { type SuggestionDropdownProps } from '../../types';
import { scrollIntoView } from './scroll-into-view';

function SuggestionDropdown<TItem>({
  forwardedRef,
  items,
  onSelect,
  renderItem,
}: SuggestionDropdownProps<TItem>) {
  const [selectedIndex, setSelectedIndex] = React.useState(0);
  const overlayScrollbarsRef = React.useRef<OverlayScrollbarsComponentRef>(null);
  const selectedItemRef = React.useRef<HTMLLIElement>(null);

  function selectItem(index: number) {
    const item = items[index];

    if (item) {
      onSelect(item);
    }
  }

  React.useEffect(
    function scrollSelectedItemIntoView() {
      const { current: selectedElement } = selectedItemRef;
      const { viewport } = overlayScrollbarsRef.current?.osInstance()?.elements() || {};

      if (viewport && selectedElement) {
        scrollIntoView(selectedElement, {
          scrollContainer: viewport,
          x: false,
          y: { ifNeeded: true },
        });
      }
    },
    [selectedIndex]
  );

  React.useImperativeHandle(forwardedRef, () => ({
    onKeyDown: ({ event }) => {
      if (event.key === 'ArrowUp') {
        setSelectedIndex((selectedIndex + items.length - 1) % items.length);
        return true;
      }

      if (event.key === 'ArrowDown') {
        setSelectedIndex((selectedIndex + 1) % items.length);
        return true;
      }

      if (event.key === 'Enter') {
        selectItem(selectedIndex);
        return true;
      }

      return false;
    },
  }));

  if (items.length === 0) {
    return null;
  }

  return (
    <OverlayScrollbarsComponent
      ref={overlayScrollbarsRef}
      className="suggestion-dropdown"
      data-overlayscrollbars=""
    >
      <ul>
        {items?.map((item, index) => (
          <li
            key={index}
            className={cn('suggestion-item', index === selectedIndex && 'bg-dark-50')}
            onClick={() => selectItem(index)}
            ref={index === selectedIndex ? selectedItemRef : null}
          >
            {renderItem(item)}
          </li>
        ))}
      </ul>
    </OverlayScrollbarsComponent>
  );
}

export default SuggestionDropdown;
