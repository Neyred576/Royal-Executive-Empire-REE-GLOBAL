import os
import glob

def inject_fcm_script():
    directory = r"c:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\Web"
    html_files = glob.glob(os.path.join(directory, "**", "*.html"), recursive=True)
    
    fcm_script = '<script src="https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js"></script>'
    init_script = '<script src="js/firebase-init.js"></script>'
    init_script_alt = '<script src="../js/firebase-init.js"></script>'
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'firebase-messaging-compat' not in content:
            if init_script in content:
                content = content.replace(init_script, fcm_script + '\n  ' + init_script)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Injected FCM into {file_path}")
            elif init_script_alt in content:
                content = content.replace(init_script_alt, fcm_script + '\n  ' + init_script_alt)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Injected FCM into {file_path}")

if __name__ == "__main__":
    inject_fcm_script()
