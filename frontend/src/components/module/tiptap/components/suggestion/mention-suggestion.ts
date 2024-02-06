import { type MentionOptions } from '@tiptap/extension-mention';
import { ReactRenderer } from '@tiptap/react';
import tippy, { type Instance, type Props as TippyProps } from 'tippy.js';
import { MENTION_SUGGESTIONS } from '../../constants';
import { type SuggestionDropdownRef } from '../../types';
import { MentionList } from './mention-list';

export const MentionSuggestion: MentionOptions['suggestion'] = {
  items({ query }) {
    return MENTION_SUGGESTIONS.filter(({ label }) =>
      label.toLowerCase().includes(query.toLowerCase())
    );
  },

  render: () => {
    let component: ReactRenderer<SuggestionDropdownRef>;
    let popup: Instance<TippyProps>[];

    return {
      onStart: props => {
        component = new ReactRenderer(MentionList, {
          props,
          editor: props.editor,
        });

        if (!props.clientRect) return;

        // @ts-ignore
        popup = tippy('body', {
          getReferenceClientRect: props.clientRect,
          appendTo: () => document.body,
          content: component.element,
          showOnCreate: true,
          interactive: true,
          trigger: 'manual',
          placement: 'bottom-start',
        });
      },

      onUpdate: props => {
        component.updateProps(props);

        if (!props.clientRect) return;

        popup[0].setProps({
          // @ts-ignore
          getReferenceClientRect: props.clientRect,
        });
      },

      onKeyDown: props => {
        if (props.event.key === 'Escape') {
          popup[0].hide();

          return true;
        }
        return Boolean(component.ref?.onKeyDown(props));
      },

      onExit: () => {
        popup[0].destroy();
        component.destroy();
      },
    };
  },
};
