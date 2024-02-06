import Link from '@tiptap/extension-link';
import Mention from '@tiptap/extension-mention';

import Underline from '@tiptap/extension-underline';
import type { Extensions } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';

import { HashtagSuggestion, MentionSuggestion } from './components/suggestion';
import type { Mention as MentionProps } from './types';

export const MENTION_SUGGESTIONS: MentionProps[] = [
  { id: 8506571847, label: 'Aer' },
  { id: 8506571847, label: 'Ana' },
  { id: 7964905155, label: 'Anaïs' },
  { id: 5334942580, label: 'Robin Wright' },
  { id: 2591305900, label: 'Russell Crowe' },
  { id: 1977748635, label: 'Salma Hayek' },
  { id: 3079884396, label: 'Sam Shepard' },
  { id: 8332805759, label: 'Samuel L. Jackson' },
  { id: 7306599690, label: 'Sandra Bullock' },
  { id: 7671603007, label: 'Sarah Polley' },
  { id: 2129815758, label: 'Scarlett Johansson' },
  { id: 9708799963, label: 'Sean Connery' },
  { id: 8394170501, label: 'Sean Penn' },
  { id: 2649803916, label: 'Sebastian Koch' },
  { id: 5548407635, label: 'Sharon Stone' },
  { id: 7347736269, label: 'Sigourney Weaver' },
  { id: 4969491119, label: 'Steve McQueen' },
  { id: 7013789089, label: 'Susan Sarandon' },
  { id: 5903890148, label: 'Tilda Swinton' },
  { id: 1548869538, label: 'Tim Robbins' },
  { id: 2674694556, label: 'Tom Cruise' },
  { id: 1385349506, label: 'Tom Hanks' },
  { id: 4123717713, label: 'Tommy Lee Jones' },
  { id: 3540585850, label: 'Uma Thurman' },
  { id: 4826556381, label: 'Val Kilmer' },
  { id: 1372118055, label: 'Virginia Madsen' },
  { id: 5371208488, label: 'Whoopi Goldberg' },
  { id: 6003049383, label: 'Will Smith' },
  { id: 6521381385, label: 'Willem Dafoe' },
  { id: 3494505187, label: 'William Hurt' },
  { id: 6234091504, label: 'Winona Ryder' },
  { id: 6675088912, label: 'Woody Harrelson' },
  { id: 7964905155, label: 'Yves Montand' },
  { id: 8506571847, label: 'Ziyi Zhang' },
];

export const HASHTAG_SUGGESTIONS: MentionProps[] = [
  { id: Math.floor(Math.random() * 1000), label: 'development' },
  { id: Math.floor(Math.random() * 1000), label: 'test' },
  { id: Math.floor(Math.random() * 1000), label: 'frontend' },
  { id: Math.floor(Math.random() * 1000), label: 'backend' },
  { id: Math.floor(Math.random() * 1000), label: 'webdevelopment' },
  { id: Math.floor(Math.random() * 1000), label: 'lezgoo' },
  { id: Math.floor(Math.random() * 1000), label: 'testing' },
  { id: Math.floor(Math.random() * 1000), label: 'youcandoit' },
  { id: Math.floor(Math.random() * 1000), label: 'hakdog' },
];

export const extensions: Extensions = [
  StarterKit.configure({
    heading: false,
  }),
  Underline,
  Link.configure({
    // validate: (href) => /^https?:\/\//.test(href),
    linkOnPaste: false,
    openOnClick: false,
  }),

  Mention.extend({ name: 'hashtagSuggestion' }).configure({
    HTMLAttributes: {
      class: 'mention',
    },

    renderLabel: ({ options, node }) => {
      return `${options.suggestion.char}${node.attrs.label}`;
    },

    suggestion: HashtagSuggestion,
  }),

  Mention.extend({
    name: 'mentionSuggestion',
  }).configure({
    HTMLAttributes: {
      class: 'mention',
    },

    renderLabel: ({ node }) => {
      return `${node.attrs.label}`;
    },

    suggestion: MentionSuggestion,
  }),
];
