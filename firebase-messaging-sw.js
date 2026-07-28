importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');

const firebaseConfig = {
  apiKey: "AIzaSyA0CCQzLvA4pZc_fJJSzN6V98IwN9TfofY",
  authDomain: "royal-executive-empire-ree.firebaseapp.com",
  databaseURL: "https://royal-executive-empire-ree-default-rtdb.firebaseio.com",
  projectId: "royal-executive-empire-ree",
  storageBucket: "royal-executive-empire-ree.firebasestorage.app",
  messagingSenderId: "933257264677",
  appId: "1:933257264677:web:d5ee8e282f819cf39a89cc"
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = payload.notification.title || payload.data.title || 'New Notification';
  const notificationOptions = {
    body: payload.notification.body || payload.data.message || 'You have a new alert from REEL.',
    icon: '/Images/icons/icon-192x192.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
