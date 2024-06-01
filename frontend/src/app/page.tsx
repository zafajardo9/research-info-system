import logo from "@/assets/images/myPUPQC.png";
import { Background } from "@/components/global";
import { HeroSection } from "@/components/module/home";
import Image from "next/image";

export default function Home() {
  let currentYear = new Date().getFullYear();
  return (
    <>
      <Background />
      <div className="flex min-h-screen flex-col items-center justify-between px-5 inset-0 relative">
        <div className="w-full">
          <Image
            src={logo}
            alt="PUPQC RIS"
            quality={100}
            height={200}
            width={150}
            className="mt-10"
          />
        </div>

        <HeroSection />

        <footer className="flex-0 flex w-full items-center justify-center py-3">
          <div className="text-xs">
            <span>PUPQC RIS © {currentYear}</span>
          </div>
        </footer>
      </div>
    </>
  );
}
