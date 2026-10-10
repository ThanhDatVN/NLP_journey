# Thẻ dữ liệu (Data Card) — bộ dữ liệu của khóa học

Mọi tệp trong thư mục này **do giáo trình tự biên soạn** (trừ `tu_ghep_phobert.txt`, trích từ từ vựng mô hình). Mục đích duy nhất: **học quy trình NLP và để mọi kết quả chạy lại được**. Không dùng để suy luận về chất lượng mô hình ngoài đời thực, và không chứa dữ liệu cá nhân thật.

## Bảng tóm tắt

| Tệp | Nội dung | Kích thước | Cách tạo | Dùng ở |
|---|---|---|---|---|
| `reviews_vi.csv` | đánh giá tổng hợp: `id, text, label, domain, split` | 1.800 dòng | **sinh tự động** bằng `tools/make_data.py` (seed 20261003) | Bài 0–8, 10 (dự phòng), 14 |
| `reviews_hard.csv` | 40 câu "khó" viết tay: `id, text, label, hien_tuong` | 40 dòng | viết tay | Bài 3, 6, 7, 8, 10, 13, 14 |
| `ner_mini.txt` | 38 câu có thực thể (PER/LOC/ORG/DATE), dạng `[cụm\|LOẠI]` | 38 câu, 86 thực thể | viết tay | Bài 11 |
| `faq_docs.json` | 24 đoạn FAQ của một cửa hàng **hư cấu** | 24 đoạn | viết tay | Bài 12, 13 |
| `faq_queries.json` | 33 truy vấn có đáp án (`gold`) và `kieu` | 33 truy vấn | viết tay | Bài 12, 13 |
| `tu_ghep_phobert.txt` | từ điển 22.226 từ ghép (có `_`), dùng cho bộ tách từ thuần Python | 22.226 dòng | trích từ từ vựng `vinai/phobert-base` (MIT), lọc bỏ mảnh vụn | `nlpvi/segment.py` |

Mã hóa: **UTF-8** (`reviews_vi.csv` có BOM; đọc bằng `encoding="utf-8-sig"`).

## `reviews_vi.csv` — đánh giá tổng hợp

**Cách sinh.** Ghép từ các mẫu câu có kiểm soát trong năm miền (*sản phẩm, ứng dụng, ẩm thực, dịch vụ, khóa học*), ba nhãn (*tích cực, tiêu cực, trung tính*, tỉ lệ mục tiêu 45/35/20). Mỗi miền có danh sách *khía cạnh – tính từ khen – tính từ chê*. Các khuôn câu: khen/chê đơn; hai mệnh đề cùng chiều; đối lập ("Tuy A nhưng B"; **mệnh đề sau quyết định nhãn**); phủ định ("không tệ" → tích cực; "không tốt" → tiêu cực); "Ưu điểm … Nhược điểm …" → trung tính; câu trung tính theo miền.

**Nhiễu có chủ đích:** teencode (`ko`, `dc`, `sp`...), hạ chữ thường, **bỏ dấu** (~6%), emoji (~15%, có khi ngược nghĩa), lặp dấu `!`, câu mở đầu/kết ("Recommend nhé!", "Cho 1 sao"), và **~3% nhãn bị đảo ngẫu nhiên**.

**Chia tập:** cột `split` cố định = băm MD5 của `id` mod 100 (<70 train, <85 valid, còn lại test) → tất định và ổn định khi thêm dữ liệu.

**Phân phối:** tích cực ≈ 45,8%, tiêu cực ≈ 35,8%, trung tính ≈ 18,4%; năm miền xấp xỉ đều.

### Hạn chế đã biết (đọc trước khi diễn giải kết quả)

1. **Không phải bình luận thật.** Từ vựng rất nhỏ (~570 âm tiết khác nhau trong tập train), cấu trúc lặp lại; ngôn ngữ thật đa dạng hơn nhiều.
2. **Rò rỉ khuôn câu.** Train và test chia sẻ cùng khuôn câu; ≈5% mẫu valid/test có bản trùng ẩn trong train (Bài 0). Điểm trên valid/test vì thế **lạc quan**.
3. **Tín hiệu lối tắt.** Ví dụ mẫu "Ưu điểm … Nhược điểm …" luôn là *trung tính*; câu kết "Recommend nhé!" gần như luôn *tích cực*. Mô hình học những lối tắt này (Bài 3 mục 7; Bài 14 mục 4).
4. **Phủ cụm từ không đều.** Một số từ rất hiếm (ví dụ "tốt" chỉ xuất hiện 6 lần trong train), nên hệ số của chúng nhiễu.
5. **Nhãn nhiễu 3%** là có chủ đích; một số nhãn có thể trái trực giác (Bài 3 mục 8.1 dùng nó để thực hành tìm nhãn sai).
6. **Quy ước nhãn** là của người thiết kế: "trung tính" gồm cả câu mô tả sự kiện và câu cân bằng ưu/nhược điểm.

**Giấy phép dữ liệu:** do giáo trình tự sinh; bạn có thể dùng cho mục đích học tập. Hãy đặt giấy phép cho cả repo trước khi chia sẻ công khai.

## `reviews_hard.csv` — 40 câu khó

Mỗi dòng gắn một **hiện tượng ngôn ngữ** (`hien_tuong`): phủ định (của từ khen/chê), đối lập (vế sau quyết định), mỉa mai, không dấu, teencode, câu hỏi, so sánh, trung tính, lưỡng lự, emoji ngược nghĩa, câu không có từ cảm xúc rõ.

- Nhãn do **người biên soạn gán theo ý định hợp lý nhất**; một số ca (mỉa mai, lưỡng lự) có thể gây tranh luận.
- **Rất nhỏ**: mỗi câu = 2,5 điểm phần trăm; tỉ lệ theo từng hiện tượng (1–8 câu) chỉ mang tính gợi ý.
- **Không dùng để chọn mô hình** (sẽ biến nó thành tập validation). Nếu bạn đổi mô hình vì điểm trên tập này, hãy viết thêm một tập khó mới để kiểm tra độc lập.

## `ner_mini.txt`

38 câu viết tay, dùng ký hiệu `[cụm|LOẠI]`; token đã tách theo âm tiết và dấu câu tách khoảng trắng. Hai câu cuối **không có thực thể** (để kiểm tra dương tính giả). Nhãn mức âm tiết (BIO) được suy ra khi nạp (Bài 11). Quy ước ranh giới là của người biên soạn (ví dụ gồm cả "năm", "ngày" trong DATE) và khác dữ liệu PhoNER — chính sự khác biệt này là một bài học ở Bài 11.

## `faq_docs.json` và `faq_queries.json`

Kho FAQ của một cửa hàng **hư cấu** (đổi trả, vận chuyển, bảo hành, thanh toán, thành viên...). Mọi con số (7 ngày, 20.000 đồng...) là **bịa ra**, nên một LLM không thể biết sẵn — phù hợp để chứng minh tác dụng của RAG và ảo giác. Truy vấn được gán `kieu`: *diễn đạt lại* (23), *từ khóa trùng* (5), *chi tiết số* (3), *nhiều đáp án* (2). Với 33 truy vấn, **mỗi truy vấn ≈ 3 điểm phần trăm**; chênh lệch 1–2 truy vấn giữa các hệ thống là nhiễu.

## `tu_ghep_phobert.txt`

Danh sách từ ghép (chứa dấu gạch dưới, 2–4 âm tiết, mọi âm tiết là chữ cái) trích từ từ vựng của `vinai/phobert-base` (giấy phép MIT), dùng làm từ điển cho thuật toán khớp tối đa ở `nlpvi/segment.py`. **Giới hạn:** là xấp xỉ rẻ của RDRSegmenter, không phải nó; nhiều từ ghép thông dụng (như "giao hàng") có thể không có trong danh sách; còn lẫn một số mảnh BPE hiếm.

## `tom_tat_mini.json` (Bài 19)

**16 đoạn văn hư cấu** (mỗi đoạn 5 câu, ≈ 75 từ; giáo dục, y tế, kinh tế, công nghệ, giao thông, môi trường, thể thao, du lịch, thương mại điện tử, năng lượng, nông nghiệp, an ninh mạng, thời tiết, đô thị, tiêu dùng, văn hóa) kèm **hai bản tóm tắt tham chiếu** (`tom_tat_a`, `tom_tat_b`) do người biên soạn viết độc lập. Tên riêng, số liệu và sự kiện đều **bịa ra**; không phải tin thật và không nên trích dẫn như tin thật.

- **Rất nhỏ**: 16 đoạn; điểm trung bình dao động mạnh và không cho phép kết luận về chất lượng một hệ thống (Bài 19 dùng nó để học cách đo).
- Cả hai tóm tắt do **cùng một người** viết nên có thể giống phong cách nhau (đồng thuận giữa A và B ở Bài 19 là *cận trên lạc quan* của đồng thuận giữa hai người khác nhau).
- Văn bản viết theo kiểu tin tức nên **câu đầu thường nêu ý chính**: đường cơ sở "câu đầu" mạnh một phần vì cách viết này.

## `dich_mini.json` (Bài 19)

**24 câu tiếng Anh** (mua sắm, du lịch, công nghệ, đời sống) kèm **hai bản dịch tiếng Việt tham chiếu** (`vi`) do người biên soạn viết. Câu ngắn, đơn nghĩa; không có thành ngữ hay văn cảnh dài.

- **Rất nhỏ**: mỗi câu ≈ 4 điểm phần trăm; Bài 19 dùng bootstrap để cho thấy khoảng tin cậy rộng.
- Hai bản dịch chỉ là hai cách dịch hợp lý trong nhiều cách; BLEU/chrF vì vậy phụ thuộc vào số và phong cách tham chiếu.

## Dữ liệu thật dùng trong khóa (tải lúc chạy, không đi kèm)

| Bộ | Dùng ở | Nguồn | Ghi chú giấy phép |
|---|---|---|---|
| UIT-VSFC (`uitnlp/vietnamese_students_feedback`) | Bài 10, 15, 16, 17, 18 | Hugging Face Hub (nhánh `refs/convert/parquet`) | thẻ ghi `license: unknown`; dùng cho học tập/nghiên cứu, kiểm tra điều khoản gốc |
| PhoNER_COVID19 (bản sao `truongpdd/NER-covid-vietnamese-word`) | Bài 11, 17 (văn bản tin tức để huấn luyện mô hình khôi phục dấu) | Hugging Face Hub | bản sao không ghi giấy phép; dữ liệu gốc của VinAI Research |

Hai bộ này **không được phân phối lại** trong repo.
