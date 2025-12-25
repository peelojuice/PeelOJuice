import { Link } from 'react-router-dom';

export default function FeatureBanner({ 
  title, 
  titleHighlight, 
  description, 
  buttonText, 
  badgeText, 
  badgeIcon,
  imageSrc, 
  imageAlt, 
  imagePosition = 'right',
  bgGradient,
  decorativeIcons = []
}) {
  const isImageRight = imagePosition === 'right';
  
  // Content section
  const ContentSection = () => (
    <div className="animate-on-scroll slide-in-left">
      <div className="mb-4">
        <span className={`${bgGradient} text-white px-4 py-2 rounded-full text-sm font-bold inline-block shadow-lg`}>
          {badgeIcon} {badgeText}
        </span>
      </div>
      <h2 className="text-5xl md:text-6xl font-black mb-6">
        <span className="text-gray-900">{title}</span>{' '}
        <span className={`${bgGradient} bg-clip-text text-transparent`}>{titleHighlight}</span>
      </h2>
      <p className="text-xl text-gray-700 mb-6 leading-relaxed">
        {description}
      </p>
      <Link
        to="/menu"
        className={`inline-block ${bgGradient} text-white px-8 py-4 rounded-full font-bold text-lg hover:shadow-2xl transition transform hover:scale-105`}
      >
        {buttonText}
      </Link>
    </div>
  );

  // Image section
  const ImageSection = () => (
    <div className={`animate-on-scroll ${isImageRight ? 'slide-in-right' : 'slide-in-left'} flex justify-center relative ${!isImageRight ? 'order-2 md:order-1' : ''}`}>
      <div className="relative">
        <div className={`absolute inset-0 ${bgGradient.replace('bg-gradient-to-r', 'bg-gradient-to-r')}/30 blur-3xl rounded-full`}></div>
        <img
          src={imageSrc}
          alt={imageAlt}
          className="relative w-[600px] h-[600px] object-contain drop-shadow-2xl animate-float-slow"
        />
      </div>
      {/* Decorative icons */}
      {decorativeIcons.map((icon, index) => (
        <div key={index} className={icon.className}>{icon.emoji}</div>
      ))}
    </div>
  );

  return (
    <section className={`py-20 px-4 ${bgGradient.replace('bg-gradient-to-r', 'bg-gradient-to-br')} overflow-hidden`}>
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {isImageRight ? (
            <>
              <ContentSection />
              <ImageSection />
            </>
          ) : (
            <>
              <ImageSection />
              <div className={`animate-on-scroll slide-in-right order-1 md:order-2`}>
                <ContentSection />
              </div>
            </>
          )}
        </div>
      </div>
    </section>
  );
}


