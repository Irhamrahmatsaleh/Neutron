import React, { useState, useEffect } from 'react';
import { Avatar, AvatarFallback, AvatarImage } from '../components/ui/avatar';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Alert } from '../components/ui/alert';

const WalletPage: React.FC = () => {
  const [wallet, setWallet] = useState<{ private_key: string; public_key: string } | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const pub = localStorage.getItem('public_key');
    if (pub && !wallet) {
      setWallet({ private_key: '', public_key: pub });
    }
  }, []);

  const generateWallet = async () => {
    setLoading(true);
    try {
      const res = await fetch('http://127.0.0.1:8000/wallet/generate');
      const data = await res.json();
      setWallet({ private_key: data.private_key, public_key: data.public_key });
      localStorage.setItem('public_key', data.public_key);
    } catch (error) {
      alert('Failed to generate wallet.');
    }
    setLoading(false);
  };

  const copyToClipboard = async (text: string) => {
    await navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-center">🚀 Neutron Wallet Generator</h1>
      <div className="flex flex-col items-center justify-center mb-12">
        <Avatar className="w-24 h-24 mb-4 ring-4 ring-indigo-600">
          <AvatarImage
            src="https://api.dicebear.com/7.x/identicon/svg?seed=neutron"
            alt="Wallet Avatar"
          />
          <AvatarFallback>NTR</AvatarFallback>
        </Avatar>
        <p className="text-gray-400 max-w-md text-center">
          This wallet generator creates a brand new cryptographic identity. Store your private key
          securely and never share it with anyone.
        </p>
      </div>

      {!wallet && (
        <div className="flex justify-center mb-8">
          <button
            onClick={generateWallet}
            disabled={loading}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"
          >
            {loading ? 'Generating...' : 'Generate New Wallet'}
          </button>
        </div>
      )}

      {wallet && (
        <>
          <Alert className="bg-yellow-900 text-yellow-200 border-yellow-800 mb-6 max-w-3xl mx-auto text-sm shadow-lg">
            ⚠️ Important: Your private key is shown only once. Save it securely. If you lose it,
            your wallet and assets cannot be recovered.
          </Alert>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl mx-auto">
            <Card className="bg-black text-white border border-gray-800 shadow-xl">
              <CardHeader>
                <CardTitle className="text-green-400 text-lg">🔐 Private Key</CardTitle>
              </CardHeader>
              <CardContent>
                <textarea
                  readOnly
                  className="w-full bg-gray-800 text-green-400 p-3 rounded font-mono text-sm resize-y whitespace-pre overflow-auto min-h-[12rem]"
                  value={wallet.private_key}
                />

                <button
                  onClick={() => copyToClipboard(wallet.private_key)}
                  className="mt-3 bg-green-600 hover:bg-green-700 px-4 py-2 rounded text-white w-full"
                >
                  Copy Private Key
                </button>
              </CardContent>
            </Card>

            <Card className="bg-black text-white border border-gray-800 shadow-xl">
              <CardHeader>
                <CardTitle className="text-blue-400 text-lg">📬 Public Key</CardTitle>
              </CardHeader>
              <CardContent>
                <textarea
                  readOnly
                  className="w-full bg-gray-800 text-blue-400 p-3 rounded font-mono text-sm resize-y whitespace-pre overflow-auto min-h-[12rem]"
                  value={wallet.public_key}
                />

                <button
                  onClick={() => copyToClipboard(wallet.public_key)}
                  className="mt-3 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white w-full"
                >
                  Copy Public Key
                </button>
              </CardContent>
            </Card>
          </div>
        </>
      )}

      {wallet && wallet.private_key === '' && (
        <div className="max-w-xl mx-auto text-center space-y-6">
          {/* <Avatar className="w-20 h-20 mx-auto ring-4 ring-indigo-500">
            <AvatarImage
              src={`https://api.dicebear.com/7.x/identicon/svg?seed=${wallet.public_key}`}
            />
            <AvatarFallback>NTR</AvatarFallback>
          </Avatar> */}
          <p></p>
          <p></p>
          <p className="text-lg text-gray-300 font-medium">🪪 Your wallet is ready.</p>

          <p className="text-sm text-gray-400">
            You already created a wallet. You can view your public key on your profile page.
          </p>

          <p className="text-sm text-gray-500 italic">
            Private key was shown only once and never stored.
          </p>
        </div>
      )}
    </div>
  );
};

export default WalletPage;
