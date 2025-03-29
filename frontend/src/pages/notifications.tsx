import React, { useState } from 'react';
import { useNotificationStore } from '../store/useNotificationStore';

const NotificationsPage: React.FC = () => {
  const { notifications } = useNotificationStore();
  const [activeId, setActiveId] = useState<number | null>(null);

  const toggleDetail = (id: number) => {
    setActiveId((prev) => (prev === id ? null : id));
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-indigo-400 mb-4">📨 Notifications</h1>

      <div className="space-y-4">
        {notifications.map((n) => (
          <div
            key={n.id}
            className="bg-gray-800 border border-gray-700 rounded-lg p-4 shadow-md cursor-pointer hover:bg-gray-700 transition"
            onClick={() => toggleDetail(n.id)}
          >
            <p className="text-indigo-300 font-semibold text-sm">{n.title}</p>
            <p className="text-gray-400 text-xs">{n.message}</p>

            {activeId === n.id && (
              <div className="mt-4 p-3 bg-gray-900 border border-gray-700 rounded-lg text-sm">
                <p>
                  <strong>ID:</strong> {n.id}
                </p>
                <p>
                  <strong>Title:</strong> {n.title}
                </p>
                <p>
                  <strong>Message:</strong> {n.message}
                </p>
                <p>
                  <strong>Type:</strong> Transaction (dummy)
                </p>
                <p>
                  <strong>Date:</strong> March 28, 2025 (dummy)
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default NotificationsPage;
