// Firebase initialization (Compat version for standard script tags)
const firebaseConfig = {
  apiKey: "AIzaSyA0CCQzLvA4pZc_fJJSzN6V98IwN9TfofY",
  authDomain: "royal-executive-empire-ree.firebaseapp.com",
  projectId: "royal-executive-empire-ree",
  storageBucket: "royal-executive-empire-ree.firebasestorage.app",
  messagingSenderId: "933257264677",
  appId: "1:933257264677:web:d5ee8e282f819cf39a89cc"
};

// Initialize Firebase
if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

// Export database and storage to global window object
window.db = firebase.firestore();
window.storage = firebase.storage();
