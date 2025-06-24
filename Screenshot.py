import keyboard
import pyautogui
import time
import os
import sys
import tkinter as tk 
import pyperclip
import API # <<< THAY ĐỔI: Import cả module API
from Mainternance import MaintenanceWindow, CustomAlert

captured_images = []
image_counter = 0

# <<< THÊM MỚI: Hàm để lấy đường dẫn chính xác khi chạy file .exe >>>
def get_base_path():
    """Lấy đường dẫn cơ sở, hoạt động cho cả môi trường dev và PyInstaller."""
    if getattr(sys, 'frozen', False):
        # Nếu đang chạy dưới dạng file .exe đã đóng gói
        return os.path.dirname(sys.executable)
    else:
        # Nếu đang chạy file .py thông thường
        return os.path.dirname(os.path.abspath(__file__))

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
        # <<< THAY ĐỔI: Gọi hàm API_Main thông qua module đã import >>>
        API.API_Main(captured_images)
    except Exception as e:
        print(f"\n!!! Lỗi khi gửi đến AI: {e}")
    finally:
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
    Screen_Main()