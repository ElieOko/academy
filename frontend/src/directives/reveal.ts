import type { Directive } from 'vue'

export const vReveal: Directive<HTMLElement> = {
  mounted(el, binding) {
    el.classList.add('reveal')
    const delay = Number(binding.value ?? 0)
    el.style.animationDelay = `${delay}ms`
    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add('in')
          io.disconnect()
        }
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
    )
    io.observe(el)
  },
}
