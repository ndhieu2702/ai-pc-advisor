# AI PC Advisor

**Hệ chuyên gia tư vấn cấu hình máy tính cho sinh viên AI**

## Mô Tả

AI PC Advisor là chương trình hệ chuyên gia viết bằng Python, hỗ trợ sinh viên ngành Trí tuệ nhân tạo lựa chọn cấu hình máy tính phù hợp với nhu cầu học tập, nghiên cứu và thực hành AI.

Hệ thống thu thập thông tin người dùng, tính điểm cho từng nhóm nhu cầu, chọn nhóm phù hợp nhất và đưa ra cấu hình khuyến nghị kèm giải thích.

## Mục Tiêu Dự Án

- Mô phỏng một hệ chuyên gia cơ bản trong lĩnh vực tư vấn cấu hình máy tính.
- Áp dụng cơ chế suy diễn dựa trên luật và điểm phù hợp.
- Giải thích được vì sao hệ thống đưa ra kết luận.
- Lưu trữ, xuất kết quả và hỗ trợ kiểm thử tự động.

## Chức Năng Chính

- Tư vấn thủ công thông qua câu hỏi yes/no và ngân sách.
- Chạy demo mẫu với các trường hợp nhu cầu phổ biến.
- Chấm điểm mức độ phù hợp cho từng nhóm nhu cầu.
- Hiển thị top 3 nhóm nhu cầu phù hợp nhất.
- Giải thích kết quả tư vấn.
- Hiển thị dấu vết suy luận trong quá trình cộng điểm.
- Lưu lịch sử tư vấn vào `history.csv`.
- Xem lịch sử tư vấn gần nhất.
- Xuất kết quả tư vấn ra file `.txt`.
- Kiểm thử hệ thống bằng các test case mẫu.

## Kiến Trúc Hệ Chuyên Gia

| Thành phần hệ chuyên gia | Cài đặt trong dự án |
|---|---|
| User Interface | Menu trong `main.py` / các hàm nhập liệu |
| Working Memory | `self.known` |
| Knowledge Base | `knowledge_base.py` |
| Inference Engine | `tinh_diem()`, chọn nhóm có điểm cao nhất |
| Explanation Facility | `giai_thich()`, `tao_dau_vet_suy_luan()` |
| Output | Cấu hình khuyến nghị, `history.csv`, file txt |

## Cấu Trúc Thư Mục

```text
AI_PC_Advisor/
├── app.py
├── main.py
├── expert_system.py
├── knowledge_base.py
├── data/
│   └── sample_cases.json
├── outputs/
├── history.csv
├── requirements.txt
└── README.md
```

## Cách Chạy Chương Trình

Chạy giao diện web Streamlit:

```bash
streamlit run app.py
```

Chạy bằng Python:

```bash
python main.py
```

Nếu máy Windows không nhận lệnh `python`, dùng:

```bash
py main.py
```

## Menu Chương Trình

```text
===== MENU HE CHUYEN GIA =====
1. Tu van thu cong
2. Chay demo mau
3. Thoat
4. Xem lich su tu van
5. Kiem thu he thong
```

## Ví Dụ Kết Quả Đầu Ra

```text
Nhom nhu cau cua ban: machine_learning_co_ban
Muc do phu hop: 100%

Cau hinh khuyen nghi:
- CPU: Core i5 hoac Ryzen 5 tro len
- RAM: Toi thieu 16GB
- SSD: Toi thieu 512GB
- GPU: GPU roi khong bat buoc, uu tien CPU va RAM
- Man hinh: Full HD, nen co khong gian hien thi tot

Giai thich ket qua:
Ban co hoc Machine Learning, can CPU tot va RAM du lon de xu ly du lieu.

Dau vet suy luan:
- Người dùng học lập trình -> tăng điểm cho nhóm lập trình cơ bản, Machine Learning cơ bản, Deep Learning và cấu hình cân bằng.
- Người dùng học Machine Learning -> tăng điểm cho nhóm Machine Learning cơ bản, Deep Learning, Computer Vision và AI kết hợp đồ họa.
```

## Công Nghệ Sử Dụng

- Python 3
- CSV
- File handling

## Hướng Phát Triển

- Xây dựng giao diện Streamlit.
- Kết nối cơ sở dữ liệu laptop thực tế.
- Cập nhật giá theo thị trường.
- Thêm fuzzy logic hoặc certainty factor.
- Xuất báo cáo PDF.
