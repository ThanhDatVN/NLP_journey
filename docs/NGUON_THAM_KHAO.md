# Nguồn tham khảo và cách giáo trình này được xây dựng

## 1. Vì sao chọn huggingface/course làm nguồn chính

Yêu cầu ban đầu: một repo **uy tín**, **chi tiết**, dạy **NLP bằng Python** từ cơ bản đến nâng cao, **bằng tiếng Việt**, có trên GitHub. Kết quả khảo sát (số liệu lấy từ GitHub API ngày **10/10/2026**):

| Ứng viên | Sao | Fork | Giấy phép | Cập nhật cuối | Ngôn ngữ | Nhận xét |
|---|---|---|---|---|---|---|
| **[huggingface/course](https://github.com/huggingface/course)** | 4.273 | 1.440 | Apache-2.0 | 06/10/2026 | **bản dịch tiếng Việt đầy đủ** (`chapters/vi`) | được bảo trì tích cực, uy tín nhất; phủ Transformer → tinh chỉnh → các tác vụ NLP → demo |
| [fastai/course-nlp](https://github.com/fastai/course-nlp) | 3.491 | 1.452 | không ghi | 22/03/2023 | tiếng Anh | phủ cả phần cổ điển (TF-IDF, NMF, n-gram, RNN) nhưng đã **ngừng cập nhật**, không có giấy phép, không có tiếng Việt |
| [undertheseanlp/underthesea](https://github.com/undertheseanlp/underthesea) | 1.806 | 307 | Apache-2.0 | 08/10/2026 | tiếng Việt | **thư viện** NLP tiếng Việt kèm tài liệu, không phải giáo trình có cấu trúc |
| [vndee/awsome-vietnamese-nlp](https://github.com/vndee/awsome-vietnamese-nlp) | — | — | — | — | tiếng Việt | danh mục tài nguyên (không phải khóa học) |

**Kết luận:** [huggingface/course](https://github.com/huggingface/course) là lựa chọn phù hợp nhất cho yêu cầu "uy tín + tiếng Việt + cập nhật". Nhưng nó là khóa học về **hệ sinh thái Transformer** — nó không dạy phần nền trước đó (làm sạch văn bản, TF-IDF, n-gram, embedding tĩnh, mạng nơ-ron cơ bản), không có xử lý đặc thù tiếng Việt (tách từ, dấu, PhoBERT), không có RAG/LLM theo hướng ứng dụng, và không có đạo đức/triển khai chi tiết. Không tìm thấy repo nào bằng tiếng Việt bao trọn tất cả.

Do đó giáo trình này **kết hợp**:

- phần **Transformer → tinh chỉnh → các tác vụ**: bám khung của khóa Hugging Face tiếng Việt, **viết lại** với dữ liệu và ví dụ tiếng Việt (PhoBERT, UIT-VSFC, PhoNER);
- phần **cổ điển → mạng nơ-ron**: lấy tinh thần "dùng bài toán trước, giải thích dần" của fastai/course-nlp, **viết mới** hoàn toàn bằng tiếng Việt;
- phần **đặc thù tiếng Việt, tìm kiếm, RAG, triển khai, đạo đức**: bổ sung mới.

**Về bản quyền:** giáo trình chỉ *tham chiếu và liên kết* tới các nguồn trên; mã và văn bản trong repo này do giáo trình tự biên soạn, không sao chép notebook của nguồn nào. Khóa Hugging Face dùng giấy phép Apache-2.0; nếu bạn muốn dùng lại nguyên văn nội dung của họ, hãy làm theo điều khoản đó.

## 2. Bảng ánh xạ: bài của giáo trình ↔ nguồn nên đọc song song

| Bài | Chủ đề | Chương Hugging Face (tiếng Việt) | Bổ sung |
|---|---|---|---|
| 0 | Khởi động, dữ liệu | [Chương 1: Mô hình Transformer](https://huggingface.co/docs/course/vi/chapter1/1) (giới thiệu NLP) | — |
| 1 | Tiền xử lý tiếng Việt | [Chương 6: Tokenizers](https://huggingface.co/docs/course/vi/chapter6/1) | [Underthesea](https://github.com/undertheseanlp/underthesea), [VnCoreNLP](https://github.com/vncorenlp/VnCoreNLP) |
| 2 | TF-IDF, chủ đề | — (không có trong khóa HF) | fastai/course-nlp: TF-IDF, NMF/SVD · [tài liệu scikit-learn](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) |
| 3 | Phân loại và đánh giá | [Chương 3: Tinh chỉnh](https://huggingface.co/docs/course/vi/chapter3/1) (phần đánh giá) | [CheckList (ACL 2020)](https://aclanthology.org/2020.acl-main.442/) |
| 4 | n-gram | — | Jurafsky & Martin, [SLP3](https://web.stanford.edu/~jurafsky/slp3/), chương n-gram |
| 5 | Word embedding | — | Mikolov và cộng sự (2013); [PhoW2V](https://github.com/datquocnguyen/PhoW2V) |
| 6 | Mạng nơ-ron cho văn bản | — | [PyTorch tutorials](https://pytorch.org/tutorials/) |
| 7 | RNN/LSTM/GRU | — | Olah, *Understanding LSTM Networks* · fastai: RNN, dịch máy |
| 8 | Attention, Transformer | [Chương 1, mục "Cơ chế hoạt động của Transformer"](https://huggingface.co/docs/course/vi/chapter1/4) | [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) |
| 9 | Hugging Face, tokenizer | [Chương 2: Sử dụng 🤗 Transformers](https://huggingface.co/docs/course/vi/chapter2/1) · [Chương 6](https://huggingface.co/docs/course/vi/chapter6/1) | — |
| 10 | Tinh chỉnh PhoBERT | [Chương 3: Tinh chỉnh](https://huggingface.co/docs/course/vi/chapter3/1) · [Chương 4: Chia sẻ mô hình](https://huggingface.co/docs/course/vi/chapter4/1) | [PhoBERT](https://github.com/VinAIResearch/PhoBERT) |
| 11 | NER | [Chương 7: Phân loại token](https://huggingface.co/docs/course/vi/chapter7/2) | [PhoNER_COVID19](https://github.com/VinAIResearch/PhoNER_COVID19) |
| 12 | Tìm kiếm ngữ nghĩa | [Chương 5: Tìm kiếm ngữ nghĩa với FAISS](https://huggingface.co/docs/course/vi/chapter5/6) | E5, BM25 |
| 13 | LLM, RAG | [Chương 1: Mô hình giải mã](https://huggingface.co/docs/course/vi/chapter1/6) | [OWASP Top 10 cho ứng dụng LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/) |
| 14 | Triển khai, đạo đức | [Chương 9: Xây dựng và chia sẻ demo (Gradio)](https://huggingface.co/docs/course/vi/chapter9/1) | Model Cards, Datasheets for Datasets |
| 15 | LoRA, lượng tử hóa | — (khóa Hugging Face tiếng Việt không có phần này) | [Tài liệu PEFT](https://huggingface.co/docs/peft) · bài báo LoRA (Hu và cộng sự, 2021) · QLoRA (Dettmers và cộng sự, 2023) |
| 16 | Dữ liệu nhãn, nhãn yếu, học tích cực | — | Northcutt và cộng sự (2021), *Confident Learning* · Ratner và cộng sự (2017), *Snorkel* · Settles (2009), *Active Learning Literature Survey* · Artstein & Poesio (2008) |
| 17 | Khôi phục dấu tiếng Việt | — | Kernighan, Church & Gale (1990), mô hình kênh nhiễu · Jurafsky & Martin, SLP3 (n-gram, HMM/Viterbi) |
| 18 | Phân cụm, mô hình chủ đề | — | Arthur & Vassilvitskii (2007), *k-means++* · Blei, Ng & Jordan (2003), *LDA* · Grootendorst (2022), *BERTopic* · Röder và cộng sự (2015), độ nhất quán chủ đề |
| 19 | Tóm tắt, dịch máy, độ đo | [Chương 7: Dịch máy](https://huggingface.co/docs/course/vi/chapter7/4) · [Tóm tắt](https://huggingface.co/docs/course/vi/chapter7/5) (phần dùng và đánh giá; Bài 19 *không* dạy tinh chỉnh mô hình dịch/tóm tắt) | Lin (2004), *ROUGE* · Papineni và cộng sự (2002), *BLEU* · Popović (2015), *chrF* · Post (2018), *A Call for Clarity in Reporting BLEU Scores* · [sacreBLEU](https://github.com/mjpost/sacrebleu) |

**Chủ đề giáo trình này bổ sung mà khóa Hugging Face (tiếng Việt) chưa có:** tinh chỉnh hiệu quả tham số (LoRA), lượng tử hóa suy luận, RAG và đánh giá RAG, prompt injection, kiểm thử hành vi, đo thiên kiến, giám sát, chất lượng và chi phí dữ liệu nhãn (nhãn yếu, học tích cực), khôi phục dấu tiếng Việt, phân cụm/mô hình chủ đề, và cách đo chất lượng sinh văn bản (ROUGE/BLEU/chrF, điểm mù, khoảng tin cậy).

**Các chủ đề của khóa Hugging Face mà giáo trình này chưa phủ** (nên đọc tiếp sau khi xong): *tinh chỉnh* mô hình dịch máy và tóm tắt seq2seq (Bài 19 chỉ dùng mô hình có sẵn và dạy cách đo), hỏi đáp trích xuất, huấn luyện mô hình ngôn ngữ nhân quả quy mô lớn (Chương 7), gỡ lỗi và hỏi cộng đồng (Chương 8), thư viện 🤗 Datasets nâng cao (Chương 5).

## 3. Tài nguyên tiếng Việt khác

- [Học NLP nên bắt đầu từ đâu? — wiki Underthesea](https://github.com/undertheseanlp/underthesea/wiki): tổng hợp giáo trình, sách và khóa học (phần lớn tiếng Anh) kèm tài nguyên cho tiếng Việt.
- [vndee/awsome-vietnamese-nlp](https://github.com/vndee/awsome-vietnamese-nlp): danh mục dữ liệu, mô hình và công cụ NLP tiếng Việt.
- [VnCoreNLP](https://github.com/vncorenlp/VnCoreNLP): bộ công cụ tách từ (RDRSegmenter), gán nhãn từ loại, NER, phân tích cú pháp phụ thuộc — cần Java; là bộ tách từ mà PhoBERT khuyến nghị.
- [PhoBERT](https://github.com/VinAIResearch/PhoBERT), [Bài báo PhoBERT](https://aclanthology.org/2020.findings-emnlp.92/).

## 4. Giới hạn của khảo sát

- Số sao/fork thay đổi theo thời gian; hãy tra lại trước khi trích dẫn.
- "Uy tín" ở đây dựa trên: đơn vị phát hành (Hugging Face), giấy phép rõ ràng, tần suất cập nhật, số lượng người dùng. Nó không bảo đảm chất lượng bản dịch từng đoạn; khi có chỗ khó hiểu hãy đối chiếu với bản tiếng Anh.
- Việc không tìm thấy một repo tiếng Việt bao trọn toàn bộ nội dung là kết quả của khảo sát công khai ở thời điểm trên, không phải khẳng định rằng không tồn tại.
