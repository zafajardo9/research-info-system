import { SubmittedEthicsProtocolSection } from '@/components/module/faculty/components/submitted-ethics-protocol-section';

export default function FacultySubmittedEthicsProtocol() {
  return (
    <div className="py-10 min-h-screen space-y-10">
      <div className="prose dark:prose-h1:text-white">
        <h1>Submitted Ethics/Protocol</h1>
      </div>

      <SubmittedEthicsProtocolSection />
    </div>
  );
}
