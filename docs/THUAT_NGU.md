# Bảng thuật ngữ Anh – Việt

Thuật ngữ NLP/học máy tiếng Việt chưa có chuẩn thống nhất; giáo trình dùng cách dịch phổ biến và **giữ thuật ngữ gốc** khi cách dịch gây nhầm. Cột "Bài" là nơi thuật ngữ xuất hiện đầu tiên.

## Dữ liệu và tiền xử lý

| English | Tiếng Việt | Bài | Ghi chú |
|---|---|---|---|
| corpus | ngữ liệu / kho văn bản | 0 | |
| token / tokenization | token / tách token | 1 | thường để nguyên "token" |
| syllable | âm tiết | 1 | đơn vị cách nhau bằng khoảng trắng trong tiếng Việt |
| word segmentation | tách từ | 1 | ghép âm tiết thành từ: *học_sinh* |
| normalization (Unicode NFC) | chuẩn hóa (Unicode NFC) | 1 | |
| diacritics | dấu (thanh điệu và dấu phụ) | 1 | |
| stop words | từ dừng | 1 | cẩn thận với từ phủ định |
| out-of-vocabulary (OOV) | từ ngoài từ điển | 1 | |
| data leakage | rò rỉ dữ liệu | 0 | thông tin tập kiểm tra lọt vào huấn luyện |
| train / validation / test | tập huấn luyện / kiểm định (valid) / kiểm tra | 0 | |
| label noise | nhiễu nhãn | 3 | |
| class imbalance | lớp mất cân bằng | 3 | |

## Biểu diễn và mô hình cổ điển

| English | Tiếng Việt | Bài |
|---|---|---|
| bag-of-words (BoW) | túi từ | 2 |
| TF-IDF | tần suất từ – nghịch đảo tần suất văn bản | 2 |
| n-gram | n-gram | 2, 4 |
| sparse matrix | ma trận thưa | 2 |
| cosine similarity | độ tương tự cosine | 2 |
| latent semantic analysis (LSA) | phân tích ngữ nghĩa ẩn | 2 |
| topic model / NMF | mô hình chủ đề / phân rã ma trận không âm | 2 |
| baseline | mô hình cơ sở / mốc so sánh | 0, 3 |
| pipeline | quy trình (đường ống) xử lý | 3 |
| cross-validation | kiểm định chéo | 3 |
| hyperparameter | siêu tham số | 3 |
| precision / recall / F1 | độ chính xác dương / độ phủ / F1 | 3 |
| macro-F1 | F1 trung bình theo lớp | 3 |
| confusion matrix | ma trận nhầm lẫn | 3 |
| bootstrap | lấy mẫu lặp (bootstrap) | 3 |
| error analysis | phân tích lỗi | 3 |
| language model | mô hình ngôn ngữ | 4 |
| smoothing | làm mịn | 4 |
| perplexity | perplexity (độ "phân vân") | 4 |

## Embedding và mạng nơ-ron

| English | Tiếng Việt | Bài |
|---|---|---|
| distributional hypothesis | giả thuyết phân bố | 5 |
| word embedding | embedding từ (biểu diễn vector của từ) | 5 |
| skip-gram, negative sampling | skip-gram, lấy mẫu âm | 5 |
| gradient / backpropagation | gradient / lan truyền ngược | 6 |
| autograd | vi phân tự động | 6 |
| overfitting / early stopping | quá khớp / dừng sớm | 6 |
| dropout, weight decay | dropout, suy giảm trọng số | 6 |
| convolutional neural network (CNN) | mạng nơ-ron tích chập | 6 |
| recurrent neural network (RNN) | mạng nơ-ron hồi quy | 7 |
| vanishing / exploding gradient | gradient biến mất / bùng nổ | 7 |
| LSTM, GRU | LSTM, GRU (có cổng) | 7 |
| gradient clipping | cắt gradient | 7 |
| encoder–decoder (seq2seq) | bộ mã hóa – bộ giải mã (chuỗi → chuỗi) | 7 |

## Transformer và mô hình tiền huấn luyện

| English | Tiếng Việt | Bài |
|---|---|---|
| attention / self-attention | cơ chế chú ý / tự chú ý | 8 |
| query, key, value | truy vấn, khóa, giá trị | 8 |
| multi-head attention | chú ý nhiều đầu | 8 |
| positional encoding | mã hóa vị trí | 8 |
| causal mask | mặt nạ nhân quả | 8 |
| residual connection | kết nối tắt | 8 |
| layer normalization | chuẩn hóa lớp | 8 |
| subword (BPE, WordPiece) | từ con (BPE, WordPiece) | 9 |
| attention mask | mặt nạ chú ý | 9 |
| pre-training / fine-tuning | tiền huấn luyện / tinh chỉnh | 9, 10 |
| contextual embedding | embedding theo ngữ cảnh | 9 |
| model hub / model card | kho mô hình / thẻ mô hình | 9, 10 |
| learning-rate warmup | khởi động tốc độ học | 10 |
| mixed precision (fp16) | độ chính xác hỗn hợp | 10 |
| named entity recognition (NER) | nhận diện thực thể có tên | 11 |
| BIO tagging | gán nhãn BIO | 11 |
| entity-level F1 | F1 mức thực thể | 11 |
| Viterbi decoding | giải mã Viterbi | 11 |

## Tìm kiếm, LLM, triển khai

| English | Tiếng Việt | Bài |
|---|---|---|
| information retrieval | truy hồi thông tin | 12 |
| BM25 | BM25 | 12 |
| dense retrieval / bi-encoder | truy hồi dày / bộ mã hóa đôi | 12 |
| reciprocal rank fusion (RRF) | hợp nhất hạng nghịch đảo | 12 |
| recall@k, MRR, nDCG | recall@k, MRR, nDCG | 12 |
| chunking | chia đoạn | 12 |
| large language model (LLM) | mô hình ngôn ngữ lớn | 13 |
| chat template | mẫu hội thoại | 13 |
| temperature, top-k, top-p | nhiệt độ, top-k, top-p | 13 |
| prompt, few-shot, zero-shot | prompt (lời nhắc), few-shot, zero-shot | 13 |
| retrieval-augmented generation (RAG) | tạo sinh có truy hồi | 13 |
| hallucination | ảo giác | 13 |
| prompt injection | tiêm lệnh qua prompt | 13 |
| behavioral testing (CheckList) | kiểm thử hành vi | 14 |
| counterfactual test | thử nghiệm phản thực tế | 14 |
| bias | thiên kiến | 14 |
| personally identifiable information (PII) | thông tin định danh cá nhân | 14 |
| data drift / PSI | lệch phân phối dữ liệu / chỉ số ổn định dân số | 14 |

## Tinh chỉnh hiệu quả và tối ưu suy luận (Bài 15)

| English | Tiếng Việt | Bài |
|---|---|---|
| parameter-efficient fine-tuning (PEFT) | tinh chỉnh hiệu quả tham số | 15 |
| low-rank adaptation (LoRA) | thích nghi hạng thấp (LoRA) | 15 |
| rank | hạng (của ma trận) | 15 |
| adapter | adapter (mô-đun bổ sung nhỏ) | 15 |
| merge (adapter) | hợp nhất (adapter vào trọng số gốc) | 15 |
| quantization (int8, int4) | lượng tử hóa | 15 |
| distillation | chưng cất tri thức | 15 |
| activation memory | bộ nhớ kích hoạt (trung gian) | 15 |
| gradient checkpointing | lưu điểm kiểm tra gradient (tính lại kích hoạt để tiết kiệm bộ nhớ) | 15 |
| VRAM spill (sysmem fallback) | tràn VRAM sang RAM hệ thống (chạy chậm mà không báo lỗi) | 15 |

## Bài mở rộng: dữ liệu nhãn (Bài 16)

| English | Tiếng Việt | Bài |
|---|---|---|
| learning curve | đường cong học | 16 |
| inter-annotator agreement | độ đồng thuận giữa người gán nhãn | 16 |
| Cohen's kappa (κ) | hệ số κ Cohen (đồng thuận đã hiệu chỉnh theo ngẫu nhiên) | 16 |
| confident learning | học tự tin (phát hiện nhãn nghi sai bằng xác suất dự đoán chéo) | 16 |
| weak supervision | giám sát yếu / nhãn yếu | 16 |
| labeling function (LF) | hàm gán nhãn | 16 |
| active learning | học tích cực | 16 |
| uncertainty sampling | chọn mẫu theo độ bất định | 16 |
| data augmentation | tăng cường dữ liệu | 16 |
| gold set | tập vàng (tập nhãn tham chiếu chất lượng cao) | 16 |

## Bài mở rộng: khôi phục dấu tiếng Việt (Bài 17)

| English | Tiếng Việt | Bài |
|---|---|---|
| diacritic restoration | khôi phục dấu | 17 |
| noisy channel model | mô hình kênh nhiễu | 17 |
| lattice (candidate lattice) | lưới ứng viên | 17 |
| interpolated n-gram | n-gram nội suy | 17 |
| in-domain / out-of-domain | trong miền / ngoài miền | 17 |
| beam search | tìm kiếm chùm | 17 (bài tập) |

## Bài mở rộng: phân cụm và chủ đề (Bài 18)

| English | Tiếng Việt | Bài |
|---|---|---|
| clustering / k-means | phân cụm / k-means | 18 |
| k-means++ | k-means++ (khởi tạo tâm theo xác suất ∝ D²) | 18 |
| inertia | quán tính (tổng bình phương khoảng cách tới tâm) | 18 |
| silhouette | hệ số silhouette | 18 |
| normalized mutual information (NMI) | thông tin tương hỗ chuẩn hóa | 18 |
| adjusted Rand index (ARI) | chỉ số Rand điều chỉnh | 18 |
| cluster stability | độ ổn định của cụm | 18 |
| c-TF-IDF | TF-IDF theo cụm (dùng đặt tên cụm) | 18 |
| latent Dirichlet allocation (LDA) | phân bổ Dirichlet ẩn | 18 |
| topic coherence (NPMI) | độ nhất quán chủ đề (NPMI) | 18 |
| near-duplicate | câu gần trùng | 18 |

## Bài mở rộng: sinh văn bản có điều kiện (Bài 19)

| English | Tiếng Việt | Bài |
|---|---|---|
| extractive / abstractive summarization | tóm tắt trích xuất / tóm tắt diễn đạt lại | 19 |
| machine translation | dịch máy | 19 |
| ROUGE-N, ROUGE-L | ROUGE-N, ROUGE-L (độ đo tóm tắt theo n-gram / chuỗi con chung dài nhất) | 19 |
| BLEU, brevity penalty | BLEU, phạt độ dài ngắn | 19 |
| chrF | chrF (F-β trên n-gram ký tự) | 19 |
| longest common subsequence (LCS) | chuỗi con chung dài nhất | 19 |
| reference-based metric | độ đo theo tham chiếu | 19 |
| faithfulness | tính trung thực (không bịa/bóp méo so với nguồn) | 19 |
| paired bootstrap | bootstrap theo cặp | 19 |
| lead-1 baseline | đường cơ sở "câu đầu" | 19 |
