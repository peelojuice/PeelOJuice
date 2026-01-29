import { Sparkles, Zap, Heart } from 'lucide-react';

export default function WhyChooseSection() {
  return (
    <section className="py-20 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-4xl md:text-5xl font-bold text-center mb-4 text-gray-900">
          Why Choose <span className="bg-gradient-to-r from-red-500 via-orange-500 to-yellow-500 bg-clip-text text-transparent">Peel'O'Juice</span>?
        </h2>
        <p className="text-center text-gray-600 mb-16 text-lg">Experience the difference with every sip</p>
        
        <div className="grid md:grid-cols-3 gap-8">
          {/* Fresh Card */}
          <div className="group text-center p-8 rounded-3xl bg-gradient-to-br from-orange-50 to-yellow-50 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-orange-200">
            <div className="w-20 h-20 bg-gradient-to-br from-orange-400 to-yellow-400 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
              <Sparkles className="w-10 h-10 text-white" />
            </div>
            <h3 className="text-2xl font-bold mb-3 text-gray-800">100% Fresh</h3>
            <p className="text-gray-700 leading-relaxed">Made fresh daily with premium fruits sourced from local farms</p>
          </div>
          
          {/* Fast Delivery */}
          <div className="group text-center p-8 rounded-3xl bg-gradient-to-br from-red-50 to-pink-50 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-red-200">
            <div className="w-20 h-20 bg-gradient-to-br from-red-500 to-pink-500 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
              <Zap className="w-10 h-10 text-white" />
            </div>
            <h3 className="text-2xl font-bold mb-3 text-gray-800">Fast Delivery</h3>
            <p className="text-gray-700 leading-relaxed">Get your juice delivered fresh within 30 minutes</p>
          </div>
          
          {/* Healthy Choice */}
          <div className="group text-center p-8 rounded-3xl bg-gradient-to-br from-green-50 to-emerald-50 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-green-200">
            <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
              <Heart className="w-10 h-10 text-white" />
            </div>
            <h3 className="text-2xl font-bold mb-3 text-gray-800">Healthy Choice</h3>
            <p className="text-gray-700 leading-relaxed">No added sugar or preservatives, pure natural goodness</p>
          </div>
        </div>
      </div>
    </section>
  );
}
