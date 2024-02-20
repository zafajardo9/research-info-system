'use client';

import React from 'react';
import { Header } from './header';

export interface DashboardContentProps {
  children: React.ReactNode;
  changePasswordPath?: string;
  role: string;
}

export function DashboardContent({
  children,
  changePasswordPath,
  role,
}: DashboardContentProps) {
  return (
    <div className="xl:pl-64 transition-all ease-out duration-500 h-screen flex flex-col">
      <Header changePasswordPath={changePasswordPath} role={role} />
      <main className="px-2 xl:px-6">{children}</main>
    </div>
  );
}
