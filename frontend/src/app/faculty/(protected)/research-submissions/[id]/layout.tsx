import { risApi } from '@/lib/api';
import { authOptions } from '@/lib/auth-options';
import { Metadata } from 'next';
import { getServerSession } from 'next-auth';

export type GenerateMetadataProps = {
  params: { id: string };
};

export async function generateMetadata({
  params: { id },
}: GenerateMetadataProps): Promise<Metadata> {
  try {
    const session = await getServerSession(authOptions);
    const authToken = session?.user?.authToken;

    const response = await risApi.get<Research>(`/research/${id}`, {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });

    const data = response.data;

    return {
      title: data.title,
    };
  } catch (error) {
    return {
      title: 'Not Found',
    };
  }
}

export default function FacultyViewResearchSubmissionsLayout({
  children,
}: React.PropsWithChildren) {
  return children;
}
