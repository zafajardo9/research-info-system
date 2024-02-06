import { CollaborationSection } from '@/components/module/student';

export default function AdminResearchersProfile() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <CollaborationSection profilePath="/admin/researchers-profile" />
    </div>
  );
}
