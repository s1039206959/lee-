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
const contactForm = document.getElementById('contactForm');
const formStatus = document.getElementById('formStatus');
const copyWechatBtn = document.getElementById('copyWechatBtn');
const wechatImageBtn = document.getElementById('wechatImageBtn');
const wechatStatus = document.getElementById('wechatStatus');
const wechatQrBtn = document.getElementById('wechatQrBtn');

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

if (contactForm && formStatus) {
  contactForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    formStatus.className = 'form-status pending';
    formStatus.textContent = '正在提交，请稍候...';

    const formData = new FormData(contactForm);
    const action = contactForm.getAttribute('action');

    try {
      const response = await fetch(action, {
        method: 'POST',
        body: formData,
        headers: { Accept: 'application/json' },
      });

      if (response.ok) {
        formStatus.className = 'form-status success';
        formStatus.textContent = '提交成功！我们已收到您的咨询信息，将尽快与您联系。';
        contactForm.reset();
      } else {
        formStatus.className = 'form-status error';
        formStatus.textContent = '提交失败，请稍后重试或直接发送邮件至 ss1039206959@gmail.com。';
      }
    } catch (error) {
      formStatus.className = 'form-status error';
      formStatus.textContent = '网络异常，提交失败。请检查网络后重试。';
    }
  });
}

const handleWechatCopy = async () => {
  const wechatId = copyWechatBtn?.dataset.wechat || 's1039206959';

  try {
    await navigator.clipboard.writeText(wechatId);
    if (wechatStatus) {
      wechatStatus.className = 'wechat-status success';
      wechatStatus.textContent = '微信号已复制：s1039206959';
    }
  } catch (error) {
    if (wechatStatus) {
      wechatStatus.className = 'wechat-status error';
      wechatStatus.textContent = '复制失败，请手动添加微信号：s1039206959';
    }
  }
};

copyWechatBtn?.addEventListener('click', handleWechatCopy);
wechatImageBtn?.addEventListener('click', handleWechatCopy);

wechatQrBtn?.addEventListener('click', () => {
  wechatQrBtn.classList.add('active');
  setTimeout(() => wechatQrBtn.classList.remove('active'), 220);
});
