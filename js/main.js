/**
 * ====================================================================
 * REE GLOBAL — ROYALTY EXECUTIVE EMPIRE
 * Main Application Logic
 * ====================================================================
 */

document.addEventListener('DOMContentLoaded', () => {

  // 1. PRELOADER
  const preloader = document.getElementById('preloader');
  const body = document.body;
  body.classList.add('no-scroll');
  
  // Give the CSS animation time to complete
  if (preloader) {
    setTimeout(() => {
      preloader.classList.add('done');
      body.classList.remove('no-scroll');
      initHeroAnimations();
    }, 2500);
  } else {
    // No preloader on this page — show content immediately
    body.classList.remove('no-scroll');
    initHeroAnimations();
  }

  // 2. COOKIE CONSENT
  const cookieBanner = document.getElementById('cookie-consent');
  const btnAccept = document.getElementById('cookie-accept');
  const btnDecline = document.getElementById('cookie-decline');
  
  if (cookieBanner && !localStorage.getItem('ree_cookie_consent')) {
    setTimeout(() => {
      cookieBanner.classList.add('show');
    }, 3500);
  }
  
  if (btnAccept) {
    btnAccept.addEventListener('click', () => {
      localStorage.setItem('ree_cookie_consent', 'accepted');
      if (cookieBanner) cookieBanner.classList.remove('show');
    });
  }
  
  if (btnDecline) {
    btnDecline.addEventListener('click', () => {
      localStorage.setItem('ree_cookie_consent', 'declined');
      if (cookieBanner) cookieBanner.classList.remove('show');
    });
  }

  // 3. NAVIGATION HEADER
  const mainNav = document.getElementById('main-nav');
  const scrollTopBtn = document.getElementById('scroll-top-btn');
  
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    // Header Blur
    if (y > 50) {
      mainNav.classList.add('scrolled');
    } else {
      mainNav.classList.remove('scrolled');
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
  
  hamburger.addEventListener('click', toggleMenu);
  navOverlay.addEventListener('click', toggleMenu);
  
  // Close menu on link click
  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      if (hamburger.classList.contains('open')) {
        toggleMenu();
      }
    });
  });

  // 5. ACTIVE LINK HIGHLIGHTING
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
  if(track) {
    const slides = Array.from(track.children);
    const nextButton = document.getElementById('testi-next');
    const prevButton = document.getElementById('testi-prev');
    const dotsNav = document.getElementById('testi-dots');
    
    if(slides.length > 0) {
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
        if(this.size > 2) {
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
      const name    = document.getElementById('cf-name')?.value.trim() || '';
      const email   = document.getElementById('cf-email')?.value.trim() || '';
      const phone   = document.getElementById('cf-phone')?.value.trim() || 'N/A';
      const subject = document.getElementById('cf-subject')?.value.trim() || 'General Inquiry';
      const message = document.getElementById('cf-msg')?.value.trim() || '';

      // Build WhatsApp message
      const text = 
        `👋 *New Inquiry — REE Global Website*\n\n` +
        `*Name:* ${name}\n` +
        `*Email:* ${email}\n` +
        `*Phone:* ${phone}\n` +
        `*Subject:* ${subject}\n\n` +
        `*Message:*\n${message}\n\n` +
        `---\n_Sent from royaltyexecutiveempire.com_`;

      const whatsappURL = `https://wa.me/971561347581?text=${encodeURIComponent(text)}`;

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

  // 14. DYNAMIC ADMIN RENDER (Firebase Firestore)
  const renderDynamicContent = async () => {
    if (!window.db) {
      console.warn("Firebase not initialized yet.");
      return;
    }

    // --- SHOP PAGE ---
    const shopContainer = document.getElementById('dynamic-shop-container');
    if (shopContainer) {
      try {
        const snapshot = await window.db.collection('products').get();
        const products = [];
        snapshot.forEach(doc => products.push({ id: doc.id, ...doc.data() }));
        
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
      } catch(e) { console.error("Error fetching products:", e); }
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
              <button class="pf-tab" data-filter="REEL Real Estate">Real Estate</button>
              <button class="pf-tab" data-filter="REEL Branding">Branding</button>
              <button class="pf-tab" data-filter="REEL Power">Power</button>
              <button class="pf-tab" data-filter="REEL Music">Music</button>
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
      } catch(e) { console.error("Error fetching portfolio:", e); }
    }

    // --- BLOG PAGE ---
    const blogContainer = document.getElementById('dynamic-blog-container');
    if (blogContainer) {
      try {
        const snapshot = await window.db.collection('blogs').orderBy('timestamp', 'desc').get();
        const blogs = [];
        snapshot.forEach(doc => blogs.push({ id: doc.id, ...doc.data() }));

        if (blogs.length > 0) {
          blogContainer.innerHTML = ''; // Clear Coming Soon
          blogs.forEach(b => {
            blogContainer.innerHTML += `
              <article class="reveal-up" style="background: var(--w08); border: 1px solid var(--gold-border); border-radius: var(--radius-xl); overflow: hidden; margin-bottom: 40px; transition: all 0.3s;" onmouseover="this.style.boxShadow='var(--gold-glow-sm)'" onmouseout="this.style.boxShadow='none'">
                <div style="height: 350px; background: url('${b.image}') ${b.imagePos || 'center center'}/cover;"></div>
                <div style="padding: 40px;">
                  <div style="display:flex; gap:16px; margin-bottom: 16px; font-size: 0.85rem; color: var(--gold-300); text-transform: uppercase; letter-spacing: 1px;">
                    <span>${b.category}</span>
                    <span style="color:var(--w50)">${b.date}</span>
                  </div>
                  <h2 style="font-family: var(--font-display); font-size: 2rem; color: #fff; margin-bottom: 16px;">${b.title}</h2>
                  <p style="color: var(--w60); line-height: 1.8; margin-bottom: 24px;">${b.content.substring(0, 150)}...</p>
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
      } catch(e) { console.error("Error fetching blogs:", e); }
    }
  };

  // Give Firebase a tiny moment to init if scripts loaded out of order
  setTimeout(renderDynamicContent, 100);

  // 15. SHOPPING CART LOGIC
  let cart = JSON.parse(localStorage.getItem('ree_cart')) || [];

  window.addToCart = (id, name, price, image) => {
    const existing = cart.find(item => item.id === id);
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({ id, name, price, image, qty: 1 });
    }
    localStorage.setItem('ree_cart', JSON.stringify(cart));
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
    } catch(e) { console.warn('Could not load settings', e); }

    document.getElementById('cart-total-price').textContent = 'AED ' + finalTotal.toFixed(2);
  };

  window.updateCartQty = (index, newQty) => {
    const qty = parseInt(newQty);
    if (qty > 0) {
      cart[index].qty = qty;
      localStorage.setItem('ree_cart', JSON.stringify(cart));
      renderCartPage();
      updateCartCount();
    }
  };

  window.removeFromCart = (index) => {
    cart.splice(index, 1);
    localStorage.setItem('ree_cart', JSON.stringify(cart));
    renderCartPage();
    updateCartCount();
  };

  // WhatsApp Checkout
  const waBtn = document.getElementById('whatsapp-checkout-btn');
  if (waBtn) {
    waBtn.addEventListener('click', async () => {
      if (cart.length === 0) return alert("Your cart is empty!");
      let text = "Hello REE Global, I would like to place an order:%0A%0A";
      let subtotal = 0;
      cart.forEach(item => {
        text += `- ${item.qty}x ${item.name} (AED ${item.price.toFixed(2)} each)%0A`;
        subtotal += (item.price * item.qty);
      });
      
      let finalTotal = subtotal;
      try {
        if(window.db) {
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
      } catch(e) {}
      
      text += `%0A*Total: AED ${finalTotal.toFixed(2)}*`;
      
      // REPLACE 1234567890 WITH YOUR ACTUAL WHATSAPP NUMBER IN INTERNATIONAL FORMAT (e.g. 234800000000)
      const phoneNumber = "2348000000000"; 
      const waLink = `https://wa.me/${phoneNumber}?text=${text}`;
      window.open(waLink, '_blank');
    });
  }

  updateCartCount();
  renderCartPage();

});
