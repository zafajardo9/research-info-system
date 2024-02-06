import { risApi } from '@/lib/api';
import { authOptions } from '@/lib/auth-options';
import { Metadata } from 'next';
import { getServerSession } from 'next-auth';

export interface ResearchPaperDetails {
  research_paper: ResearchPaper[];
  authors: Author[];
}

export interface ResearchPaper {
  id: string;
  title: string;
  submitted_date: string;
  status: string;
  file_path: string;
  research_adviser: string;
  faculty_name: string;
  research_type: string;
}

export interface Author {
  id: string;
  name: string;
  student_number: string;
  section: string;
  course: string;
}

export type GenerateMetadataProps = {
  params: { id: string };
};

export async function generateMetadata({
  params: { id },
}: GenerateMetadataProps): Promise<Metadata> {
  try {
    const session = await getServerSession(authOptions);
    const authToken = session?.user?.authToken;

    const response = await risApi.get<ResearchPaperDetails>(`/research/${id}`, {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    const data = response.data?.research_paper[0];

    return {
      title: data?.title,
    };
  } catch (error) {
    return {
      title: 'Not Found',
    };
  }
}

export default function StudentProposalViewLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
