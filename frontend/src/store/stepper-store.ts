import { create } from 'zustand';

interface SidebarState {
  activeStep: number;
  setActiveStep: (value: number) => void;
}

export const useStepperStore = create<SidebarState>((set) => ({
  activeStep: 0,
  setActiveStep: (value) => set({ activeStep: value }, false),
}));
