import backgroundImage from "@/assets/images/bg_pupqc.png";

// export function Background() {
//   const backgroundImage = "/public/bg_pupqc.png";
//   return (
//     <div
//       className=" bg-red-400 absolute inset-0 bg-grid-slate-dark bg-[bottom_1px_center]"
//       style={{
//         maskImage: "linear-gradient(to bottom, transparent, black)",
//         WebkitMaskImage: "linear-gradient(to bottom, transparent, black)",
//       }}
//     />
//   );
// }

export function Background() {
  return (
    <div
      className="absolute inset-0 bg-cover bg-center bg-no-repeat"
      style={{
        backgroundImage: `url(${backgroundImage.src})`,
      }}
    />
  );
}
