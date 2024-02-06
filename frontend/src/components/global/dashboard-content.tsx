'use client';

import React from 'react';
import { Header } from './header';

export interface DashboardContentProps {
  children: React.ReactNode;
  role: string;
}

export function DashboardContent({ children, role }: DashboardContentProps) {
  return (
    <div className="xl:pl-64 transition-all ease-out duration-500 h-screen flex flex-col">
      <Header role={role} />
      <main className="px-2 xl:px-6">{children}</main>
    </div>
  );
}
