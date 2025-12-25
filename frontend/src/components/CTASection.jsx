import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

export default function CTASection() {
  return (
    <section className="py-20 px-4 bg-gradient-to-br from-orange-50 to-pink-50 relative overflow-hidden">
      <div className="max-w-5xl mx-auto text-center relative z-10">
        <h2 className="text-4xl md:text-5xl font-bold mb-6 text-gray-900">Ready to Get Started?</h2>
        <p className="text-xl text-gray-700 mb-10 max-w-2xl mx-auto">
          Browse our menu and discover your new favorite juice blend!
        </p>
        <Link
          to="/menu"
          className="inline-flex items-center bg-gradient-to-r from-red-500 via-orange-500 to-yellow-500 text-white px-10 py-5 rounded-full text-lg font-bold hover:scale-105 transition transform shadow-2xl"
        >
          Explore Menu <ArrowRight className="ml-2 w-5 h-5" />
        </Link>
      </div>
    </section>
  );
}
