'use client';

import { Notification } from './notification';
import { ProfileGear } from './profile-gear';

export interface HeaderProps {
  changePasswordPath?: string;
  role: string;
}

export function Header({ changePasswordPath, role }: HeaderProps) {
  return (
    <div className="flex items-center justify-end bg-card px-2 xl:px-6 transition-transform border-b z-20">
      <div className="flex items-center divide-x">
        <div className="px-6">
          <Notification />
        </div>

        <ProfileGear changePasswordPath={changePasswordPath} role={role} />
      </div>
    </div>
  );
}
