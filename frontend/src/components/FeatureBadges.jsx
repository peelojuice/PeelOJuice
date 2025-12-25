export default function FeatureBadges({ features }) {
  if (!features || features.length === 0) return null;

  // Filter out unwanted features
  const filteredFeatures = features.filter(feature => {
    const lowerFeature = feature.toLowerCase();
    return !lowerFeature.includes('liquid fruit') && 
           !lowerFeature.includes('crunch') &&
           !lowerFeature.includes('glass bottle');
  });

  if (filteredFeatures.length === 0) return null;

  const getIcon = (feature) => {
    const lowerFeature = feature.toLowerCase();
    if (lowerFeature.includes('natural')) return '🌿';
    if (lowerFeature.includes('fresh')) return '🌱';
    if (lowerFeature.includes('sugar')) return '🚫';
    if (lowerFeature.includes('preservative')) return '⚠️';
    return '✓';
  };

  return (
    <div className="flex flex-wrap gap-3 mt-6">
      {filteredFeatures.map((feature, index) => (
        <div
          key={index}
          className="flex items-center gap-2 bg-green-50 border border-green-200 px-4 py-2 rounded-lg"
        >
          <span className="text-lg">{getIcon(feature)}</span>
          <span className="text-sm font-medium text-green-800">{feature}</span>
        </div>
      ))}
    </div>
  );
}
