'use client';

import { DashboardContent, Sidebar } from '@/components/global';
import { ADMIN_NAVIGATION } from '@/lib/constants';
import { useSidebarStore } from '@/store/sidebar-store';
import { SidebarData } from '@/types/navigation';
import { useEffect, useMemo, useState } from 'react';
import { AdminWorkflowContext } from './context/process';
import { AdminSidebar } from './admin-sidebar';

export function AdminLayout({ children }: React.PropsWithChildren) {
  const { selectSidebar } = useSidebarStore();
  const [researchType, setResearchType] = useState<string>('Admin');

  const sidebars = useMemo<SidebarData[]>(() => {
    return [
      {
        key: 'admin',
        label: 'Admin',
        navigations: ADMIN_NAVIGATION,
      },
      {
        key: 'Research',
        label: 'Research',
        navigations: ADMIN_NAVIGATION,
      },
      {
        key: 'Feasibility Study',
        label: 'Feasibility Study',
        navigations: ADMIN_NAVIGATION,
      },
      {
        key: 'Capstone',
        label: 'Capstone',
        navigations: ADMIN_NAVIGATION,
      },
      {
        key: 'Business Plan',
        label: 'Business Plan',
        navigations: ADMIN_NAVIGATION,
      },
    ];
  }, []);

  useEffect(() => {
    if (sidebars.length > 0) {
      selectSidebar(sidebars[0]);
    }
  }, [sidebars, selectSidebar]);

  return (
    <div>
      <AdminWorkflowContext.Provider
        value={{
          researchType,
          setResearchType,
        }}
      >
        <AdminSidebar />
        <DashboardContent role="Admin">{children}</DashboardContent>
      </AdminWorkflowContext.Provider>
    </div>
  );
}
