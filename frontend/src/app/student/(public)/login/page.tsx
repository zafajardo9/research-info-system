import logo from "@/assets/images/myPUPQC.png";
import { Background } from "@/components/global";
import { StudentLoginForm } from "@/components/module/student";
import Image from "next/image";
import Link from "next/link";

export default function StudentLogin() {
  let currentYear = new Date().getFullYear();
  return (
    <>
      <Background />

      <div className="min-h-screen flex flex-col items-center justify-between px-5 relative">
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

        <StudentLoginForm />

        <footer className="flex flex-0 w-full py-3 justify-center items-center">
          <div className="text-xs">
            <span>PUPQC RIS © {currentYear}</span>
          </div>
        </footer>
      </div>
    </>
  );
}
