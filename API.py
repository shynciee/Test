import google.generativeai as A
import os
from dotenv import load_dotenv
from PIL import Image
import pyperclip
import time
import sys 

def get_base_path():
    """Lấy đường dẫn cơ sở, hoạt động cho cả môi trường dev và PyInstaller."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def API_Main(image_paths):

    dotenv_path = os.path.join(get_base_path(), '.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("Lỗi: Không tìm thấy GOOGLE_API_KEY. Hãy chắc chắn tệp .env tồn tại cùng với file chạy.")
        input("Nhấn Enter để thoát.") 
        return

    try:
        A.configure(api_key=api_key)
        print("✅ Cấu hình API thành công!")

        content_for_api = []

        question = "Nhìn vào các ảnh này, giải bài tập và làm theo các bước sau một cách cẩn thận cho từng ảnh/câu hỏi:" \
                   "Đọc và phân tích phát biểu A, giải thích nó đúng hay sai. " \
                   "Đọc và phân tích phát biểu B, giải thích nó đúng hay sai. " \
                   "Đọc và phân tích phát biểu C, giải thích nó đúng hay sai. " \
                   "Đọc và phân tích phát biểu D, giải thích nó đúng hay sai. " \
                   "Từ đó, đưa ra kết luận cuối cùng cho câu hỏi. " \
                   "Sau khi giải xong tất cả các câu hỏi trong tất cả các ảnh, hãy tóm tắt câu trả lời cho từng câu là đáp án nào (ví dụ: Câu 1 đáp án A, Câu 2 đáp án B)."
        
        content_for_api.append(question)

        for image_path in image_paths:
            try:
                picture = Image.open(image_path)
                content_for_api.append(picture)
            except FileNotFoundError:
                print(f"❌ Lỗi: Không tìm thấy file tại đường dẫn: {image_path}. Bỏ qua ảnh này.")
                continue
            except Exception as e:
                print(f"❌ Lỗi khi mở ảnh {image_path}: {e}. Bỏ qua ảnh này.")
                continue
        
        if len(content_for_api) <= 1:
            print("Không có ảnh hợp lệ nào để gửi đến AI.")
            return

        print(f"Đang gửi {len(image_paths)} ảnh đến AI... Vui lòng chờ.")
        model = A.GenerativeModel('gemini-2.5-flash')
        start_time = time.time()
        response = model.generate_content(content_for_api)
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("\n--- Câu trả lời ---")
        print(f"✅ AI đã trả lời xong sau {elapsed_time:.2f} giây.")
        
        print(response.text)
        pyperclip.copy(response.text)

    except Exception as e:
        print(f"❌ Đã xảy ra lỗi không mong muốn trong quá trình xử lý API: {e}")
        input("Nhấn Enter để thoát.") 

if __name__ == "__main__":
    print("Đây là tệp API, nó nên được gọi từ tệp Screenshot.py.")