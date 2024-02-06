// import { risApi } from '@/lib/api';
// import { USERS_KEY } from '@/lib/constants';
// import { useQuery } from '@tanstack/react-query';
// import { useSession } from 'next-auth/react';

// export function useGetStudentProfile() {
//   const { data: session, status } = useSession();

//   return useQuery<DefaultApiResponse<Profile>>({
//     queryKey: [USERS_KEY, '/profile/student'],
//     queryFn: async () => {
//       const res = await risApi.get<DefaultApiResponse<Profile>>(
//         USERS_KEY + '/profile/student',
//         {
//           headers: {
//             Authorization: `Bearer ${session?.user?.authToken}`,
//           },
//         }
//       );
//       return res.data;
//     },
//     enabled: status === 'authenticated',
//   });
// }
