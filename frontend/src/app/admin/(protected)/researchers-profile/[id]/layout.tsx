import { risApi } from '@/lib/api';
import { authOptions } from '@/lib/auth-options';
import { Metadata } from 'next';
import { getServerSession } from 'next-auth';

export interface ResearcherProfileData {
  id: string;
  email: string;
  name: string;
  birth: any;
  student_number: string;
  phone_number: string;
  course: string;
  section: string;
  status: string;
  roles: string[];
  papers: Paper[];
}

export interface Paper {
  research_paper: ResearchPaper;
  authors: Author[];
}

export interface ResearchPaper {
  id: string;
  title: string;
  research_type: string;
  content: string;
  abstract: string;
  keywords: string;
  date_publish: string;
}

export interface Author {
  name: string;
  student_number: string;
  course: string;
  year_section: string;
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

    const response = await risApi.get<ResearcherProfileData>(
      `/users/profile/student/${id}`,
      {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      }
    );

    const data = response.data;

    return {
      title: data?.name,
    };
  } catch (error) {
    return {
      title: 'Not Found',
    };
  }
}

export default function AdminViewResearcherProfileLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
