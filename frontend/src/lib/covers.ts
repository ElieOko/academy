const bySlug: Record<string, string> = {
  anglais: '/images/gallery-02.jpg',
  'communication-professionnelle': '/images/back-01.jpg',
  'intelligence-artificielle-fondamentale': '/images/back-03.jpg',
  'intelligence-artificielle-avancee': '/images/gallery-03.jpg',
  entrepreneuriat: '/images/back-02.jpg',
  'bureautique-moderne': '/images/gallery-01.jpg',
}

export function programCover(slug: string, imageUrl = '') {
  if (imageUrl && !imageUrl.includes('unsplash')) return imageUrl
  return bySlug[slug] || '/images/back-01.jpg'
}
