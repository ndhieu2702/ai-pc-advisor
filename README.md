# AI PC Advisor

**Hệ chuyên gia tư vấn cấu hình máy tính cho sinh viên ngành Trí tuệ nhân tạo**

## Mô Tả

AI PC Advisor là dự án cuối kì môn Hệ chuyên gia. Hệ thống thu thập nhu cầu học tập, ngân sách và các yêu cầu phụ của người dùng, sau đó suy diễn nhóm nhu cầu phù hợp để đề xuất cấu hình máy tính.

Dự án hỗ trợ cả giao diện web Streamlit và phiên bản terminal.

## Mục Tiêu

- Mô phỏng một hệ chuyên gia tư vấn cấu hình máy tính cho sinh viên AI.
- Áp dụng suy diễn tiến bằng luật ưu tiên và điểm phù hợp.
- Bổ sung suy diễn lùi để kiểm tra giả thuyết kết luận.
- Phát hiện xung đột giữa ngân sách, hiệu năng và tính di động.
- Giải thích được kết quả và lưu lại lịch sử tư vấn.

## Chức Năng Chính

- Tư vấn cấu hình theo dữ liệu người dùng nhập.
- Chạy demo mẫu từ `data/sample_cases.json`.
- Chấm điểm và hiển thị top 3 nhóm nhu cầu phù hợp.
- Tính độ tin cậy tư vấn theo điểm, khoảng cách và xung đột.
- Giải thích kết quả và hiển thị dấu vết suy luận.
- Phát hiện xung đột nhu cầu như ngân sách thấp nhưng cần Deep Learning hoặc Computer Vision.
- Lưu lịch sử tư vấn vào `history.csv`.
- Xuất kết quả tư vấn ra file `.txt` trong thư mục `outputs/`.
- Kiểm thử hệ thống bằng các test case mẫu.
- Kiểm tra suy diễn lùi theo từng giả thuyết.

## Kiến Trúc Hệ Chuyên Gia

| Thành phần hệ chuyên gia | Cài đặt trong dự án |
|---|---|
| User Interface | `app.py` Streamlit, menu terminal trong `main.py` |
| Working Memory | `self.known` |
| Knowledge Base | `knowledge_base.py` |
| Inference Engine | `suy_dien_nhom_chinh()`, `tinh_diem()` |
| Backward Chaining | `kiem_tra_gia_thuyet()` |
| Explanation Facility | `giai_thich()`, `tao_dau_vet_suy_luan()` |
| Conflict Detection | `phat_hien_xung_dot()` |
| Certainty Evaluation | `tinh_muc_do_chac_chan()` |
| Output | Cấu hình khuyến nghị, `history.csv`, file txt trong `outputs/` |

## Cấu Trúc Thư Mục

```text
AI_PC_Advisor/
├── app.py
├── main.py
├── expert_system.py
├── knowledge_base.py
├── requirements.txt
├── README.md
├── history.csv
├── data/
│   └── sample_cases.json
├── outputs/
└── TuVanMayTinhAI.py
```

`main.py` là file chính để chạy bản terminal. `TuVanMayTinhAI.py` chỉ giữ vai trò tương thích với phiên bản cũ.

## Cách Chạy

Cài thư viện:

```bash
pip install -r requirements.txt
```

Chạy giao diện web:

```bash
streamlit run app.py
```

Chạy terminal:

```bash
python main.py
```

Nếu Windows không nhận `python`, dùng:

```bash
py main.py
```

## Menu Terminal

```text
===== MENU HE CHUYEN GIA =====
1. Tu van thu cong
2. Chay demo mau
3. Thoat
4. Xem lich su tu van
5. Kiem thu he thong
6. Kiem tra suy dien lui
```

## Ví Dụ Kết Quả

```text
Nhom nhu cau cua ban: ai_tiet_kiem_cloud
Muc do chac chan theo luat: 85%

Cau hinh khuyen nghi:
- CPU: Core i5 hoặc Ryzen 5, ưu tiên hiệu năng ổn định
- RAM: Tối thiểu 16GB
- SSD: Tối thiểu 512GB
- GPU: Không bắt buộc GPU rời; nên dùng Google Colab, Kaggle Notebook hoặc máy phòng lab cho mô hình nặng
- Man hinh: Full HD, 14-15.6 inch

Canh bao xung dot:
- Ngân sách thấp nhưng người dùng có nhu cầu học Deep Learning...

Giai thich ket qua:
Người dùng có nhu cầu học AI/Deep Learning/Computer Vision nhưng ngân sách thấp chưa phù hợp để mua laptop GPU mạnh...
```

## Công Nghệ Sử Dụng

- Python 3
- Streamlit
- Pandas
- CSV
- JSON
- File handling

## Hướng Phát Triển

- Kết nối cơ sở dữ liệu laptop thực tế.
- Cập nhật giá theo thị trường.
- Thêm fuzzy logic hoặc certainty factor nâng cao.
- Xuất báo cáo PDF.
- Bổ sung bộ luật theo từng chuyên ngành AI cụ thể.
