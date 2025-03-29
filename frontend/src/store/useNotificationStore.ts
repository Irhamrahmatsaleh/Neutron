import { create } from 'zustand';

interface Notification {
  id: number;
  title: string;
  message: string;
}

interface NotificationStore {
  isOpen: boolean;
  notifications: Notification[];
  readIds: number[];
  openModal: () => void;
  closeModal: () => void;
  addNotification: (notification: Notification) => void;
  markAllAsRead: () => void;
  unreadCount: () => number;
  setSelectedNotification: (notification: Notification) => void;
  selectedNotification: Notification | null;
}

export const useNotificationStore = create<NotificationStore>((set, get) => ({
  isOpen: false,
  notifications: [
    { id: 1, title: 'Transaction Successful', message: 'You sent 1.0 NTR to 0xabc...123' },
    { id: 2, title: 'New Reward', message: 'You received 0.5 NTR from mining.' },
  ],
  readIds: [],
  openModal: () => {
    set({ isOpen: true });
    set((state) => ({
      readIds: [...state.notifications.map((n) => n.id)],
    }));
  },
  closeModal: () => set({ isOpen: false }),
  addNotification: (notification) =>
    set((state) => ({
      notifications: [...state.notifications, notification],
    })),
  markAllAsRead: () => {
    set((state) => ({
      readIds: [...state.notifications.map((n) => n.id)],
    }));
  },
  unreadCount: () => {
    const { notifications, readIds } = get();
    return notifications.filter((n) => !readIds.includes(n.id)).length;
  },
  selectedNotification: null,
  setSelectedNotification: (notification) => set({ selectedNotification: notification }),
}));
