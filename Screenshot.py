import keyboard
import pyautogui
import time
import os
import sys
import tkinter as tk 
import pyperclip
import API # <<< THAY ĐỔI: Import cả module API
from Mainternance import MaintenanceWindow, CustomAlert
from Mainternance import window_maintenance
import requests
captured_images = []
image_counter = 0
from dotenv import load_dotenv, dotenv_values
import pkgutil
import traceback
import time

def get_base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable) 
    else:
        return os.path.dirname(os.path.abspath(__file__))

env_path = os.path.join(get_base_path(), ".env")
def load_embedded_env():
    if getattr(sys, 'frozen', False):
        try:
            env_path = os.path.join(sys._MEIPASS, ".env")
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip() and not line.startswith("#"):
                            key, value = line.strip().split("=", 1)
                            os.environ[key] = value
        except Exception as e:
            print(f"⚠️ Không thể đọc .env từ exe: {e}")
    else:
        load_dotenv()


load_embedded_env()

class RegionSelector:
    """Lớp giao diện đồ họa để chọn vùng màn hình (Không thay đổi)."""
    def __init__(self, root):
        self.root = root
        self.x = self.y = 0
        self.rect = None
        self.start_x = self.start_y = 0
        self.canvas = tk.Canvas(root, cursor="cross", bg='grey75')
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=2)

    def on_mouse_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.root.quit()

def capture_selected_region():
    """Chụp một vùng màn hình và thêm vào danh sách chờ."""
    global image_counter
    print(f"\n[{time.strftime('%H:%M:%S')}] Đã nhấn 'Ctrl+B'. Vui lòng kéo chuột để chọn vùng cần chụp...")

    root = tk.Tk()
    root.attributes("-alpha", 0.01) 
    root.attributes("-fullscreen", True)
    root.wait_visibility(root) 

    selector = RegionSelector(root)
    root.mainloop() 
    root.destroy() 

    x1 = min(selector.start_x, selector.end_x)
    y1 = min(selector.start_y, selector.end_y)
    x2 = max(selector.start_x, selector.end_x)
    y2 = max(selector.start_y, selector.end_y)

    width = x2 - x1
    height = y2 - y1

    if width <= 10 or height <= 10:
        print("-> Vùng chọn quá nhỏ. Đã hủy thao tác.")
        return

    try:
        time.sleep(0.2)
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))

        # <<< THAY ĐỔI: Tạo thư mục Data bên cạnh file .exe hoặc .py >>>
        folder_name = os.path.join(get_base_path(), "Data")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Lưu với tên duy nhất và thêm vào danh sách
        file_name = f"image_question_{image_counter}.png"
        file_path = os.path.join(folder_name, file_name)
        screenshot.save(file_path)

        captured_images.append(file_path)
        image_counter += 1

        print(f"-> Đã lưu ảnh thành công: {os.path.abspath(file_path)}")
        print(f"-> Tổng số ảnh đã chụp: {len(captured_images)}. Nhấn 'Ctrl+G' để gửi, hoặc 'Ctrl+B' để thêm ảnh.")

    except Exception as e:
        print(f"\n!!! Đã có lỗi xảy ra khi chụp ảnh: {e}")

def process_and_send_to_api():
    """Gửi tất cả ảnh đã chụp đến AI và xóa danh sách chờ."""
    global captured_images, image_counter
    if not captured_images:
        print(f"\n[{time.strftime('%H:%M:%S')}] Chưa có ảnh nào được chụp. Vui lòng nhấn 'Ctrl+B' để chụp ảnh trước.")
        return

    print(f"\n[{time.strftime('%H:%M:%S')}] Đã nhấn 'Ctrl+G'. Đang tổng hợp {len(captured_images)} ảnh và gửi đến AI...")

    try:
        API.API_Main(captured_images)
    except Exception as e:
        print(f"\n!!! Lỗi khi gửi đến AI: {e}")
    finally:
        try:
            print("-> Tác vụ hoàn tất, di chuyển con trỏ chuột về giữa màn hình.")
            screenWidth, screenHeight = pyautogui.size() # Lấy kích thước màn hình
            centerX, centerY = screenWidth / 2, screenHeight / 2 # Tính tọa độ trung tâm
            pyautogui.moveTo(centerX, centerY, duration=0.25) # Di chuyển chuột tới trung tâm
        except Exception as e_move:
            print(f"!!! Lỗi khi di chuyển chuột: {e_move}")
        
        print(f"\n[{time.strftime('%H:%M:%S')}] Hoàn tất! Đang chờ lệnh tiếp theo ('Ctrl+B' hoặc 'Ctrl+C').")
        captured_images = []
        image_counter = 0

def exit_program():
    """Hàm để thoát chương trình."""
    print("\n-----------------------------------------------------")
    print("Đã nhận lệnh thoát 'Ctrl+C'. Tạm biệt!")
    os._exit(0)

def Screen_Main():
    """Hàm chính, đăng ký các phím tắt."""
    print("\nChương trình đang chạy...")
    print("- Nhấn 'Ctrl+B' để chọn vùng và chụp ảnh.")
    print("- Nhấn 'Ctrl+G' để gửi các ảnh đã chụp cho AI.")
    print("- Nhấn 'Ctrl+C' để thoát chương trình.")
    
    keyboard.add_hotkey('ctrl+b', capture_selected_region)
    keyboard.add_hotkey('ctrl+g', process_and_send_to_api)
    keyboard.add_hotkey('ctrl+c', exit_program)

    keyboard.wait()

if __name__ == "__main__":
    try:
        response = requests.get("https://demo-backend-byp9.onrender.com/view_status", timeout=15)
        data = response.json()
        status = data.get("status")

        if status == "maintain":
            Screen_Main()
        elif status == "maintenance":
            window_maintenance()
        else:
            print("⚠️ Lỗi không xác định trạng thái.")
    except Exception as e:
        traceback.print_exc()
        print(f"❌ Không kết nối được tới server: {e}")