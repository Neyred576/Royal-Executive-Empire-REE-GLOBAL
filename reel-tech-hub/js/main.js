/**
 * REEL TECH HUB — Interactive Web Experience Engine
 * Theme: Deep Space Dark | Cyan & Gold | Modern 3D Tech
 */

document.addEventListener('DOMContentLoaded', () => {

  // 1. PRELOADER DISMISSAL
  const preloader = document.getElementById('preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        preloader.classList.add('done');
      }, 700);
    });
    // Fallback if window load already fired
    setTimeout(() => {
      preloader.classList.add('done');
    }, 1800);
  }

  // 2. STICKY NAV & ACTIVE LINKS
  const nav = document.getElementById('mainNav');
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id]');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }

    // Active link highlighting
    let current = '';
    const scrollPos = window.scrollY + 140;
    sections.forEach(sec => {
      if (scrollPos >= sec.offsetTop && scrollPos < sec.offsetTop + sec.offsetHeight) {
        current = sec.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });

    // Scroll to Top Button Visibility
    const scrollBtn = document.getElementById('scrollTopBtn');
    if (scrollBtn) {
      if (window.scrollY > 600) {
        scrollBtn.classList.add('show');
      } else {
        scrollBtn.classList.remove('show');
      }
    }
  }, { passive: true });

  // Scroll to top click
  const scrollBtn = document.getElementById('scrollTopBtn');
  if (scrollBtn) {
    scrollBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // 3. MOBILE NAVIGATION TOGGLE
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navLinks');
  const navOverlay = document.getElementById('navOverlay');

  if (navToggle && navMenu && navOverlay) {
    const toggleMenu = () => {
      navToggle.classList.toggle('open');
      navMenu.classList.toggle('open');
      navOverlay.classList.toggle('show');
      document.body.style.overflow = navMenu.classList.contains('open') ? 'hidden' : '';
    };

    navToggle.addEventListener('click', toggleMenu);
    navOverlay.addEventListener('click', toggleMenu);

    navMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        if (navMenu.classList.contains('open')) toggleMenu();
      });
    });
  }

  // 4. INTERACTIVE 3D PARTICLE NETWORK CANVAS (HERO - OPTIMIZED)
  const canvas = document.getElementById('particle-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];
    let mouse = { x: null, y: null, radius: 120 };
    let animationFrameId = null;
    let isHeroVisible = true;

    const resizeCanvas = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = canvas.parentElement.offsetHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    window.addEventListener('mousemove', (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
    }, { passive: true });

    window.addEventListener('mouseleave', () => {
      mouse.x = null;
      mouse.y = null;
    });

    class Particle {
      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.radius = Math.random() * 2 + 1.2;
        this.color = Math.random() > 0.35 ? 'rgba(0, 212, 255, 0.85)' : 'rgba(212, 175, 55, 0.85)';
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > width) this.vx *= -1;
        if (this.y < 0 || this.y > height) this.vy *= -1;

        if (mouse.x !== null && mouse.y !== null) {
          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < mouse.radius && dist > 0) {
            const force = (mouse.radius - dist) / mouse.radius;
            this.x -= (dx / dist) * force * 2.5;
            this.y -= (dy / dist) * force * 2.5;
          }
        }
      }

      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
      }
    }

    const count = Math.min(Math.floor(window.innerWidth / 30), 45);
    particles = Array.from({ length: count }, () => new Particle());

    const animateParticles = () => {
      if (!isHeroVisible) return;
      ctx.clearRect(0, 0, width, height);

      const pLen = particles.length;
      for (let i = 0; i < pLen; i++) {
        particles[i].update();
        particles[i].draw();

        for (let j = i + 1; j < pLen; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 100) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            const alpha = 1 - (dist / 100);
            ctx.strokeStyle = `rgba(0, 212, 255, ${alpha * 0.18})`;
            ctx.lineWidth = 0.7;
            ctx.stroke();
          }
        }
      }
      animationFrameId = requestAnimationFrame(animateParticles);
    };

    // Pause canvas animation when scrolled away to guarantee 60fps across the site
    const heroObserver = new IntersectionObserver((entries) => {
      isHeroVisible = entries[0].isIntersecting;
      if (isHeroVisible) {
        if (!animationFrameId) animateParticles();
      } else {
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
          animationFrameId = null;
        }
      }
    }, { threshold: 0.05 });

    const heroSec = document.getElementById('hero');
    if (heroSec) heroObserver.observe(heroSec);
    animateParticles();
  }

  // 5. 3D TILT EFFECT ON CARDS
  const tiltCards = document.querySelectorAll('.product-card, .service-card');
  tiltCards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      const rotX = (y / (rect.height / 2)) * -6;
      const rotY = (x / (rect.width / 2)) * 6;
      card.style.transform = `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-6px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  // 6. SCROLL REVEAL OBSERVER
  const revealElements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');
  const revealObserver = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  revealElements.forEach(el => revealObserver.observe(el));

  // 7. RETURN TO MAIN EMPIRE PORTAL
  window.goToMainEmpire = function() {
    if (window.location.protocol === 'file:') {
      window.location.href = '../Royal Exercutive Empire/Test/Web/index.html';
    } else if (window.location.port === '5500') {
      window.location.href = 'http://localhost:8080/';
    } else {
      window.location.href = '../index.html';
    }
  };

  // 8. HARDWARE PRODUCT FILTER TABS
  const filterTabs = document.querySelectorAll('.ptab');
  const productCards = document.querySelectorAll('.product-card');

  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      filterTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filter = tab.getAttribute('data-filter');
      productCards.forEach(card => {
        const cat = card.getAttribute('data-category');
        if (filter === 'all' || cat === filter) {
          card.style.display = 'block';
          setTimeout(() => { card.style.opacity = '1'; card.style.transform = ''; }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.95)';
          setTimeout(() => { card.style.display = 'none'; }, 200);
        }
      });
    });
  });

  // 9. QUOTE MODAL SYSTEM
  const quoteModalOverlay = document.getElementById('quoteModalOverlay');
  const quoteModalClose = document.getElementById('quoteModalClose');
  const modalProductName = document.getElementById('modalProductName');
  const modalProductCategory = document.getElementById('modalProductCategory');

  window.openQuoteModal = (productName, category) => {
    if (modalProductName) modalProductName.innerText = productName;
    if (modalProductCategory) modalProductCategory.innerText = category;
    if (quoteModalOverlay) quoteModalOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  const closeModal = () => {
    if (quoteModalOverlay) quoteModalOverlay.classList.remove('open');
    document.body.style.overflow = '';
  };

  if (quoteModalClose) quoteModalClose.addEventListener('click', closeModal);
  if (quoteModalOverlay) {
    quoteModalOverlay.addEventListener('click', (e) => {
      if (e.target === quoteModalOverlay) closeModal();
    });
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && quoteModalOverlay && quoteModalOverlay.classList.contains('open')) {
      closeModal();
    }
  });

  window.submitModalQuote = () => {
    const prod = modalProductName ? modalProductName.innerText : 'Hardware';
    const qty = document.getElementById('modalQty').value;
    const name = document.getElementById('modalName').value;
    const contact = document.getElementById('modalContact').value;
    const os = document.getElementById('modalOS').value;

    const message = `REEL Tech Hub Request Received!\n\nSystem: ${prod}\nQuantity: ${qty}\nClient: ${name}\nContact: ${contact}\nOS: ${os}\n\nOur hardware lead will contact you within 2 business hours.`;
    alert(message);
    closeModal();
  };

  // 10. CONTACT FORM HANDLER
  window.handleProcurementSubmit = () => {
    const name = document.getElementById('contactName').value;
    const email = document.getElementById('contactEmail').value;
    const need = document.getElementById('contactNeed').value;

    const msg = `Thank you, ${name}!\n\nYour message regarding "${need}" has been sent to REEL Tech Hub.\n\nOur team will respond promptly to ${email} or via WhatsApp.`;
    alert(msg);
    document.getElementById('procurementForm').reset();
  };

});
