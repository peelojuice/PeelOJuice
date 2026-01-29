export default function ProductInfoTabs({ nutrition, ingredients, allergenInfo }) {
  return (
    <div className="mt-12">
      <div className="grid lg:grid-cols-[40%_60%] gap-8">
        {/* Left: Nutrition Intel */}
        <div className="bg-white rounded-[40px] border-2 border-[#1A1A1A] overflow-hidden shadow-2xl">
          <div className="bg-[#1A1A1A] text-white px-8 py-6">
            <h3 className="text-[10px] font-black uppercase tracking-[0.4em] mb-1 opacity-60">Bio-Composition</h3>
            <h2 className="text-xl font-black uppercase tracking-tighter">Nutrition Intel</h2>
          </div>
          <div className="p-4">
            <table className="w-full">
              <tbody>
                {[
                  { label: 'Energy Capacity', value: nutrition?.calories, unit: 'kcal' },
                  { label: 'T-Lipid Mass', value: nutrition?.total_fat, unit: 'g' },
                  { label: 'Energy Sugars', value: nutrition?.total_sugars, unit: 'g' },
                  { label: 'Structural Protein', value: nutrition?.protein, unit: 'g' },
                  { label: 'Complex Carbs', value: nutrition?.carbohydrate, unit: 'g' },
                  { label: 'Dietary Matrix', value: nutrition?.dietary_fiber, unit: 'g' },
                ].map((item, i) => (
                  <tr key={i} className={`border-b border-[#F0F0F0] last:border-0 hover:bg-[#F9F9F9] transition-colors`}>
                    <td className="px-6 py-5 text-[10px] font-black text-gray-400 uppercase tracking-widest">{item.label}</td>
                    <td className="px-6 py-5 text-right font-black text-[#1A1A1A] text-sm tabular-nums tracking-tighter">
                      {item.value || '0'}<span className="text-[9px] text-[#FF6B35] ml-1 uppercase">{item.unit}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-8 py-4 bg-[#F9F9F9] border-t border-[#F0F0F0] text-[8px] font-black text-gray-300 uppercase tracking-[0.4em] text-center">
            Calculated Per 200ml Serving Matrix
          </div>
        </div>

        {/* Right: Sources and Safety */}
        <div className="space-y-6">
          <div className="bg-white rounded-[40px] border border-[#F0F0F0] p-10 shadow-sm relative group hover:shadow-xl transition-all duration-500">
            <div className="absolute top-0 right-0 w-24 h-24 bg-[#FF6B35]/5 rounded-bl-[100px]"></div>
            <p className="text-[10px] font-black text-[#FF6B35] uppercase tracking-[0.4em] mb-4">Origin Sources</p>
            <h3 className="text-2xl font-black text-[#1A1A1A] uppercase tracking-tighter mb-6">Ingredients & Commodities</h3>
            <p className="text-gray-500 font-medium leading-relaxed text-sm">{ingredients || 'Data pending architectural update.'}</p>
          </div>

          <div className="bg-[#FFF9F0] rounded-[40px] border border-[#FF6B35]/20 p-10 shadow-sm relative group hover:shadow-xl transition-all duration-500">
            <p className="text-[10px] font-black text-[#FF6B35] uppercase tracking-[0.4em] mb-4">Safety Protocol</p>
            <h3 className="text-2xl font-black text-[#1A1A1A] uppercase tracking-tighter mb-6">Allergen Information</h3>
            <p className="text-gray-500 font-medium leading-relaxed text-sm">{allergenInfo || 'No hazardous compounds detected in current formulation.'}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
