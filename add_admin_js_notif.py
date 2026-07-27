import os

def update_admin_js_notifications():
    file_path = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web\admin\js\admin.js"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    notif_logic = """
    // -- PUSH NOTIFICATIONS --
    const notifForm = document.getElementById('form-notification');
    if(notifForm) {
      notifForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = document.getElementById('notif-title').value;
        const body = document.getElementById('notif-body').value;
        
        if (window.db) {
          window.db.collection('notifications').add({
            title: title,
            message: body,
            timestamp: Date.now()
          }).then(() => {
            alert('Broadcast Sent Successfully!');
            e.target.reset();
          }).catch(err => {
            console.error(err);
            alert('Failed to send notification: ' + err.message);
          });
        } else {
          alert('Firebase not connected! Cannot send broadcast.');
        }
      });
    }
    """
    
    # Check if Firebase is initialized in admin.js
    firebase_init = """
    // Initialize Firebase in Admin if not present
    if (typeof firebase !== 'undefined' && !window.db) {
        window.db = firebase.firestore();
    }
    """

    if 'form-notification' not in content:
        content = content.replace("  }\n});", notif_logic + "\n  }\n});")
        content = content.replace("// 4. Initialize Data Arrays", firebase_init + "\n    // 4. Initialize Data Arrays")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated admin.js with push notifications")

if __name__ == "__main__":
    update_admin_js_notifications()
