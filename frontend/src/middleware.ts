import { getToken } from 'next-auth/jwt';
import { withAuth } from 'next-auth/middleware';
import { NextFetchEvent, NextRequest, NextResponse } from 'next/server';
import { USER_ROLE } from './lib/constants';
import { UserCredentials } from './types/next-auth';

const StudentPath = '/student';
const FacultyPath = '/faculty';
const AdminPath = '/admin';

const StudentRestrictedPaths = ['/student/login'];
const FacultyRestrictedPaths = ['/faculty/login'];
const AdminRestrictedPaths = ['/admin/login'];

export default async function middleware(
  req: NextRequest,
  event: NextFetchEvent
) {
  // prettier-ignore
  const token = (await getToken({ req, secret: process.env.NEXTAUTH_SECRET })) as any;
  const hasToken = Boolean(token);
  const pathname = req.nextUrl.pathname;
  const origin = req.nextUrl.origin;
  const user = token?.user as UserCredentials;
  const role = user?.role ?? '';

  const aStudentPath = pathname.startsWith(StudentPath);
  const aFacultyPath = pathname.startsWith(FacultyPath);
  const aAdminPath = pathname.startsWith(AdminPath);
  const aIndexPath = pathname === '/';

  // prettier-ignore
  const aStudentRestrictedPath = StudentRestrictedPaths.some((path) => pathname.startsWith(path))
  // prettier-ignore
  const aFacultyRestrictedPath = FacultyRestrictedPaths.some((path) => pathname.startsWith(path))
  // prettier-ignore
  const aAdminRestrictedPath = AdminRestrictedPaths.some((path) => pathname.startsWith(path))

  if (aStudentPath || aIndexPath) {
    if ((aIndexPath || aStudentRestrictedPath) && hasToken) {
      switch (role) {
        case USER_ROLE.FACULTY:
          return NextResponse.redirect(
            new URL(`${FacultyPath}/dashboard`, origin)
          );

        case USER_ROLE.ADMIN:
          return NextResponse.redirect(
            new URL(`${AdminPath}/dashboard`, origin)
          );

        default:
          return NextResponse.redirect(
            new URL(`${StudentPath}/progress`, origin)
          );
      }
    }
  }

  if (aFacultyPath || aIndexPath) {
    if ((aIndexPath || aFacultyRestrictedPath) && hasToken) {
      switch (role) {
        case USER_ROLE.STUDENT:
          return NextResponse.redirect(
            new URL(`${StudentPath}/progress`, origin)
          );

        case USER_ROLE.ADMIN:
          return NextResponse.redirect(
            new URL(`${AdminPath}/dashboard`, origin)
          );

        default:
          return NextResponse.redirect(
            new URL(`${FacultyPath}/dashboard`, origin)
          );
      }
    }
  }

  if (aAdminPath || aIndexPath) {
    if ((aIndexPath || aAdminRestrictedPath) && hasToken) {
      switch (role) {
        case USER_ROLE.STUDENT:
          return NextResponse.redirect(
            new URL(`${StudentPath}/progress`, origin)
          );

        case USER_ROLE.FACULTY:
          return NextResponse.redirect(
            new URL(`${FacultyPath}/dashboard`, origin)
          );

        default:
          return NextResponse.redirect(
            new URL(`${AdminPath}/dashboard`, origin)
          );
      }
    }
  }

  // prettier-ignore
  if (!aIndexPath && !aStudentRestrictedPath && !aFacultyRestrictedPath && !aAdminRestrictedPath) {
    const authMiddleware = withAuth({
      pages: {
        signIn: '/',
      },

      callbacks: {
        authorized: ({ token }) => {
          if (aAdminPath) {
            return token?.user?.role === USER_ROLE.ADMIN;
          }

          if (aStudentPath) {
            return token?.user?.role === USER_ROLE.STUDENT;
          }

          if (aFacultyPath) {
            return token?.user?.role === USER_ROLE.FACULTY;
          }

          return token !== null;
        },
      },
    });

    // @ts-expect-error
    return authMiddleware(req, event);
  }
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon|sw).*)',
  ],
};
