import os

def update_notifications_js():
    file_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\js\notifications.js"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_permission_logic = """
  // Handle Permissions & FCM Token
  if (enableBtn) {
    if (Notification.permission === 'granted') {
      enableBtn.style.display = 'none';
      // If already granted, ensure token is refreshed/saved silently
      if(typeof firebase !== 'undefined' && firebase.messaging) {
        setTimeout(() => {
          try {
            const messaging = firebase.messaging();
            messaging.getToken({ vapidKey: 'BEp5FxDvfKevIU0clBfu5PRO2KfraAcW1q133smI_WDUh0NqzMTMP47Iwl3nKyxO-vJXGnequLXbylrB1qSWvJg' }).then((currentToken) => {
              if (currentToken && window.db) {
                window.db.collection('subscribers').doc(currentToken).set({ token: currentToken, lastActive: Date.now() }, {merge: true});
              }
            }).catch(e => console.log('FCM token error:', e));
          } catch(e) {}
        }, 2000);
      }
    } else if (Notification.permission === 'denied') {
      enableBtn.textContent = 'Blocked';
      enableBtn.style.opacity = '0.5';
      enableBtn.disabled = true;
    }
    
    enableBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      Notification.requestPermission().then(perm => {
        if (perm === 'granted') {
          enableBtn.style.display = 'none';
          
          if(typeof firebase !== 'undefined' && firebase.messaging) {
            const messaging = firebase.messaging();
            messaging.getToken({ vapidKey: 'BEp5FxDvfKevIU0clBfu5PRO2KfraAcW1q133smI_WDUh0NqzMTMP47Iwl3nKyxO-vJXGnequLXbylrB1qSWvJg' }).then((currentToken) => {
              if (currentToken) {
                if (window.db) {
                  window.db.collection('subscribers').doc(currentToken).set({ token: currentToken, timestamp: Date.now() }, {merge: true});
                }
                new Notification("REEL", { body: "Push notifications enabled!", icon: "/Images/icons/icon-192x192.png" });
              }
            }).catch((err) => {
              console.log('An error occurred while retrieving token. ', err);
            });
          } else {
             new Notification("REEL", { body: "Push notifications enabled!", icon: "/Images/icons/icon-192x192.png" });
          }
          
        } else {
          enableBtn.textContent = 'Blocked';
          enableBtn.disabled = true;
        }
      });
    });
  }
"""
    
    # Replace the old handle permissions block
    parts = content.split('// Handle Permissions')
    if len(parts) > 1:
        part2 = parts[1].split('// Fetch from Firestore', 1)
        if len(part2) > 1:
            content = parts[0] + new_permission_logic + '  // Fetch from Firestore' + part2[1]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_notifications_js()
