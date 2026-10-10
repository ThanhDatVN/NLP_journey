# NLP tiếng Việt với Python — từ cơ bản đến nâng cao

Giáo trình tự học **xử lý ngôn ngữ tự nhiên (NLP) tiếng Việt** bằng Python, gồm **20 bài Jupyter Notebook (Bài 0–19)** chạy được trên máy cá nhân (không cần khóa API). Lộ trình đi từ làm sạch văn bản, TF-IDF và phân loại cổ điển, qua mạng nơ-ron, attention/Transformer, tinh chỉnh **PhoBERT** (phân loại, NER), tìm kiếm ngữ nghĩa, **LLM + RAG**, triển khai và đạo đức dữ liệu, phần nâng cao **LoRA** và tối ưu suy luận, và kết thúc bằng bốn bài **mở rộng** cho dự án thực tế: dữ liệu nhãn (nhãn yếu, học tích cực), khôi phục dấu tiếng Việt, phân cụm/chủ đề, và tóm tắt/dịch cùng cách đo.

Mỗi bài có: mục tiêu, giải thích ngắn, mã **chạy được và đã chạy** (kết quả được lưu trong notebook), phần *đọc kết quả một cách thận trọng*, bài tập có gợi ý đáp án.

## Nguồn tham khảo chính

Khung kỹ thuật phần Transformer bám theo **[huggingface/course](https://github.com/huggingface/course)** — khóa học chính thức của Hugging Face, **có bản dịch tiếng Việt đầy đủ** (thư mục `chapters/vi`, đọc online tại [huggingface.co/docs/course/vi](https://huggingface.co/docs/course/vi/chapter1/1)). Số liệu GitHub tại ngày khảo sát 10/10/2026:

| Repo | Sao | Giấy phép | Cập nhật cuối | Ngôn ngữ | Vai trò trong giáo trình |
|---|---|---|---|---|---|
| [huggingface/course](https://github.com/huggingface/course) | ~4,3 nghìn | Apache-2.0 | 06/10/2026 | có bản tiếng Việt đầy đủ | **nguồn chính** cho phần Transformer (Bài 8–13) |
| [fastai/course-nlp](https://github.com/fastai/course-nlp) | ~3,5 nghìn | không ghi | 03/2023 | tiếng Anh | tham khảo thứ tự "bài toán trước, giải thích sau" cho phần cổ điển (Bài 2–7) |
| [undertheseanlp/underthesea](https://github.com/undertheseanlp/underthesea) | ~1,8 nghìn | Apache-2.0 | 08/10/2026 | tiếng Việt | công cụ NLP tiếng Việt, tách từ |
| [VinAIResearch/PhoBERT](https://github.com/VinAIResearch/PhoBERT) | — | MIT (mô hình v1) | — | tiếng Việt | mô hình tiền huấn luyện chính (Bài 9–11) |

**Điều cần nói thẳng:** không có repo đơn lẻ nào *vừa* bằng tiếng Việt *vừa* bao trọn từ NLP cổ điển đến LLM. Khóa Hugging Face tiếng Việt phủ phần Transformer nhưng không dạy phần nền (làm sạch, TF-IDF, n-gram, embedding, mạng nơ-ron) và không có xử lý đặc thù tiếng Việt, RAG hay đạo đức dữ liệu. Giáo trình này **viết mới** các phần đó và đối chiếu từng bài với chương tương ứng của khóa Hugging Face. Nội dung là biên soạn mới, không sao chép notebook của nguồn nào. Xem [docs/NGUON_THAM_KHAO.md](docs/NGUON_THAM_KHAO.md) để biết lý do chọn và bảng ánh xạ chi tiết.

## Lộ trình 20 bài

| Phần | Bài | Notebook | Bạn làm được gì | Cần |
|---|---|---|---|---|
| **I. Nền tảng** | 0 | `00_khoi_dong_va_du_lieu` | khám phá dữ liệu, chia tập cố định, phát hiện trùng/rò rỉ, baseline | CPU |
| | 1 | `01_tien_xu_ly_tieng_viet` | Unicode NFC, regex, teencode, tách câu/từ, đo tác hại của bỏ dấu | CPU |
| | 2 | `02_bieu_dien_van_ban` | Bag-of-Words, TF-IDF tự cài, cosine, LSA/NMF, tránh rò rỉ | CPU |
| | 3 | `03_phan_loai_va_danh_gia` | Pipeline, CV, độ đo tự cài, phân tích lỗi, bootstrap, bộ "câu khó" | CPU |
| | 4 | `04_mo_hinh_ngon_ngu_ngram` | n-gram, làm mịn, perplexity, sinh văn bản | CPU |
| | 5 | `05_word_embedding` | PPMI-SVD, Skip-gram từ đầu, giới hạn của embedding tĩnh | CPU |
| **II. Học sâu** | 6 | `06_mang_no_ron_cho_van_ban` | softmax + gradient tay, PyTorch, CNN, nhiều seed | CPU |
| | 7 | `07_rnn_lstm_gru` | RNN, gradient biến mất (đo thật), BiLSTM, nút thắt seq2seq | CPU (~2 phút) |
| | 8 | `08_attention_va_transformer` | attention, mặt nạ, vị trí, Transformer, mini-GPT | CPU (~6 phút) |
| **III. Tiền huấn luyện** | 9 | `09_huggingface_va_tokenizer` | Hub/giấy phép, BPE tự cài, so tokenizer, embedding theo ngữ cảnh | Internet (~0,6 GB) |
| | 10 | `10_phobert_tinh_chinh` | tinh chỉnh PhoBERT trên UIT-VSFC, bootstrap, khác miền, thẻ mô hình | **GPU ≥4 GB** (~4 phút) |
| | 11 | `11_gan_nhan_chuoi_ner` | BIO, F1 mức thực thể, căn chỉnh subword, NER PhoNER, Viterbi | **GPU** (~3 phút) |
| **IV. Ứng dụng** | 12 | `12_embedding_cau_va_tim_kiem` | BM25, dense retrieval, RRF, Recall/MRR/nDCG, chunking | Internet (~1 GB) |
| | 13 | `13_llm_va_rag` | LLM cục bộ, prompt, RAG, ảo giác, prompt injection | **GPU ≥4 GB** (~3 GB tải) |
| | 14 | `14_trien_khai_dao_duc_do_an` | API/Gradio, CheckList, thiên kiến, PII, giám sát, đồ án | CPU |
| **V. Nâng cao** | 15 | `15_lora_va_toi_uu_suy_luan` | đo VRAM thật, gradient checkpointing, LoRA tự cài, LoRA (`peft`) cho LLM nhỏ, lượng tử hóa từng phần, bản đồ chọn công cụ | **GPU ≥4 GB** (mục 3) |
| **VI. Mở rộng** *(độc lập, không bắt buộc)* | 16 | `16_du_lieu_nhan_va_hoc_it_nhan` | đường cong học, κ đồng thuận, nhiễu nhãn, phát hiện nhãn sai, nhãn yếu, học tích cực, tăng cường dữ liệu | CPU (~4 phút) |
| | 17 | `17_khoi_phuc_dau_tieng_viet` | khôi phục dấu bằng kênh nhiễu + Viterbi, trong/ngoài miền, cứu truy vấn không dấu, so với LLM | CPU (mục 8 dùng GPU) |
| | 18 | `18_phan_cum_va_chu_de` | k-means từ đầu, silhouette/NMI/ổn định, c-TF-IDF, LDA/NMF + NPMI, câu gần trùng | CPU (~6 phút lần đầu) |
| | 19 | `19_sinh_van_ban_tom_tat_dich` | ROUGE/BLEU/chrF tự cài, bẫy token hóa, tóm tắt, dịch máy, khoảng tin cậy, điểm mù của độ đo | **GPU** (mục 5–6) |

Tổng thời lượng gợi ý khoảng **49 giờ** cho Bài 0–15 và **≈ 62 giờ** nếu học cả bốn bài mở rộng (chưa tính đồ án). Chi tiết ở [docs/GIAO_TRINH.md](docs/GIAO_TRINH.md); tự kiểm tra bằng [docs/CAU_HOI_ON_TAP.md](docs/CAU_HOI_ON_TAP.md) (câu hỏi trắc nghiệm có đáp án cho mọi bài); đề tài và rubric đồ án ở [docs/DO_AN.md](docs/DO_AN.md), kèm một [báo cáo đồ án mẫu](docs/DO_AN_MAU.md).

## Bắt đầu

Yêu cầu: **Python 3.11+** và kiến thức Python cơ bản. Bài 0–8 và 14 chỉ cần CPU (Bài 15 và 19 có thể chạy một phần trên CPU; Bài 16–18 chạy trên CPU nhưng nên có `requirements-transformers.txt` để dùng dữ liệu thật). Mở PowerShell tại thư mục dự án:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt                 # Bài 0-8, 14
pip install -r requirements-transformers.txt   # Bài 9-19 (PyTorch, Transformers, Datasets, PEFT, SentencePiece)
jupyter lab
```

Với GPU NVIDIA hãy cài bản PyTorch khớp CUDA theo hướng dẫn trên [pytorch.org](https://pytorch.org/get-started/locally/) *trước* khi cài `requirements-transformers.txt`. Mở các notebook trong `notebooks/` **theo thứ tự**.

Môi trường đã chạy thử toàn bộ: Windows 11, Python 3.11.9, NumPy 2.4.6, pandas 2.3.3, scikit-learn 1.7.2, PyTorch 2.14 (CUDA 12.6), Transformers 5.17.0, Datasets 5.0.1, GPU RTX 3050 Laptop 4 GB. Số liệu trong notebook là của **một lần chạy** ở môi trường đó; bạn sẽ nhận số lệch nhẹ (nhất là trên GPU), còn hình dạng kết luận thì giữ nguyên.

Nếu gặp lỗi (DLL bị chặn trên Windows, hết VRAM, tải mô hình chậm, tiếng Việt thành `?`...) xem [docs/KHAC_PHUC_SU_CO.md](docs/KHAC_PHUC_SU_CO.md).

## Cấu trúc thư mục

```text
notebooks/   20 bài học (.ipynb) kèm kết quả đã chạy; notebooks/dap_an/ là đáp án bằng mã cho bài tập
nlpvi/       tiện ích dùng chung: nạp dữ liệu, chuẩn hóa, tách từ, mạng nơ-ron, truy hồi, khôi phục dấu, độ đo sinh văn bản
data/        bộ dữ liệu của khóa học + DATA_CARD.md (đọc trước khi dùng)
docs/        giáo trình, nguồn tham khảo, thuật ngữ, câu hỏi ôn tập, đồ án (+ bài mẫu), khắc phục sự cố
app/         API (FastAPI) và demo (Gradio) cho Bài 14
tools/       sinh dữ liệu tổng hợp, kiểm tra chạy notebook, dựng notebook từ nguồn văn bản (notebook_src/)
tests/       kiểm thử tự động (pytest): gói nlpvi, toàn vẹn dữ liệu/mã hóa (kể cả ký tự điều khiển và công thức LaTeX bị vỡ), độ tái lập, kiểm thử hành vi
outputs/     (sinh ra khi chạy; bị bỏ qua bởi git) mô hình đã huấn luyện
```

## Dữ liệu và giấy phép

- **Dữ liệu tự biên soạn** (trong `data/`): bộ đánh giá **tổng hợp** 1.800 mẫu, 40 câu "khó" viết tay, 38 câu NER, kho FAQ + truy vấn cho tìm kiếm, và (Bài 19) 16 đoạn văn hư cấu kèm 2 tóm tắt tham chiếu, 24 câu Anh–Việt kèm 2 bản dịch tham chiếu. Bộ tổng hợp dùng để học quy trình và để mọi kết quả chạy lại được; **nó không đại diện cho bình luận thật** và cố ý chứa nhiễu (xem [data/DATA_CARD.md](data/DATA_CARD.md)). Đừng dùng kết quả trên nó để tuyên bố chất lượng ngoài đời.
- **Dữ liệu thật tải lúc chạy** (không đi kèm repo): UIT-VSFC cho Bài 10, 15, 16, 17, 18 và bản sao PhoNER_COVID19 cho Bài 11, 17. Thẻ trên Hub không ghi giấy phép (UIT-VSFC ghi `unknown`); hãy dùng cho học tập/nghiên cứu và kiểm tra điều khoản gốc trước khi dùng cách khác.
- **Mô hình**: `vinai/phobert-base` (MIT), `intfloat/multilingual-e5-small` (MIT), `bkai-foundation-models/vietnamese-bi-encoder` (Apache-2.0), `Qwen/Qwen2.5-1.5B-Instruct` và `Qwen/Qwen2.5-0.5B-Instruct` (Apache-2.0), `Helsinki-NLP/opus-mt-en-vi` (Bài 19; kiểm tra giấy phép tại thẻ mô hình). Lưu ý `vinai/phobert-base-v2` ghi **AGPL-3.0** — khóa học cố ý dùng bản v1 (MIT); luôn kiểm tra lại giấy phép tại thẻ mô hình.
- **Mã nguồn và nội dung giáo trình** chưa kèm tệp giấy phép. Hãy thêm giấy phép bạn chọn (ví dụ MIT cho mã, CC BY 4.0 cho nội dung) trước khi chia sẻ công khai.

## Kiểm tra tái lập

```powershell
pytest -q                                  # kiểm thử tự động (vài giây): gói nlpvi, dữ liệu, độ tái lập, CheckList
python tools/check_notebooks.py            # chạy lại các bài chỉ cần CPU (00-07, 14) và báo lỗi
python tools/check_notebooks.py --all      # chạy cả bài cần Internet/GPU (08-19; ≈ 60-90 phút, chưa tính tải mô hình lần đầu)
python tools/make_data.py                  # sinh lại data/reviews_vi.csv (seed cố định)
```

## Dành cho người bảo trì

Notebook được **dựng từ nguồn văn bản** `tools/notebook_src/*.nbsrc` (mỗi dòng `@@@ md` hoặc `@@@ code` mở một ô) rồi chạy để lưu kết quả. Nguồn dạng văn bản dễ sửa lời văn và dễ xem khác biệt hơn JSON:

```powershell
python tools/build_notebooks.py 03 --run   # dựng + chạy lại Bài 03, lưu kết quả vào notebook
```

Khi sửa lời văn có chứa số liệu, hãy chạy lại và đối chiếu số liệu với lời văn (giáo trình cố ý viết các nhận xét dựa trên số đo thật). Nếu sửa trực tiếp `.ipynb`, hãy sửa cả `.nbsrc` tương ứng để hai bên không lệch nhau.

## Tài liệu tham khảo

- [Hugging Face NLP Course (tiếng Việt)](https://huggingface.co/docs/course/vi/chapter1/1) và [repo nguồn](https://github.com/huggingface/course)
- [fastai/course-nlp](https://github.com/fastai/course-nlp) — *A Code-First Introduction to NLP*
- [Underthesea](https://github.com/undertheseanlp/underthesea) · [PhoBERT](https://github.com/VinAIResearch/PhoBERT) · [Bài báo PhoBERT (Findings of EMNLP 2020)](https://aclanthology.org/2020.findings-emnlp.92/)
- Jurafsky & Martin, [*Speech and Language Processing*](https://web.stanford.edu/~jurafsky/slp3/) · [Stanford CS224n](https://web.stanford.edu/class/cs224n/)
