import { Link } from 'react-router-dom';

export default function HeroBanner() {
  return (
    <section className="relative bg-gradient-to-br from-pink-200 via-pink-100 to-orange-100 py-20 px-4 overflow-hidden min-h-[600px]">
      {/* Decorative elements */}
      <div className="absolute top-10 left-10 w-32 h-32 bg-red-400 rounded-full opacity-30 blur-3xl"></div>
      <div className="absolute bottom-20 right-20 w-40 h-40 bg-orange-300 rounded-full opacity-20 blur-3xl"></div>
      
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="relative z-10">
            <div className="mb-6">
              <span className="bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-semibold text-gray-700 border border-white/80 shadow-sm inline-block">
                🍹 Fresh Juice Delivered Daily
              </span>
            </div>
            
            <h1 className="text-6xl md:text-7xl font-black leading-tight mb-4">
              <span className="text-gray-900">Get Fresh</span><br/>
              <span className="bg-gradient-to-r from-red-500 via-orange-500 to-red-600 bg-clip-text text-transparent">PeelOJuice</span><br/>
              <span className="text-gray-900">Everyday</span>
            </h1>
            
            <p className="text-gray-700 text-lg mb-6 font-medium">
              100% Natural • No Preservatives • Made Fresh Daily
            </p>
            
            <Link
              to="/menu"
              className="inline-block bg-gradient-to-r from-red-500 to-orange-500 text-white px-8 py-4 rounded-lg font-bold text-lg hover:shadow-xl transition transform hover:scale-105 shadow-lg uppercase tracking-wide"
            >
              Order Now
            </Link>
          </div>

          {/* Right Content - Milkshake Image */}
          <div className="flex-1 flex justify-center items-center relative">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-orange-400/20 to-red-400/20 blur-3xl rounded-full"></div>
              <img 
                src="/hero-milkshake.png" 
                alt="Delicious Milkshake"
                className="relative w-[600px] h-[600px] object-contain drop-shadow-2xl animate-float"
              />
            </div>
          </div>

          {/* Decorative chocolate items */}
          <div className="absolute bottom-10 left-10 text-6xl animate-bounce">🍫</div>
          <div className="absolute top-20 right-10 text-5xl animate-pulse">🍪</div>
          <div className="absolute bottom-32 right-24 text-5xl">🧁</div>
        </div>
      </div>
    </section>
  );
}
