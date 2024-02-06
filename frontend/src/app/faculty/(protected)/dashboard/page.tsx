import { FacultyDashboardSection } from '@/components/module/faculty';

export default function FacultyDashboard() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Dashboard</h1>
      </div>

      <FacultyDashboardSection />
    </div>
  );
}
