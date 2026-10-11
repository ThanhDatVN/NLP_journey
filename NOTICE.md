# Ghi nguồn và thông báo của bên thứ ba

## 1. Thành phần được trích từ tác phẩm khác

### `data/tu_ghep_phobert.txt`

Danh sách từ ghép trích từ **từ vựng của `vinai/phobert-base`** (PhoBERT), dùng làm từ điển cho bộ tách từ thuần Python ở `nlpvi/segment.py`. PhoBERT được phát hành theo giấy phép MIT:

```text
MIT License

Copyright (c) 2020 VinAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Nguồn: <https://github.com/VinAIResearch/PhoBERT>. Bài báo: Nguyen & Nguyen (2020), *PhoBERT: Pre-trained language models for Vietnamese*, Findings of EMNLP.

## 2. Nguồn cảm hứng (không sao chép nội dung)

- **[huggingface/course](https://github.com/huggingface/course)** (Apache-2.0, có bản dịch tiếng Việt): khung kỹ thuật phần Transformer của giáo trình bám theo thứ tự các chương của khóa này. Các notebook trong repo là **biên soạn mới**, không sao chép notebook hay văn bản của nguồn đó.
- **[fastai/course-nlp](https://github.com/fastai/course-nlp)**: tham khảo thứ tự "bài toán trước, giải thích sau" cho phần cổ điển.

## 3. Dữ liệu và mô hình tải lúc chạy (không phân phối trong repo)

Các tài nguyên sau được tải từ Hugging Face Hub khi chạy notebook; mỗi tài nguyên theo giấy phép của nơi phát hành. **Hãy đọc thẻ gốc trước khi dùng ngoài mục đích học tập.**

| Tài nguyên | Dùng ở | Ghi chú giấy phép (kiểm tra lại tại nguồn) |
|---|---|---|
| UIT-VSFC (`uitnlp/vietnamese_students_feedback`) | Bài 10, 15–18 | thẻ ghi `unknown` |
| PhoNER_COVID19 (bản sao `truongpdd/NER-covid-vietnamese-word`) | Bài 11, 17 | bản sao không ghi giấy phép; dữ liệu gốc của VinAI Research |
| `vinai/phobert-base` | Bài 9–11 | MIT (lưu ý `phobert-base-v2` là AGPL-3.0, khóa học không dùng) |
| `intfloat/multilingual-e5-small` | Bài 12, 17–19 | MIT |
| `bkai-foundation-models/vietnamese-bi-encoder` | Bài 12 | Apache-2.0 |
| `Qwen/Qwen2.5-0.5B-Instruct`, `Qwen/Qwen2.5-1.5B-Instruct` | Bài 13, 15, 17, 19 | Apache-2.0 |
| `Helsinki-NLP/opus-mt-en-vi` | Bài 19 | xem thẻ mô hình |

## 4. Thư viện

Khóa học dùng các thư viện mã nguồn mở (NumPy, pandas, scikit-learn, PyTorch, Transformers, Datasets, PEFT, FastAPI, Gradio...) theo giấy phép của từng thư viện; chúng được cài qua `pip` và **không** được phân phối trong repo.
