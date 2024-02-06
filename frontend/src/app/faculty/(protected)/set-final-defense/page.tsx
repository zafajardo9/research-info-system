import { SetFinalDefenseSection } from '@/components/module/faculty/components/set-final-defense-section';

export default function FacultyFinalDefense() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Set Final Defense</h1>
      </div>

      <SetFinalDefenseSection />
    </div>
  );
}
