export default function BenefitsPanel({ benefits }) {
  if (!benefits || benefits.length === 0) return null;

  return (
    <div className="bg-gray-50 rounded-xl p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Juice Benefits</h2>
      <div className="space-y-4">
        {benefits.map((benefit, index) => (
          <div key={index} className="border-b border-gray-200 pb-4 last:border-b-0">
            <h3 className="font-bold text-gray-900 mb-1">{benefit.title}</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{benefit.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
