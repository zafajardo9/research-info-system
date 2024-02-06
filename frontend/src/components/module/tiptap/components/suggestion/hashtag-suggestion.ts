import { type MentionOptions } from '@tiptap/extension-mention';
import { PluginKey } from '@tiptap/pm/state';
import { ReactRenderer } from '@tiptap/react';
import tippy, { type Instance, type Props as TippyProps } from 'tippy.js';

import { HASHTAG_SUGGESTIONS } from '../../constants';
import { type SuggestionDropdownRef } from '../../types';
import { HashtagList } from './hashtag-list';

export const HashtagSuggestion: MentionOptions['suggestion'] = {
  char: '#',
  allowSpaces: true,
  pluginKey: new PluginKey('hashtagSuggestion'),

  command: ({ editor, range, props }) => {
    const nodeAfter = editor.view.state.selection.$to.nodeAfter;
    const overrideSpace = nodeAfter?.text?.startsWith(' ');

    if (overrideSpace) {
      range.to += 1;
    }

    editor
      .chain()
      .focus()
      .insertContentAt(range, [
        {
          type: 'hashtagSuggestion',
          attrs: props,
        },
        {
          type: 'text',
          text: ' ',
        },
      ])
      .run();
  },
  allow: ({ editor, range }) => {
    return editor.can().insertContentAt(range, { type: 'hashtagSuggestion' });
  },

  items({ query }) {
    return HASHTAG_SUGGESTIONS.filter(({ label }) =>
      label.toLowerCase().includes(query.toLowerCase())
    );
  },

  render: () => {
    let component: ReactRenderer<SuggestionDropdownRef>;
    let popup: Instance<TippyProps>[];

    return {
      onStart: props => {
        component = new ReactRenderer(HashtagList, {
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
