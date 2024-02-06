import { risApi } from '@/lib/api';
import { authOptions } from '@/lib/auth-options';
import { Metadata } from 'next';
import { getServerSession } from 'next-auth';

export interface FacultyResearchPaper {
  created_at: string;
  id: string;
  content: string;
  file_path: string;
  category: string;
  user_id: string;
  title: string;
  modified_at: string;
  abstract: string;
  date_publish: string;
  publisher: string;
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

    const response = await risApi.get<FacultyResearchPaper>(
      `/admin/faculty-paper-view/${id}`,
      {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      }
    );

    const data = response.data;

    return {
      title: data?.title,
    };
  } catch (error) {
    return {
      title: 'Not Found',
    };
  }
}

export default function FacultyViewCopyrightedResearchSubmissionsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
