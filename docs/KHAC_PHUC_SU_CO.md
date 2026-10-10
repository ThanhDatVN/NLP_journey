# Khắc phục sự cố

Các lỗi dưới đây đều **đã gặp thật** khi biên soạn và chạy giáo trình này (Windows 11, Python 3.11, GPU 4 GB).

## 1. Tiếng Việt biến thành dấu `?`

**Triệu chứng:** văn bản hiển thị như `B?i 1 ? Ti?n x? l? v?n b?n`; tệp CSV chứa hàng trăm ký tự `?` thay cho chữ có dấu.

**Nguyên nhân:** tệp bị **ghi bằng mã hóa không hỗ trợ tiếng Việt** (thường là bảng mã ANSI mặc định của PowerShell 5.1 khi dùng `Set-Content`, `Out-File`, `>` mà không chỉ định mã hóa). Ký tự không biểu diễn được bị thay bằng `?` **vĩnh viễn** — không khôi phục được từ tệp hỏng; phải tạo lại từ nguồn.

**Phát hiện nhanh:**

```powershell
python -c "s=open('data/reviews_vi.csv',encoding='utf-8-sig').read(); print('số dấu ? :', s.count('?'), '| ký tự non-ASCII:', sum(ord(c)>127 for c in s))"
```

Dữ liệu tiếng Việt lành mạnh có hàng nghìn ký tự non-ASCII và hầu như không có `?` ngoài câu hỏi thật.

**Phòng tránh:**

- Ghi tệp bằng trình soạn thảo/công cụ xuất **UTF-8**; trong PowerShell: `Set-Content -Encoding utf8` (PowerShell 7 mặc định UTF-8), hoặc dùng Python `open(..., encoding="utf-8")`.
- Đọc CSV bằng `pd.read_csv(path, encoding="utf-8-sig")` (chịu được BOM của Excel).
- Đặt `PYTHONUTF8=1` khi chạy script trên Windows.
- Thêm kiểm tra "đếm `?`" ở trên vào bước nạp dữ liệu (Bài 0 làm đúng việc này).

## 2. `ImportError: DLL load failed ... An Application Control policy has blocked this file`

**Triệu chứng:** `import underthesea` (hoặc `pycrfsuite`, `sklearn_crfsuite`, `pyvi`) báo lỗi nạp DLL bị chính sách bảo mật chặn.

**Nguyên nhân:** chính sách **Application Control** (Smart App Control / WDAC) của Windows chặn các tệp `.dll`/`.pyd` biên dịch sẵn chưa được tin cậy. Đây **không phải lỗi cài đặt** của bạn, và hành vi có thể *chập chờn* (có lúc chặn, có lúc cho phép).

**Cách xử lý, theo thứ tự nên thử:**

1. **Không cần làm gì**: giáo trình dùng bộ tách từ thuần Python (`nlpvi.segment`) làm mặc định, nên Bài 0–14 chạy được mà không cần các thư viện đó. `get_segmenter("underthesea")` tự lùi về bộ mặc định và in một dòng cảnh báo.
2. Chạy trong **WSL2** hoặc một máy Linux/conda khác không có chính sách này.
3. Nếu máy do tổ chức quản lý, hỏi quản trị viên về việc cho phép gói cụ thể. **Đừng tắt tính năng bảo mật của toàn hệ thống** chỉ để chạy một thư viện.

> Mẫu mã *sai* thường gặp: `try: import X ... except ImportError: print("pip install X")`. Khi nguyên nhân là DLL bị chặn, thông báo "hãy cài thêm" sẽ gây hiểu nhầm. Giáo trình bắt `Exception` rộng và in loại lỗi thật.

## 3. Hết bộ nhớ GPU (`CUDA out of memory`)

- Giảm `BATCH` (Bài 10: 32 → 16 → 8), giảm `MAX_LEN`, đặt `MAX_TRAIN` nhỏ hơn.
- Giữ fp16/autocast bật (đã bật mặc định trên GPU).
- Đóng notebook khác đang giữ VRAM (mỗi kernel Jupyter giữ VRAM cho đến khi tắt): **Kernel → Shut Down**.
- Bài 13: máy dưới ~3,8 GB VRAM tự động lùi về `Qwen2.5-0.5B-Instruct` (chất lượng kém hơn). Bộ nhúng E5 trong bài này chạy trên CPU để dành VRAM cho LLM.
- Kiểm tra: `nvidia-smi`. Mức dùng đã đo trên RTX 3050 4 GB: Bài 10 đỉnh ≈ 3,1 GB; Bài 13 ≈ 3,1 GB cho mô hình 1,5B.
- Không có GPU: đặt `MAX_TRAIN = 1000–2000` ở Bài 10/11 (vẫn đủ để thấy quy trình), hoặc chạy trên Google Colab/Kaggle.

**Bài 15 (LoRA)** dễ tràn VRAM vì *kích hoạt* (không phải trọng số) mới là khoản lớn nhất khi dùng LoRA. Notebook giảm bộ nhớ bằng hai cách: `logits_to_keep` (chỉ tính logit vài vị trí cuối thay vì toàn bộ từ điển ≈152 nghìn token ở mọi vị trí) và **gradient checkpointing**; mục 3.0 đo VRAM đỉnh của từng cấu hình trước khi huấn luyện.

> **Cảnh báo riêng cho Windows:** khi VRAM đỉnh vượt VRAM vật lý, trình điều khiển NVIDIA thường **không báo lỗi hết bộ nhớ** mà lặng lẽ dùng RAM hệ thống làm bộ nhớ GPU. Huấn luyện vẫn chạy nhưng chậm đi nhiều lần (đã gặp trong lúc biên soạn bài này: batch 16 không bật checkpointing đạt đỉnh 7,56 GB trên card 4,3 GB và mất 16 phút). Nếu bước huấn luyện chậm bất thường, hãy so `VRAM đỉnh` với VRAM của card; notebook in cảnh báo khi vượt. Cách xử lý: bật checkpointing, giảm `BATCH`, hoặc rút ngắn độ dài chuỗi.

## 4. Tải mô hình/dữ liệu chậm hoặc lỗi

- Lần đầu mỗi mô hình tải 0,5–3 GB về `~/.cache/huggingface`. Chạy lại sẽ dùng bản đã lưu.
- Sau khi đã tải đủ, có thể làm việc **ngoại tuyến**: `HF_HUB_OFFLINE=1` (PowerShell: `$env:HF_HUB_OFFLINE = "1"`).
- Mạng chập chờn: chạy lại ô; `huggingface_hub` tự tiếp tục tải dở.
- Bộ **UIT-VSFC** dùng script cũ nên `datasets` bản mới báo `Dataset scripts are no longer supported`. Bài 10 đã xử lý bằng cách nạp nhánh `refs/convert/parquet`. Nếu vẫn lỗi, bài tự lùi về dữ liệu tổng hợp.
- Thư mục cache có thể rất lớn (hàng GB); dọn bằng cách xóa thư mục tương ứng trong `~/.cache/huggingface/hub` hoặc dùng lệnh quản lý cache của `huggingface_hub` (xem tài liệu của phiên bản bạn cài).
- Nếu tokenizer của XLM-R báo thiếu `sentencepiece` (trên bản `transformers` cũ), cài `pip install sentencepiece`.

## 5. Khác biệt giữa các phiên bản `transformers`

Giáo trình đã chạy với `transformers` **5.17**. Nếu bạn dùng bản khác:

- Tham số tải mô hình `dtype=` (mới, ≥ 4.56) thay cho `torch_dtype=` (cũ). Cài `transformers>=4.56` để khớp.
- `TrainingArguments(eval_strategy=...)` thay cho `evaluation_strategy=...` ở bản cũ (chỉ liên quan đến mã mẫu `Trainer` ở Bài 10, không chạy trong notebook).
- Tokenizer của PhoBERT là bản **chậm** (không có `word_ids()`); Bài 11 tự căn chỉnh nhãn thay vì dựa vào đó.
- Thư viện in "LOAD REPORT"/cảnh báo "trọng số khởi tạo mới" khi nạp mô hình có đầu mới: bình thường. Notebook đã đặt `transformers.logging.set_verbosity_error()` để giảm nhiễu.
- `apply_chat_template(tokenize=True)` có thể trả về từ điển thay vì danh sách; Bài 13 đếm token bằng cách tự tokenize chuỗi đã áp mẫu.

## 6. Lỗi thường gặp khi dùng PhoBERT

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| điểm thấp bất thường, số token nhiều | quên **tách từ** | `segment(text)` trước tokenizer |
| `Token indices sequence length is longer than ... 256` / lỗi vị trí | câu dài hơn 256 token | `truncation=True, max_length=...` (đừng tin `tok.model_max_length` của PhoBERT) |
| huấn luyện "sụp" về một lớp | learning rate quá lớn | dùng 1e-5…5e-5 + warmup |
| NER lệch ranh giới giữa huấn luyện/suy luận | khác bộ tách từ hoặc khác cách tách token (`15/3`) | dùng đúng quy trình của dữ liệu huấn luyện (Bài 11, mục 9) |
| nhầm giấy phép khi dùng thương mại | `phobert-base-v2` là AGPL-3.0 | đọc giấy phép; dùng `phobert-base` (MIT) hoặc tuân thủ AGPL |

## 7. Notebook không tìm thấy `nlpvi` hoặc dữ liệu

Mỗi notebook đầu tiên thêm thư mục gốc dự án vào `sys.path` và hoạt động nếu thư mục làm việc là `notebooks/` hoặc thư mục gốc. Nếu bạn mở notebook từ nơi khác, đặt thư mục làm việc về gốc dự án. Kiểm tra: `import nlpvi; print(nlpvi.ROOT)`.

## 8. Kết quả khác với số trong notebook

- **Mạng nơ-ron và GPU không tất định từng bit**: chạy lại có thể lệch vài phần nghìn đến vài phần trăm; mô hình nhỏ và dữ liệu nhỏ lệch nhiều hơn. Kết luận (xu hướng, thứ hạng lớn) vẫn giữ.
- Cố định seed bằng `nlpvi.set_seed(seed)`; ghi lại phiên bản thư viện.
- Kiểm tra nhanh toàn bộ: `python tools/check_notebooks.py`.

## 9. Mô hình/dữ liệu sinh ra làm repo quá nặng

Thư mục `outputs/` (mô hình PhoBERT đã tinh chỉnh, ≈ 0,5 GB) được ghi vào `.gitignore`. Đừng đưa nó lên git; dùng Hugging Face Hub hoặc Git LFS nếu cần chia sẻ.

## 10. Các bài mở rộng (Bài 16–19)

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| Bài 16/17/18 in `⚠ Không tải được UIT-VSFC...` rồi chạy trên dữ liệu tổng hợp | không có Internet, chưa cài `datasets`, hoặc cache chưa có | cài `requirements-transformers.txt` và chạy online một lần; số liệu trên dữ liệu tổng hợp **cao giả tạo** (khuôn mẫu), đừng so với số trong bài |
| Bài 17 mục 7 hoặc Bài 18 mục 4 tải mô hình rất lâu | lần đầu tải `multilingual-e5-small` (≈ 0,5 GB) | chờ; sau đó dùng bản đã lưu. Bài 18 còn lưu embedding vào `outputs/cache/*.npy` (xóa tệp để tính lại) |
| Bài 18: lần đầu mất ≈ 3 phút ở ô tính embedding | tính 11,4 nghìn câu bằng e5 trên CPU | bình thường; các lần sau đọc từ bộ nhớ đệm |
| Bài 19 mục 6 in `Bỏ qua Marian vì thiếu thư viện` | `MarianTokenizer` cần `sentencepiece` | `pip install sentencepiece` (đã có trong `requirements-transformers.txt`) |
| Bài 19: bản dịch/tóm tắt của Qwen lẫn **chữ Hán** | mô hình đa ngôn ngữ đôi khi đổi ngôn ngữ giữa chừng | đây là hiện tượng thật, bài đếm nó (mục 5, 6); giảm bằng prompt chặt hơn, mô hình lớn hơn hoặc giải mã có ràng buộc |
| Bài 17 mục 8 / Bài 19 mục 5–6 chạy rất chậm hoặc bỏ qua | không có GPU | các mục này tự bỏ qua khi không có CUDA; muốn chạy trên CPU hãy dùng mô hình `Qwen2.5-0.5B-Instruct` và ít mẫu hơn |
| Điểm ROUGE/BLEU của bạn khác con số trong bài hoặc khác thư viện | khác cách tách token, số tham chiếu, làm mịn | xem Bài 19 mục 2.1; thử đối chiếu bản tự cài với `sacrebleu` (xem `tests/test_metrics_gen.py`) |

