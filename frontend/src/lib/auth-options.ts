import axios from 'axios';
import type { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import { risApi } from './api';
import { USER_ROLE } from './constants';

export interface AuthHandlerValues {
  username: string;
  password: string;
  role: keyof typeof USER_ROLE;
}

export interface Data {
  authToken: string;
  role: keyof typeof USER_ROLE;
}

export type AuthHandlerResponse = [Data | null, string | null] | undefined;

async function authHandler({
  role,
  ...creds
}: AuthHandlerValues): Promise<AuthHandlerResponse> {
  try {
    if (role === USER_ROLE.STUDENT) {
      // prettier-ignore
      const response = await risApi.post<LoginResponse>('/auth/login/student', creds)

      const data = {
        authToken: response.data.result.access_token,
        role,
      };

      return [data, null];
    }

    if (role === USER_ROLE.FACULTY) {
      // prettier-ignore
      const response = await risApi.post<LoginResponse>('/auth/login/faculty', creds)

      const data = {
        authToken: response.data.result.access_token,
        role,
      };

      return [data, null];
    }

    if (role === USER_ROLE.ADMIN) {
      // prettier-ignore
      const response = await risApi.post<LoginResponse>('/auth/login/admin', creds)

      const data = {
        authToken: response.data.result.access_token,
        role,
      };

      return [data, null];
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      return [null, error.response?.data?.detail];
    }
  }
}

// prettier-ignore
async function studentProfileHandler(authToken: string): Promise<StudentProfile | undefined> {
  try {
    // prettier-ignore
    const response = await risApi.get<DefaultApiResponse<StudentProfile>>(
      '/users/profile/student',
      {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      }
    );

    return response.data.result
  } catch (error) {
    return undefined
  }
}

// prettier-ignore
async function facultyProfileHandler(authToken: string): Promise<FacultyProfile | undefined> {
  try {
    // prettier-ignore
    const response = await risApi.get<DefaultApiResponse<FacultyProfile>>(
      '/users/profile/faculty',
      {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      }
    );

    return response.data.result
  } catch (error) {
    return undefined
  }
}

export const SESSION_MAX_AGE = 600;

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: 'Username/Student ID', type: 'text' },
        password: { label: 'Password', type: 'password' },
        role: { label: 'Role', type: 'text' },
      },

      async authorize(credentials) {
        try {
        } catch (error) {}
        const payload: AuthHandlerValues = {
          username: credentials?.username ?? '',
          password: credentials?.password ?? '',
          role: (credentials?.role ?? 'STUDENT') as keyof typeof USER_ROLE,
        };

        const response = await authHandler(payload);

        const [data, error] = response ?? [];

        if (data && !error) {
          // prettier-ignore
          const studentProfileResponse = await studentProfileHandler(data.authToken)

          // prettier-ignore
          const facultyProfileResponse = await facultyProfileHandler(data.authToken)

          return {
            authToken: data.authToken,
            role: data.role,
            studentProfile: studentProfileResponse,
            facultyProfile: facultyProfileResponse,
          };
        }

        throw Error(error as string);
      },
    }),
  ],

  secret: process.env.NEXTAUTH_SECRET,

  session: { maxAge: SESSION_MAX_AGE },

  jwt: { maxAge: SESSION_MAX_AGE },

  callbacks: {
    async jwt({ token, user }) {
      if (user) return { user };
      return token;
    },

    async session({ session, token }) {
      session.user = token.user as any;
      return session;
    },
  },
};
