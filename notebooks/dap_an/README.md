# Đáp án bằng mã cho bài tập

Mỗi notebook ở đây giải **các bài tập của bài học tương ứng** bằng mã chạy được và có **kết quả đã lưu**, kèm phần "Đọc kết quả" — nơi nhận xét luôn đối chiếu với số đo thật (nhiều chỗ kết quả *khác* điều ta kỳ vọng, và đáp án nói rõ như vậy).

**Cách dùng:** hãy tự làm bài tập trước, rồi mới mở đáp án để đối chiếu. Đáp án không phải duy nhất; nếu cách của bạn khác nhưng cho cùng kết luận và bạn giải thích được vì sao, đó cũng là đáp án đúng.

| Notebook | Bài | Cần | Ghi chú |
|---|---|---|---|
| `00_dap_an_bai_00` | 0 · Khởi động và dữ liệu | CPU | độ dài theo nhãn (bootstrap), trùng ẩn, stratify, `GroupShuffleSplit` |
| `01_dap_an_bai_01` | 1 · Tiền xử lý | CPU | regex số, teencode, tách câu, ứng viên từ ghép bằng PMI, từ điển riêng |
| `02_dap_an_bai_02` | 2 · Biểu diễn văn bản | CPU | binary vs đếm, idf, cosine, NMF 3/5/8, n-gram ký tự |
| `03_dap_an_bai_03` | 3 · Phân loại và đánh giá | CPU | luật tay có phủ định, ổn định thứ hạng qua nhiều cách chia, sửa/loại nhãn |
| `04_dap_an_bai_04` | 4 · n-gram | CPU | PP test, add-k, stupid backoff, bộ phân loại sinh |
| `05_dap_an_bai_05` | 5 · Embedding | CPU | cửa sổ, số chiều, trọng số idf, ghép TF-IDF, subsampling |
| `06_dap_an_bai_06` | 6 · Mạng nơ-ron | CPU (~5 phút) | SGD vs Adam, kernels, khởi tạo PPMI-SVD, label smoothing, BiGRU |
| `07_dap_an_bai_07` | 7 · RNN/LSTM/GRU | CPU (~5 phút) | gradient, seq2seq hidden/hai chiều, pack, LSTM cell NumPy |
| `08_dap_an_bai_08` | 8 · Transformer | CPU (~5 phút) | số đầu, bỏ vị trí, O(L²), mini-GPT, cross-attention |
| `09_dap_an_bai_09` | 9 · Hugging Face | Internet (+GPU tùy chọn) | quét BPE, tách từ, các lớp PhoBERT, đặc trưng đóng băng, WordPiece |
| `12_dap_an_bai_12` | 12 · Tìm kiếm | Internet | BM25 k1/b, RRF, truy vấn không dấu, nDCG chia bậc |
| `14_dap_an_bai_14` | 14 · Triển khai, đạo đức | CPU (+PhoBERT từ Bài 10) | che tên, CheckList, phản thực tế giới tính + bootstrap, rate limiter, pytest |
| `16_dap_an_bai_16` | 16 · Dữ liệu nhãn *(mở rộng)* | CPU (~4 phút) | κ theo mức cẩu thả, kiểu nhiễu bất đối xứng × trọng số lớp, học tích cực theo lô đa dạng |
| `17_dap_an_bai_17` | 17 · Khôi phục dấu *(mở rộng)* | CPU, Internet (dữ liệu) | trọng số nội suy λ, từ điển bổ sung theo lượng dữ liệu, beam search so với Viterbi |
| `18_dap_an_bai_18` | 18 · Phân cụm, chủ đề *(mở rộng)* | CPU (~5 phút), cần embedding của Bài 18 | `n_init` và độ ổn định, tiền tố e5, phân cụm phân cấp, chỉ câu tiêu cực |
| `19_dap_an_bai_19` | 19 · Sinh văn bản, độ đo *(mở rộng)* | CPU (e5 tải lần đầu) | tách token âm tiết vs từ ghép, phép thử sửa-ít-chữ, ROUGE-S, bộ kiểm tra trung thực v2 |

**Các bài 10, 11, 13, 15** (cần GPU và chạy lâu) chỉ có **gợi ý đáp án bằng lời** ở cuối notebook bài tương ứng. Với Bài 16–19, đáp án mã chỉ giải các bài tập chạy được trên CPU; bài tập nặng (BiLSTM, PhoBERT, LLM làm giám khảo) chỉ có gợi ý bằng lời. Bạn nên tự cài đặt, vì việc này cho bạn trải nghiệm trực tiếp về siêu tham số, VRAM và thời gian chạy.

## Dựng lại

```powershell
python tools/build_notebooks.py --dap-an 03 --run     # dựng và chạy lại đáp án Bài 03
```

Nguồn văn bản của đáp án nằm ở `tools/notebook_src/dap_an/`.
