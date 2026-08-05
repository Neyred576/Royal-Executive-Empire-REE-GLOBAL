/**
 * ====================================================================
 * REEL — ROYALTY EXECUTIVE EMPIRE LIMITED
 * Main Application Logic
 * ====================================================================
 */

document.addEventListener('DOMContentLoaded', () => {

  // 1. PRELOADER
  const preloader = document.getElementById('preloader');
  const body = document.body;
  body.classList.add('no-scroll');

  // Wait for the window to fully load for a snappy, precise preloader
  if (preloader) {
    const hidePreloader = () => {
      if (preloader.classList.contains('done')) return;
      preloader.classList.add('done');
      body.classList.remove('no-scroll');
      initHeroAnimations();
    };

    if (document.readyState === 'complete') {
      setTimeout(hidePreloader, 400);
    } else {
      window.addEventListener('load', () => setTimeout(hidePreloader, 400));
      // Fallback in case loading gets stuck (max 1.5s wait)
      setTimeout(hidePreloader, 1500);
    }
  } else {
    // No preloader on this page — show content immediately
    body.classList.remove('no-scroll');
    initHeroAnimations();
  }

  // 2. COOKIE CONSENT
  const cookieBanner = document.getElementById('cookie-consent');
  const btnAccept = document.getElementById('cookie-accept');
  const btnDecline = document.getElementById('cookie-decline');

  try {
    if (cookieBanner && !localStorage.getItem('ree_cookie_consent')) {
      setTimeout(() => {
        cookieBanner.classList.add('show');
      }, 3500);
    }
  } catch (e) {
    console.warn("Local storage unavailable", e);
  }

  if (btnAccept) {
    btnAccept.addEventListener('click', () => {
      try { localStorage.setItem('ree_cookie_consent', 'accepted'); } catch (e) { }
      if (cookieBanner) cookieBanner.classList.remove('show');
      // After cookie consent, show the install app modal
      setTimeout(() => {
        if (typeof showInstallPromotion === 'function') showInstallPromotion();
      }, 600);
    });
  }

  if (btnDecline) {
    btnDecline.addEventListener('click', () => {
      try { localStorage.setItem('ree_cookie_consent', 'declined'); } catch (e) { }
      if (cookieBanner) cookieBanner.classList.remove('show');
    });
  }

  // 3. NAVIGATION HEADER
  const mainNav = document.getElementById('main-nav');
  const scrollTopBtn = document.getElementById('scroll-top-btn');

  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    // Header Blur
    if (mainNav) {
      if (y > 50) {
        mainNav.classList.add('scrolled');
      } else {
        mainNav.classList.remove('scrolled');
      }
    }
    // Scroll To Top Button
    if (scrollTopBtn) {
      if (y > 600) {
        scrollTopBtn.classList.add('show');
      } else {
        scrollTopBtn.classList.remove('show');
      }
    }
  }, { passive: true });

  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // 4. MOBILE MENU
  const hamburger = document.getElementById('nav-hamburger');
  const navLinks = document.getElementById('nav-links');
  const navOverlay = document.getElementById('nav-overlay');

  const toggleMenu = () => {
    if (!hamburger || !navLinks || !navOverlay) return;
    const isOpen = hamburger.classList.contains('open');
    if (isOpen) {
      hamburger.classList.remove('open');
      navLinks.classList.remove('open');
      navOverlay.classList.remove('show');
      hamburger.setAttribute('aria-expanded', 'false');
      body.classList.remove('no-scroll');
    } else {
      hamburger.classList.add('open');
      navLinks.classList.add('open');
      navOverlay.classList.add('show');
      hamburger.setAttribute('aria-expanded', 'true');
      body.classList.add('no-scroll');
    }
  };

  if (hamburger) hamburger.addEventListener('click', toggleMenu);
  if (navOverlay) navOverlay.addEventListener('click', toggleMenu);

  // Close menu on link click
  if (navLinks && hamburger) {
    navLinks.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        if (hamburger.classList.contains('open')) {
          toggleMenu();
        }
      });
    });
  }

  // Swipe Gestures for Mobile Menu
  let touchStartX = 0;
  let touchEndX = 0;

  const handleSwipe = () => {
    if (window.innerWidth > 992) return; // Only handle on mobile
    if (!hamburger) return;

    const swipeDist = touchEndX - touchStartX;
    const minSwipe = 60; // Minimum distance to be considered a swipe
    const isOpen = hamburger.classList.contains('open');

    // Swipe Left (pulling from the right edge)
    if (swipeDist < -minSwipe && !isOpen) {
      toggleMenu();
    }
    // Swipe Right (pushing back to the right edge)
    else if (swipeDist > minSwipe && isOpen) {
      toggleMenu();
    }
    // Fallback: If they swipe right from the left edge and it's closed, open it anyway (user request)
    else if (swipeDist > minSwipe && !isOpen && touchStartX < 50) {
      toggleMenu();
    }
  };

  document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, { passive: true });


  // 5. ACTIVE LINK HIGHLIGHTING
  const navItems = document.querySelectorAll('.nav-link');
  let currentUrl = window.location.pathname.split('/').pop() || 'index.html';

  navItems.forEach(link => {
    link.classList.remove('active');
    const href = link.getAttribute('href');
    if (href && (href === currentUrl || (currentUrl === '' && href === 'index.html'))) {
      link.classList.add('active');
    }
  });

  // Mobile Dropdown Toggle
  const dropdownToggles = document.querySelectorAll('.nav-item-dropdown > .nav-link');
  dropdownToggles.forEach(toggle => {
    toggle.addEventListener('click', (e) => {
      if (window.innerWidth <= 768) {
        e.preventDefault();
        const dropdown = toggle.nextElementSibling;
        if (dropdown.style.visibility === 'visible') {
          dropdown.style.visibility = 'hidden';
          dropdown.style.opacity = '0';
          dropdown.style.transform = 'translateY(10px)';
        } else {
          dropdown.style.visibility = 'visible';
          dropdown.style.opacity = '1';
          dropdown.style.transform = 'translateY(0)';
        }
      }
    });
  });

  // 5.5 CUSTOM CURSOR LOGIC
  const cursorDot = document.getElementById('cursor-dot');
  const cursorRing = document.getElementById('cursor-ring');

  if (cursorDot && cursorRing) {
    // Hide custom cursor elements
    cursorDot.style.display = 'none';
    cursorRing.style.display = 'none';
    
    // Restore default cursor on body
    document.body.style.cursor = 'auto';
  }


  // 6. SCROLL REVEAL ANIMATIONS (Intersection Observer)
  const revealElements = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');

  window.revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null,
    threshold: 0.15,
    rootMargin: "0px 0px -50px 0px"
  });

  revealElements.forEach(el => window.revealObserver.observe(el));


  // 7. COUNTER ANIMATION
  const counterItems = document.querySelectorAll('.ctr-number');
  let hasCounted = false;

  const startCounters = () => {
    counterItems.forEach(counter => {
      const target = +counter.getAttribute('data-target');
      const suffix = counter.getAttribute('data-suffix');
      const duration = 2000;
      const increment = target / (duration / 16);
      let current = 0;

      const updateCounter = () => {
        current += increment;
        if (current < target) {
          counter.innerText = Math.ceil(current) + suffix;
          requestAnimationFrame(updateCounter);
        } else {
          // Add commas for large numbers
          counter.innerText = target.toLocaleString() + suffix;
        }
      };
      updateCounter();
    });
  };

  const statsSection = document.getElementById('statistics');
  if (statsSection) {
    const statsObserver = new IntersectionObserver((entries) => {
      const entry = entries[0];
      if (entry.isIntersecting && !hasCounted) {
        hasCounted = true;
        setTimeout(startCounters, 200);
      }
    }, { threshold: 0.5 });
    statsObserver.observe(statsSection);
  }


  // 8. PORTFOLIO FILTER
  const pfTabs = document.querySelectorAll('.pf-tab');
  const pfItems = document.querySelectorAll('.pf-item');

  pfTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active class
      pfTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const filter = tab.getAttribute('data-filter');

      pfItems.forEach(item => {
        // Reset animation state
        item.classList.remove('in-view');

        if (filter === 'all' || item.getAttribute('data-cat') === filter) {
          item.classList.remove('hidden');
          // small timeout to allow display:block to apply before animating opacity
          setTimeout(() => {
            item.classList.add('in-view');
          }, 50);
        } else {
          item.classList.add('hidden');
        }
      });
    });
  });


  // 9. TESTIMONIALS CAROUSEL
  const track = document.getElementById('testi-track');
  if (track) {
    const slides = Array.from(track.children);
    const nextButton = document.getElementById('testi-next');
    const prevButton = document.getElementById('testi-prev');
    const dotsNav = document.getElementById('testi-dots');

    if (slides.length > 0) {
      // Create dots
      slides.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.classList.add('testi-dot');
        dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
        if (i === 0) dot.classList.add('active');
        dotsNav.appendChild(dot);
      });
      const dots = Array.from(dotsNav.children);

      let currentIndex = 0;

      const moveToSlide = (index) => {
        if (index < 0) index = slides.length - 1;
        if (index >= slides.length) index = 0;

        track.style.transform = 'translateX(-' + (index * 100) + '%)';
        dots.forEach(d => d.classList.remove('active'));
        dots[index].classList.add('active');
        currentIndex = index;
      };

      nextButton.addEventListener('click', () => moveToSlide(currentIndex + 1));
      prevButton.addEventListener('click', () => moveToSlide(currentIndex - 1));

      dots.forEach((dot, i) => {
        dot.addEventListener('click', () => moveToSlide(i));
      });

      // Auto advance
      let autoPlay = setInterval(() => moveToSlide(currentIndex + 1), 3500);

      // Pause on hover
      const carouselContainer = document.querySelector('.testi-carousel');
      if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', () => clearInterval(autoPlay));
        carouselContainer.addEventListener('mouseleave', () => {
          autoPlay = setInterval(() => moveToSlide(currentIndex + 1), 3500);
        });
      }
    }
  }


  // 10. HERO PARTICLES ANIMATION (Gold Dust)
  const canvas = document.getElementById('hero-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height;
    let particles = [];

    const resizeCanvas = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    class Particle {
      constructor() {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.size = Math.random() * 2.5 + 0.5;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.speedY = Math.random() * -1 - 0.5; // Always float up slowly
        this.opacity = Math.random() * 0.5 + 0.1;
      }
      update() {
        this.x += this.speedX;
        this.y += this.speedY;

        // Wrap around
        if (this.y < -10) {
          this.y = height + 10;
          this.x = Math.random() * width;
        }
        if (this.x < -10) this.x = width + 10;
        if (this.x > width + 10) this.x = -10;
      }
      draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(212, 175, 55, ${this.opacity})`;
        ctx.fill();
        // Add subtle glow to larger particles
        if (this.size > 2) {
          ctx.shadowBlur = 10;
          ctx.shadowColor = 'rgba(212, 175, 55, 0.8)';
        } else {
          ctx.shadowBlur = 0;
        }
      }
    }

    const initParticles = () => {
      particles = [];
      const particleCount = Math.min(window.innerWidth / 15, 100); // Responsive count
      for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
      }
    };

    const animateParticles = () => {
      ctx.clearRect(0, 0, width, height);
      particles.forEach(p => {
        p.update();
        p.draw();
      });
      requestAnimationFrame(animateParticles);
    };

    initParticles();
    animateParticles();
  }

  // Set hero text animations after preloader
  function initHeroAnimations() {
    const heroAnims = document.querySelectorAll('[data-anim]');
    heroAnims.forEach(el => {
      // Small delay just to let UI settle
      setTimeout(() => {
        el.setAttribute('data-anim', 'fade-up'); // Ensure CSS triggers
      }, parseInt(el.getAttribute('data-delay') || '0') * 100);
    });
  }


  // 11. CONTACT FORM — Send via WhatsApp
  const contactForm = document.getElementById('contact-form');
  const successMsg = document.getElementById('form-success-msg');
  const submitBtn = document.getElementById('cf-submit');

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Basic validation
      let isValid = true;
      contactForm.querySelectorAll('[required]').forEach(input => {
        if (!input.value.trim()) {
          isValid = false;
          input.style.borderColor = '#e74c3c';
          input.style.boxShadow = '0 0 0 3px rgba(231,76,60,0.15)';
        } else {
          input.style.borderColor = '';
          input.style.boxShadow = '';
        }
      });

      if (!isValid) return;

      // Collect form data
      const name = document.getElementById('cf-name')?.value.trim() || '';
      const email = document.getElementById('cf-email')?.value.trim() || '';
      const phone = document.getElementById('cf-phone')?.value.trim() || 'N/A';
      const subject = document.getElementById('cf-subject')?.value.trim() || 'General Inquiry';
      const message = document.getElementById('cf-msg')?.value.trim() || '';

      // Build WhatsApp message
      const text =
        `👋 *New Inquiry — REEL Website*\n\n` +
        `*Name:* ${name}\n` +
        `*Email:* ${email}\n` +
        `*Phone:* ${phone}\n` +
        `*Subject:* ${subject}\n\n` +
        `*Message:*\n${message}\n\n` +
        `---\n_Sent from royaltyexecutiveempire.com_`;

      const whatsappURL = `https://wa.me/2348067029444?text=${encodeURIComponent(text)}`;

      // Show success state on button
      const originalHTML = submitBtn.innerHTML;
      submitBtn.innerHTML = '<span>✅ Opening WhatsApp...</span>';
      submitBtn.style.background = 'linear-gradient(135deg, #25D366, #128C7E)';
      submitBtn.disabled = true;

      if (successMsg) {
        successMsg.style.display = 'block';
        successMsg.innerHTML = '✅ Opening WhatsApp! Complete the send to reach our team instantly.';
      }

      // Open WhatsApp
      window.open(whatsappURL, '_blank');

      // Reset after 4 seconds
      setTimeout(() => {
        submitBtn.innerHTML = originalHTML;
        submitBtn.disabled = false;
        submitBtn.style.background = '';
        contactForm.reset();
        if (successMsg) successMsg.style.display = 'none';
      }, 4000);
    });
  }

  // 12. FOOTER YEAR
  const yearEl = document.getElementById('footer-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  // 13. CUSTOM LUXURY CURSOR
  // Disabled by request to restore the normal cursor.
  /*
  const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  if (!isTouchDevice) {
    const cursor = document.createElement('div');
    cursor.classList.add('custom-cursor');
    const cursorDot = document.createElement('div');
    cursorDot.classList.add('custom-cursor-dot');
    document.body.appendChild(cursor);
    document.body.appendChild(cursorDot);

    let mouseX = 0, mouseY = 0;
    let cursorX = 0, cursorY = 0;

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      // Dot follows immediately
      cursorDot.style.left = `${mouseX}px`;
      cursorDot.style.top = `${mouseY}px`;
    });

    // Ring follows with easing
    const animateCursor = () => {
      let distX = mouseX - cursorX;
      let distY = mouseY - cursorY;
      cursorX += distX * 0.2;
      cursorY += distY * 0.2;
      cursor.style.left = `${cursorX}px`;
      cursor.style.top = `${cursorY}px`;
      requestAnimationFrame(animateCursor);
    };
    animateCursor();

    // Hover effect on interactables
    const interactables = document.querySelectorAll('a, button, input, textarea, select, .product-card, .division-card, .glass-card, .btn-primary, .btn-secondary, .listing-card');
    interactables.forEach(el => {
      el.addEventListener('mouseenter', () => {
        cursor.classList.add('hovered');
        cursorDot.classList.add('hovered');
      });
      el.addEventListener('mouseleave', () => {
        cursor.classList.remove('hovered');
        cursorDot.classList.remove('hovered');
      });
    });
  }
  */

  // 14. DYNAMIC ADMIN RENDER (Firebase Firestore)
  const renderDynamicContent = async () => {
    if (!window.db) {
      console.warn("Firebase not initialized yet.");
      return;
    }

    // --- SHOP PAGE ---
    // Helper: checks if an item should be visible to the public
    const isLive = (item) => {
      const now = Date.now();
      if (!item.status || item.status === 'published') return true;
      if (item.status === 'scheduled') {
        // Show if the scheduled time has already passed
        return item.scheduleTime && new Date(item.scheduleTime).getTime() <= now;
      }
      return false;
    };

    const shopContainer = document.getElementById('dynamic-shop-container');
    if (shopContainer) {
      try {
        const snapshot = await window.db.collection('products').get();
        const products = [];
        snapshot.forEach(doc => {
          const data = { id: doc.id, ...doc.data() };
          if (isLive(data)) products.push(data);
        });

        if (products.length > 0) {
          shopContainer.innerHTML = `
            <div class="shop-layout">
              <aside class="shop-sidebar reveal-left">
                <h3>Categories</h3>
                <ul class="cat-list">
                  <li><a href="#">All Categories</a></li>
                  <li><a href="#">Electronics</a></li>
                  <li><a href="#">Corporate Gifts</a></li>
                  <li><a href="#">Apparel</a></li>
                  <li><a href="#">Accessories</a></li>
                </ul>
              </aside>
              <main class="products-grid reveal-right" id="products-grid-inner"></main>
            </div>
          `;

          const gridInner = document.getElementById('products-grid-inner');
          products.forEach(p => {
            gridInner.innerHTML += `
              <div class="product-card">
                <div class="product-img" style="background: url('${p.image}') ${p.imagePos || 'center center'}/cover; min-height:240px;"></div>
                <div class="product-info">
                  <div class="product-cat">${p.category}</div>
                  <h3 class="product-title">${p.name}</h3>
                  <div class="product-price">AED ${Number(p.price).toFixed(2)}</div>
                  <button class="btn-gold" style="width:100%; justify-content:center;" onclick="addToCart('${p.id}', '${p.name.replace(/'/g, "\\'")}', ${Number(p.price)}, '${p.image}')">Add to Cart</button>
                </div>
              </div>
            `;
          });
        }
      } catch (e) { console.error("Error fetching products:", e); }
    }

    // --- PORTFOLIO PAGE ---
    const pfContainer = document.getElementById('dynamic-portfolio-container');
    if (pfContainer) {
      try {
        const snapshot = await window.db.collection('portfolio').get();
        const portfolio = [];
        snapshot.forEach(doc => portfolio.push({ id: doc.id, ...doc.data() }));

        if (portfolio.length > 0) {
          pfContainer.innerHTML = `
            <div class="portfolio-filters reveal-up">
              <button class="pf-tab active" data-filter="all">All Projects</button>
              <button class="pf-tab" data-filter="REEL Branding">Branding</button>
              <button class="pf-tab" data-filter="REEL Power">Power</button>
            </div>
            <div class="portfolio-masonry reveal-up" id="pf-masonry-inner" style="columns: 3; column-gap: 24px;"></div>
          `;

          const pfInner = document.getElementById('pf-masonry-inner');
          portfolio.forEach(p => {
            pfInner.innerHTML += `
              <div class="pf-item" style="break-inside: avoid; margin-bottom: 24px; border-radius: var(--radius-lg); overflow: hidden; position: relative;">
                <div class="pf-item-inner" style="background: var(--black-700); border: 1px solid var(--gold-border); border-radius: var(--radius-lg); overflow:hidden;">
                  <div style="background: url('${p.image}') ${p.imagePos || 'center center'}/cover; min-height: 300px;"></div>
                  <div class="pf-overlay" style="padding: 20px; background: var(--black-900);">
                    <div class="pf-cat-tag" style="font-size: 0.7rem; text-transform: uppercase; color: var(--gold-300); margin-bottom: 6px;">${p.category}</div>
                    <h3 class="pf-title" style="font-family: var(--font-display); font-size: 1.1rem; color: #fff;">${p.title}</h3>
                  </div>
                </div>
              </div>
            `;
          });
        }
      } catch (e) { console.error("Error fetching portfolio:", e); }
    }

    // --- BLOG PAGE ---
    const blogContainer = document.getElementById('dynamic-blog-container');
    if (blogContainer) {
      try {
        const snapshot = await window.db.collection('blogs').orderBy('timestamp', 'desc').get();
        const blogs = [];
        snapshot.forEach(doc => {
          const data = { id: doc.id, ...doc.data() };
          if (isLive(data)) blogs.push(data);
        });

        if (blogs.length > 0) {
          blogContainer.innerHTML = ''; // Clear Coming Soon
          blogs.forEach(b => {
            // Strip HTML tags for safe snippet preview
            const plainText = b.content ? b.content.replace(/<[^>]+>/g, '') : '';
            blogContainer.innerHTML += `
              <article class="reveal-up" style="background: var(--w08); border: 1px solid var(--gold-border); border-radius: var(--radius-xl); overflow: hidden; margin-bottom: 40px; transition: all 0.3s;" onmouseover="this.style.boxShadow='var(--gold-glow-sm)'" onmouseout="this.style.boxShadow='none'">
                <div style="height: 350px; background: url('${b.image}') ${b.imagePos || 'center center'}/cover;"></div>
                <div style="padding: 40px;">
                  <div style="display:flex; gap:16px; margin-bottom: 16px; font-size: 0.85rem; color: var(--gold-300); text-transform: uppercase; letter-spacing: 1px;">
                    <span>${b.category}</span>
                    <span style="color:var(--w50)">${b.date}</span>
                  </div>
                  <h2 style="font-family: var(--font-display); font-size: 2rem; color: #fff; margin-bottom: 16px;">${b.title}</h2>
                  <p style="color: var(--w60); line-height: 1.8; margin-bottom: 24px;">${plainText.substring(0, 150)}...</p>
                  <a href="article.html?id=${b.id}" class="gold-link" style="font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem;">Read Full Article &rarr;</a>
                </div>
              </article>
            `;
          });

          // Trigger animations on newly loaded blog cards
          if (typeof window.revealObserver !== 'undefined') {
            blogContainer.querySelectorAll('.reveal-up').forEach(el => window.revealObserver.observe(el));
          }
        }
      } catch (e) { console.error("Error fetching blogs:", e); }
    }

    // --- HOMEPAGE RECENT INSIGHTS SLIDER ---
    const hpBlogSlider = document.getElementById('dynamic-homepage-blogs');
    if (hpBlogSlider) {
      try {
        const snapshot = await window.db.collection('blogs').orderBy('timestamp', 'desc').limit(8).get();
        const hpBlogs = [];
        snapshot.forEach(doc => {
          const data = { id: doc.id, ...doc.data() };
          if (isLive(data)) hpBlogs.push(data);
        });

        if (hpBlogs.length > 0) {
          hpBlogSlider.innerHTML = ''; 
          // We duplicate the array to ensure seamless infinite scrolling
          const sliderBlogs = [...hpBlogs, ...hpBlogs, ...hpBlogs]; 

          sliderBlogs.forEach(b => {
            hpBlogSlider.innerHTML += `
              <a href="article.html?id=${b.id}" class="hp-blog-card">
                <img src="${b.image}" alt="${b.title}" class="hp-blog-img" onerror="this.src='Images/BG/logo%20bg.png'"/>
                <div class="hp-blog-body">
                  <span class="hp-blog-cat">${b.category || 'Updates'}</span>
                  <h3 class="hp-blog-title">${b.title}</h3>
                  <span class="hp-blog-date">${b.date}</span>
                </div>
              </a>
            `;
          });
        } else {
          hpBlogSlider.innerHTML = '<p style="color:var(--w50); padding: 20px;">No insights available yet.</p>';
        }
      } catch (e) { console.error("Error fetching homepage blogs:", e); }
    }

    const allianceContainer = document.getElementById('dynamic-alliance-container');
    if (allianceContainer) {
      try {
        const snapshot = await window.db.collection('brands').orderBy('timestamp', 'asc').get();
        const brands = [];
        snapshot.forEach(doc => {
          const data = { id: doc.id, ...doc.data() };
          // We can reuse isLive for scheduling, or just push. Let's use isLive.
          if (isLive(data)) brands.push(data);
        });

        if (brands.length > 0) {
          let htmlStr = '';
          brands.forEach(b => {
            let linkHref = 'javascript:void(0)';
            let target = '';
            
            if (b.linkedBlogId) {
              linkHref = `article.html?id=${b.linkedBlogId}`;
            } else if (b.link) {
              linkHref = b.link;
              target = 'target="_blank"';
            }

            htmlStr += `
              <a href="${linkHref}" ${target} style="display:flex;align-items:center;">
                <img src="${b.image}" alt="${b.name}" class="partner-logo" onerror="this.style.display='none'" />
              </a>
            `;
          });
          // Duplicate for seamless marquee scroll
          allianceContainer.innerHTML = htmlStr + htmlStr;
        }
      } catch (e) { console.error("Error fetching brands:", e); }
    }

    // --- REEL POWER PRODUCT LINEUP ---
    const powerGrid = document.getElementById('power-lineup-grid');
    if (powerGrid) {
      try {
        const pSnap = await window.db.collection('power_products').orderBy('timestamp', 'desc').get();
        const powerProds = [];
        pSnap.forEach(doc => {
          const d = { id: doc.id, ...doc.data() };
          if (isLive(d)) powerProds.push(d);
        });

        if (powerProds.length === 0) {
          powerGrid.innerHTML = `<div class="power-lineup-empty"><p>No products available yet. Check back soon.</p></div>`;
        } else {
          powerGrid.innerHTML = '';
          powerProds.forEach(prod => {
            const card = document.createElement('div');
            card.className = 'power-prod-card reveal-up';
            card.innerHTML = `
              <div class="power-prod-card-img-wrap">
                <img src="${prod.image || ''}" alt="${prod.title || ''}" loading="lazy" onerror="this.parentElement.style.background='rgba(212,175,55,0.05)';this.style.display='none'" />
                <div class="power-prod-card-badge">REEL Power</div>
                <div class="power-prod-card-click-hint">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
                  View Details
                </div>
              </div>
              <div class="power-prod-card-body">
                <div class="power-prod-card-title">${prod.title || 'Product'}</div>
                <div class="power-prod-card-caption">${prod.caption || ''}</div>
                ${prod.price ? `<div class="power-prod-card-price">${prod.price}</div>` : ''}
              </div>
              <div class="power-prod-card-footer">
                <button class="power-prod-card-btn" data-action="view">View Details</button>
                <button class="power-prod-card-btn whatsapp-btn" data-action="wa">Enquire</button>
              </div>
            `;

            // Open modal
            const openModal = () => {
              const overlay = document.getElementById('power-modal-overlay');
              const imgs = prod.images && prod.images.length > 0 ? prod.images : (prod.image ? [prod.image] : []);
              let currentIdx = 0;

              const mainImg = document.getElementById('power-modal-main-img');
              const counter = document.getElementById('power-gallery-counter');
              const dotsWrap = document.getElementById('power-gallery-dots');
              const prevBtn = document.getElementById('power-gallery-prev');
              const nextBtn = document.getElementById('power-gallery-next');

              // Render dots
              dotsWrap.innerHTML = imgs.map((_, i) => `<div class="power-gallery-dot${i === 0 ? ' active' : ''}"></div>`).join('');
              const dots = dotsWrap.querySelectorAll('.power-gallery-dot');

              const showImg = (idx) => {
                currentIdx = (idx + imgs.length) % imgs.length;
                mainImg.src = imgs[currentIdx];
                counter.textContent = `${currentIdx + 1} / ${imgs.length}`;
                dots.forEach((d, i) => d.classList.toggle('active', i === currentIdx));
              };
              showImg(0);

              // Show/hide nav buttons
              prevBtn.style.display = imgs.length > 1 ? 'flex' : 'none';
              nextBtn.style.display = imgs.length > 1 ? 'flex' : 'none';
              prevBtn.onclick = () => showImg(currentIdx - 1);
              nextBtn.onclick = () => showImg(currentIdx + 1);
              dots.forEach((d, i) => { d.onclick = () => showImg(i); });

              // Text content
              document.getElementById('power-modal-title').textContent = prod.title || '';
              document.getElementById('power-modal-details').textContent = prod.details || 'No additional details provided.';
              const priceEl = document.getElementById('power-modal-price');
              priceEl.textContent = prod.price || '';
              priceEl.style.display = prod.price ? 'flex' : 'none';

              // Video
              const vidContainer = document.getElementById('power-modal-video-container');
              if (prod.videoLink) {
                let embedUrl = prod.videoLink;
                const ytMatch = prod.videoLink.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/))([^&?/]+)/);
                if (ytMatch) embedUrl = `https://www.youtube.com/embed/${ytMatch[1]}?rel=0&modestbranding=1`;
                vidContainer.innerHTML = `<div class="power-modal-video-wrap"><iframe src="${embedUrl}" allowfullscreen allow="autoplay; encrypted-media"></iframe></div>`;
              } else {
                vidContainer.innerHTML = '';
              }

              // WhatsApp
              const waBtn = document.getElementById('power-modal-wa-btn');
              const waMsg = `Hello REEL Power! 👋%0A%0AI'm interested in the *${prod.title}*. Could you please share more details on pricing and availability?`;
              waBtn.href = `https://wa.me/2348067029444?text=${waMsg}`;

              overlay.classList.add('open');
              document.body.style.overflow = 'hidden';
            };

            card.querySelector('[data-action="view"]').addEventListener('click', openModal);
            card.querySelector('[data-action="wa"]').addEventListener('click', (e) => {
              e.stopPropagation();
              const msg = `Hello REEL Power! 👋%0A%0AI'm interested in the *${prod.title}*. Could you please share more details?`;
              window.open(`https://wa.me/2348067029444?text=${msg}`, '_blank');
            });
            card.addEventListener('click', (e) => {
              if (!e.target.closest('button')) openModal();
            });

            powerGrid.appendChild(card);
          });

          // Observe new cards for reveal animations
          if (typeof window.revealObserver !== 'undefined') {
            powerGrid.querySelectorAll('.reveal-up').forEach(el => window.revealObserver.observe(el));
          }
        }
      } catch (e) { console.error("Error fetching power products:", e); }
    }

    // Power Modal close logic
    const powerOverlay = document.getElementById('power-modal-overlay');
    if (powerOverlay) {
      const closeModal = () => {
        powerOverlay.classList.remove('open');
        document.body.style.overflow = '';
        // Stop any playing video
        const vid = document.getElementById('power-modal-video-container');
        if (vid) vid.innerHTML = '';
      };
      document.getElementById('power-modal-close-btn')?.addEventListener('click', closeModal);
      powerOverlay.addEventListener('click', (e) => {
        if (e.target === powerOverlay) closeModal();
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && powerOverlay.classList.contains('open')) closeModal();
      });
    }
  };

  // Give Firebase a tiny moment to init if scripts loaded out of order
  setTimeout(renderDynamicContent, 100);

  // 14.b CONTACT FORM INTERCEPTION (Save to Firebase)
  const firebaseContactForm = document.getElementById('contact-form');
  if (firebaseContactForm) {
    firebaseContactForm.addEventListener('submit', async (e) => {
      // We don't preventDefault if it's Web3Forms, but we can hook in to save to Firebase before it finishes
      const name = document.getElementById('cf-name').value;
      const email = document.getElementById('cf-email').value;
      const phone = document.getElementById('cf-phone').value;
      const subject = document.getElementById('cf-subject').value;
      const msg = document.getElementById('cf-msg').value;

      if (name && email && msg) {
        if (window.db) {
          try {
            await window.db.collection('messages').add({
              name, email, phone, subject, message: msg,
              date: new Date().toLocaleString(),
              timestamp: firebase.firestore.FieldValue.serverTimestamp(),
              status: 'unread'
            });
          } catch (err) { console.warn("Could not save message to Firebase:", err); }
        }
      }
    });
  }

  // 15. SHOPPING CART LOGIC
  let cart = [];
  try {
    cart = JSON.parse(localStorage.getItem('ree_cart')) || [];
  } catch (e) {
    console.warn("Local storage unavailable for cart", e);
  }

  window.addToCart = (id, name, price, image) => {
    const existing = cart.find(item => item.id === id);
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({ id, name, price, image, qty: 1 });
    }
    try { localStorage.setItem('ree_cart', JSON.stringify(cart)); } catch (e) { }
    updateCartCount();

    // Custom Toast for Cart
    const t = document.createElement('div');
    t.className = 'toast';
    t.innerHTML = `
      <div class="toast-icon">🛍️</div>
      <div class="toast-content">
        <h4>Added to Cart</h4>
        <p>${name}</p>
      </div>
    `;
    document.body.appendChild(t);
    setTimeout(() => t.classList.add('show'), 10);
    setTimeout(() => {
      t.classList.remove('show');
      setTimeout(() => t.remove(), 300);
    }, 3000);
  };

  const updateCartCount = () => {
    const count = cart.reduce((acc, item) => acc + item.qty, 0);
    document.querySelectorAll('.cart-count').forEach(el => {
      el.textContent = count;
      el.style.display = count > 0 ? 'flex' : 'none';
    });
  };

  // Render Cart Page if we are on it
  const renderCartPage = async () => {
    const container = document.getElementById('cart-items-container');
    if (!container) return; // not on cart page

    if (cart.length === 0) {
      container.innerHTML = `
        <div class="cart-empty" style="text-align: center; padding: 80px 40px;">
          <div class="cart-empty-icon" style="font-size: 4rem; margin-bottom: 16px;">🛍️</div>
          <h3 style="font-family: var(--font-display); font-size: 1.8rem; color: #fff; margin-bottom: 8px;">Your cart is empty</h3>
          <p style="color: var(--w50); margin-bottom: 28px;">Looks like you haven't added anything to your cart yet.</p>
        </div>
      `;
      document.getElementById('cart-total-price').textContent = 'AED 0.00';
      return;
    }

    container.innerHTML = '';
    let subtotal = 0;
    cart.forEach((item, index) => {
      const itemTotal = item.price * item.qty;
      subtotal += itemTotal;
      container.innerHTML += `
        <div class="cart-row">
          <div class="cart-item-info">
            <div class="cart-thumb"><img src="${item.image}" alt="" style="width:100%; height:100%; object-fit:cover; border-radius:4px;"></div>
            <div>
              <div class="cart-item-name">${item.name}</div>
            </div>
          </div>
          <div class="cart-price">AED ${item.price.toFixed(2)}</div>
          <input type="number" class="qty-input" value="${item.qty}" min="1" max="99" onchange="updateCartQty(${index}, this.value)" />
          <div class="cart-price subtotal-col">AED ${itemTotal.toFixed(2)}</div>
          <button class="cart-remove" title="Remove item" onclick="removeFromCart(${index})">✕</button>
        </div>
      `;
    });

    // Wait for DB if not ready
    if (!window.db) {
      setTimeout(renderCartPage, 100);
      return;
    }

    let finalTotal = subtotal;
    try {
      const taxDoc = await window.db.collection('settings').doc('tax').get();
      if (taxDoc.exists) {
        const d = taxDoc.data();
        if (d.enabled === 'yes') finalTotal += finalTotal * (parseFloat(d.rate) / 100);
      }
      const discountDoc = await window.db.collection('settings').doc('discount').get();
      if (discountDoc.exists) {
        const d = discountDoc.data();
        const discountPercent = parseFloat(d.percent) || 0;
        if (discountPercent > 0) finalTotal -= finalTotal * (discountPercent / 100);
      }
    } catch (e) { console.warn('Could not load settings', e); }

    document.getElementById('cart-total-price').textContent = 'AED ' + finalTotal.toFixed(2);
  };

  window.updateCartQty = (index, newQty) => {
    const qty = parseInt(newQty);
    if (qty > 0) {
      cart[index].qty = qty;
      try { localStorage.setItem('ree_cart', JSON.stringify(cart)); } catch (e) { }
      renderCartPage();
      updateCartCount();
    }
  };

  window.removeFromCart = (index) => {
    cart.splice(index, 1);
    try { localStorage.setItem('ree_cart', JSON.stringify(cart)); } catch (e) { }
    renderCartPage();
    updateCartCount();
  };

  // WhatsApp Checkout
  const waBtn = document.getElementById('whatsapp-checkout-btn');
  if (waBtn) {
    waBtn.addEventListener('click', async () => {
      if (cart.length === 0) return alert("Your cart is empty!");
      let text = "Hello REEL, I would like to place an order:%0A%0A";
      let subtotal = 0;
      cart.forEach(item => {
        text += `- ${item.qty}x ${item.name} (AED ${item.price.toFixed(2)} each)%0A`;
        subtotal += (item.price * item.qty);
      });

      let finalTotal = subtotal;
      try {
        if (window.db) {
          const taxDoc = await window.db.collection('settings').doc('tax').get();
          if (taxDoc.exists) {
            const d = taxDoc.data();
            if (d.enabled === 'yes') finalTotal += finalTotal * (parseFloat(d.rate) / 100);
          }
          const discountDoc = await window.db.collection('settings').doc('discount').get();
          if (discountDoc.exists) {
            const d = discountDoc.data();
            const discountPercent = parseFloat(d.percent) || 0;
            if (discountPercent > 0) finalTotal -= finalTotal * (discountPercent / 100);
          }
        }
      } catch (e) { }

      text += `%0A*Total: AED ${finalTotal.toFixed(2)}*`;

      // Save order to Firebase
      if (window.db) {
        try {
          await window.db.collection('orders').add({
            items: cart,
            subtotal: subtotal,
            total: finalTotal,
            date: new Date().toLocaleString(),
            timestamp: firebase.firestore.FieldValue.serverTimestamp(),
            status: 'pending'
          });
          // Clear cart after order is initiated
          cart = [];
          try { localStorage.removeItem('ree_cart'); } catch (e) { }
          renderCartPage();
          updateCartCount();
        } catch (err) { console.warn("Could not save order to Firebase:", err); }
      }

      // REEL WhatsApp Business Numbers
      const phoneNumber = "971561347581"; // UAE: +971 56 134 7581
      const waLink = `https://wa.me/${phoneNumber}?text=${text}`;
      window.open(waLink, '_blank');
    });
  }

  updateCartCount();
  renderCartPage();

});
