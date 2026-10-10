"""Sinh bộ dữ liệu đánh giá tiếng Việt TỔNG HỢP cho giáo trình.

Chạy lại (tái lập được, seed cố định):  python tools/make_data.py

Đây là dữ liệu ghép từ mẫu câu có kiểm soát, KHÔNG phải bình luận thật. Mục đích:
học quy trình (làm sạch, vector hóa, đánh giá, phân tích lỗi). Nó cố ý chứa các
hiện tượng khó: phủ định ("không tệ"), đối lập ("A tốt nhưng B kém"), teencode,
bỏ dấu, emoji và ~3% nhãn bị đảo. Xem data/DATA_CARD.md.
"""
import csv
import hashlib
import random
import unicodedata
from pathlib import Path

SEED = 20261003
N_TARGET = 1800
OUT = Path(__file__).resolve().parent.parent / "data" / "reviews_vi.csv"

# (chủ thể, [tính từ tích cực], [tính từ tiêu cực])
ASPECTS = {
    "sản phẩm": [
        ("chất lượng", ["tốt", "ổn", "cao"], ["kém", "tệ", "thấp"]),
        ("giao hàng", ["nhanh", "đúng hẹn", "gọn gàng"], ["chậm", "trễ hẹn", "lâu"]),
        ("đóng gói", ["cẩn thận", "chắc chắn", "đẹp"], ["sơ sài", "ẩu", "cẩu thả"]),
        ("màu sắc", ["đẹp", "tươi", "giống hình"], ["xỉn", "phai", "khác hình"]),
        ("giá", ["rẻ", "hợp lý", "mềm"], ["đắt", "cao", "chát"]),
        ("chất liệu", ["mềm", "bền", "dày dặn"], ["mỏng", "kém bền", "thô"]),
        ("tư vấn của shop", ["nhiệt tình", "chu đáo", "nhanh"], ["qua loa", "chậm", "thiếu nhiệt tình"]),
    ],
    "ứng dụng": [
        ("giao diện", ["đẹp", "dễ dùng", "thân thiện"], ["rối", "khó dùng", "xấu"]),
        ("tốc độ", ["nhanh", "mượt", "ổn định"], ["chậm", "giật", "thất thường"]),
        ("ứng dụng", ["mượt", "ổn định", "ít lỗi"], ["hay treo", "nhiều lỗi", "hay văng"]),
        ("tính năng", ["đầy đủ", "hữu ích", "tiện lợi"], ["nghèo nàn", "thừa thãi", "khó tìm"]),
        ("thông báo", ["kịp thời", "rõ ràng"], ["chậm", "hay trễ", "khó hiểu"]),
        ("hỗ trợ khách hàng", ["nhiệt tình", "nhanh", "chu đáo"], ["chậm", "thiếu chuyên nghiệp", "qua loa"]),
    ],
    "ẩm thực": [
        ("món ăn", ["ngon", "đậm đà", "vừa miệng"], ["dở", "nhạt", "mặn chát"]),
        ("phục vụ", ["nhanh", "chu đáo", "niềm nở"], ["chậm", "thờ ơ", "kém"]),
        ("không gian", ["thoáng", "sạch sẽ", "ấm cúng"], ["chật", "ồn", "bẩn"]),
        ("giá", ["hợp lý", "rẻ", "phải chăng"], ["đắt", "cao", "chát"]),
        ("khẩu phần", ["đầy đặn", "vừa ăn"], ["ít", "nhỏ", "sơ sài"]),
        ("nguyên liệu", ["tươi", "sạch", "chất lượng"], ["ôi", "cũ", "kém"]),
    ],
    "dịch vụ": [
        ("nhân viên", ["thân thiện", "chuyên nghiệp", "nhiệt tình"], ["thờ ơ", "thiếu chuyên nghiệp", "cáu gắt"]),
        ("thủ tục", ["gọn nhẹ", "nhanh", "đơn giản"], ["rườm rà", "phức tạp", "chậm"]),
        ("thời gian chờ", ["ngắn", "hợp lý"], ["lâu", "quá dài", "bất hợp lý"]),
        ("phòng ốc", ["sạch sẽ", "thoải mái", "thoáng"], ["bẩn", "cũ", "chật"]),
        ("việc giải quyết khiếu nại", ["nhanh", "thỏa đáng"], ["chậm", "qua loa"]),
        ("chi phí", ["hợp lý", "minh bạch"], ["cao", "mập mờ"]),
    ],
    "khóa học": [
        ("giảng viên", ["dễ hiểu", "nhiệt tình", "giỏi chuyên môn"], ["khó hiểu", "thiếu nhiệt tình", "hời hợt"]),
        ("nội dung", ["bổ ích", "có hệ thống", "sát thực tế"], ["sơ sài", "lan man", "lỗi thời"]),
        ("bài tập", ["hay", "vừa sức", "thực tế"], ["quá khó", "nhàm chán", "ít"]),
        ("tài liệu", ["đầy đủ", "rõ ràng", "dễ theo dõi"], ["thiếu", "khó theo dõi", "cũ"]),
        ("tốc độ giảng", ["vừa phải", "hợp lý"], ["quá nhanh", "quá chậm"]),
        ("học phí", ["hợp lý", "xứng đáng"], ["cao", "đắt"]),
    ],
}

NEUTRAL_CLAUSES = {
    "sản phẩm": ["Hàng giống mô tả", "Đóng gói bình thường", "Giá ở mức trung bình",
                 "Dùng được, không có gì đặc biệt", "Mới nhận hàng nên chưa đánh giá được nhiều",
                 "Màu sắc giống trong ảnh", "Giao hàng đúng thời gian dự kiến", "Kích cỡ đúng bảng size"],
    "ứng dụng": ["Ứng dụng có đủ các chức năng cơ bản", "Giao diện không thay đổi nhiều so với bản cũ",
                 "Mình mới cài nên chưa dùng nhiều", "Dung lượng khoảng 80 MB",
                 "Cần đăng nhập mới xem được nội dung", "Chạy bình thường trên máy mình",
                 "Bản cập nhật mới có thêm chế độ tối"],
    "ẩm thực": ["Quán nằm trên đường chính", "Món ăn ở mức bình thường", "Giá trung bình so với quanh đây",
                "Quán mở cửa đến 22 giờ", "Mình đi vào buổi trưa", "Khẩu phần vừa đủ một người",
                "Thực đơn khá nhiều món"],
    "dịch vụ": ["Mình đến làm thủ tục vào buổi sáng", "Nhân viên hướng dẫn theo đúng quy trình",
                "Thời gian xử lý khoảng hai ngày", "Dịch vụ giống như quảng cáo",
                "Chi phí ở mức trung bình", "Mình chờ khoảng mười phút", "Có thể thanh toán bằng thẻ"],
    "khóa học": ["Khóa học gồm mười hai buổi", "Học qua Zoom vào buổi tối",
                 "Tài liệu gửi qua email sau mỗi buổi", "Nội dung đúng như mô tả ban đầu",
                 "Mình mới học được vài buổi", "Lớp có khoảng ba mươi học viên", "Học phí thanh toán một lần"],
}
NEUTRAL_ADJ = ["bình thường", "tạm được", "tàm tạm", "không có gì đặc biệt", "ở mức trung bình", "cũng được"]

OPENERS = {
    "sản phẩm": ["Đặt hàng hôm thứ Ba, nhận hàng hôm thứ Sáu.", "Mua tặng người nhà.", "Mình dùng được một tuần rồi."],
    "ứng dụng": ["Dùng trên điện thoại Android được hai tuần.", "Mình dùng bản mới nhất.", "Cài về từ tháng trước."],
    "ẩm thực": ["Cả nhà ghé ăn tối cuối tuần.", "Đi ăn với bạn bè.", "Lần đầu mình ghé quán."],
    "dịch vụ": ["Mình đến vào giờ cao điểm.", "Mình dùng dịch vụ lần thứ hai.", "Đi công tác nên mình ghé."],
    "khóa học": ["Mình học online được một tháng.", "Mình đăng ký theo lời giới thiệu của bạn.", "Mình học buổi tối sau giờ làm."],
}
CLOSERS = {
    "tích cực": ["Sẽ ủng hộ tiếp.", "Recommend nhé!", "Cho 5 sao.", "Rất đáng thử."],
    "tiêu cực": ["Sẽ không quay lại.", "Không khuyên mua.", "Cho 1 sao.", "Thất vọng."],
    "trung tính": ["Cho 3 sao.", "Chưa biết có dùng lại không.", "Mình ghi nhận xét vậy thôi."],
}

POS_INT = ["", "", "rất", "khá", "cực kỳ", "thực sự", "quá"]
NEG_INT = ["", "", "rất", "khá", "quá", "hơi"]
TEEN = [("không", ["ko", "k", "hok"]), ("được", ["dc", "đc"]), ("sản phẩm", ["sp"]),
        ("mình", ["mik", "m"]), ("rất", ["rất", "r"]), ("nhân viên", ["nv"]), ("cảm ơn", ["cám ơn", "thanks"])]
EMOJI = {"tích cực": ["🙂", "👍", "❤️", "😍"], "tiêu cực": ["😡", "👎", "😞", "😤"], "trung tính": ["😐", "🤔"]}
LABELS = ["tích cực", "tiêu cực", "trung tính"]


def strip_accents(s: str) -> str:
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    return unicodedata.normalize("NFC", "".join(c for c in s if unicodedata.category(c) != "Mn"))


class Gen:
    def __init__(self, rng: random.Random):
        self.r = rng

    def pick_aspects(self, domain, k):
        return self.r.sample(ASPECTS[domain], k)

    def clause(self, aspect, kind):
        subj, pos, neg = aspect
        r = self.r
        if kind == "P":
            adj = r.choice(pos)
            return f"{subj} {r.choice(POS_INT)} {adj}".replace("  ", " ")
        if kind == "N":
            adj = r.choice(neg)
            inten = "" if adj.startswith("quá") else r.choice(NEG_INT)
            return f"{subj} {inten} {adj}".replace("  ", " ")
        if kind == "NP":  # phủ định của tích cực -> tiêu cực
            adj = r.choice(pos)
            w = r.choice(["không", "không", "chưa", "chẳng"])
            tail = r.choice(["", "", " lắm", " chút nào"]) if w == "không" else ""
            return f"{subj} {w} {adj}{tail}"
        if kind == "NN":  # phủ định của tiêu cực -> tích cực
            adj = r.choice(neg)
            return f"{subj} {r.choice(['không', 'không hề', 'chẳng hề'])} {adj}"
        if kind == "U":
            return f"{subj} {r.choice(NEUTRAL_ADJ)}"
        raise ValueError(kind)

    def build(self, label, domain):
        r, A = self.r, self.pick_aspects
        c = self.clause
        x = r.random()
        if label == "tích cực":
            a, b, d = A(domain, 3)
            if x < 0.38:
                parts = [c(a, "P")]
            elif x < 0.58:
                parts = [c(a, "P") + r.choice([", ", " và ", ", lại còn "]) + c(b, "P")]
            elif x < 0.78:
                parts = [r.choice([f"Tuy {c(a, 'N')} nhưng {c(b, 'P')}", f"{c(a, 'N').capitalize()}, nhưng {c(b, 'P')}",
                                   f"{c(a, 'N').capitalize()} nhưng bù lại {c(b, 'P')}"])]
            elif x < 0.92:
                parts = [c(a, "NN")] + ([c(b, "P")] if r.random() < 0.4 else [])
            else:
                parts = [r.choice(NEUTRAL_CLAUSES[domain]), c(a, "P")]
        elif label == "tiêu cực":
            a, b, d = A(domain, 3)
            if x < 0.38:
                parts = [c(a, "N")]
            elif x < 0.58:
                parts = [c(a, "N") + r.choice([", ", " và ", ", lại còn "]) + c(b, "N")]
            elif x < 0.78:
                parts = [r.choice([f"Tuy {c(a, 'P')} nhưng {c(b, 'N')}", f"{c(a, 'P').capitalize()}, nhưng {c(b, 'N')}",
                                   f"{c(a, 'P').capitalize()} nhưng tiếc là {c(b, 'N')}"])]
            elif x < 0.92:
                parts = [c(a, "NP")] + ([c(b, "N")] if r.random() < 0.4 else [])
            else:
                parts = [r.choice(NEUTRAL_CLAUSES[domain]), c(a, "N")]
        else:  # trung tính
            a, b, d = A(domain, 3)
            if x < 0.45:
                parts = [r.choice(NEUTRAL_CLAUSES[domain])]
            elif x < 0.60:
                n = r.sample(NEUTRAL_CLAUSES[domain], 2)
                parts = [n[0] + ", " + n[1][0].lower() + n[1][1:]]
            elif x < 0.80:
                parts = [c(a, "U")]
            else:
                parts = [f"Ưu điểm: {c(a, 'P')}. Nhược điểm: {c(b, 'N')}"]
        text = ". ".join(p[0].upper() + p[1:] for p in parts)
        text = text.rstrip(".") + "."
        if r.random() < 0.30:
            text = r.choice(OPENERS[domain]) + " " + text
        if r.random() < 0.35:
            text = text + " " + r.choice(CLOSERS[label])
        return text

    def add_noise(self, text, label):
        r = self.r
        if r.random() < 0.12:
            for src, options in TEEN:
                if src in text and r.random() < 0.6:
                    text = text.replace(src, r.choice(options), 1)
        if r.random() < 0.20:
            text = text.lower()
        if r.random() < 0.06:
            text = strip_accents(text)
        if r.random() < 0.15:
            pool = EMOJI[label] if r.random() < 0.8 else EMOJI[r.choice(LABELS)]
            text = text + " " + r.choice(pool)
        if r.random() < 0.15:
            text = text.rstrip(".") + r.choice(["!", "!!", "!!!", "..."])
        return text


def split_of(row_id: str) -> str:
    h = int(hashlib.md5(row_id.encode()).hexdigest(), 16) % 100
    return "train" if h < 70 else "valid" if h < 85 else "test"


def main():
    rng = random.Random(SEED)
    gen = Gen(rng)
    weights = {"tích cực": 0.45, "tiêu cực": 0.35, "trung tính": 0.20}
    domains = list(ASPECTS)
    seen, rows = set(), []
    guard = 0
    while len(rows) < N_TARGET and guard < N_TARGET * 50:
        guard += 1
        label = rng.choices(LABELS, weights=[weights[k] for k in LABELS])[0]
        domain = rng.choice(domains)
        text = gen.add_noise(gen.build(label, domain), label)
        key = unicodedata.normalize("NFC", text).lower()
        if key in seen:
            continue
        seen.add(key)
        final = label
        if rng.random() < 0.03:  # nhiễu nhãn có chủ đích
            final = rng.choice([k for k in LABELS if k != label])
        rows.append((text, final, domain))
    rng.shuffle(rows)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, lineterminator="\n")        # LF trên mọi hệ điều hành (khớp .gitattributes)
        w.writerow(["id", "text", "label", "domain", "split"])
        for i, (text, label, domain) in enumerate(rows, 1):
            rid = f"r{i:04d}"
            w.writerow([rid, text, label, domain, split_of(rid)])
    print(f"Đã ghi {len(rows)} dòng -> {OUT}")


if __name__ == "__main__":
    main()
