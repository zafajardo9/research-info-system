import { IconBaseProps } from 'react-icons';

export type SidebarData = {
  key: string
  label: string;
  navigations: NavigationParent;
};

export type NavigationParent = Array<NavigationChildren | Navigation>;

export interface NavigationChildren {
  label: string;
  nodeList: Navigation[];
}

export interface Navigation {
  label: string;
  Icon: React.JSXElementConstructor<IconBaseProps>;
  href: string;
  className?: string;
  isHidden?: boolean;
}

export interface CustomStep {
  label: string;
  Icon: React.JSXElementConstructor<IconBaseProps>;
}
