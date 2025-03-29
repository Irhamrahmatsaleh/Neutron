import React from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
  return (
    <>
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute top-0 left-0 w-full h-full object-cover opacity-20 z-0"
      >
        <source src="/videos/video.mp4" type="video/mp4" />
      </video>
      {/* <img
        src="/images/image.jpg"
        alt="Background Image"
        className="absolute top-0 left-0 w-full h-full object-cover opacity-20 z-0"
      /> */}

      <div className="flex flex-col min-h-screen bg-gradient-to-b from-black via-gray-900 to-black text-white">
        <main className="relative flex-grow container mx-auto px-4 py-20 flex flex-col items-center justify-center text-center z-10">
          <h1 className="text-5xl font-extrabold mb-6 text-indigo-400 drop-shadow-md">
            🚀 Welcome to Neutron
          </h1>
          <p className="text-gray-400 text-lg mb-10 max-w-xl">
            Revolutionizing decentralized finance with elegance, power, and simplicity.
          </p>

          <Card className="w-full max-w-md bg-gray-950 border-gray-800 shadow-2xl">
            <CardHeader>
              <CardTitle className="text-indigo-300 text-2xl">Start your journey</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-400 mb-4">
                Generate your wallet to enter the Neutron ecosystem.
              </p>
              <Link to="/wallet">
                <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
                  Generate Wallet
                </Button>
              </Link>
            </CardContent>
          </Card>
        </main>
      </div>
    </>
  );
};

export default HomePage;
