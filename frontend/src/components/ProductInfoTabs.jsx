export default function ProductInfoTabs({ nutrition, ingredients, allergenInfo }) {
  return (
    <div className="mt-8">
      <div className="grid lg:grid-cols-[45%_55%] gap-6">
        {/* Left: Nutrition Table */}
        <div className="bg-white rounded-lg border border-gray-200">
          <div className="bg-black text-white px-4 py-2 rounded-t-lg font-semibold">
            Nutrition Facts Per 200 ml*
          </div>
          <table className="w-full">
            <tbody>
              <tr className="border-b border-gray-200">
                <td className="px-4 py-3 text-gray-700">Calories</td>
                <td className="px-4 py-3 text-right font-semibold">{nutrition?.calories || '0'}kcal</td>
              </tr>
              <tr className="border-b border-gray-200">
                <td className="px-4 py-3 text-gray-700">Total Fat</td>
                <td className="px-4 py-3 text-right font-semibold">{nutrition?.total_fat || '0'}g</td>
              </tr>
              <tr className="border-b border-gray-200">
                <td className="px-4 py-3 text-gray-700">Carbohydrate</td>
                <td className="px-4 py-3 text-right font-semibold">{nutrition?.carbohydrate || '0'}g</td>
              </tr>
              <tr className="border-b border-gray-200">
                <td className="px-4 py-3 text-gray-700">Dietary Fiber</td>
                <td className="px-4 py-3 text-right font-semibold">{nutrition?.dietary_fiber || '0'}g</td>
              </tr>
              <tr className="border-b border-gray-200">
                <td className="px-4 py-3 text-gray-700">Total Sugars</td>
                <td className="px-4 py-3 text-right font-semibold">{nutrition?.total_sugars || '0'}g</td>
              </tr>
              <tr>
                <td className="px-4 py-3 text-gray-700">Protein</td>
                <td className="px-4 py-3 text-right font-semibold">{nutrition?.protein || '0'}g</td>
              </tr>
            </tbody>
          </table>
          <div className="px-4 py-2 text-xs text-gray-500 bg-gray-50 rounded-b-lg">
            * Approximate Values
          </div>
        </div>

        {/* Right: Ingredients and Allergen Info */}
        <div className="space-y-4">
          {/* Ingredients */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-bold text-gray-900 mb-3 text-center">Ingredients / Commodities</h3>
            <p className="text-gray-700 text-sm">{ingredients || 'No ingredient information available'}</p>
          </div>

          {/* Allergen Info */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-bold text-gray-900 mb-3 text-center">Allergen Info</h3>
            <p className="text-gray-700 text-sm">{allergenInfo || 'No allergen information available'}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
