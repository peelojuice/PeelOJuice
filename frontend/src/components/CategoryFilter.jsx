export default function CategoryFilter({ categories, selectedCategory, onSelectCategory }) {
  return (
    <div className="w-full overflow-x-auto no-scrollbar pb-4 mb-4">
      <div className="flex px-6 space-x-3 min-w-max">
        <button
          onClick={() => onSelectCategory('all')}
          className={`px-8 py-3 rounded-[18px] font-extrabold text-sm transition-all duration-300 whitespace-nowrap tracking-tight ${
            selectedCategory === 'all'
              ? 'bg-[#1A1A1A] text-white shadow-lg transform scale-105'
              : 'bg-white text-gray-500 hover:bg-gray-50 border-2 border-[#F0F0F0]'
          }`}
        >
          All Juices
        </button>
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => onSelectCategory(category.id)}
            className={`px-8 py-3 rounded-[18px] font-extrabold text-sm transition-all duration-300 whitespace-nowrap tracking-tight ${
              selectedCategory === category.id
                ? 'bg-[#1A1A1A] text-white shadow-lg transform scale-105'
                : 'bg-white text-gray-500 hover:bg-gray-50 border-2 border-[#F0F0F0]'
            }`}
          >
            {category.name}
          </button>
        ))}
      </div>
    </div>
  );
}
