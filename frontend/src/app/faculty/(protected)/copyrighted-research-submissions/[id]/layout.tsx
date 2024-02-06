import { risApi } from '@/lib/api';
import { authOptions } from '@/lib/auth-options';
import { Metadata } from 'next';
import { getServerSession } from 'next-auth';

export interface CopyrightedResearchData {
  created_at: string;
  user_id: string;
  modified_at: string;
  id: string;
  title: string;
  content: string;
  abstract: string;
  file_path: string;
  date_publish: string;
  category: string;
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

    const response = await risApi.get<CopyrightedResearchData>(
      `/faculty/my-research-papers/${id}`,
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
