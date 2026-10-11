# Giấy phép cho nội dung giáo trình và dữ liệu tự biên soạn

Repo này dùng **hai giấy phép** tùy loại nội dung:

| Phần | Giấy phép | Gồm |
|---|---|---|
| **Mã nguồn** | [MIT](LICENSE) | `nlpvi/`, `app/`, `tools/`, `tests/`, các ô *mã* trong notebook, tệp `requirements*.txt`, workflow CI |
| **Nội dung giáo trình và dữ liệu tự biên soạn** | **CC BY 4.0** (bên dưới) | `README.md`, `docs/`, các ô *văn bản* (markdown) và lời nhận xét trong notebook (kể cả `notebooks/dap_an/`), `tools/notebook_src/*.nbsrc` (phần văn bản), và các tệp dữ liệu do tác giả biên soạn trong `data/`: `reviews_vi.csv` (tổng hợp), `reviews_hard.csv`, `ner_mini.txt`, `faq_docs.json`, `faq_queries.json`, `tom_tat_mini.json`, `dich_mini.json`, `DATA_CARD.md` |

Một ngoại lệ trong `data/`: `tu_ghep_phobert.txt` được **trích từ từ vựng của `vinai/phobert-base`** (giấy phép MIT), xem [NOTICE.md](NOTICE.md).

## Tóm tắt CC BY 4.0 (không thay thế văn bản pháp lý)

Bạn được **sao chép, phân phối, chỉnh sửa và dùng cho mục đích thương mại**, với điều kiện **ghi công** tác giả (nêu tên *ThanhDatVN*, kèm liên kết tới repo và tới giấy phép, và nêu rõ nếu bạn có thay đổi). Không có bảo đảm nào đi kèm.

> This work is licensed under the Creative Commons Attribution 4.0 International License.
> To view a copy of this license, visit <https://creativecommons.org/licenses/by/4.0/> or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

Văn bản pháp lý đầy đủ: <https://creativecommons.org/licenses/by/4.0/legalcode>.

## Điều **không** thuộc hai giấy phép trên

Dữ liệu và mô hình **tải về lúc chạy** (UIT-VSFC, PhoNER_COVID19, `PhoBERT`, `multilingual-e5-small`, `Qwen2.5`, `opus-mt-en-vi`...) **không** được phân phối trong repo này và theo giấy phép riêng của từng nơi phát hành; xem [NOTICE.md](NOTICE.md) và [data/DATA_CARD.md](data/DATA_CARD.md).
