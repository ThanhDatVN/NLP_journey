"""Demo giao diện web bằng Gradio (tương ứng Chương 9 khóa Hugging Face).

Chạy:   python app/demo_gradio.py     (mở http://127.0.0.1:7860)
Yêu cầu: pip install -r app/requirements-app.txt
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Riêng tư theo mặc định: tắt dữ liệu phân tích ẩn danh/kiểm tra phiên bản của Gradio (đặt biến này TRƯỚC khi import gradio).
os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")

import gradio as gr  # noqa: E402

from app.du_doan import predict  # noqa: E402


def phan_loai(van_ban: str):
    if not van_ban or not van_ban.strip():
        return {}, "Hãy nhập một đánh giá."
    kq = predict(van_ban)
    ghi_chu = (f"Dự đoán: **{kq['nhan']}** (độ tin cậy {kq['do_tin_cay']:.0%}). "
               "Độ tin cậy là điểm của mô hình, không phải xác suất đã hiệu chuẩn.")
    return kq["xac_suat"], ghi_chu


demo = gr.Interface(
    fn=phan_loai,
    inputs=gr.Textbox(lines=3, label="Đánh giá của khách hàng", placeholder="Ví dụ: Giao hàng nhanh, đóng gói cẩn thận."),
    outputs=[gr.Label(label="Xác suất theo lớp"), gr.Markdown()],
    examples=[["Giao hàng nhanh, đóng gói cẩn thận, rất hài lòng!"], ["Ứng dụng hay treo, thất vọng quá."],
              ["Mình mới nhận hàng nên chưa đánh giá được."]],
    title="Phân loại cảm xúc đánh giá tiếng Việt",
    description="Demo giáo trình NLP. Mô hình học trên dữ liệu tổng hợp nhỏ — **không dùng để ra quyết định thật**.",
    flagging_mode="never",
)

if __name__ == "__main__":
    demo.launch()
