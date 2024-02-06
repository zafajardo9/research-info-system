import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { ClockIcon } from '@radix-ui/react-icons';
import moment from 'moment';
import { memo, useEffect, useState } from 'react';

const COOLDOWN = 45; // 45 seconds palitan niyo nalang kung ilang seconds cooldown gusto nyo after ng update

function padStart(n: number, length: number) {
  return Math.floor(n).toString().padStart(length, '0');
}

export interface Cooldown {
  modified_at: string;
  isCooldown: boolean;
  setIsCooldown: (value: boolean) => void;
}

const Cooldown = memo(function Cooldown({
  modified_at,
  isCooldown,
  setIsCooldown,
}: Cooldown) {
  const [secs, setSecs] = useState<number>(0);

  useEffect(() => {
    const end_date = (
      modified_at
        ? moment(moment.utc(modified_at).toDate()).local(true)
        : moment()
    ).add(COOLDOWN, 'seconds');

    const intervalId = setInterval(() => {
      const current_date = moment();

      if (current_date.isSameOrAfter(end_date)) {
        setSecs(0);
        setIsCooldown(false);

        clearInterval(intervalId);
      } else {
        const duration = moment.duration(end_date.diff(current_date));

        const s = duration.asSeconds();

        setSecs(s);

        setIsCooldown(true);
      }
    }, 1000);

    return () => {
      clearInterval(intervalId);
    };
  }, [modified_at, setIsCooldown]);

  if (!isCooldown) return null;

  return (
    <Alert className="[&>svg]:text-yellow-500 text-yellow-500 border-yellow-500 bg-yellow-50">
      <ClockIcon className="h-4 w-4" />
      <AlertTitle>
        <span>{padStart(secs, 2)}</span>
        <small className="ml-1">seconds</small>
      </AlertTitle>
      <AlertDescription>
        This record has been recently updated. Currently, all actions are
        disabled. Please wait for a cooldown period before attempting any
        further actions.
      </AlertDescription>
    </Alert>
  );
});

export default Cooldown;
