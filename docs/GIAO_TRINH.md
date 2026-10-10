# Giáo trình NLP tiếng Việt thực hành

## Mục tiêu khóa học

Sau khóa học, người học có thể:

1. **Chuẩn bị dữ liệu văn bản tiếng Việt đúng cách**: chuẩn hóa Unicode, làm sạch có kiểm soát, tách câu/từ, kiểm tra trùng lặp và rò rỉ, chia tập cố định.
2. **Giải thích và tự cài đặt** các khái niệm nền: TF-IDF, n-gram, perplexity, embedding, gradient của softmax, attention, BPE, BM25, các độ đo (F1, entity-F1, Recall@k, MRR).
3. **Xây quy trình học máy có kỷ luật**: baseline → mô hình → đánh giá (khoảng tin cậy, khác miền, theo hiện tượng) → phân tích lỗi.
4. **Tinh chỉnh và dùng mô hình tiền huấn luyện tiếng Việt** (PhoBERT) cho phân loại và NER; chọn tokenizer, giấy phép và phần cứng phù hợp.
5. **Xây hệ thống tìm kiếm và RAG**, đo ảo giác, nhận diện rủi ro như prompt injection.
6. **Triển khai có trách nhiệm**: API/demo, kiểm thử hành vi, đo thiên kiến, bảo vệ dữ liệu cá nhân, giám sát, thẻ mô hình.
7. **Tinh chỉnh và suy luận hiệu quả**: tính bộ nhớ, LoRA, lượng tử hóa; chọn công cụ theo dữ liệu, ngân sách và độ trễ.
8. **Làm việc với dữ liệu nhãn** *(Bài 16, mở rộng)*: đường cong học, đồng thuận người gán (κ), nhiễu nhãn, nhãn yếu, học tích cực.
9. **Giải bài toán riêng của tiếng Việt và khám phá dữ liệu** *(Bài 17–18, mở rộng)*: khôi phục dấu bằng kênh nhiễu + Viterbi; phân cụm và mô hình chủ đề, kiểm chứng cụm.
10. **Đo chất lượng sinh văn bản** *(Bài 19, mở rộng)*: ROUGE/BLEU/chrF tự cài, bẫy token hóa, khoảng tin cậy và điểm mù của độ đo.

## Đối tượng và kiến thức đầu vào

Người đã biết Python cơ bản (hàm, vòng lặp, list/dict), đọc được DataFrame của pandas, biết sơ bộ xác suất, vector/ma trận và khái niệm train/test. Không cần biết trước học máy hay học sâu — khóa học xây từ đầu. Bài 0 ôn lại cách nạp và kiểm tra dữ liệu.

**Phần cứng:** Bài 0–8 và 14 chạy trên CPU thường. Bài 10, 11, 13, 15 nên có GPU NVIDIA ≥ 4 GB VRAM (đã chạy thử trên RTX 3050 Laptop 4 GB); xem cách rút gọn cho CPU ở từng bài. Bài 16–18 chạy trên CPU (Bài 17 mục 8 và Bài 19 mục 5–6 dùng GPU, tự bỏ qua nếu không có). Bài 9, 12, 13, 17, 18, 19 cần Internet lần đầu để tải mô hình/dữ liệu.

## Lộ trình 20 buổi (16 buổi chính + 4 buổi mở rộng)

| Bài | Trọng tâm | Thời lượng | Kết quả cần nộp |
|---|---|---|---|
| **0** Khởi động và dữ liệu | môi trường, đặc điểm tiếng Việt, mô tả dữ liệu, chia tập, rò rỉ ẩn, baseline | 90' | bảng thống kê dữ liệu + 2 vấn đề chất lượng dữ liệu bạn tìm thấy |
| **1** Tiền xử lý tiếng Việt | NFC, regex, teencode, bỏ dấu (đo va chạm), tách câu/từ, từ dừng và phủ định, Zipf | 120' | hàm tiền xử lý có ví dụ trước/sau và lý do mỗi quyết định |
| **2** Biểu diễn văn bản | BoW, TF-IDF tự cài, ma trận thưa, n-gram, cosine, LSA/NMF, rò rỉ khi vector hóa | 120' | TF-IDF tự cài khớp scikit-learn; bộ tìm câu gần nhất; diễn giải 3 chủ đề |
| **3** Phân loại và đánh giá | baseline (ngốc, luật), NB/LR/SVM, Pipeline, CV, GridSearch, độ đo tự cài, class_weight, phân tích lỗi, nhãn nhiễu, bộ câu khó, bootstrap | 150' | bảng so sánh có độ lệch chuẩn + 10 lỗi phân loại theo hiện tượng ngôn ngữ |
| **4** Mô hình ngôn ngữ n-gram | Markov, đếm, add-k, nội suy, perplexity, lấy mẫu, giới hạn | 120' | perplexity valid/test của mô hình chọn được + giải thích 3 giới hạn của n-gram |
| **5** Word embedding | giả thuyết phân bố, PPMI+SVD, Skip-gram (PyTorch), trái nghĩa ≈ gần nhau, so với TF-IDF | 150' | láng giềng của 5 từ bạn chọn + nhận xét về điều embedding bắt được/không bắt được |
| **6** Mạng nơ-ron cho văn bản | softmax NumPy + kiểm tra gradient, PyTorch, Dataset/DataLoader, CNN, dừng sớm, nhiều seed | 180' | bảng mean ± std qua ≥ 3 seed so với TF-IDF + LR |
| **7** RNN/LSTM/GRU | ô RNN, gradient biến mất (thực nghiệm), BiLSTM, pack/mask, clipping, nút thắt seq2seq | 180' | đồ thị gradient theo độ dài + kết luận về mô hình có thứ tự |
| **8** Attention và Transformer | QKV, √d, mặt nạ, vị trí, multi-head, khối Transformer, attention cho seq2seq, mini-GPT | 210' | đồ thị đảo chuỗi 3 mô hình + giải thích vai trò của thông tin vị trí |
| **9** Hugging Face và tokenizer | Hub/giấy phép, BPE tự cài, so tokenizer (PhoBERT/XLM-R/mBERT/Qwen), embedding theo ngữ cảnh, đằng sau pipeline | 180' | bảng chi phí token + bài tập ngữ cảnh "đá" |
| **10** Tinh chỉnh PhoBERT | tách từ, đệm động, vòng huấn luyện (AdamW, warmup, fp16), bootstrap, khác miền, thẻ mô hình | 240' | notebook thử nghiệm có báo cáo từng lớp + thẻ mô hình |
| **11** Gán nhãn chuỗi (NER) | BIO, F1 mức thực thể, căn chỉnh subword, tinh chỉnh, Viterbi, phân tích lỗi, đổi miền | 240' | bảng F1 theo loại thực thể + phân tích 3 dạng lỗi |
| **12** Embedding câu và tìm kiếm | Recall/MRR/nDCG, BM25, dense (E5), RRF, chunking, ảnh hưởng của dấu và tiền tố | 210' | bảng so sánh các hệ thống + 20 truy vấn của bạn |
| **13** LLM và RAG | chat template, lấy mẫu, đo prompt, RAG có trích dẫn, đánh giá RAG, từ chối, prompt injection | 270' | bộ kiểm tra RAG (có câu không đáp án) + kết quả thử injection |
| **14** Triển khai, đạo đức, đồ án | API/Gradio, CheckList, thiên kiến phản thực tế, PII, giám sát lệch phân phối, thẻ mô hình | 210' | bộ CheckList + đo thiên kiến + kế hoạch đồ án |
| **15** Nâng cao: LoRA và tối ưu suy luận | bộ nhớ ≈16 B/tham số và đo VRAM thật (kích hoạt, gradient checkpointing), LoRA tự cài, `peft` trên LLM nhỏ, lượng tử hóa int8 (đo theo lớp), bản đồ chọn công cụ | 270' | bảng so sánh chi phí–chất lượng + quyết định chọn phương pháp cho đồ án |
| **16** *(mở rộng)* Dữ liệu nhãn và học ít nhãn | đường cong học, κ Cohen (tự cài), nhiễu nhãn ở train vs test, gắn cờ nhãn nghi sai, hàm gán nhãn (nhãn yếu), học tích cực, tăng cường dữ liệu | 180' | đường cong học + so sánh biện pháp theo cùng ngân sách + danh sách nhãn nghi sai đã tự rà soát |
| **17** *(mở rộng)* Khôi phục dấu tiếng Việt | mơ hồ khi bỏ dấu, kênh nhiễu, n-gram nội suy + Viterbi, trong/ngoài miền, cứu truy vấn không dấu, so với LLM | 180' | bộ khôi phục dấu + bảng độ chính xác trong/ngoài miền + phân tích lỗi (thiếu từ điển hay sai ngữ cảnh) |
| **18** *(mở rộng)* Phân cụm và mô hình chủ đề | k-means++ tự cài, TF-IDF vs embedding, silhouette/NMI/ổn định, c-TF-IDF, LDA/NMF + NPMI, câu gần trùng | 180' | bảng đánh giá cụm theo k + tên cụm có bằng chứng + nhận xét về trục chi phối của dữ liệu |
| **19** *(mở rộng)* Tóm tắt, dịch và cách đo | ROUGE/BLEU/chrF tự cài, tokenizer, đường cơ sở trích xuất, tóm tắt LLM + kiểm tra trung thực, dịch máy + bootstrap, điểm mù | 210' | bảng đánh giá có khoảng tin cậy + nhận xét lỗi đọc từ mẫu thật + 3 bộ ba "diễn đạt đúng / sai nghĩa" của bạn |

Tổng ≈ 2.940 phút ≈ **49 giờ** học cho Bài 0–15 và ≈ 3.690 phút ≈ **62 giờ** nếu học cả bốn bài mở rộng (chưa tính đồ án). Có thể chia theo nhịp một bài mỗi tuần hoặc gom nhóm hai bài một buổi cho lớp học cường độ cao. **Bài 16–19 độc lập với nhau** và chỉ cần các bài nền ghi ở cột nội dung, nên có thể chọn theo nhu cầu.

## Các lộ trình gợi ý

| Lộ trình | Dành cho | Bài |
|---|---|---|
| **Nhanh – ứng dụng** (≈ 18 giờ) | muốn dùng mô hình hiện đại sớm | 0 → 1 → 3 → 9 → 10 → 12 → 13 → 14 (đọc lướt 2, 6–8 khi cần) |
| **Đầy đủ** (≈ 49 giờ; ≈ 62 giờ nếu thêm Bài 16–19) | tự học có hệ thống | 0 → 15 theo thứ tự, rồi chọn Bài 16–19 theo nhu cầu |
| **Nghiên cứu** (≈ 80 giờ) | muốn hiểu sâu cơ chế | đầy đủ + làm *mọi* bài tập "Khó" + đọc bài báo gốc ở mục "Đọc thêm" |
| **Dự án dữ liệu thực** (≈ 17 giờ) | làm việc với dữ liệu thật ít nhãn / không nhãn / cần sinh văn bản | 0 → 3 (nền) → 16 → 17 → 18 → 19 (đọc kèm Bài 12–13 nếu dùng embedding/LLM) |

## Cách học mỗi bài

1. Đọc mục tiêu và phần khái niệm trước khi chạy ô mã.
2. Chạy từng ô từ trên xuống; **đoán kết quả trước khi chạy**; sửa một tham số và ghi lại điều gì đổi.
3. Đọc phần **"Đọc kết quả"**: khóa học cố ý chỉ ra khi một kết quả *không* theo kịch bản mong đợi (ví dụ bỏ dấu lại tăng điểm ở Bài 3, RAG k=1 thắng k=3 ở Bài 13).
4. Làm bài tập trong notebook; chỉ xem gợi ý đáp án sau khi đã thử. Cuối mỗi bài, tự kiểm tra bằng các câu hỏi ở [CAU_HOI_ON_TAP.md](CAU_HOI_ON_TAP.md).
5. Với mô hình có tải về: ghi lại tên checkpoint, phiên bản thư viện, seed, bước tách từ.

## Phương pháp đánh giá đề xuất

| Thành phần | Tỉ trọng | Tiêu chí |
|---|---|---|
| Bài tập trong notebook | 30% | tính đúng, giải thích được quyết định, ghi lại điều đã thử |
| Sản phẩm của từng bài (cột "Kết quả cần nộp") | 20% | có số liệu, có nhận xét thận trọng |
| Đồ án cuối khóa | 40% | xem [DO_AN.md](DO_AN.md); tham khảo bài mẫu [DO_AN_MAU.md](DO_AN_MAU.md) |
| Báo cáo ngắn / vấn đáp | 10% | giải thích kết quả, rủi ro, giới hạn; không chỉ nêu accuracy |

Nguyên tắc chấm xuyên suốt: **thưởng cho sự trung thực** (nêu rõ kết quả không như mong đợi, nêu cỡ mẫu, nêu giới hạn) hơn là điểm số cao đạt được bằng cách chọn lọc.

## Quy tắc xử lý tiếng Việt xuyên suốt khóa học

- Luôn chuẩn hóa **Unicode NFC** ngay khi đọc dữ liệu.
- Mặc định **giữ dấu** nhưng **đo** trước khi kết luận (Bài 3 cho thấy bỏ dấu có thể tăng điểm trên dữ liệu nhỏ lẫn nhiều dòng không dấu; ngược lại Bài 12 cho thấy mô hình dense sụp khi gặp văn bản không dấu).
- **Không xóa từ phủ định** ("không", "chưa", "chẳng") và đối lập ("nhưng") một cách máy móc.
- Phân biệt **âm tiết**, **từ**, **subword**. Khoảng trắng không phải ranh giới từ.
- Với PhoBERT: **tách từ trước**, đúng như lúc tiền huấn luyện; bộ tách từ định nghĩa cả đơn vị của thực thể (Bài 11).
- Mọi pipeline cần dùng **cùng một cách tiền xử lý** ở huấn luyện và triển khai.

## Nguồn tham khảo

Xem [NGUON_THAM_KHAO.md](NGUON_THAM_KHAO.md) để biết lý do chọn nguồn chính, bảng ánh xạ từng bài sang chương Hugging Face (tiếng Việt) và tài liệu bổ sung. Thuật ngữ Anh–Việt: [THUAT_NGU.md](THUAT_NGU.md).
