import { MagnifyingGlassIcon } from '@radix-ui/react-icons';
import { Input } from './input';

export function SearchBar() {
  return (
    <div className="relative w-full h-fit xl:w-80">
      <MagnifyingGlassIcon className="absolute h-6 w-6 left-1 top-1/2 -translate-y-1/2 text-muted-foreground" />
      <Input
        placeholder="Search here..."
        className="indent-5 bg-white text-base rounded-xl"
      />
    </div>
  );
}
