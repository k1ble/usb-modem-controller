import tkinter as tk
import threading
from PIL import Image
import pystray
from pystray import MenuItem as item

from logger import logger
from adb_core import get_full_status, run_RND, run_USB_reset, run_MTP, get_target_mode


def show_window(icon=None, item=None):
    root.after(0, root.deiconify)
    
def quit_app(icon=None, item=None):
    root.quit()

  
def create_tray_icon():
    
    width = 32
    height = 32
    image = Image.new('RGB', (width, height), '#00ff00')
    return image

def run_tray():
    image = create_tray_icon()
    menu = (
        item('show window', show_window),
        item('run modem-connect', run_RND),
        item('exit', quit_app)
    )
    icon = pystray.Icon("check", image, "USB connecting", menu)
    icon.run() 


def hide_window():
    root.withdraw()
    if not hasattr(root, 'tray_thread') or not root.tray_thread.is_alive():
        root.tray_thread = threading.Thread(target=run_tray, daemon=True)
        root.tray_thread.start()

root = tk.Tk()     
status_label = tk.Label(root, text="Статус: ожидание", font=("Arial", 10))
status_label.pack()
root.title("usb modem controller")
root.geometry("400x300")
root.protocol("WM_DELETE_WINDOW", hide_window)

btn = tk.Button(root, text="enable modem", command=run_RND)
btnMTP = tk.Button(root, text = "enable mtp", command= run_MTP)
reset_btn = tk.Button(root, text = "reset USB", command=run_USB_reset)

prev_connect = False
def update_loop():
    def soworker():
        global prev_connect
        status = get_full_status()
        
        if status["connect"]:
            if not prev_connect:
                logger.info("device connected...")
                mode = get_target_mode()
                if mode == 'rndis':
                    run_RND()
                elif mode == 'mtp':
                    run_MTP()
                    
            status_label.config(text=f"Подключено: {status['mode']}")
            prev_connect = True
        else:
            if prev_connect:
                logger.info("device disconnected...")
            status_label.config(text="Отключено")
            prev_connect = False
    
    threading.Thread(target = soworker, daemon=True).start()
    root.after(2000, update_loop)  

btn.pack(side= "top")
btnMTP.pack()
reset_btn.pack()

if __name__ == "__main__":
    update_loop()
    root.mainloop()