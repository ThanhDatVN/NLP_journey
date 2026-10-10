# Đồ án cuối khóa

Đồ án là cơ hội áp dụng **cả quy trình** của khóa học vào một bài toán nhỏ có thật — đề cao *độ trung thực của đánh giá* hơn là điểm số cao.

> Muốn thấy một báo cáo đạt yêu cầu trông thế nào? Xem [DO_AN_MAU.md](DO_AN_MAU.md) (bài mẫu, kèm tự chấm trung thực theo rubric).

## 1. Chọn đề tài

Chọn **một** bài toán có nhãn hoặc tiêu chí đánh giá rõ ràng, quy mô vừa sức (một người, 3–4 tuần). Gợi ý:

| # | Đề tài | Baseline gợi ý | Cải tiến gợi ý | Độ đo chính |
|---|---|---|---|---|
| 1 | Phân loại **cảm xúc** đánh giá/phản hồi trong một miền (nhà hàng, giáo dục, ứng dụng...) | TF-IDF + LR | PhoBERT (Bài 10) | macro-F1, theo lớp, khác miền |
| 2 | Phân loại **chủ đề / ý định** (tin tức, câu hỏi chatbot) | TF-IDF + LR/SVM | PhoBERT, embedding E5 + LR | macro-F1, confusion matrix |
| 3 | **NER** cho một miền (y tế, hành chính, thương mại) | luật + từ điển | PhoBERT token classification (Bài 11) | entity-F1 theo loại |
| 4 | **Hỏi–đáp FAQ có RAG** cho tài liệu công khai của một tổ chức | BM25 | hybrid + LLM cục bộ (Bài 12–13) | Hit@k/MRR, đúng/từ chối, injection |
| 5 | **Phát hiện câu trùng/gần nghĩa** (gộp ticket, câu hỏi lặp) | TF-IDF cosine | embedding E5/bkai | Precision@k, PR-curve |
| 6 | **Trích xuất thông tin** từ văn bản bán cấu trúc (hóa đơn, thông báo) với che PII | regex | NER + regex | entity-F1, PII recall |
| 7 | *Nghiên cứu nhỏ:* tác động của **tiền xử lý tiếng Việt** (bỏ dấu, tách từ, tokenizer) lên chất lượng | một cấu hình cố định | thay đổi từng yếu tố | CV nhiều seed + khoảng tin cậy |
| 8 | *Nghiên cứu nhỏ:* **thiên kiến** của một mô hình tiếng Việt qua thử nghiệm phản thực tế | — | bộ mẫu câu + bootstrap | chênh lệch + khoảng tin cậy |
| 9 | *So sánh chi phí–chất lượng:* LLM nhỏ cục bộ (zero-shot, **LoRA** — Bài 15) vs PhoBERT tinh chỉnh vs TF-IDF trên cùng một bài toán; có thể thêm lượng tử hóa | TF-IDF | PhoBERT, LLM zero/few-shot, LoRA | chất lượng (theo lớp), độ trễ, chi phí, bộ nhớ |
| 10 | *Dữ liệu nhãn:* với một bộ có nhãn bạn chọn, vẽ **đường cong học**, so **học tích cực** / **nhãn yếu** với chọn ngẫu nhiên ở cùng ngân sách, và rà soát danh sách **nhãn nghi sai** (Bài 16) | chọn mẫu ngẫu nhiên | học tích cực, hàm gán nhãn, làm sạch nhãn | macro-F1 theo số nhãn (nhiều seed), κ, số nhãn tiết kiệm được |
| 11 | **Khôi phục dấu** cho một miền cụ thể (tin nhắn, ticket, mạng xã hội) và đo tác động lên bước sau (tìm kiếm hoặc phân loại) (Bài 17) | dạng phổ biến nhất | n-gram + Viterbi, thêm văn bản cùng miền, mô hình thần kinh | độ chính xác token/câu trong và ngoài miền, chất lượng bước sau |
| 12 | **Khám phá dữ liệu không nhãn:** phân cụm + mô hình chủ đề cho một kho phản hồi; đặt tên cụm và *kiểm chứng* bằng nhãn tham chiếu hoặc người đọc (Bài 18) | k-means TF-IDF | embedding + c-TF-IDF, LDA/NMF | NMI/ARI, độ ổn định, NPMI, đồng thuận đặt tên |
| 13 | **Tóm tắt hoặc dịch** trong một miền hẹp, đánh giá bằng độ đo tự động *và* đánh giá thủ công có kiểm tra tính trung thực (Bài 19) | câu đầu / mô hình dịch có sẵn | LLM nhỏ + prompt, mô hình chuyên dụng | ROUGE/BLEU/chrF kèm khoảng tin cậy, tỉ lệ lỗi sai ý khi đọc mẫu |

Bạn có thể đề xuất đề tài khác nếu có (a) dữ liệu hợp pháp, (b) cách đánh giá rõ ràng, (c) giảng viên/người hướng dẫn đồng ý.

### Về dữ liệu

- Ưu tiên dữ liệu công khai có **giấy phép rõ ràng** cho mục đích của bạn. Trên [Hugging Face Hub](https://huggingface.co/datasets?language=language:vi) có nhiều bộ dữ liệu tiếng Việt, nhưng **chất lượng và giấy phép rất khác nhau** (nhiều bộ ghi `unknown`): bạn phải tự đọc thẻ dữ liệu, kiểm tra nguồn gốc và điều khoản.
- Hai bộ dữ liệu thật đã dùng trong khóa học: UIT-VSFC (cảm xúc và chủ đề; Bài 10, 15–18) và bản sao PhoNER_COVID19 (NER, Bài 11; văn bản tin tức cho Bài 17); cả hai đều cần kiểm tra điều khoản gốc trước khi dùng ngoài mục đích học tập. Các bộ `data/tom_tat_mini.json` và `data/dich_mini.json` (Bài 19) rất nhỏ và hư cấu: chỉ để học cách đo, không dùng để tuyên bố chất lượng.
- **Tự thu thập dữ liệu**: chỉ khi có quyền hợp pháp; **không** thu thập dữ liệu cá nhân, không vi phạm điều khoản của trang web; che PII trước khi lưu; ghi lại cách thu thập.
- **Không** dùng `data/reviews_vi.csv` (tổng hợp) để tuyên bố chất lượng thực tế.

## 2. Yêu cầu nộp

1. **Mô tả bài toán**: ai dùng, quyết định nào dựa vào đầu ra, **sai thì ai chịu hậu quả**.
2. **Dữ liệu**: nguồn, giấy phép/quyền sử dụng, nhãn và cách gán, **kiểm tra trùng lặp/rò rỉ**, dữ liệu cá nhân, cách chia train/valid/test (và vì sao).
3. **Baseline đơn giản** (ít nhất một mô hình TF-IDF/luật/BM25) và **một cải tiến** (PhoBERT, embedding, RAG...), kèm ghi rõ checkpoint, phiên bản, seed, bước tiền xử lý/tách từ.
4. **Đánh giá trung thực**: độ đo phù hợp với bài toán (macro-F1, entity-F1, Recall@k...), **khoảng tin cậy** hoặc nhiều seed, **phân tích lỗi** có ví dụ, và **ít nhất một phép thử ngoài phân phối** (dữ liệu khác miền/tập câu khó/bộ CheckList).
5. **Rủi ro**: thiên kiến (đã đo hay chỉ nêu?), quyền riêng tư, an ninh (nếu có LLM/RAG: prompt injection), các tình huống **không nên dùng** hệ thống.
6. **Sản phẩm tái lập được**: mã chạy lại từ đầu (hoặc script + hướng dẫn), `requirements`, seed; **thẻ mô hình** (mẫu ở Bài 14, mục 8); tùy chọn: demo Gradio hoặc API (Bài 14).
7. **Báo cáo ngắn** (3–6 trang): tóm tắt các mục trên, nêu **điều không như mong đợi** và **giới hạn**.

## 3. Tiêu chí chấm (tự đánh giá trước khi nộp)

Mỗi tiêu chí 0 – 1 – 2 điểm (tối đa 12 điểm; quy đổi sang thang của lớp):

| Tiêu chí | 0 – Thiếu | 1 – Cơ bản | 2 – Tốt |
|---|---|---|---|
| **Dữ liệu** | không rõ nguồn/giấy phép | có nguồn; chia train/valid/test | + kiểm tra trùng/rò rỉ, riêng tư, thẻ dữ liệu |
| **Baseline** | không có | có TF-IDF/luật/BM25 | + so sánh nhiều baseline qua nhiều seed |
| **Đánh giá** | chỉ accuracy | macro-F1 (hoặc độ đo phù hợp) + confusion matrix | + khoảng tin cậy, ngoài phân phối, kiểm thử hành vi |
| **Phân tích lỗi** | không | liệt kê vài lỗi | + phân loại lỗi, nguyên nhân, đề xuất sửa/kiểm tra nhãn |
| **Rủi ro & đạo đức** | không | nêu rủi ro | + **đo** thiên kiến/riêng tư, biện pháp giảm thiểu |
| **Tái lập & sản phẩm** | khó chạy lại | có mã + requirements | + seed, phiên bản, thẻ mô hình, demo/API |

**Điểm cộng** (tối đa +2): phát hiện và **báo cáo trung thực một kết quả âm tính** (ví dụ mô hình lớn không thắng baseline); tự viết bộ kiểm thử mới; đóng góp lại một lỗi/cải tiến cho giáo trình.

## 4. Những điều **không** được làm

- Chọn mô hình/siêu tham số bằng tập **test**; mở test nhiều lần.
- Báo cáo điểm trên dữ liệu tổng hợp hoặc dữ liệu có rò rỉ như thể là chất lượng thực tế.
- Giấu hoặc bỏ qua kết quả không như mong đợi.
- Đưa dữ liệu cá nhân vào repo, nhật ký hoặc prompt gửi dịch vụ bên ngoài.
- Dùng mô hình/dữ liệu mà không đọc giấy phép (đặc biệt AGPL/CC-BY-NC).

## 5. Lịch trình gợi ý (4 tuần)

| Tuần | Việc | Sản phẩm |
|---|---|---|
| 1 | chọn đề tài, tìm dữ liệu, đọc giấy phép, kiểm tra dữ liệu (Bài 0–1), chia tập | 1 trang đề cương + thống kê dữ liệu + lược đồ chia tập |
| 2 | baseline + đánh giá đúng (Bài 2–3) | notebook baseline, bảng điểm có khoảng tin cậy |
| 3 | mô hình cải tiến (Bài 9–13), phân tích lỗi | notebook + 10 lỗi được phân tích |
| 4 | kiểm thử hành vi/thiên kiến/riêng tư (Bài 14), thẻ mô hình, báo cáo, (tùy chọn) demo | báo cáo + repo tái lập + thẻ mô hình |

## 6. Mẫu cấu trúc báo cáo

```text
1. Bài toán và bối cảnh sử dụng (ai dùng, sai thì sao)
2. Dữ liệu (nguồn, giấy phép, nhãn, chia tập, kiểm tra chất lượng, riêng tư)
3. Phương pháp (baseline, mô hình cải tiến, siêu tham số, phần cứng, phiên bản)
4. Kết quả (bảng + khoảng tin cậy; biểu đồ)
5. Phân tích lỗi (loại lỗi, ví dụ, nguyên nhân)
6. Kiểm thử ngoài phân phối / hành vi / thiên kiến
7. Rủi ro, giới hạn, khi nào KHÔNG nên dùng
8. Tái lập (cách chạy lại, seed, thẻ mô hình)
9. Điều không như mong đợi và bài học
```

## 7. Ví dụ khung tối thiểu cho đề tài 1 (cảm xúc)

1. Lấy dữ liệu công khai có giấy phép phù hợp; kiểm tra phân phối nhãn, trùng lặp ẩn (Bài 0).
2. Baseline TF-IDF + LR; báo cáo macro-F1 ± độ lệch chuẩn qua CV (Bài 3).
3. Tinh chỉnh PhoBERT (Bài 10) với 3 seed; so sánh bằng bootstrap.
4. Viết 30–50 câu "khó" của riêng bạn (phủ định, mỉa mai, không dấu...) làm tập kiểm tra ngoài phân phối; chạy CheckList (Bài 14).
5. Đo thiên kiến phản thực tế với một thuộc tính phù hợp với miền của bạn.
6. Viết thẻ mô hình; (tùy chọn) bọc bằng Gradio/FastAPI.
