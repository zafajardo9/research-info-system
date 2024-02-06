import { SidebarData } from '@/types/navigation';
import { create } from 'zustand';

interface SidebarState {
  currentSidebar?: SidebarData | null;
  selectSidebar: (sidebar: SidebarData | null) => void;
}

export const useSidebarStore = create<SidebarState>((set) => ({
  selectSidebar: (sidebar) => set({ currentSidebar: sidebar }, false),
}));
