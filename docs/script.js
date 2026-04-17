const menuBtn = document.getElementById('menuBtn');
const nav = document.getElementById('navMenu');

menuBtn?.addEventListener('click', () => {
  nav?.classList.toggle('open');
});

nav?.querySelectorAll('a').forEach((item) => {
  item.addEventListener('click', () => nav.classList.remove('open'));
});

const counters = document.querySelectorAll('[data-target]');
const revealItems = document.querySelectorAll('.reveal');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');

        if (entry.target.matches('[data-target]')) {
          const target = Number(entry.target.dataset.target);
          let value = 0;
          const step = Math.max(1, Math.ceil(target / 40));
          const timer = setInterval(() => {
            value += step;
            if (value >= target) {
              value = target;
              clearInterval(timer);
            }
            entry.target.textContent = value;
          }, 30);
        }

        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.2 }
);

revealItems.forEach((item) => observer.observe(item));
counters.forEach((counter) => observer.observe(counter));
