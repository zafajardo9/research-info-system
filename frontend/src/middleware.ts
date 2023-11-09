import { withAuth } from 'next-auth/middleware';
import { NextFetchEvent, NextRequest } from 'next/server';
// import type { UserCredentials } from './shared/types/next-auth';

// Access Allowed Only for Signed-In Users:
const PrivatePaths: string[] = ['/student/dashboard'];

export default async function middleware(
  req: NextRequest,
  event: NextFetchEvent
) {
  const pathname = req.nextUrl.pathname;

  // prettier-ignore
  const aPrivatePath = PrivatePaths.some((path) => pathname.startsWith(path));

  if (aPrivatePath) {
    const authMiddleware = withAuth({
      pages: {
        signIn: '/student/login',
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
    '/((?!api|_next/static|_next/image|favicon/favicon.ico).*)',
  ],
};
