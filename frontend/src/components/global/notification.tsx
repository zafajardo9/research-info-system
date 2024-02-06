'use client';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  useDeleteAllNotifications,
  useDeleteAnnouncementById,
  useGetNotifications,
} from '@/hooks/use-notification-query';
import { BellIcon, TrashIcon } from '@radix-ui/react-icons';
import moment from 'moment';
import { ScrollArea } from '../ui/scroll-area';

export function Notification() {
  const { data: notifications = [], isLoading } = useGetNotifications();
  const deleteAll = useDeleteAllNotifications();
  const deleteOne = useDeleteAnnouncementById();

  const notificationList = notifications.sort(
    (a, b) =>
      new Date(b.Notification.created_at).valueOf() -
      new Date(a.Notification.created_at).valueOf()
  );

  return (
    <>
      {!isLoading && (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="h-10 w-10 p-0 rounded-full">
              <BellIcon className="h-6 w-6" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-96">
            <DropdownMenuLabel>Notifications</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <ScrollArea className="h-60">
                {notificationList.map(
                  ({ Notification: { id, message, created_at } }) => (
                    <div
                      key={id}
                      className="p-2 flex items-center justify-between gap-2"
                    >
                      <div className="text-sm">
                        <p>{message}</p>
                        <small className="text-muted-foreground">
                          {moment(moment.utc(created_at).toDate())
                            .local(true)
                            .fromNow()}
                        </small>
                      </div>
                      <div>
                        <button
                          type="button"
                          className="text-red-500"
                          onClick={async () => {
                            try {
                              await deleteOne.mutateAsync({ id });
                            } catch (error) {
                              console.log(error);
                            }
                          }}
                        >
                          <TrashIcon className="h-6 w-6" />
                        </button>
                      </div>
                    </div>
                  )
                )}

                {notificationList.length === 0 && (
                  <div className="h-60 flex items-center justify-center text-sm text-muted-foreground">
                    🔔 You have no notifications
                  </div>
                )}
              </ScrollArea>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="justify-center"
              onClick={async () => {
                try {
                  await deleteAll.mutateAsync();
                } catch (error) {
                  console.log(error);
                }
              }}
            >
              Delete all
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )}
    </>
  );
}
