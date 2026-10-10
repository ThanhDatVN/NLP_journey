# Báo cáo đồ án mẫu: phân loại cảm xúc phản hồi sinh viên bằng PhoBERT

> **Mục đích của tài liệu này:** cho bạn thấy một báo cáo đồ án **đạt yêu cầu** trông thế nào, theo mẫu ở [DO_AN.md](DO_AN.md). Toàn bộ số liệu lấy từ Bài 10 và Bài 14 của giáo trình (một lần chạy, một seed, máy RTX 3050 4 GB), nên đây là **bài mẫu minh họa cấu trúc và độ trung thực**, chưa phải một đồ án hoàn chỉnh — phần 9 nêu rõ những thiếu sót để bạn không bắt chước chúng. Hãy đọc kèm các notebook tương ứng để thấy mã.

---

## 1. Bài toán và bối cảnh sử dụng

**Bài toán:** phân loại một câu phản hồi của sinh viên về giảng viên/chương trình đào tạo thành *tích cực / tiêu cực / trung tính*.

**Người dùng giả định:** bộ phận đảm bảo chất lượng của một khoa muốn **tổng hợp sơ bộ** hàng nghìn phản hồi cuối kỳ để biết nên *đọc kỹ* nhóm nào trước.

**Quyết định dựa vào đầu ra:** thứ tự ưu tiên đọc phản hồi — **không** dùng để chấm điểm giảng viên hay ra quyết định về con người.

**Sai thì ai chịu hậu quả:**

- Bỏ sót phản hồi tiêu cực → vấn đề nghiêm trọng bị đọc muộn (hậu quả vừa).
- Gán nhầm tiêu cực cho phản hồi tích cực → tốn công đọc thừa (hậu quả nhẹ).
- Dùng điểm số để đánh giá một giảng viên cụ thể → **ngoài phạm vi và không được phép** (hậu quả nặng, đã loại khỏi bài toán).

→ Ưu tiên **recall của lớp tiêu cực** và theo dõi lớp *trung tính* (hiếm, khó); luôn có con người đọc lại.

## 2. Dữ liệu

| Mục | Nội dung |
|---|---|
| Nguồn | UIT-VSFC (`uitnlp/vietnamese_students_feedback`), nạp từ Hugging Face Hub (nhánh `refs/convert/parquet`) |
| Giấy phép | thẻ ghi `unknown` → **chỉ dùng cho học tập/nghiên cứu, không phân phối lại**; kiểm tra điều khoản gốc trước khi dùng cách khác |
| Quy mô | train 11.426 · valid 1.583 · test 3.166 câu (chia sẵn của bộ dữ liệu) |
| Nhãn | tiêu cực / trung tính / tích cực |
| Phân phối nhãn | tích cực ≈ 49–51%, tiêu cực ≈ 45–47%, **trung tính ≈ 4–5%** (rất lệch) |
| Độ dài | trung bình ≈ 13,5 token PhoBERT; p99,5 = 55 → `MAX_LEN = 55` |
| Dữ liệu cá nhân | không thấy trong mẫu đọc; chưa quét tự động (hạn chế) |
| Kiểm tra chất lượng | đã đọc 12 lỗi "tự tin nhất" của mô hình: nhiều câu có **nhãn đáng ngờ** (ví dụ "dạy dễ hiểu, không bị rối" gán *tiêu cực*) → nhãn nhiễu đặt trần cho mọi mô hình |

Kiểm tra trùng/rò rỉ: **chưa làm** (xem phần 9).

## 3. Phương pháp

- **Baseline:** TF-IDF (1–2-gram, `min_df=2`, `sublinear_tf`) + Logistic Regression `C=10`, `class_weight="balanced"`.
- **Mô hình cải tiến:** PhoBERT-base (`vinai/phobert-base`, MIT) + đầu phân loại; tinh chỉnh 3 epoch, batch 32, lr 3e-5, warmup 10%, AdamW (weight decay 0,01), cắt gradient 1,0, fp16, seed 42, **chọn epoch tốt nhất theo macro-F1 trên valid**.
- **Tiền xử lý:** chuẩn hóa NFC; tách từ bằng bộ tách từ từ điển thuần Python của giáo trình (xấp xỉ RDRSegmenter — một nguồn lệch đã biết).
- **Phần cứng/phiên bản:** RTX 3050 Laptop 4 GB; PyTorch 2.14, Transformers 5.17; huấn luyện ≈ 3,4 phút, VRAM đỉnh ≈ 3,1 GB.

## 4. Kết quả (tập test, một lần mở)

| Mô hình | Accuracy | Macro-F1 | Macro-F1, khoảng tin cậy 95% (bootstrap test) |
|---|---|---|---|
| TF-IDF + LR | 0,883 | 0,721 | [0,696; 0,745] |
| **PhoBERT tinh chỉnh** | **0,941** | **0,840** | [0,815; 0,863] |
| Hiệu (PhoBERT − LR) | | | [0,092; 0,146]; PhoBERT hơn ở 100% lần lấy mẫu |

Theo từng lớp (PhoBERT):

| Lớp | Precision | Recall | F1 | Số mẫu |
|---|---|---|---|---|
| tiêu cực | 0,948 | 0,967 | 0,957 | 1.409 |
| trung tính | 0,719 | **0,521** | 0,604 | 167 |
| tích cực | 0,952 | 0,963 | 0,957 | 1.590 |

**Đọc kết quả:** PhoBERT hơn baseline rõ rệt và khoảng tin cậy của hiệu không chứa 0. Nhưng accuracy 0,94 **che giấu** việc lớp *trung tính* bị bỏ sót gần một nửa (recall 0,52). Khoảng tin cậy trên chỉ phản ánh độ bất định do **cỡ tập test**, không phản ánh biến thiên do seed.

## 5. Phân tích lỗi

- **Nhãn đáng ngờ / quy ước riêng:** phần lớn 12 lỗi tự tin nhất là "thật: trung tính, đoán: tích cực" cho câu nghe như lời khen ("giảng dạy thực tế", "sự tận tình"), hoặc nhãn tiêu cực cho câu khen. Nghĩa là lỗi nằm một phần ở **dữ liệu**, không chỉ ở mô hình.
- **Lớp trung tính:** hiếm (≈5%) và định nghĩa mơ hồ → recall thấp.
- **Hướng sửa đề xuất:** (1) rà soát thủ công ~100 mẫu nhãn nghi sai nhất và sửa/loại; (2) thử `class_weight`/lấy mẫu lại cho lớp trung tính, báo cáo cả precision/recall đánh đổi; (3) mô tả rõ quy ước nhãn trung tính cho người gán nhãn.

## 6. Kiểm thử ngoài phân phối và hành vi

**Ngoài miền (40 câu đánh giá sản phẩm viết tay, `data/reviews_hard.csv`):**

| Mô hình (huấn luyện trên UIT-VSFC) | Accuracy | Macro-F1 |
|---|---|---|
| TF-IDF + LR | 0,450 | 0,386 |
| PhoBERT | 0,625 | 0,611 |

Cả hai **tụt mạnh** so với trong miền (0,94 / 0,88). PhoBERT chuyển miền tốt hơn nhưng vẫn yếu ở *phủ định của từ tiêu cực* (≈ 1/4 đúng), mỉa mai và câu lưỡng lự. Cỡ mẫu 40 → chỉ mang tính gợi ý.

**Thiên kiến (thử nghiệm phản thực tế, 6 mẫu câu):** thay "Thầy/Cô", "miền Bắc/Trung/Nam", "trẻ/lớn tuổi" trong cùng mẫu câu khen/chê giảng viên, chênh lệch lớn nhất của xác suất nhãn đúng ≤ 0,002. **Không thấy thiên kiến lớn ở các mẫu này** — nhưng chỉ thử vài mẫu câu *rõ ràng* (từ cảm xúc rất mạnh); chưa thử câu mơ hồ.

## 7. Rủi ro, giới hạn, khi nào KHÔNG nên dùng

- **Không dùng** để đánh giá, xếp hạng hay kỷ luật một giảng viên/sinh viên cụ thể.
- **Không dùng** cho văn bản ngoài miền giáo dục mà không kiểm tra lại (điểm tụt từ 0,94 xuống 0,63 ở miền sản phẩm).
- Lớp *trung tính* bị bỏ sót nhiều → đừng dùng "không có phản hồi trung tính" như một kết luận.
- Độ tin cậy softmax **chưa hiệu chuẩn**; đừng dùng như xác suất.
- Quyền riêng tư: dữ liệu phản hồi có thể chứa thông tin định danh; nếu triển khai thật phải che PII trước khi lưu/log (mẫu ở Bài 14).
- An ninh: không có thành phần LLM nên không có rủi ro prompt injection, nhưng API công khai cần giới hạn đầu vào và tần suất.

## 8. Tái lập và sản phẩm

- Mã: Bài 10 (`notebooks/10_phobert_tinh_chinh.ipynb`); seed 42; phiên bản thư viện ghi trong `README.md`.
- Mô hình lưu ở `outputs/phobert-cam-xuc/` (không đưa lên git; ≈ 0,5 GB) kèm **thẻ mô hình** `README.md` sinh tự động (nguồn dữ liệu, siêu tham số, kết quả, giới hạn).
- Tùy chọn triển khai: bọc bằng `app/api.py`/`app/demo_gradio.py` (đổi lõi dự đoán sang PhoBERT như hướng dẫn ở `app/du_doan.py`).

## 9. Điều không như mong đợi, thiếu sót và bài học

**Không như mong đợi:**

- Lớp trung tính khó hơn nhiều so với dự tính; accuracy rất cao nhưng macro-F1 chỉ 0,84.
- Nhiều lỗi "của mô hình" hóa ra là **nhãn đáng ngờ** — đáng đầu tư vào dữ liệu hơn là đổi kiến trúc.
- Chỉ số "trong miền" gần như không nói gì về chất lượng ngoài miền.

**Thiếu sót của bài mẫu này (đừng bắt chước):**

- **Chỉ một seed** → chưa biết biến thiên do huấn luyện; đồ án thật cần ≥ 3 seed và báo cáo mean ± std.
- **Chưa kiểm tra trùng/rò rỉ** giữa train/valid/test của UIT-VSFC.
- **Chưa quét PII** trên dữ liệu.
- Bộ tách từ không phải RDRSegmenter; chưa đo mức ảnh hưởng.
- Tập "ngoài miền" chỉ 40 câu do giáo trình tự viết, và cũng là tập được nhìn lại nhiều lần trong bài học.
- Chưa hiệu chuẩn độ tin cậy, chưa có kiểm thử CheckList riêng cho miền giáo dục.

## Tự chấm theo rubric ([DO_AN.md](DO_AN.md), mục 3)

| Tiêu chí | Điểm | Lý do |
|---|---|---|
| Dữ liệu | 1 | có nguồn, giấy phép (không rõ), chia tập; **thiếu** kiểm tra trùng/rò rỉ và quét PII |
| Baseline | 1 | có TF-IDF + LR; **thiếu** nhiều baseline/nhiều seed |
| Đánh giá | 2 | macro-F1, theo lớp, khoảng tin cậy, phép thử ngoài miền (việc thiếu nhiều seed đã bị trừ ở tiêu chí Baseline) |
| Phân tích lỗi | 2 | phân loại nguyên nhân (nhãn nghi sai / lớp hiếm), có hướng sửa |
| Rủi ro & đạo đức | 1 | có nêu và đo sơ bộ thiên kiến; **thiếu** thử câu mơ hồ, chưa đo riêng tư |
| Tái lập & sản phẩm | 2 | có seed, phiên bản, thẻ mô hình; demo tùy chọn |
| **Tổng** | **9 / 12** | |

> Cách tự chấm trung thực — chỉ ra rõ chỗ mình còn thiếu — là một phần của yêu cầu "đánh giá trung thực". Một báo cáo 9/12 *tự nhận biết đúng* điểm yếu của mình đáng tin hơn một báo cáo tự nhận 12/12.
