import React from 'react';
import TxDetailModal from '../components/TxDetailModal';

interface PageWrapperProps {
  children: React.ReactNode;
}

const PageWrapper: React.FC<PageWrapperProps> = ({ children }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
      {/* Left Sidebar (hidden on mobile) */}
      <aside className="hidden lg:flex lg:col-span-3 flex-col space-y-6">
        {/* Judul Balance */}
        <h2 className="text-indigo-300 text-base font-semibold pl-1">🪙 Balance</h2>
        {/* Box Balance */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 shadow-md">
          <p className="text-white text-2xl font-bold mb-2">23.000 NTR</p>
          <p className="text-sm text-gray-400">≈ $10,560 USD</p>
        </div>

        {/* Judul Transaction History */}
        <h2 className="text-indigo-300 text-base font-semibold pl-1">🧾 Transaction History</h2>
        {/* Box Transaction List */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 shadow-md flex-grow">
          <div className="flex flex-col space-y-4 text-sm">
            <TxDetailModal
              title="Transaction #1"
              from="0xNeutron123"
              to="0xabc...123"
              amount="1.0"
              date="2025-03-28"
              triggerLabel="➡️ Sent 1.0 NTR to 0xabc...123"
            />
            <TxDetailModal
              title="Transaction #2"
              from="0xdef...456"
              to="0xNeutron123"
              amount="2.5"
              date="2025-03-27"
              triggerLabel="⬅️ Received 2.5 NTR from 0xdef...456"
            />
            <TxDetailModal
              title="Transaction #3"
              from="0xNeutron123"
              to="0x999...zzz"
              amount="0.75"
              date="2025-03-26"
              triggerLabel="➡️ Sent 0.75 NTR to 0x999...zzz"
            />
            <TxDetailModal
              title="Transaction #4"
              from="0xaaa...111"
              to="0xNeutron123"
              amount="3.25"
              date="2025-03-25"
              triggerLabel="⬅️ Received 3.25 NTR from 0xaaa...111"
            />
            <TxDetailModal
              title="Transaction #5"
              from="0xNeutron123"
              to="0xwalletxyz"
              amount="5.0"
              date="2025-03-24"
              triggerLabel="➡️ Sent 5.0 NTR to 0xwalletxyz"
            />
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="col-span-1 lg:col-span-8">{children}</main>

      {/* Right Sidebar (hidden on mobile) */}
      <aside className="hidden lg:block lg:col-span-2">
        {/* Future: Blockchain Stats, Quotes, etc */}
      </aside>
    </div>
  );
};

export default PageWrapper;
