import { SetPreOralDefenseSection } from '@/components/module/faculty/components/set-pre-oral-defense-section';

export default function FacultySetPreOralDefense() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Set Pre Oral Defense</h1>
      </div>

      <SetPreOralDefenseSection />
    </div>
  );
}
