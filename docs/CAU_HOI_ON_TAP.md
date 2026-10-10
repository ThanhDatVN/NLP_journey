# Câu hỏi ôn tập

Mỗi bài (0–19) có 5–6 câu trắc nghiệm (một đáp án đúng) để **tự kiểm tra** sau khi học, tương tự phần "Đố vui" của khóa Hugging Face. Hãy tự trả lời trước, rồi mở phần **Đáp án** (bấm vào dòng chữ để mở). Mỗi đáp án có giải thích ngắn và chỉ ra mục trong bài để đọc lại.

> Một số câu hỏi dựa trên con số đo được trong notebook ("≈…"). Các con số này là của một lần chạy ở máy biên soạn; nếu bạn chạy lại và thấy lệch nhẹ, hãy dựa vào *hình dạng của kết luận* chứ không phải chữ số cuối cùng.

---

## Bài 0 · Khởi động và dữ liệu

**1.** Mô hình luôn đoán nhãn phổ biến nhất trên `reviews_vi.csv` có accuracy ≈ 0,45 nhưng macro-F1 chỉ ≈ 0,2. Lý do?

- A. Macro-F1 luôn nhỏ hơn accuracy ở mọi mô hình.
- B. Mô hình không bao giờ dự đoán hai lớp còn lại nên F1 của chúng bằng 0, kéo trung bình xuống.
- C. Dữ liệu bị sai nhãn.
- D. Macro-F1 chỉ tính trên lớp phổ biến nhất.

**2.** Hai chuỗi `"học"` (NFC) và `"học"` (NFD) hiển thị giống hệt nhau nhưng `==` trả `False`. Vì sao, và nên làm gì?

- A. Do khác phông chữ; đổi phông.
- B. Do độ dài chuỗi khác nhau vì thêm khoảng trắng; dùng `strip()`.
- C. Do dùng chuỗi điểm mã Unicode khác nhau (dựng sẵn vs tổ hợp); chuẩn hóa về NFC khi đọc dữ liệu.
- D. Do Python so sánh theo hình dạng; không có cách sửa.

**3.** Vì sao khóa học cố định cột `split` bằng cách băm `id` thay vì chia ngẫu nhiên mỗi lần chạy?

- A. Để tăng accuracy.
- B. Để kết quả chạy lại giống nhau và thêm dữ liệu mới không làm các mẫu cũ đổi sang tập khác.
- C. Vì băm giúp cân bằng lớp hoàn hảo.
- D. Vì `train_test_split` bị cấm.

**4.** ≈5% mẫu valid/test có "bản trùng ẩn" trong train (sau khi hạ chữ, bỏ dấu...). Hệ quả chính?

- A. Điểm trên valid/test có xu hướng lạc quan hơn chất lượng thật.
- B. Điểm trên valid/test thấp hơn chất lượng thật.
- C. Không ảnh hưởng gì vì không trùng từng ký tự.
- D. Mô hình không thể học.

**5.** Tập nào được xem **nhiều lần** khi chọn mô hình/siêu tham số, và tập nào chỉ mở một lần ở cuối?

- A. Test xem nhiều lần; valid mở một lần.
- B. Cả hai xem nhiều lần.
- C. Valid xem nhiều lần; test mở một lần ở cuối.
- D. Train mở một lần; test xem nhiều lần.

<details><summary><b>Đáp án Bài 0</b></summary>

1. **B.** Không bao giờ đoán lớp *tiêu cực* và *trung tính* ⇒ precision/recall/F1 của hai lớp đó = 0; macro-F1 là trung bình F1 các lớp. (Mục 6.)
2. **C.** Python so sánh theo điểm mã; "ọ" có thể là 1 hoặc 2–3 điểm mã. `unicodedata.normalize("NFC", ...)`. (Mục 3c.)
3. **B.** Băm `id` tất định và ổn định khi dữ liệu tăng. (Mục 5.)
4. **A.** Mô hình gặp lại thứ nó đã thấy; hơn nữa train/test còn chia sẻ khuôn câu. (Mục 5.1.)
5. **C.** Valid để chọn mô hình; test chỉ để báo cáo cuối cùng, một lần. (Mục 5 bảng.)
</details>

---

## Bài 1 · Tiền xử lý tiếng Việt

**1.** "Học sinh đang học xử lý ngôn ngữ tự nhiên" tách theo khoảng trắng được 10 âm tiết. Sau khi tách từ đúng, bao nhiêu từ?

- A. 10  B. 8  C. 6  D. 4

**2.** Biểu thức `re.sub(r"(\w)\1{2,}", r"\1", "Giá 1000 đồng")` gây lỗi gì?

- A. Không lỗi.
- B. Biến "1000" thành "10" vì `\w` cũng khớp chữ số — hỏng số liệu một cách âm thầm.
- C. Xóa toàn bộ chữ "đồng".
- D. Báo lỗi cú pháp.

**3.** Vì sao không nên xóa "không", "chưa", "chẳng" như từ dừng trong bài toán cảm xúc?

- A. Vì chúng quá hiếm.
- B. Vì chúng mang tín hiệu cảm xúc và đảo nghĩa ("giá không rẻ" ≠ "giá rẻ"); đo được cả trên CV lẫn trên câu khó.
- C. Vì tokenizer không xử lý được.
- D. Vì chúng luôn là từ tích cực.

**4.** Phát biểu nào về **bỏ dấu** là đúng theo khóa học?

- A. Luôn có lợi vì giảm kích thước từ điển.
- B. Luôn có hại vì làm mất nghĩa.
- C. Mặc định nên giữ dấu, nhưng phải **đo**: trên dữ liệu nhỏ lẫn nhiều dòng không dấu, bỏ dấu có thể không hại (Bài 3), còn với mô hình tiền huấn luyện thì thường hại (Bài 9, 12).
- D. Không có ảnh hưởng gì.

**5.** Thuật toán *khớp tối đa từ trái sang phải* (forward maximum matching) làm gì?

- A. Tại mỗi vị trí thử ghép 4, 3, 2 âm tiết liên tiếp; nếu cụm có trong từ điển thì lấy cụm dài nhất.
- B. Huấn luyện một mạng nơ-ron để dự đoán ranh giới từ.
- C. Chia câu theo dấu chấm.
- D. Sắp xếp âm tiết theo tần suất.

<details><summary><b>Đáp án Bài 1</b></summary>

1. **C.** Học_sinh · đang · học · xử_lý · ngôn_ngữ · tự_nhiên = 6 từ. (Mục 6.)
2. **B.** Phải dùng `([^\W\d_])\1{2,}` để chỉ gộp chữ cái. (Mục 2.)
3. **B.** Bảng tần suất ở mục 7 và thí nghiệm ở Bài 3 mục 11 (xóa phủ định làm giảm điểm CV và câu khó).
4. **C.** Xem Bài 1 mục 4 và Bài 3 mục 11; lưu ý chiều ngược lại ở Bài 9 (số token tăng mạnh) và Bài 12 (dense sụp với truy vấn không dấu).
5. **A.** Mục 6; từ điển lấy từ các từ ghép trong từ vựng PhoBERT.
</details>

---

## Bài 2 · Biểu diễn văn bản

**1.** Với `smooth_idf=True`, từ xuất hiện trong **mọi** văn bản có idf bằng?

- A. 0  B. 1  C. ln 2  D. vô cùng

**2.** Vì sao cosine được ưa dùng hơn khoảng cách Euclid để so hai văn bản TF-IDF?

- A. Cosine không phụ thuộc độ dài văn bản (chỉ xét hướng của vector).
- B. Cosine luôn nhanh hơn 100 lần.
- C. Euclid không áp dụng được cho ma trận thưa.
- D. Cosine cho kết quả âm.

**3.** Truy vấn "shipper tới trễ nhiều ngày" không tìm được câu "giao hàng chậm" bằng TF-IDF vì?

- A. TF-IDF so khớp *chữ*, không so khớp *nghĩa*; hai câu gần như không chung từ.
- B. TF-IDF chỉ làm việc với tiếng Anh.
- C. Ma trận quá dày.
- D. Do hạ chữ thường.

**4.** Việc `fit` TfidfVectorizer trên toàn bộ dữ liệu (cả test) rồi mới chia có hại gì?

- A. Không hại vì TF-IDF không có nhãn.
- B. Từ điển và idf đã "thấy" thống kê của tập kiểm tra → rò rỉ, điểm kiểm tra lạc quan.
- C. Làm ma trận thưa hơn.
- D. Làm mô hình quá khớp trên train.

**5.** NMF khác SVD (LSA) ở điểm nào khiến chủ đề dễ đọc hơn?

- A. NMF nhanh hơn.
- B. NMF ràng buộc mọi phần tử ≥ 0 nên mỗi chủ đề là tổ hợp *cộng* các từ, không có thành phần âm.
- C. NMF dùng nhãn.
- D. NMF luôn cho đúng 5 chủ đề.

<details><summary><b>Đáp án Bài 2</b></summary>

1. **B.** idf = ln((1+n)/(1+df)) + 1; df = n ⇒ ln 1 + 1 = 1. (Mục 1.2; kết quả ở "giao", dấu ",".)
2. **A.** Mục 3.
3. **A.** Mục 3; Embedding (Bài 5, 12) sinh ra để khắc phục.
4. **B.** Mục 5.
5. **B.** Mục 4.2.
</details>

---

## Bài 3 · Phân loại và đánh giá

**1.** Vì sao dùng `Pipeline([TfidfVectorizer, LogisticRegression])` trong cross-validation giúp tránh rò rỉ?

- A. Vì Pipeline chạy nhanh hơn.
- B. Vì ở mỗi fold, bộ vector hóa được `fit` lại chỉ trên phần train của fold đó.
- C. Vì Pipeline tự chọn tham số tốt nhất.
- D. Vì Pipeline loại bỏ từ dừng.

**2.** Bật `class_weight="balanced"` thường làm gì?

- A. Tăng recall của lớp hiếm, đổi lại có thể giảm precision của nó — một đánh đổi, không miễn phí.
- B. Luôn tăng cả accuracy và macro-F1.
- C. Giảm số tham số.
- D. Không thay đổi gì.

**3.** Khoảng tin cậy bootstrap 95% của macro-F1 trên valid (≈ [0,85; 0,92]) cho biết?

- A. Độ bất định của điểm số do kích thước tập kiểm tra hữu hạn.
- B. Độ biến thiên do chọn seed khi huấn luyện.
- C. Mô hình đúng ít nhất 85% lần.
- D. Điểm trên test chắc chắn nằm trong khoảng này.

**4.** Mô hình đạt ≈0,89 accuracy trên valid nhưng ≈0,58 trên 40 câu "khó". Bài học chính?

- A. Tập câu khó có lỗi.
- B. Điểm trên tập *cùng phân phối với huấn luyện* chỉ nói về "vùng quen thuộc"; cần tập kiểm tra khó/khác phân phối.
- C. Cần thêm epoch.
- D. Phải xóa từ phủ định.

**5.** Bạn thấy mô hình bigram tốt hơn trên tập câu khó nên đổi mô hình theo đó. Điều gì xảy ra với tập câu khó?

- A. Không có gì.
- B. Nó trở thành tập validation thứ hai, không còn là phép thử độc lập; cần viết thêm tập khó mới.
- C. Nó trở thành tập train.
- D. Nó tự động đáng tin hơn.

<details><summary><b>Đáp án Bài 3</b></summary>

1. **B.** Mục 2.
2. **A.** Mục 6.
3. **A.** Mục 10; bootstrap lấy mẫu lại *tập kiểm tra*, không phản ánh biến thiên huấn luyện.
4. **B.** Mục 9.
5. **B.** Nhận xét cuối mục 12.
</details>

---

## Bài 4 · Mô hình ngôn ngữ n-gram

**1.** Một mô hình đoán đều trên từ điển V từ có perplexity bằng?

- A. 1  B. V  C. log V  D. V²

**2.** Vì sao bigram MLE gán xác suất 0 cho một câu chứa một cặp từ chưa từng thấy?

- A. Vì xác suất cả câu là *tích* các xác suất có điều kiện; một thừa số 0 làm cả tích bằng 0.
- B. Vì thiếu dấu câu.
- C. Vì từ điển quá lớn.
- D. Vì dùng log.

**3.** Nội suy $\lambda_1 P(w)+\lambda_2 P(w|v)+\lambda_3 P(w|u,v)$ có các hệ số λ nên chọn trên tập nào?

- A. Train.  B. Test.  C. Validation.  D. Tập bất kỳ.

**4.** Perplexity của hai mô hình ngôn ngữ chỉ so sánh trực tiếp được khi?

- A. Chúng có cùng số tham số.
- B. Chúng dùng cùng từ điển và cùng cách tách token (trên cùng dữ liệu).
- C. Chúng cùng ngôn ngữ.
- D. Không bao giờ so được.

**5.** Giới hạn nào dưới đây **không** phải của n-gram?

- A. Dữ liệu thưa khi n tăng.
- B. Không có khái niệm "gần nghĩa" giữa các từ.
- C. Chỉ nhìn được ngữ cảnh ngắn.
- D. Không thể tính được xác suất của câu.

<details><summary><b>Đáp án Bài 4</b></summary>

1. **B.** Mỗi bước phân vân giữa V ứng viên. (Mục 5.)
2. **A.** Mục 4; giải quyết bằng add-k/nội suy.
3. **C.** Không chọn trên test. (Mục 5.2.)
4. **B.** Ghi chú cuối mục 9.
5. **D.** n-gram *tính* được xác suất câu; A–C là giới hạn thật (mục 8).
</details>

---

## Bài 5 · Word embedding

**1.** "Giả thuyết phân bố" nói gì?

- A. Từ có nghĩa giống nhau thì viết giống nhau.
- B. Nghĩa của từ có thể suy ra từ ngữ cảnh nó xuất hiện (từ đi cùng).
- C. Mọi từ phân bố đều trong văn bản.
- D. Từ phổ biến thì quan trọng.

**2.** Vì sao PPMI dùng phân phối ngữ cảnh làm mịn $P(c)\propto \text{count}^{0.75}$?

- A. Để ưu ái từ hiếm một chút, giảm thiên lệch về từ ngữ cảnh rất phổ biến.
- B. Để làm ma trận dày hơn.
- C. Để tăng tốc SVD.
- D. Vì công thức PMI yêu cầu.

**3.** Vì sao "nhanh" và "chậm" có thể có embedding gần nhau?

- A. Vì chúng cùng nghĩa.
- B. Vì chúng thường xuất hiện trong cùng ngữ cảnh ("giao hàng *nhanh*/*chậm*"); embedding đo khả năng thay thế trong ngữ cảnh chứ không đo đồng nghĩa.
- C. Do lỗi huấn luyện.
- D. Vì cùng số âm tiết.

**4.** Vì sao vector trung bình embedding + LR kém TF-IDF + LR trên dữ liệu của khóa?

- A. Kho nhỏ, trung bình làm mất thứ tự/phủ định, embedding không giám sát chỉ mã hóa cảm xúc gián tiếp.
- B. Embedding luôn kém TF-IDF.
- C. Do dùng PyTorch.
- D. Do dùng GPU.

**5.** Hạn chế "một vector cho mỗi từ" của embedding tĩnh được giải quyết bằng?

- A. Tăng số chiều.
- B. Embedding theo ngữ cảnh (BERT/PhoBERT).
- C. Bỏ dấu.
- D. Dùng cửa sổ lớn hơn.

<details><summary><b>Đáp án Bài 5</b></summary>

1. **B.** Mục 1.
2. **A.** Mục 3.2 (mẹo của Word2Vec).
3. **B.** Mục 3.3 và 6; kết quả cũng cho thấy SVD và Skip-gram khác nhau ở chi tiết.
4. **A.** Mục 7.
5. **B.** Mục 8; Bài 9 mục 6 minh họa bằng "đá".
</details>

---

## Bài 6 · Mạng nơ-ron cho văn bản

**1.** Gradient của loss cross-entropy trung bình đối với $W$ trong hồi quy softmax là?

- A. $\frac1n X^\top (P-Y)$  B. $X (P-Y)^\top$  C. $P-Y$  D. $\frac1n X^\top P$

**2.** Mục đích của *gradient check* (so với sai phân số)?

- A. Tăng tốc huấn luyện.
- B. Phát hiện lỗi khi tự cài gradient: gradient giải tích phải khớp xấp xỉ gradient số.
- C. Chọn learning rate.
- D. Chuẩn hóa dữ liệu.

**3.** Vì sao khi lấy trung bình embedding phải dùng mặt nạ bỏ ô đệm?

- A. Để nhanh hơn.
- B. Nếu không, các vector đệm (và độ dài câu) lọt vào kết quả.
- C. Vì ô đệm có nhãn.
- D. Vì embedding không chấp nhận số 0.

**4.** Đường cong loss: loss train giảm đều, loss valid giảm rồi tăng. Bạn nên?

- A. Huấn luyện thêm.
- B. Dừng/chọn checkpoint ở điểm valid tốt nhất (dừng sớm) — dấu hiệu quá khớp.
- C. Tăng learning rate.
- D. Bỏ tập valid.

**5.** Vì sao báo cáo mean ± std qua nhiều seed thay vì một lần chạy?

- A. Để trông chuyên nghiệp.
- B. Kết quả mạng nơ-ron phụ thuộc seed (khởi tạo, thứ tự batch, dropout); một seed dễ là "chọn quả anh đào".
- C. Vì seed làm tăng điểm.
- D. Vì GPU cần nhiều seed.

<details><summary><b>Đáp án Bài 6</b></summary>

1. **A.** Mục 1.
2. **B.** Mục 1 (sai lệch cỡ 1e-11 trong notebook).
3. **B.** Mục 3–4.
4. **B.** Mục 5.
5. **B.** Mục 6.
</details>

---

## Bài 7 · RNN, LSTM, GRU

**1.** Vì sao gradient trong RNN thường biến mất khi chuỗi dài?

- A. Vì dữ liệu ít.
- B. Gradient qua T bước là tích của T ma trận Jacobi $\operatorname{diag}(1-\mathbf h^2)W_{hh}$; tích đó co theo cấp số mũ.
- C. Vì learning rate nhỏ.
- D. Vì dùng GPU.

**2.** Điều gì cho phép LSTM giữ thông tin xa tốt hơn RNN thường?

- A. Nhiều tham số hơn.
- B. Ô nhớ cập nhật chủ yếu bằng *cộng* có cổng quên/nhập, nên thông tin và gradient đi xuyên nhiều bước mà không bị nhân với ma trận ở mỗi bước.
- C. Dùng hàm kích hoạt ReLU.
- D. Đọc chuỗi ngược.

**3.** Vì sao dùng `pack_padded_sequence` với BiLSTM?

- A. Để RNN không xử lý ô đệm; trạng thái không bị "pha" bởi số 0.
- B. Để tăng số tham số.
- C. Để bỏ dropout.
- D. Để chuẩn hóa batch.

**4.** Gradient clipping giải quyết vấn đề nào?

- A. Gradient bùng nổ (chuẩn gradient đột ngột rất lớn).
- B. Gradient biến mất.
- C. Quá khớp.
- D. Dữ liệu mất cân bằng.

**5.** Thí nghiệm đảo ngược chuỗi chữ số cho thấy encoder–decoder không attention thế nào?

- A. Hoạt động tốt với mọi độ dài.
- B. Độ chính xác tụt mạnh khi chuỗi dài, vì toàn bộ nguồn bị nén vào một vector cố định (nút thắt).
- C. Chỉ hỏng khi có từ lạ.
- D. Không huấn luyện được.

<details><summary><b>Đáp án Bài 7</b></summary>

1. **B.** Mục 3 (đo thực nghiệm: cả bốn đường đều đi xuống).
2. **B.** Mục 4.
3. **A.** Mục 4.
4. **A.** Biến mất cần kiến trúc khác (LSTM/GRU, attention). Mục 3–4.
5. **B.** Mục 5; Bài 8 mục 7 giải quyết bằng attention.
</details>

---

## Bài 8 · Attention và Transformer

**1.** Vì sao chia tích vô hướng QKᵀ cho √dₖ?

- A. Để kết quả nằm trong [0,1].
- B. Phương sai của q·k tăng theo dₖ; không chia thì softmax bão hòa (một phần tử ≈ 1) và gradient gần như 0.
- C. Để giảm bộ nhớ.
- D. Vì công thức của RNN.

**2.** Mặt nạ **nhân quả** cho phép vị trí t nhìn những vị trí nào?

- A. Tất cả vị trí.
- B. Chỉ các vị trí ≤ t (ma trận tam giác dưới).
- C. Chỉ vị trí t.
- D. Chỉ các vị trí > t.

**3.** Vì sao Transformer cần mã hóa vị trí?

- A. Vì self-attention là hoán vị-tương-đương: không biết thứ tự; nếu xáo đầu vào, đầu ra chỉ bị xáo theo.
- B. Để tăng số tham số.
- C. Vì embedding từ quá nhỏ.
- D. Để làm mặt nạ.

**4.** Chi phí bộ nhớ/tính toán của self-attention theo độ dài chuỗi L là?

- A. O(L)  B. O(L log L)  C. O(L²)  D. O(1)

**5.** Trong thí nghiệm đảo chuỗi, mô hình dùng embedding vị trí *học được* đạt ≈100% ở L ≤ 16 nhưng ≈0% ở L = 20 và 24. Giải thích?

- A. Mô hình quá nhỏ.
- B. Embedding vị trí cho các chỉ số chưa từng thấy lúc huấn luyện chưa được học; nó không *ngoại suy*.
- C. Do lỗi mặt nạ.
- D. Do học quá lâu.

<details><summary><b>Đáp án Bài 8</b></summary>

1. **B.** Mục 2 (thực nghiệm: std của q·k ≈ √d).
2. **B.** Mục 3.
3. **A.** Mục 4 (kiểm tra bằng số).
4. **C.** Bảng tổng kết mục 9.
5. **B.** Mục 7; gợi ý hướng nghiên cứu: mã hóa vị trí tương đối, RoPE, ALiBi.
</details>

---

## Bài 9 · Hugging Face và tokenizer

**1.** Điều kiện đầu vào bắt buộc để dùng PhoBERT đúng cách là?

- A. Văn bản không dấu.
- B. Văn bản đã **tách từ** (ví dụ `Hà_Nội`, `thủ_đô`).
- C. Văn bản chữ hoa.
- D. Văn bản dưới 10 từ.

**2.** Giới hạn độ dài của PhoBERT là?

- A. 128 token.
- B. 256 token (258 vị trí gồm 2 token đặc biệt); không nên tin `tok.model_max_length` của tokenizer này.
- C. 512 token.
- D. Không giới hạn.

**3.** Điểm cần lưu ý về giấy phép của họ PhoBERT trên Hugging Face?

- A. Cả hai bản đều MIT.
- B. `phobert-base` ghi MIT nhưng `phobert-base-v2` ghi AGPL-3.0 (copyleft mạnh); luôn đọc lại thẻ mô hình.
- C. Chỉ dùng được cho nghiên cứu.
- D. Không có giấy phép.

**4.** Ký hiệu `@@` ở cuối một mảnh BPE của PhoBERT (ví dụ `shi@@`) nghĩa là?

- A. Từ đã kết thúc.
- B. Còn mảnh tiếp theo của cùng một từ.
- C. Từ lạ bị bỏ.
- D. Token đặc biệt.

**5.** Trong thí nghiệm "đá" (đá bóng / hòn đá / nước đá), điều gì đúng?

- A. Ở lớp embedding tĩnh các nghĩa tách nhau; ở lớp cuối thì giống nhau.
- B. Ở lớp cuối vector của "đá" phụ thuộc câu: hai lần dùng cùng nghĩa có cosine cao hơn các nghĩa khác nhau; ở lớp embedding tĩnh thì gần như không phân biệt.
- C. Không có khác biệt.
- D. PhoBERT không xử lý được từ này.

**6.** Vì sao tokenizer cấp byte (Qwen) tốn nhiều token hơn cho tiếng Việt so với tokenizer huấn luyện chủ yếu trên tiếng Việt?

- A. Vì tiếng Việt dài hơn.
- B. Một phần vì chữ có dấu gồm nhiều byte UTF-8 phải được học gộp, và từ điển chia cho nhiều ngôn ngữ.
- C. Vì Qwen không biết tiếng Việt.
- D. Vì lỗi tokenizer.

<details><summary><b>Đáp án Bài 9</b></summary>

1. **B.** Mục 2.1.
2. **B.** Mục 2.1 (đọc `model.config.max_position_embeddings` = 258).
3. **B.** Mục 1 (bảng tra từ Hub).
4. **B.** Mục 2.1.
5. **B.** Mục 6 (cosine TB cùng nghĩa ≈ 0,75, khác nghĩa ≈ 0,56; lớp 0 ≈ 0,97 cho cả hai).
6. **B.** Mục 4 (token/âm tiết: PhoBERT ≈ 1,0; Qwen ≈ 1,4).
</details>

---

## Bài 10 · Tinh chỉnh PhoBERT

**1.** Vì sao tinh chỉnh dùng learning rate nhỏ (1e-5…5e-5) kèm warmup?

- A. Vì dữ liệu ít.
- B. Ta chỉ nhích trọng số đã tốt; warmup tránh cập nhật lớn làm hỏng trọng số khi đầu phân loại còn ngẫu nhiên.
- C. Vì GPU yếu.
- D. Vì fp16.

**2.** Chọn checkpoint tốt nhất theo tập nào?

- A. Train.  B. Valid.  C. Test.  D. Bất kỳ.

**3.** UIT-VSFC có lớp *trung tính* chỉ ≈4–5%. Hệ quả cho đánh giá?

- A. Accuracy ≈0,94 che giấu việc lớp hiếm bị bỏ sót (recall ≈0,5); cần macro-F1 và báo cáo từng lớp.
- B. Không cần quan tâm lớp này.
- C. Phải xóa lớp này.
- D. Accuracy là độ đo tốt nhất.

**4.** Khoảng tin cậy bootstrap của hiệu macro-F1 (PhoBERT − TF-IDF) ≈ [0,09; 0,15] **không** đo điều gì?

- A. Độ bất định do kích thước tập test.
- B. Biến thiên do seed huấn luyện.
- C. Có chắc PhoBERT hơn trên *tập test này*.
- D. Tỉ lệ lần bootstrap PhoBERT hơn.

**5.** Mô hình tinh chỉnh trên phản hồi giáo dục, thử trên 40 câu đánh giá sản phẩm: accuracy ≈0,63 (so với ≈0,94 trong miền). Bài học?

- A. Mô hình tồi.
- B. Điểm trong miền không dự đoán được chất lượng ngoài miền; cần dữ liệu kiểm tra từ chính miền triển khai.
- C. Cần thêm epoch.
- D. PhoBERT không hỗ trợ sản phẩm.

<details><summary><b>Đáp án Bài 10</b></summary>

1. **B.** Mục 5 (bảng).
2. **B.** Test chỉ mở một lần.
3. **A.** Mục 6.
4. **B.** Mục 7: bootstrap chỉ đo bất định do *tập test*; muốn đo biến thiên seed phải huấn luyện lại nhiều seed.
5. **B.** Mục 9.
</details>

---

## Bài 11 · Gán nhãn chuỗi (NER)

**1.** Mô hình luôn đoán `O` có accuracy theo token rất cao (≈79% trên dữ liệu PhoNER) nhưng F1 mức thực thể = 0. Vì sao dùng độ đo mức thực thể?

- A. Vì token-level quá chậm.
- B. Vì phần lớn token là `O`; chỉ có độ đo mức thực thể (khớp chính xác ranh giới + loại) phản ánh việc tìm đúng thực thể.
- C. Vì F1 luôn lớn hơn accuracy.
- D. Vì NER không có nhãn.

**2.** Khi căn chỉnh nhãn từ → subword với PhoBERT, quy ước đúng là?

- A. Gán nhãn từ cho mọi mảnh.
- B. Mảnh đầu của mỗi từ mang nhãn của từ; các mảnh còn lại và token đặc biệt nhận −100 (bị loss bỏ qua).
- C. Chỉ mảnh cuối mang nhãn.
- D. Bỏ hết nhãn `O`.

**3.** Chuỗi nhãn `O I-LOC` là sai BIO. Cách đảm bảo đầu ra luôn hợp lệ mà không cần huấn luyện thêm?

- A. Tăng epoch.
- B. Giải mã Viterbi với các chuyển tiếp bị cấm (`I-X` chỉ sau `B-X`/`I-X`).
- C. Xóa nhãn `I-`.
- D. Dùng softmax.

**4.** Khi chạy mô hình NER trên `ner_mini` ("Lê Hoàng Nam"), F1 của `PER` rất thấp vì?

- A. Mô hình không biết tên người nào.
- B. Dữ liệu huấn luyện hầu hết có `NAME` là *một từ* (bộ tách từ gốc ghép cả họ tên), còn bộ tách từ của ta không ghép nên mô hình báo hai thực thể liền nhau.
- C. Do GPU.
- D. Do dùng fp16.

**5.** Dạng lỗi nhiều nhất của PhoBERT trên tập test PhoNER là?

- A. Sai loại.
- B. Sai ranh giới (≈2,3% thực thể), tiếp theo thừa và bỏ sót; sai loại hiếm nhất.
- C. Bỏ sót.
- D. Không có lỗi.

<details><summary><b>Đáp án Bài 11</b></summary>

1. **B.** Mục 2.
2. **B.** Mục 4.
3. **B.** Mục 7.
4. **B.** Mục 9.
5. **B.** Mục 8.
</details>

---

## Bài 12 · Embedding câu và tìm kiếm

**1.** Một hệ thống xếp hạng [0, 2, 1, 4, 3], tài liệu đúng là {2, 4}. MRR bằng?

- A. 1  B. 1/2  C. 1/4  D. 0

**2.** BM25 khác TF-IDF ở hai điểm chính nào?

- A. Dùng nhãn và dùng GPU.
- B. Bão hòa theo tần suất từ (tf tăng nhưng tăng chậm dần) và chuẩn hóa theo độ dài tài liệu.
- C. Chỉ dùng bigram.
- D. Dùng embedding.

**3.** Vì sao RRF (Reciprocal Rank Fusion) thuận tiện để kết hợp BM25 và dense?

- A. Chỉ dùng *hạng*, nên không phải chuẩn hóa hai thang điểm khác nhau (điểm BM25 và cosine).
- B. Luôn cho kết quả tốt nhất.
- C. Cần huấn luyện.
- D. Nhanh gấp 10 lần.

**4.** Với `multilingual-e5-small`, bạn **phải**?

- A. Bỏ dấu câu.
- B. Thêm tiền tố `query: ` / `passage: `, gộp trung bình có mặt nạ và chuẩn hóa L2 theo thẻ mô hình.
- C. Tách từ bằng RDRSegmenter.
- D. Dùng GPU.

**5.** Khi người dùng gõ truy vấn không dấu, điều gì xảy ra trong thí nghiệm của khóa?

- A. Cả BM25 và dense không bị ảnh hưởng.
- B. BM25 gần như hỏng nếu hai phía không cùng chuẩn hóa; dense cũng sụt mạnh (Hit@1 ≈0,88 → ≈0,24).
- C. Chỉ BM25 bị ảnh hưởng.
- D. Dense cải thiện.

**6.** Vì sao phải chia tài liệu dài thành các đoạn (chunk) có chồng lấn?

- A. Một vector cho đoạn quá dài "pha loãng" ý; chồng lấn tránh mất ngữ cảnh ở biên.
- B. Vì máy không đọc được tài liệu dài.
- C. Để tăng số tài liệu.
- D. Không cần thiết.

<details><summary><b>Đáp án Bài 12</b></summary>

1. **B.** Tài liệu đúng đầu tiên (2) ở hạng 2 ⇒ 1/2. (Mục 1.)
2. **B.** Mục 2.
3. **A.** Mục 4.
4. **B.** Mục 3; trong tập nhỏ của khóa bỏ tiền tố chưa đổi xếp hạng, nhưng cứ làm đúng thẻ mô hình.
5. **B.** Mục 6.2.
6. **A.** Mục 7.
</details>

---

## Bài 13 · LLM và RAG

**1.** Với RAG và trích xuất cần câu trả lời ổn định, nên dùng cách giải mã nào?

- A. Temperature cao.
- B. Greedy hoặc temperature rất thấp.
- C. Top-k = 1000.
- D. Ngẫu nhiên hoàn toàn.

**2.** Chat template là gì?

- A. Một mô hình riêng.
- B. Quy tắc biến danh sách lượt hội thoại thành một chuỗi token (kèm token đặc biệt như `<|im_start|>`); mỗi họ mô hình có mẫu riêng, nên dùng `apply_chat_template`.
- C. Một loại prompt injection.
- D. Một bộ dữ liệu.

**3.** Hệ thống *không RAG* trả lời đúng ≈33% câu về chính sách cửa hàng hư cấu. Cách hiểu đúng?

- A. Mô hình đã biết chính sách đó.
- B. Các câu đúng là con số "điển hình" (7 ngày, 12 tháng...) đoán trúng do tình cờ; chấm bằng từ khóa thổi phồng điểm — nên cần trích dẫn nguồn để kiểm chứng.
- C. Phép chấm hoàn toàn chính xác.
- D. Không RAG tốt hơn RAG.

**4.** Trong thí nghiệm prompt injection, mô hình bị lừa nhiều nhất ở kịch bản nào?

- A. Có đủ tài liệu sạch trong ngữ cảnh.
- B. Tài liệu bị nhiễm là *nguồn duy nhất* trong ngữ cảnh — kể cả khi dùng prompt "an toàn" có thẻ phân tách.
- C. Không có tài liệu nào.
- D. Cả hai như nhau.

**5.** Một câu trả lời RAG sai, nhưng đoạn đúng **có** trong top-3. Lỗi nằm ở đâu?

- A. Khâu truy hồi.
- B. Khâu sinh (prompt, mô hình, nhiễu ngữ cảnh) — phải tách lỗi truy hồi và lỗi sinh vì cách chữa khác nhau.
- C. Dữ liệu huấn luyện của BM25.
- D. Không thể biết.

**6.** Ngưỡng cosine top-1 tách tốt câu *lạc đề xa* nhưng kém với câu *đúng chủ đề mà không có thông tin* (AUROC ≈0,72). Hệ quả?

- A. Chỉ cần ngưỡng cosine là đủ chống bịa.
- B. Loại câu sau (dễ gây bịa nhất) cần được chặn bằng chính LLM (dặn từ chối), kiểm tra riêng hoặc bộ phân loại chuyên dụng.
- C. Bỏ qua.
- D. Tăng k.

<details><summary><b>Đáp án Bài 13</b></summary>

1. **B.** Mục 1.2.
2. **B.** Mục 1.1.
3. **B.** Mục 4.
4. **B.** Mục 7 (≈3/4 bị lừa với prompt thường, 4/4 với prompt "an toàn" ở kịch bản B; 0/4 ở kịch bản A).
5. **B.** Mục 4.1.
6. **B.** Mục 5.
</details>

---

## Bài 14 · Triển khai, đạo đức, đồ án

**1.** Trong CheckList, ba loại kiểm thử là?

- A. Unit, integration, system.
- B. MFT (chức năng tối thiểu), INV (bất biến), DIR (kỳ vọng theo hướng).
- C. Train, valid, test.
- D. Precision, recall, F1.

**2.** Sau khi *che tên vùng miền* (thay "Miền Trung/Bắc/Nam" bằng `VUNG`) trên mô hình bị gieo tương quan giả, ba vùng bị đối xử y hệt nhau nhưng mô hình vẫn lệch. Vì sao?

- A. Che không có tác dụng gì.
- B. Tương quan giả thật ra là "*có nhắc tới vùng miền* ⇒ hay là tiêu cực"; che danh tính loại bỏ chênh lệch *giữa các vùng* nhưng không xóa lối tắt. Cần chẩn đoán nguyên nhân (ví dụ xóa cả câu nhắc vùng).
- C. Do overfitting.
- D. Do lỗi code.

**3.** PSI (Population Stability Index) dùng để làm gì trong giám sát?

- A. Đo độ chính xác.
- B. So sánh phân phối của một chỉ báo (độ tin cậy, độ dài...) giữa dữ liệu tham chiếu và dữ liệu mới để phát hiện lệch phân phối mà không cần nhãn.
- C. Chọn siêu tham số.
- D. Che PII.

**4.** Với bộ che PII bằng quy tắc, điều nào đúng?

- A. Precision 100% là đủ.
- B. Recall quan trọng (bỏ sót = rò rỉ), nhưng quy tắc luôn bỏ sót thứ chưa lường (tên, địa chỉ, tài khoản có định dạng riêng); log không được chứa dữ liệu thô.
- C. Regex che được mọi PII.
- D. Không cần đo.

**5.** Vì sao cẩn thận khi nạp tệp `joblib`/`pickle` từ nguồn lạ?

- A. Vì file lớn.
- B. Vì pickle có thể thực thi mã tùy ý khi nạp; ưu tiên định dạng an toàn như `safetensors` cho mô hình Transformer.
- C. Vì mất dấu tiếng Việt.
- D. Vì chậm.

<details><summary><b>Đáp án Bài 14</b></summary>

1. **B.** Mục 4.
2. **B.** Mục 5.2 (cả ba vùng Δ ≈ −0,41; sau khi xóa cả câu Δ = 0 và accuracy về ≈0,89).
3. **B.** Mục 7.
4. **B.** Mục 6.
5. **B.** Mục 2 (cảnh báo).
</details>

---

## Bài 15 · LoRA và tối ưu suy luận

**1.** Tinh chỉnh toàn bộ một mô hình bằng AdamW (trọng số fp32 + autocast) cần khoảng bao nhiêu byte cho mỗi tham số (chưa tính kích hoạt trung gian)?

- A. 2  B. 4  C. ≈16 (trọng số 4 + gradient 4 + hai moment Adam 8)  D. ≈100

**2.** Trong LoRA, vì sao khởi tạo $B=0$ (và $A$ ngẫu nhiên nhỏ)?

- A. Để mô hình không học được.
- B. Để $\Delta W=\frac{\alpha}{r}BA=0$ lúc bắt đầu: mô hình y hệt mô hình gốc, huấn luyện đi dần từ đó.
- C. Để tiết kiệm bộ nhớ.
- D. Vì $A$ và $B$ phải bằng nhau.

**3.** Ma trận trọng số 896×896 có 802.816 tham số. LoRA hạng $r=16$ thêm bao nhiêu tham số huấn luyện?

- A. 16 × 896 = 14.336
- B. 16 × (896 + 896) = 28.672 (≈ 3,6%)
- C. 896 × 896 = 802.816
- D. 16 × 16 = 256

**4.** Lợi ích của việc *hợp nhất* adapter vào trọng số gốc sau huấn luyện?

- A. Suy luận không tốn thêm phép tính cho nhánh LoRA, và chỉ còn một bộ trọng số duy nhất.
- B. Tăng accuracy.
- C. Giảm số tham số của mô hình gốc.
- D. Cho phép huấn luyện tiếp bằng fp16.

**5.** Khi lượng tử hóa int8 một mô hình phân loại, vì sao cần đo chất lượng **theo từng lớp** chứ không chỉ accuracy?

- A. Vì int8 chỉ ảnh hưởng một lớp.
- B. Vì accuracy tổng thể bị lớp phổ biến chi phối; lớp hiếm có thể bị sụt mạnh mà accuracy gần như không đổi (macro-F1 mới lộ ra).
- C. Vì độ đo theo lớp nhanh hơn.
- D. Không cần.

**6.** Bạn chưa có dữ liệu nhãn, tác vụ thay đổi hằng tuần, và dữ liệu không nhạy cảm. Lựa chọn thực dụng nhất theo bản đồ quyết định của Bài 15?

- A. Tinh chỉnh PhoBERT cho từng tác vụ.
- B. Dùng prompt với một LLM (qua API hoặc cục bộ), đo trên một tập kiểm tra nhỏ rồi quyết định.
- C. Huấn luyện từ đầu một Transformer.
- D. Dùng TF-IDF mà không đánh giá.

**7.** Huấn luyện LoRA trên GPU 4 GB (Windows): với batch 16 mỗi bước lâu gấp ≈ 5 lần so với batch 8 (dù chỉ gấp đôi số mẫu), nhưng chương trình không báo lỗi hết bộ nhớ. Nguyên nhân khả dĩ nhất và cách xử lý?

- A. LoRA luôn chậm theo cấp số nhân khi tăng batch; không cần làm gì.
- B. Dữ liệu bị nhiễu nên cần làm sạch lại.
- C. VRAM đỉnh vượt VRAM vật lý nên trình điều khiển dùng RAM hệ thống; so `torch.cuda.max_memory_allocated()` với VRAM của card, rồi bật gradient checkpointing hoặc giảm batch.
- D. Hạng $r$ của adapter quá nhỏ nên phải tăng $r$.

<details><summary><b>Đáp án Bài 15</b></summary>

1. **C.** Mục 1; công thức khớp số đo của PhoBERT ở Bài 10 (≈2,2 GB tính toán so với đỉnh thực 3,1 GB gồm kích hoạt).
2. **B.** Mục 2 (đã kiểm tra bằng `torch.allclose`).
3. **B.** Mục 2: $r(d_{in}+d_{out})$.
4. **A.** Mục 3.5.
5. **B.** Mục 4: accuracy giảm vài điểm nhưng macro-F1 của lớp hiếm có thể tụt nhiều.
6. **B.** Mục 5; lưu ý chi phí theo token và quyền riêng tư nếu dùng API.
7. **C.** Mục 3.0: batch 16 không bật checkpointing đạt đỉnh 4,33 GB trên card 4,29 GB và chạy ≈ 1,8 giây/bước so với ≈ 0,34 giây/bước ở batch 8; bật checkpointing đưa đỉnh về ≈ 1,4 GB. Trên Windows, tràn VRAM thường chỉ làm chậm chứ không báo lỗi.
</details>

---

## Bài 16 · Dữ liệu nhãn và học ít nhãn

**1.** Hai người gán nhãn có đồng thuận thô 0,93 (nhị phân: "là trung tính" / "không") trên một lớp chiếm 4% dữ liệu, nhưng κ riêng lớp chỉ ≈ 0,27. Vì sao?

- A. κ luôn nhỏ hơn đồng thuận thô ba lần.
- B. Dữ liệu bị rò rỉ giữa hai người gán.
- C. Cả hai gần như luôn chọn "không phải lớp hiếm", nên khớp ngẫu nhiên kỳ vọng đã ≈ 0,90; phần vượt trên mức đó rất nhỏ.
- D. κ chỉ tính cho lớp phổ biến.

**2.** Cùng 20% nhãn sai nhưng nằm ở **tập test** (mô hình huấn luyện trên nhãn sạch). Điều gì đúng?

- A. Mô hình tệ đi vì học từ nhãn sai.
- B. Mô hình không đổi nhưng điểm đo được thấp hơn thực tế: thước đo bị hỏng.
- C. Điểm tăng vì tập test lớn hơn.
- D. Không ảnh hưởng gì.

**3.** Khi gắn cờ nhãn nghi sai bằng xác suất dự đoán, vì sao dùng **dự đoán chéo** (cross-validation) thay vì mô hình huấn luyện trên toàn bộ?

- A. Để chạy nhanh hơn.
- B. Vì kiểm tra chéo luôn cho precision bằng 1.
- C. Không cần; hai cách như nhau.
- D. Vì mô hình có thể đã ghi nhớ nhãn của chính mẫu đó (kể cả nhãn sai) nên xác suất của nó không phản ánh việc nhãn đáng ngờ.

**4.** Nhãn yếu (độ chính xác ≈ 0,90 ở phần được phủ) huấn luyện mô hình đạt macro-F1 0,585 nhưng F1 lớp "trung tính" chỉ ≈ 0,11. Giải thích hợp lý nhất?

- A. Các luật gần như không bao giờ gán lớp hiếm (luật "trung tính" chỉ chính xác ≈ 0,24 và có ít mẫu dev để ước lượng) nên mô hình không có dữ liệu để học lớp đó; độ chính xác tổng thể của nhãn yếu che điều này.
- B. Có quá nhiều hàm gán nhãn.
- C. Nhãn yếu luôn không dùng được.
- D. Cần PhoBERT mới học được nhãn yếu.

**5.** Học tích cực (độ tự tin thấp nhất) cần ≈ 600 nhãn để đạt điểm mà chọn ngẫu nhiên cần ≈ 950 nhãn. Một lý do chính?

- A. Nó chọn các câu dài nhất.
- B. Nó chọn nhiều mẫu **lớp hiếm** hơn hẳn (≈ 15% so với 4%), mà macro-F1 coi mọi lớp ngang nhau.
- C. Nó dùng mô hình lớn hơn.
- D. Nó lặp lại cùng các mẫu.

**6.** Khi tăng cường dữ liệu cảm xúc bằng cách **xóa từ ngẫu nhiên**, rủi ro cần kiểm tra là gì?

- A. Từ điển tăng kích thước.
- B. Mô hình chạy chậm đi.
- C. Biến đổi có thể làm đổi nghĩa (xóa "không") khiến nhãn cũ không còn đúng.
- D. Không có rủi ro vì chỉ xóa chữ.

<details><summary><b>Đáp án Bài 16</b></summary>

1. **C.** Mục 2.1: với lớp hiếm, $p_e=0{,}05^2+0{,}95^2\approx 0{,}90$ nên 0,926 chỉ hơn mức ngẫu nhiên chút ít; κ riêng lớp ≈ 0,27 dù κ tổng thể 0,83. Báo cáo κ theo lớp.
2. **B.** Mục 2.2: nhiễu 20% ở test cho 0,585 trong khi mô hình sạch không đổi (nhiễu 20% ở train cho 0,617). Không thể đo mô hình tốt hơn chất lượng nhãn của tập đánh giá cho phép.
3. **D.** Mục 2.3: dự đoán chéo cho mỗi mẫu một xác suất từ mô hình *chưa thấy* nó. Với 20% nhiễu tiêm vào: precision 0,51, recall 0,72; loại mẫu bị gắn cờ nâng macro-F1 từ 0,613 lên 0,685.
4. **A.** Mục 3: 0 nhãn thật vẫn ngang 200 nhãn thật (0,585 so với 0,563) nhưng F1 "trung tính" chỉ 0,11 (so với 0,38 khi có toàn bộ nhãn thật).
5. **B.** Mục 4: 15% "trung tính" trong 1.000 nhãn được chọn so với 4% khi ngẫu nhiên; ở ≤ 200 nhãn học tích cực chưa hơn ngẫu nhiên (khởi động nguội).
6. **C.** Mục 5: xóa ngẫu nhiên đổi dự đoán ở 6,0% câu có từ phủ định, giảm còn 2,7% khi giữ lại từ phủ định; lợi ích huấn luyện chỉ ≈ 0,00–0,01.
</details>

---

## Bài 17 · Khôi phục dấu tiếng Việt

**1.** Vì sao khôi phục dấu **không** giải được bằng quy tắc "chữ không dấu → một chữ có dấu"?

- A. Vì tiếng Việt có quá ít chữ.
- B. Vì nhiều âm tiết có dấu khác nhau cùng thành một dạng không dấu (≈ 86% token mơ hồ), nên phải dựa vào ngữ cảnh.
- C. Vì Unicode không biểu diễn được dấu.
- D. Vì máy tính không bỏ dấu được.

**2.** Trong mô hình kênh nhiễu $\hat y=\arg\max_y P(y)P(x\mid y)$ cho khôi phục dấu, thành phần $P(x\mid y)$ là gì?

- A. Xác suất người dùng gõ sai.
- B. Bằng 1 nếu bỏ dấu của $y$ đúng bằng $x$, ngược lại bằng 0; nên chỉ còn việc chọn chuỗi ứng viên có xác suất ngôn ngữ $P(y)$ lớn nhất.
- C. Luôn bằng 0,5.
- D. Xác suất của từ hiếm.

**3.** Mô hình n-gram huấn luyện trên phản hồi sinh viên đạt 97,8% token trong miền nhưng chỉ ≈ 77% trên văn bản FAQ cửa hàng. Kết luận đúng?

- A. Điểm trong miền không dự báo điểm ngoài miền; luôn nói rõ con số đo *trên dữ liệu nào*.
- B. Mô hình bị lỗi cài đặt.
- C. Cần tăng bậc n-gram lên 5.
- D. Cần từ điển lớn hơn.

**4.** Phân tích lỗi trên FAQ: 137/139 lỗi là *dạng đúng có trong danh sách ứng viên nhưng mô hình chọn dạng khác*; chỉ 2 lỗi thiếu ứng viên. Cách cải thiện hợp lý nhất?

- A. Mở rộng từ điển ứng viên.
- B. Thêm văn bản có dấu cùng miền (không cần nhãn) để mô hình ngôn ngữ biết ngữ cảnh của miền đó.
- C. Bỏ mô hình ngôn ngữ, chỉ dùng từ điển.
- D. Giảm bậc n-gram xuống 1.

**5.** Với truy vấn không dấu: BM25 "bỏ dấu cả hai phía" (Hit@1 0,848) thắng khôi phục dấu (0,576); còn với e5, khôi phục dấu (0,667) thắng bỏ dấu cả hai phía (0,394). Bài học?

- A. Khôi phục dấu luôn tốt hơn.
- B. Bỏ dấu cả hai phía luôn tốt hơn.
- C. Chọn cách sửa theo hệ thống phía sau: khớp chuỗi chỉ cần hai phía nhất quán; mô hình dense cần chữ có dấu đúng.
- D. Hai cách như nhau.

**6.** Tính chất nào của kênh nhiễu cho phép **kiểm tra tự động** đầu ra của một LLM khi nhờ nó thêm dấu?

- A. Đầu ra phải ngắn hơn đầu vào.
- B. Đầu ra phải có nhiều chữ Hán.
- C. Đầu ra phải bằng đầu vào sau khi bỏ dấu (LLM đã vi phạm điều này ở 23/24 tài liệu).
- D. Đầu ra phải có đúng 20 từ.

<details><summary><b>Đáp án Bài 17</b></summary>

1. **B.** Mục 1.1: 1.445 dạng không dấu trong 144 nghìn token; "doi" có 13 dạng (*đổi, đối, đôi*...), "de" có 12.
2. **B.** Mục 2: phép bỏ dấu là tất định nên $P(x\mid y)\in\{0,1\}$; giải mã bằng Viterbi trên lưới ứng viên.
3. **A.** Mục 5: ma trận trong/ngoài miền; tất cả các kho gộp cũng chỉ đạt 0,85 trên FAQ và 10% câu đúng hoàn toàn.
4. **B.** Mục 6: từ điển bổ sung từ PhoBERT cứu 9/11 token thiếu ứng viên nhưng độ chính xác không đổi (0,853); nút thắt là ngữ cảnh/miền.
5. **C.** Mục 7: chọn theo hệ thống phía sau.
6. **C.** Mục 8: tính chất kênh nhiễu cho kiểm tra tự động; LLM giữ nguyên chữ chỉ ở 1/24 tài liệu.
</details>

---

## Bài 18 · Phân cụm và mô hình chủ đề

**1.** Trên UIT-VSFC, k-means (embedding e5, k = 2) có NMI với **cảm xúc** 0,47 nhưng NMI với **chủ đề** chỉ 0,13. Giải thích?

- A. Chủ đề là nhãn khó gán hơn cảm xúc.
- B. k-means đã tìm đúng trục khác biệt lớn nhất trong dữ liệu (khen/chê); nó không biết bạn muốn trục nào.
- C. e5 không hiểu tiếng Việt.
- D. k = 2 quá nhỏ cho chủ đề.

**2.** Silhouette trên UIT-VSFC chỉ 0,03–0,09 và với TF-IDF còn *tăng* theo k. Kết luận về việc chọn k?

- A. Chọn k có silhouette cao nhất.
- B. Silhouette thấp cho thấy cấu trúc cụm yếu; không nên dùng nó một mình để chọn k.
- C. Silhouette âm nghĩa là cụm tốt.
- D. k luôn bằng số nhãn.

**3.** Độ ổn định (ARI giữa hai seed) của e5 là 1,00 ở k = 2 nhưng ≈ 0,4–0,5 ở k ≥ 6. Ý nghĩa?

- A. Cách chia mịn phụ thuộc điểm khởi tạo; và cách chia ổn định nhất lại là phép chia khen/chê — ổn định không có nghĩa là có ý nghĩa với mục tiêu của bạn.
- B. k-means bị lỗi ở k lớn.
- C. ARI chỉ đúng khi k = 2.
- D. Cần tăng số vòng lặp.

**4.** c-TF-IDF dùng để làm gì?

- A. Giảm chiều embedding.
- B. Đánh giá silhouette.
- C. Sinh câu mới cho mỗi cụm.
- D. Chấm các từ *đặc trưng* của từng cụm (nhiều ở cụm đó, ít ở nơi khác) để đặt tên cụm.

**5.** LDA có độ nhất quán NPMI cao hơn NMF (0,078 so với 0,039 ở K = 4). Điều này có nghĩa?

- A. Các chủ đề của LDA khớp mục tiêu của bạn hơn.
- B. Các từ hàng đầu của chủ đề LDA hay xuất hiện *cùng nhau* hơn; nhưng điều đó không bảo đảm chủ đề khớp với trục bạn muốn khám phá.
- C. LDA nhanh hơn NMF.
- D. NMF sai.

**6.** Sau khi chiếu bỏ hướng cảm xúc khỏi embedding, NMI cảm xúc của cụm rơi (0,31 → 0,01) nhưng NMI chủ đề **không tăng**. Rút ra điều gì?

- A. Phép chiếu bị lỗi.
- B. Mô hình học sâu hơn là cần thiết.
- C. Gỡ được trục không mong muốn không tự động làm lộ trục mong muốn; có thể nhãn chủ đề không tương ứng cấu trúc ngữ nghĩa của embedding.
- D. Chủ đề luôn không có thật.

<details><summary><b>Đáp án Bài 18</b></summary>

1. **B.** Mục 5: NMI cảm xúc 0,47 (k = 2) và 0,31 (k = 4), NMI chủ đề 0,09–0,13 ở mọi k.
2. **B.** Mục 5: silhouette cao nhất ở k = 2 với e5 (phép chia khen/chê); với TF-IDF tăng từ 0,034 lên 0,053 theo k nên không chỉ ra k nào.
3. **A.** Mục 5: ARI 0,99–1,00 ở k = 2–4 rồi 0,42–0,54 từ k ≥ 6.
4. **D.** Mục 6: $W_{t,c}=\mathrm{tf}_{t,c}\cdot\log(1+A/f_t)$; các cụm ở k = 8 hóa ra mô tả *kiểu phản hồi* (khen / chê khó hiểu / góp ý).
5. **B.** Mục 7: NPMI đo sự đi cùng nhau của từ, không đo mức khớp mục tiêu.
6. **C.** Mục 5.2: đối chứng bỏ 3 hướng ngẫu nhiên không đổi gì; NMI chủ đề 0,094 → 0,106 → 0,075 (k = 4).
</details>

---

## Bài 19 · Sinh văn bản có điều kiện: tóm tắt, dịch và cách đo

**1.** Cùng một cặp câu, ROUGE-1 F1 là 0,57 / 0,50 / 0,35 tùy cách tách token (ASCII / âm tiết / từ ghép). Bài học?

- A. ROUGE bị lỗi.
- B. Chỉ nên dùng tokenizer ASCII.
- C. Điểm không phụ thuộc cách tách token.
- D. Cách tách token là một quyết định phải ghi lại; tokenizer mặc định chỉ giữ `a–z`, `0–9` còn phá hỏng tiếng Việt.

**2.** BLEU không làm mịn của "the cat is on the mat" so với tham chiếu "the cat sat on the mat" là bao nhiêu và vì sao?

- A. 0, vì câu không có 4-gram nào trùng; làm mịn (≈ 38) và dùng mức corpus giúp tránh hiện tượng này.
- B. 100, vì chỉ khác một chữ.
- C. 83, vì 5/6 chữ trùng.
- D. Không tính được.

**3.** Chép **toàn văn** làm "tóm tắt" đạt ROUGE-1 F1 0,351, cao hơn điểm hai người viết tóm tắt chấm nhau (0,263). Giải thích?

- A. Người viết tóm tắt kém.
- B. ROUGE tính sai.
- C. ROUGE thưởng sự trùng chữ/recall; tóm tắt của người *diễn đạt lại* nên ít trùng chữ. Vì vậy luôn kèm precision, độ dài và các đường cơ sở.
- D. Toàn văn là tóm tắt tốt nhất.

**4.** Bootstrap theo cặp cho hiệu BLEU (Marian − Qwen) = −12,5, khoảng 95% từ −24,5 đến +0,4 trên 24 câu. Nên kết luận thế nào?

- A. Hai hệ thống bằng nhau.
- B. Marian chắc chắn tốt hơn.
- C. Qwen tốt hơn một cách chắc chắn.
- D. Nghiêng về Qwen nhưng khoảng tin cậy chạm 0; 24 câu chưa đủ để kết luận chắc chắn.

**5.** Cả bốn độ đo đếm chữ chấm bản **đổi nghĩa bằng một chữ** ("không", "tăng", đổi con số) cao hơn bản diễn đạt đúng ở 8/8 bộ ba. Vì sao?

- A. Sửa một chữ giữ lại gần như mọi n-gram, còn diễn đạt lại phá vỡ chúng; độ đo mù với đảo phủ định và đổi con số.
- B. Do dữ liệu quá nhỏ.
- C. Do ROUGE chỉ chấm câu dài.
- D. Do bản diễn đạt lại bị sai.

**6.** Kiểm tra tự động "con số/tên riêng của tóm tắt có trong nguồn" gắn cờ 2 mục (cả hai là dương tính giả) và bỏ sót ít nhất 5 bản tóm tắt sai ý của LLM. Rút ra điều gì?

- A. Kiểm tra này đủ để bảo đảm tính trung thực.
- B. Nó chỉ bắt được thông tin *vắng mặt*, không bắt được thông tin *bị bóp méo* (đảo "giảm" thành "tăng", "hơn" thành "gần"); cần đọc mẫu hoặc mô hình suy diễn văn bản.
- C. LLM không bao giờ sai.
- D. Nên bỏ mọi kiểm tra tự động.

<details><summary><b>Đáp án Bài 19</b></summary>

1. **D.** Mục 2.1: tokenizer ASCII cũng cho hai câu khác nghĩa ("Tôi thích phở" / "Tôi ghét bún") ROUGE-1 0,364 vì các mảnh vụn trùng nhau.
2. **A.** Mục 2: BLEU không làm mịn bằng 0; làm mịn `exp` ≈ 38 (giá trị đối chiếu với sacreBLEU trong `tests/test_metrics_gen.py`).
3. **C.** Mục 4: chép toàn văn recall 0,87; câu đầu (0,401) là đường cơ sở rất mạnh; đồng thuận người 0,263.
4. **D.** Mục 6: Marian cao hơn chỉ trong 3% lần lấy mẫu; hai khoảng tin cậy riêng lẻ chồng nhau nên phải so theo cặp.
5. **A.** Mục 7: ROUGE-L 0,80–0,95 cho bản sai nghĩa so với 0,22–0,43 cho bản diễn đạt đúng; cosine e5 chỉ đúng 2/8.
6. **B.** Mục 5: tt11 đổi "giảm nhẹ" thành "tăng nhẹ", tt16 đổi "hơn 300" thành "gần 300"... (đọc của tác giả).
</details>
