import { motion } from 'motion/react';
import { useLanguage } from '../contexts/LanguageContext';
import { useInView } from 'motion/react';
import { useRef } from 'react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { ArrowUpRight } from 'lucide-react';
import usePortfolio from '../api/hooks/usePortfolio';

type ProjectType = {
  id: number
  image: string
  field_ru: string
  field_uz: string
  field_en: string
  title_ru: string
  title_uz: string
  title_en: string
  link: string
  created_at: string
  updated_at: string
}

export const Portfolio = () => {
  const { t, language } = useLanguage();
  const ref = useRef(null);
  const isInView = useInView(ref, { once: false, margin: "-50px", amount: 0.2 });

  const { getPortfolio } = usePortfolio();
  const { data: projects } = getPortfolio();


  const handleLanguageTitle = ({ title_ru, title_uz, title_en}: { title_ru: string, title_uz: string, title_en: string }) => {
    switch (language) {
      case 'ru':
        return title_ru;
      case 'uz':
        return title_uz;
      case 'en':
        return title_en;
      default:
        return title_en;
    }
  }

  const handleLanguageField = ({ field_ru, field_uz, field_en }: { field_ru: string, field_uz: string, field_en: string }) => {
    switch (language) {
      case 'ru':
        return field_ru;
      case 'uz':
        return field_uz;
      case 'en':
        return field_en;
      default:
        return field_en;
    }
  }

  return (
    <section id="portfolio" className="py-32 bg-gray-50 relative overflow-hidden" ref={ref}>
      {/* Ultra subtle texture */}
      <div className="absolute inset-0 opacity-[0.015]" style={{
        backgroundImage: `radial-gradient(circle at 1px 1px, black 1px, transparent 0)`,
        backgroundSize: '40px 40px'
      }} />
      
      <div className="max-w-7xl mx-auto px-6 lg:px-8 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
          transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
          className="text-center mb-20"
        >
          <div className="inline-flex items-center gap-2 mb-8">
            <div className="w-12 h-[1px] bg-gradient-to-r from-transparent via-gray-300 to-transparent" />
            <span className="text-xs uppercase tracking-[0.3em] text-gray-400">
              {t('language') === 'uz' ? 'Portfolio' : t('language') === 'ru' ? 'Портфолио' : 'Portfolio'}
            </span>
            <div className="w-12 h-[1px] bg-gradient-to-r from-transparent via-gray-300 to-transparent" />
          </div>
          <h2 className="mb-6" style={{ fontWeight: 300, fontSize: 'clamp(2rem, 5vw, 3rem)' }}>{t('portfolio.title')}</h2>
          <p className="text-gray-600 max-w-2xl mx-auto leading-loose" style={{ fontWeight: 300 }}>
            {t('portfolio.subtitle')}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects?.map((project: ProjectType, index: number) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
              transition={{ duration: 0.8, delay: index * 0.08, ease: [0.16, 1, 0.3, 1] }}
              className="group cursor-pointer"
            >
              <div className="relative overflow-hidden rounded-3xl bg-white border border-gray-100 hover:border-gray-200 hover:shadow-2xl transition-all duration-500">
                <div className="relative overflow-hidden aspect-[4/3]">
                  <ImageWithFallback
                    src={project.image}
                    alt={handleLanguageTitle({ title_ru: project.title_ru, title_uz: project.title_uz, title_en: project.title_en })}
                    className="w-full h-full object-cover transition-all duration-700 group-hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  
                  {/* Hover content */}
                  <div className="absolute inset-0 flex items-end p-6 opacity-0 group-hover:opacity-100 transition-all duration-500">
                    <div className="transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                      <div className="text-xs text-white/80 mb-2 tracking-wide" style={{ fontWeight: 400 }}>
                        {handleLanguageField({ field_ru: project.field_ru, field_uz: project.field_uz, field_en: project.field_en })}
                      </div>
                      <h3 className="text-white flex items-center gap-2" style={{ fontSize: '1.125rem', fontWeight: 500 }}>
                        {handleLanguageTitle({ title_ru: project.title_ru, title_uz: project.title_uz, title_en: project.title_en })}
                        <ArrowUpRight className="w-4 h-4" strokeWidth={2} />
                      </h3>
                    </div>
                  </div>
                </div>
                
                <div className="p-6">
                  <div className="text-xs text-gray-500 mb-2 tracking-wide" style={{ fontWeight: 400 }}>
                    {handleLanguageField({ field_ru: project.field_ru, field_uz: project.field_uz, field_en: project.field_en })}
                  </div>
                  <h3 className="text-gray-900 group-hover:text-black transition-colors" style={{ fontSize: '1.125rem', fontWeight: 500 }}>
                    {handleLanguageTitle({ title_ru: project.title_ru, title_uz: project.title_uz, title_en: project.title_en })}
                  </h3>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};