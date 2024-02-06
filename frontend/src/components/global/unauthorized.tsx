import Warning from '@/assets/svgs/warning';

export function Unauthorized() {
  return (
    <div className="flex flex-col items-center justify-center gap-3">
      <Warning className="h-56 w-56" />
      <div className="prose prose-sm max-w-none text-center">
        <h1>Unauthorized Access Warning</h1>
        <p>
          Oops! You&apos;re not authorized to view this page. If you think this
          is a mistake, contact the administrator.
        </p>
        <p>PUPQC RIS</p>
      </div>
    </div>
  );
}
