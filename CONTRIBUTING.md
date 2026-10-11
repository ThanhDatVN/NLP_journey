# Hướng dẫn đóng góp

Cảm ơn bạn đã quan tâm! Repo là một **giáo trình**, nên chất lượng của lời văn và độ trung thực của số liệu quan trọng ngang với mã.

## Báo lỗi và đề xuất

Mở một *issue* và nêu: bài và mục (ví dụ "Bài 17, mục 5"), điều bạn thấy, điều bạn mong đợi, phiên bản Python/thư viện và hệ điều hành. Với lỗi số liệu, hãy dán kết quả bạn nhận được. Lưu ý các con số trong bài là của **một lần chạy** (xem README), nên chênh nhẹ là bình thường; chênh *đổi kết luận* mới là lỗi.

## Nguyên tắc nội dung

1. **Lời văn phải khớp số đo.** Mọi nhận xét "Đọc kết quả" dựa trên số thật in ra trong notebook. Sửa mã/dữ liệu làm đổi kết quả thì phải chạy lại và sửa lời văn.
2. **Đừng "làm đẹp" kết luận.** Kết quả âm tính hay trái dự đoán là một phần giá trị của giáo trình (ví dụ bỏ dấu lại tăng điểm ở Bài 3). Nếu một khẳng định chưa được đo, hãy viết rõ là chưa đo.
3. **Nêu cỡ mẫu, seed và giới hạn.** Không kết luận từ một con số trên tập nhỏ.
4. **Dữ liệu và giấy phép.** Không thêm dữ liệu thật vào repo nếu chưa chắc quyền phân phối lại; ghi nguồn và giấy phép trong `data/DATA_CARD.md` và `NOTICE.md`.
5. **Tiếng Việt chuẩn Unicode NFC**, lưu tệp UTF-8.

## Cách sửa notebook

Notebook được **dựng từ nguồn văn bản** `tools/notebook_src/*.nbsrc` (mỗi dòng `@@@ md` hoặc `@@@ code` mở một ô). **Hãy sửa `.nbsrc`, không sửa trực tiếp `.ipynb`.**

```bash
python tools/build_notebooks.py 17 --sync-text     # chỉ đổi lời văn: giữ nguyên kết quả đã chạy (từ chối nếu mã đổi)
python tools/build_notebooks.py 17 --run           # đổi mã: dựng và chạy lại, lưu kết quả
python tools/build_notebooks.py 17 --dap-an --run  # đáp án mã của bài (tools/notebook_src/dap_an/)
```

Kiểm tra lỗi phổ biến: ô lỗi, ô chưa chạy, và nguồn lệch notebook (so sánh `parse(nbsrc)` với ô của `.ipynb`).

## Trước khi gửi pull request

```bash
pip install -r requirements-dev.txt
python -m pytest -q                              # kiểm thử: nlpvi, dữ liệu, mã hóa, liên kết, app
python tools/check_links.py                      # liên kết nội bộ và định dạng notebook
python tools/check_notebooks.py                  # chạy lại các bài CPU (00-07, 14); thêm --all cho cả bài cần Internet/GPU
```

Danh sách kiểm:

- [ ] test và kiểm tra liên kết đạt;
- [ ] đã chạy lại notebook bị ảnh hưởng và lời nhận xét khớp số mới;
- [ ] không đưa vào `outputs/`, mô hình, khóa API hay dữ liệu cá nhân;
- [ ] tệp mới có giấy phép phù hợp (xem [LICENSE](LICENSE), [LICENSE-NOI-DUNG.md](LICENSE-NOI-DUNG.md)).

## Một lưu ý kỹ thuật hay gặp

Công thức LaTeX (`\frac`, `\alpha`, `\text`...) viết trong **chuỗi Python thường** (không `r"..."`) sẽ bị vỡ vì `\f`, `\a`, `\t` thành ký tự điều khiển. Hãy dùng chuỗi thô hoặc sửa tệp trực tiếp bằng trình soạn thảo; bộ kiểm thử có một test quét lỗi này.

Khi đóng góp, bạn đồng ý đóng góp của mình được cấp phép theo MIT (mã) và CC BY 4.0 (nội dung) như mô tả trong [LICENSE-NOI-DUNG.md](LICENSE-NOI-DUNG.md).
