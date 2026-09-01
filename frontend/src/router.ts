import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior() {
    return { top: 0 }
  },
  routes: [
    { path: '/', name: 'home', component: () => import('./views/HomeView.vue') },
    { path: '/a-propos', name: 'about', component: () => import('./views/AboutView.vue') },
    { path: '/formations', name: 'programs', component: () => import('./views/ProgramsView.vue') },
    { path: '/formations/:slug', name: 'program', component: () => import('./views/ProgramDetailView.vue') },
    { path: '/calendrier', name: 'calendar', component: () => import('./views/CalendarView.vue') },
    { path: '/entreprises', name: 'enterprise', component: () => import('./views/EnterpriseView.vue') },
    { path: '/actualites', name: 'news', component: () => import('./views/NewsView.vue') },
    { path: '/actualites/:slug', name: 'news-detail', component: () => import('./views/NewsDetailView.vue') },
    { path: '/contact', name: 'contact', component: () => import('./views/ContactView.vue') },
    { path: '/inscription', name: 'enroll', component: () => import('./views/EnrollView.vue') },
    { path: '/confidentialite', name: 'privacy', component: () => import('./views/PrivacyView.vue') },
    { path: '/admin/login', name: 'admin-login', component: () => import('./views/admin/AdminLogin.vue'), meta: { admin: true } },
    {
      path: '/admin',
      component: () => import('./views/admin/AdminLayout.vue'),
      meta: { admin: true, auth: true },
      children: [
        { path: '', name: 'admin-home', component: () => import('./views/admin/AdminHome.vue') },
        { path: 'formations', name: 'admin-programs', component: () => import('./views/admin/AdminPrograms.vue') },
        { path: 'sessions', name: 'admin-sessions', component: () => import('./views/admin/AdminSessions.vue') },
        { path: 'inscriptions', name: 'admin-enrollments', component: () => import('./views/admin/AdminEnrollments.vue') },
        { path: 'actualites', name: 'admin-news', component: () => import('./views/admin/AdminNews.vue') },
        { path: 'temoignages', name: 'admin-testimonials', component: () => import('./views/admin/AdminTestimonials.vue') },
        { path: 'entreprises', name: 'admin-enterprise', component: () => import('./views/admin/AdminEnterprise.vue') },
        { path: 'messages', name: 'admin-messages', component: () => import('./views/admin/AdminMessages.vue') },
        { path: 'parametres', name: 'admin-settings', component: () => import('./views/admin/AdminSettings.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  if (to.meta.auth && !localStorage.getItem('academy_token')) {
    return { name: 'admin-login' }
  }
})

export default router
