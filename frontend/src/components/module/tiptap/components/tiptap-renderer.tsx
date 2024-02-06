import { cn } from '@/lib/utils';
import parse from 'html-react-parser';

type Props = {
  html: string;
  className?: string;
};

export const TiptapRenderer = ({ html, className }: Props) => {
  // console.log({ html });
  // const output = useMemo(() => {
  //   return generateHTML(html, extensions);
  // }, [html]);

  return <div className={cn('prose max-w-none', className)}>{parse(html)}</div>;
};
