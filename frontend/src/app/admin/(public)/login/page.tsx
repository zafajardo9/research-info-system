import logo from '@/assets/images/logo13.png';
import { Background } from '@/components/global';
import { AdminLoginForm } from '@/components/module/admin';
import Image from 'next/image';
import Link from 'next/link';

export default function AdminLogin() {
  return (
    <>
      <Background />
      <div className="flex min-h-screen flex-col items-center justify-between px-5 relative">
        <Link
          href="/"
          className="z-50 mt-10 transition-transform hover:scale-105"
        >
          <Image
            src={logo}
            alt="PUPQC RIS"
            quality={100}
            height={200}
            width={150}
          />
        </Link>

        <AdminLoginForm />

        <footer className="flex-0 flex w-full items-center justify-center py-3">
          <div className="text-xs">
            <span>PUPQC RIS © 2023</span>
          </div>
        </footer>
      </div>
    </>
  );
}
