/**
 * REEL - Admin Controller
 * Handles authentication and saving data to LocalStorage for prototype.
 */

// Hardcoded CEO Password
const MASTER_PASS = "REEGLOBAL@090021";

document.addEventListener('DOMContentLoaded', () => {
  
  // --- LOGIN LOGIC ---
  const loginForm = document.getElementById('admin-login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const passInput = document.getElementById('admin-pass').value;
      const errorMsg = document.getElementById('login-error');
      
      if (passInput === MASTER_PASS) {
        // Authenticated! Save flag to sessionStorage so it resets when browser closes
        sessionStorage.setItem('ree_admin_auth', 'true');
        // Redirect to dashboard
        window.location.href = 'index.html';
      } else {
        errorMsg.style.display = 'block';
        // Shake animation for error
        const card = document.querySelector('.admin-login-card');
        card.style.transform = 'translateX(-10px)';
        setTimeout(() => card.style.transform = 'translateX(10px)', 100);
        setTimeout(() => card.style.transform = 'translateX(-10px)', 200);
        setTimeout(() => card.style.transform = 'translateX(10px)', 300);
        setTimeout(() => card.style.transform = 'translateX(0)', 400);
      }
    });
  }

  // --- DASHBOARD LOGIC ---
  const dashboard = document.getElementById('admin-dashboard');
  if (dashboard) {
    // 1. Security Check
    if (sessionStorage.getItem('ree_admin_auth') !== 'true') {
      window.location.href = 'login.html';
      return;
    }

    // 2. Logout functionality
    document.getElementById('logout-btn').addEventListener('click', (e) => {
      e.preventDefault();
      sessionStorage.removeItem('ree_admin_auth');
      window.location.href = 'login.html';
    });

    // 3. Tab Switching Logic
    const navLinks = document.querySelectorAll('.admin-nav-link');
    const sections = document.querySelectorAll('.admin-section');
    
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        // Remove active class from all
        navLinks.forEach(l => l.classList.remove('active'));
        sections.forEach(s => s.classList.remove('active'));
        
        // Add active class to clicked
        link.classList.add('active');
        const targetId = link.getAttribute('data-target');
        document.getElementById(targetId).classList.add('active');
      });
    });

    // 4. Initialize Data Arrays from LocalStorage
    // We store arrays of objects for Blog, Portfolio, and Shop
    let blogs = JSON.parse(localStorage.getItem('ree_blogs')) || [];
    let portfolio = JSON.parse(localStorage.getItem('ree_portfolio')) || [];
    let products = JSON.parse(localStorage.getItem('ree_products')) || [];

    // Helper to render lists in the admin panel
    const renderAdminList = (dataArray, containerId, type) => {
      const container = document.getElementById(containerId);
      if (!container) return;
      
      container.innerHTML = '';
      if (dataArray.length === 0) {
        container.innerHTML = `<div class="empty-state">No ${type} items found. Add one above.</div>`;
        return;
      }
      
      dataArray.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'admin-list-item';
        div.innerHTML = `
          <div class="item-info">
            <strong>${item.title || item.name}</strong>
            <span class="item-date">${item.date || item.category || item.price}</span>
          </div>
          <button class="btn-delete" data-index="${index}" data-type="${type}">Delete</button>
        `;
        container.appendChild(div);
      });

      // Attach delete listeners
      container.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const idx = e.target.getAttribute('data-index');
          const t = e.target.getAttribute('data-type');
          if (confirm(`Are you sure you want to delete this ${t} item?`)) {
            if (t === 'blog') {
              blogs.splice(idx, 1);
              localStorage.setItem('ree_blogs', JSON.stringify(blogs));
              renderAdminList(blogs, 'blog-list', 'blog');
            } else if (t === 'portfolio') {
              portfolio.splice(idx, 1);
              localStorage.setItem('ree_portfolio', JSON.stringify(portfolio));
              renderAdminList(portfolio, 'portfolio-list', 'portfolio');
            } else if (t === 'product') {
              products.splice(idx, 1);
              localStorage.setItem('ree_products', JSON.stringify(products));
              renderAdminList(products, 'product-list', 'product');
            }
            alert('Item deleted successfully!');
          }
        });
      });
    };

    // Initial Renders
    renderAdminList(blogs, 'blog-list', 'blog');
    renderAdminList(portfolio, 'portfolio-list', 'portfolio');
    renderAdminList(products, 'product-list', 'product');

    // 5. Handle Form Submissions (Image Uploads are simulated via Base64 FileReader for local storage)
    
    // -- BLOG --
    document.getElementById('form-blog').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('blog-title').value;
      const category = document.getElementById('blog-cat').value;
      const content = document.getElementById('blog-content').value;
      const fileInput = document.getElementById('blog-img');
      
      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          blogs.unshift({
            title, category, content, 
            image: evt.target.result, 
            date: new Date().toLocaleDateString('en-US', {month: 'short', day: 'numeric', year: 'numeric'})
          });
          localStorage.setItem('ree_blogs', JSON.stringify(blogs));
          renderAdminList(blogs, 'blog-list', 'blog');
          e.target.reset();
          alert('Blog Post Published!');
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        alert("Please select an image.");
      }
    });

    // -- PORTFOLIO --
    document.getElementById('form-portfolio').addEventListener('submit', (e) => {
      e.preventDefault();
      const title = document.getElementById('pf-title').value;
      const category = document.getElementById('pf-cat').value;
      const fileInput = document.getElementById('pf-img');
      
      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          portfolio.unshift({
            title, category,
            image: evt.target.result
          });
          localStorage.setItem('ree_portfolio', JSON.stringify(portfolio));
          renderAdminList(portfolio, 'portfolio-list', 'portfolio');
          e.target.reset();
          alert('Portfolio Project Added!');
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        alert("Please select an image.");
      }
    });

    // -- SHOP --
    document.getElementById('form-shop').addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('shop-name').value;
      const price = document.getElementById('shop-price').value;
      const category = document.getElementById('shop-cat').value;
      const fileInput = document.getElementById('shop-img');
      
      if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          products.unshift({
            name, price, category,
            image: evt.target.result
          });
          localStorage.setItem('ree_products', JSON.stringify(products));
          renderAdminList(products, 'product-list', 'product');
          e.target.reset();
          alert('Product Added to Shop!');
        };
        reader.readAsDataURL(fileInput.files[0]);
      } else {
        alert("Please select an image.");
      }
    });

  }
});
