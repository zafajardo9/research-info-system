import { RepositorySection } from '@/components/module/student';

export default function StudentRepository() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Repository</h1>
      </div>

      <RepositorySection />
    </div>
  );
}
