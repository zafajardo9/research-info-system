export function Background() {
  return (
    <div
      className="absolute inset-0 bg-grid-slate-dark bg-[bottom_1px_center] dark:bg-grid-slate-white dark:bg-bottom dark:border-b dark:border-slate-100/5"
      style={{
        maskImage: 'linear-gradient(to bottom, transparent, black)',
        WebkitMaskImage: 'linear-gradient(to bottom, transparent, black)',
      }}
    />
  );
}
