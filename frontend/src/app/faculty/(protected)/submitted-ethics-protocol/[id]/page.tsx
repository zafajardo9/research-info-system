import { EthicsProtocolViewSection } from '@/components/module/faculty/components/ethics-protocol-view-section';

export interface FacultyViewSubmittedEthicsProtocol {
  params: { id: string };
}

export default function FacultyViewSubmittedEthicsProtocol({
  params: { id },
}: FacultyViewSubmittedEthicsProtocol) {
  return <EthicsProtocolViewSection id={id} />;
}
