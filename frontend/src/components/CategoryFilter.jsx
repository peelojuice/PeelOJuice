export default function CategoryFilter({ categories, selectedCategory, onSelectCategory }) {
  return (
    <div className="flex flex-wrap justify-center gap-3 mb-12 px-4">
      <button
        onClick={() => onSelectCategory('all')}
        className={`px-6 py-2.5 rounded-lg font-medium transition-all duration-300 whitespace-nowrap ${
          selectedCategory === 'all'
            ? 'bg-black text-white shadow-md'
            : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
        }`}
      >
        All Juices
      </button>
      {categories.map(category => (
        <button
          key={category.id}
          onClick={() => onSelectCategory(category.id)}
          className={`px-6 py-2.5 rounded-lg font-medium transition-all duration-300 whitespace-nowrap ${
            selectedCategory === category.id
              ? 'bg-black text-white shadow-md'
              : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
          }`}
        >
          {category.name}
        </button>
      ))}
    </div>
  );
}
