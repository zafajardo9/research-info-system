import logo from "@/assets/images/myPUPQC.png";
import { Background } from "@/components/global";
import { FacultyLoginForm } from "@/components/module/faculty/components/faculty-login-form";
import Image from "next/image";
import Link from "next/link";

export default function FacultLogin() {
  let currentYear = new Date().getFullYear();
  return (
    <>
      <Background />
      <div className="flex min-h-screen flex-col items-center justify-between px-5 relative">
        <div className="w-full mt-10">
          <Link
            href="/"
            className="z-50 mt-10 hover:scale-105 transition-transform"
          >
            <Image
              src={logo}
              alt="PUPQC RIS"
              quality={100}
              height={200}
              width={150}
            />
          </Link>
        </div>

        <FacultyLoginForm />

        <footer className="flex-0 flex w-full items-center justify-center py-3">
          <div className="text-xs">
            <span>PUPQC RIS © {currentYear}</span>
          </div>
        </footer>
      </div>
    </>
  );
}
