import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/card';
import { Avatar, AvatarImage, AvatarFallback } from '../components/ui/avatar';
import PageWrapper from '../components/PageWrapper';

const ProfilePage: React.FC = () => {
  const username = 'Guest User'; // nanti akan diisi dari login
  const publicKey = localStorage.getItem('public_key') || '';

  return (
    <PageWrapper>
      <div className="flex flex-col items-center justify-center text-center">
        <h1 className="text-3xl font-bold mb-6 text-indigo-400">👤 My Profile</h1>

        <Card className="w-full max-w-md bg-gray-950 border border-gray-800 shadow-lg">
          <CardHeader>
            <CardTitle className="text-indigo-300">User Info</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-center">
              <Avatar className="w-20 h-20 ring-4 ring-indigo-600">
                <AvatarImage src="https://api.dicebear.com/7.x/shapes/svg?seed=neutron" />
                <AvatarFallback>N</AvatarFallback>
              </Avatar>
            </div>
            <p className="text-white font-medium">Username: {username}</p>
            <textarea
              readOnly
              placeholder="No bio yet..."
              className="w-full bg-gray-800 text-white rounded p-3 resize-y min-h-[6rem] font-mono text-sm border border-gray-700"
              defaultValue="Hello! I'm a proud member of the Neutron network."
            ></textarea>

            {publicKey ? (
              <p className="text-green-400 text-sm break-all">Public Key: {publicKey}</p>
            ) : (
              <p className="text-gray-500 text-sm">No public key generated yet.</p>
            )}
          </CardContent>
        </Card>
      </div>
    </PageWrapper>
  );
};

export default ProfilePage;
