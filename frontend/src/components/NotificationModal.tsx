import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { useNotificationStore } from '../store/useNotificationStore';
import { useNavigate } from 'react-router-dom';

const NotificationModal: React.FC = () => {
  const { isOpen, closeModal, notifications } = useNotificationStore();
  const { setSelectedNotification } = useNotificationStore();
  const navigate = useNavigate();

  return (
    <Dialog open={isOpen} onOpenChange={closeModal}>
      <DialogContent className="bg-gray-900 border border-gray-700 text-white">
        <DialogHeader>
          <DialogTitle className="text-indigo-400">🔔 Notifications</DialogTitle>
        </DialogHeader>
        <div className="mt-4 space-y-4 text-sm max-h-[300px] overflow-y-auto">
          {notifications.length > 0 ? (
            notifications.map((notif) => {
              const { readIds } = useNotificationStore.getState(); // akses langsung dari Zustand
              const isUnread = !readIds.includes(notif.id);

              return (
                <div
                  key={notif.id}
                  onClick={() => {
                    setSelectedNotification(notif);
                    closeModal();
                    navigate('/notifications');
                  }}
                  className={`p-3 border rounded-lg cursor-pointer transition ${
                    isUnread
                      ? 'bg-indigo-900 border-indigo-700 text-white'
                      : 'bg-gray-800 border-gray-700 text-gray-400'
                  } hover:bg-gray-700`}
                >
                  <p className="font-semibold">{notif.title}</p>
                  <p className="text-sm">{notif.message}</p>
                </div>
              );
            })
          ) : (
            <p className="text-gray-500 italic">No notifications yet.</p>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default NotificationModal;
