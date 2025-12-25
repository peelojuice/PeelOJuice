import { useEffect } from 'react';

export default function LoadingScreen({ onComplete }) {
  useEffect(() => {
    // Auto-complete after 2 seconds
    const timer = setTimeout(() => {
      onComplete && onComplete();
    }, 2000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className="fixed inset-0 z-50 bg-gradient-to-br from-orange-400 via-pink-400 to-purple-400 flex items-center justify-center">
      {/* Background decorative elements */}
      <div className="absolute inset-0">
        <div className="absolute top-20 left-20 w-32 h-32 bg-yellow-300 rounded-full opacity-30 blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 right-20 w-40 h-40 bg-pink-300 rounded-full opacity-30 blur-3xl animate-pulse animation-delay-500"></div>
      </div>

      {/* Simple bouncing fruits */}
      <div className="relative z-10 flex flex-col items-center">
        <div className="flex gap-4 mb-8">
          <div className="text-4xl animate-bounce">🍊</div>
          <div className="text-4xl animate-bounce animation-delay-200">🍓</div>
          <div className="text-4xl animate-bounce animation-delay-400">🥝</div>
        </div>
        
        <h2 className="text-white text-2xl font-bold drop-shadow-lg">
          Loading...
        </h2>
      </div>
    </div>
  );
}
