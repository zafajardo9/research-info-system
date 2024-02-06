import { risApi } from '@/lib/api';
import { SECTION_KEY } from '@/lib/constants';
import { useQuery } from '@tanstack/react-query';
import { useSession } from 'next-auth/react';

export function useGetClassRooms() {
  const { data: session, status } = useSession();

  return useQuery<DefaultApiResponse<ClassRoomData[]>>({
    queryKey: [SECTION_KEY],
    queryFn: async () => {
      const res = await risApi.get<DefaultApiResponse<ClassRoomData[]>>(
        SECTION_KEY + '/course_with_year_list',
        {
          headers: {
            Authorization: `Bearer ${session?.user?.authToken}`,
          },
        }
      );
      return res.data;
    },
    enabled: status === 'authenticated',
    refetchOnMount: true,
  });
}
