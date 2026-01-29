export default function CategoryFilter({ categories, selectedCategory, onSelectCategory }) {
  return (
    <div className="w-full overflow-x-auto no-scrollbar pb-4 mb-4">
      <div className="flex px-6 space-x-3 min-w-max">
        <button
          onClick={() => onSelectCategory('all')}
          className={`px-6 py-2.5 rounded-full font-black text-[10px] uppercase tracking-widest transition-all duration-300 whitespace-nowrap ${
            selectedCategory === 'all'
              ? 'bg-[#FF6B35] text-white shadow-[0_8px_20px_rgba(255,107,53,0.3)]'
              : 'bg-white text-gray-400 border border-[#F0F0F0] hover:border-[#FF6B35]/30'
          }`}
        >
          All Juices
        </button>
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => onSelectCategory(category.id)}
            className={`px-6 py-2.5 rounded-full font-black text-[10px] uppercase tracking-widest transition-all duration-300 whitespace-nowrap ${
              selectedCategory === category.id
                ? 'bg-[#FF6B35] text-white shadow-[0_8px_20px_rgba(255,107,53,0.3)]'
                : 'bg-white text-gray-400 border border-[#F0F0F0] hover:border-[#FF6B35]/30'
            }`}
          >
            {category.name}
          </button>
        ))}
      </div>
    </div>
  );
}
