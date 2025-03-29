import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Bell, Menu, Video, X } from 'lucide-react';
import NotificationModal from '../components/NotificationModal';
import { useNotificationStore } from '../store/useNotificationStore';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const menu = [
    { name: 'Home', path: '/' },
    { name: 'Wallet', path: '/wallet' },
    { name: 'Profile', path: '/profile' },
    { name: 'About', path: '/about' },
    { name: 'Explore', path: '/explore' },
    { name: 'Docs', path: '/docs' },
    { name: 'Login', path: '/login' },
    { name: 'Signup', path: '/signup' },
  ];

  const { openModal, unreadCount } = useNotificationStore();
  const count = unreadCount();

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white flex flex-col">
      {/* Navbar */}
      <header className="sticky top-0 z-50 bg-gray-950 bg-opacity-90 backdrop-blur border-b border-gray-800 shadow-sm">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link to="/" className="text-2xl font-bold text-indigo-400">
              ⚛️ Neutron
            </Link>

            {/* 🔔 Notification Icon */}
            <button
              className="relative text-white hover:text-indigo-400 transition"
              onClick={() => openModal()}
              aria-label="Notifications"
            >
              <Bell className="w-5 h-5 mt-1" />
              {count > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-600 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">
                  {count}
                </span>
              )}
            </button>

            {/* 🎥 Video Icon */}
            <button
              className="text-white hover:text-indigo-400 transition"
              aria-label="Tutorial Videos"
              onClick={() => alert('🎥 Video tutorial feature coming soon!')}
            >
              <Video className="w-5 h-5 mt-1" />
            </button>
          </div>

          {/* Desktop Menu */}
          <nav className="hidden md:flex space-x-4 text-sm font-medium">
            {menu.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className={`hover:text-indigo-400 ${
                  location.pathname === item.path ? 'text-indigo-400 underline' : 'text-white'
                }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button onClick={() => setIsMenuOpen(!isMenuOpen)} aria-label="Toggle Menu">
              {isMenuOpen ? (
                <X className="w-6 h-6 text-white" />
              ) : (
                <Menu className="w-6 h-6 text-white" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Dropdown Menu */}
        {isMenuOpen && (
          <div className="md:hidden px-6 pb-4">
            <nav className="flex flex-col space-y-2">
              {menu.map((item) => (
                <Link
                  key={item.name}
                  to={item.path}
                  onClick={() => setIsMenuOpen(false)}
                  className={`hover:text-indigo-400 ${
                    location.pathname === item.path ? 'text-indigo-400 underline' : 'text-white'
                  }`}
                >
                  {item.name}
                </Link>
              ))}
            </nav>
          </div>
        )}
      </header>
      <NotificationModal />

      {/* Content */}
      <main className="flex-grow container mx-auto px-6 py-10">{children}</main>

      {/* Footer */}
      <footer className="text-center text-sm py-6 text-gray-500 border-t border-gray-800">
        &copy; {new Date().getFullYear()} Neutron. All rights reserved.
      </footer>
    </div>
  );
};

export default Layout;

// <div className="flex items-center gap-6">
//   <Link to="/" className="text-2xl font-bold text-indigo-400">
//     ⚛️ Neutron
//   </Link>

//   {/* Notification Icon */}
//   <button
//     className="text-white hover:text-indigo-400 transition"
//     aria-label="Notifications"
//     onClick={() => alert('🔔 Notification system coming soon!')}
//   >
//     <Bell className="w-5 h-5 mt-1" />
//   </button>
// </div>;
