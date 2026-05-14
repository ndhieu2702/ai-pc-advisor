# ============================================================
# KNOWLEDGE BASE - Cấu hình máy tính cho sinh viên AI
# ============================================================

CPU_KB = {
    "lap_trinh_co_ban": "Core i3/i5 hoặc Ryzen 3/5",
    "machine_learning_co_ban": "Core i5 hoặc Ryzen 5 trở lên",
    "ai_tiet_kiem_cloud": "Core i5 hoặc Ryzen 5, ưu tiên hiệu năng ổn định",
    "deep_learning_co_ban": "Core i5 H-series hoặc Ryzen 5 H-series",
    "deep_learning_hieu_nang": "Core i7/Ryzen 7 H-series",
    "computer_vision_hieu_nang": "Core i7/Ryzen 7 H-series",
    "ai_game_do_hoa": "Core i5/i7 H-series hoặc Ryzen 5/7 H-series",
    "may_mong_nhe_pin_lau": "Core i5 U-series hoặc Ryzen 5 U-series",
    "cau_hinh_can_bang": "Core i5/Ryzen 5 hoặc Core i7/Ryzen 7 tùy ngân sách",
}

RAM_KB = {
    "lap_trinh_co_ban": "Tối thiểu 8GB, khuyến nghị 16GB",
    "machine_learning_co_ban": "Tối thiểu 16GB",
    "ai_tiet_kiem_cloud": "Tối thiểu 16GB",
    "deep_learning_co_ban": "16GB, khuyến nghị 32GB nếu có điều kiện",
    "deep_learning_hieu_nang": "32GB",
    "computer_vision_hieu_nang": "16GB-32GB",
    "ai_game_do_hoa": "16GB-32GB",
    "may_mong_nhe_pin_lau": "16GB",
    "cau_hinh_can_bang": "16GB",
}

SSD_KB = {
    "lap_trinh_co_ban": "256GB-512GB",
    "machine_learning_co_ban": "Tối thiểu 512GB",
    "ai_tiet_kiem_cloud": "Tối thiểu 512GB",
    "deep_learning_co_ban": "512GB-1TB",
    "deep_learning_hieu_nang": "1TB",
    "computer_vision_hieu_nang": "1TB",
    "ai_game_do_hoa": "512GB-1TB",
    "may_mong_nhe_pin_lau": "512GB",
    "cau_hinh_can_bang": "512GB-1TB",
}

GPU_KB = {
    "lap_trinh_co_ban": "Không bắt buộc GPU rời",
    "machine_learning_co_ban": "Không bắt buộc, ưu tiên CPU/RAM",
    "ai_tiet_kiem_cloud": "Không bắt buộc GPU rời; nên dùng Google Colab, Kaggle Notebook hoặc máy phòng lab cho mô hình nặng",
    "deep_learning_co_ban": "Nên có RTX 3050/4050 nếu ngân sách cho phép",
    "deep_learning_hieu_nang": "RTX 4050/4060 trở lên",
    "computer_vision_hieu_nang": "RTX 4050/4060 trở lên",
    "ai_game_do_hoa": "RTX 3050/4050/4060 tùy ngân sách",
    "may_mong_nhe_pin_lau": "Không bắt buộc GPU rời",
    "cau_hinh_can_bang": "Tùy nhu cầu, không bắt buộc nếu dùng Cloud",
}

MAN_HINH_KB = {
    "lap_trinh_co_ban": "Full HD, 14-15.6 inch",
    "machine_learning_co_ban": "Full HD",
    "ai_tiet_kiem_cloud": "Full HD, 14-15.6 inch",
    "deep_learning_co_ban": "Full HD, 15.6 inch",
    "deep_learning_hieu_nang": "Full HD/2K, 15.6 inch trở lên",
    "computer_vision_hieu_nang": "Full HD/2K, màu sắc tốt",
    "ai_game_do_hoa": "Full HD, tần số quét và màu sắc tốt",
    "may_mong_nhe_pin_lau": "14 inch Full HD",
    "cau_hinh_can_bang": "Full HD, 14-15.6 inch",
}

GIAI_THICH_KB = {
    "lap_trinh_co_ban": (
        "Người dùng chủ yếu học lập trình cơ bản, không yêu cầu huấn luyện mô hình AI nặng, "
        "nên cấu hình vừa phải là phù hợp."
    ),
    "machine_learning_co_ban": (
        "Người dùng học Machine Learning cơ bản, cần CPU ổn định và RAM đủ lớn để xử lý dữ liệu, "
        "chạy Python và các mô hình ML nhỏ đến trung bình."
    ),
    "ai_tiet_kiem_cloud": (
        "Người dùng có nhu cầu học AI/Deep Learning/Computer Vision nhưng ngân sách thấp chưa phù hợp "
        "để mua laptop GPU mạnh. Hệ thống đề xuất cấu hình vừa đủ để học lập trình, xử lý dữ liệu "
        "và chạy mô hình nhỏ; với mô hình nặng nên dùng Google Colab, Kaggle Notebook hoặc máy phòng lab."
    ),
    "deep_learning_co_ban": (
        "Người dùng học Deep Learning với ngân sách trung bình, nên ưu tiên CPU H-series, RAM 16GB trở lên "
        "và có thể chọn GPU RTX phổ thông nếu ngân sách cho phép."
    ),
    "deep_learning_hieu_nang": (
        "Người dùng học Deep Learning với ngân sách cao, nên ưu tiên CPU H-series, RAM 32GB, SSD 1TB "
        "và GPU RTX để hỗ trợ huấn luyện mô hình hiệu quả hơn."
    ),
    "computer_vision_hieu_nang": (
        "Người dùng có nhu cầu xử lý ảnh hoặc Computer Vision, thường cần GPU rời, RAM lớn và màn hình "
        "có chất lượng hiển thị tốt để làm việc với dữ liệu hình ảnh."
    ),
    "ai_game_do_hoa": (
        "Người dùng vừa học AI vừa có nhu cầu game hoặc đồ họa, nên cần GPU rời, CPU H-series "
        "và tản nhiệt tốt để đảm bảo hiệu năng."
    ),
    "may_mong_nhe_pin_lau": (
        "Người dùng ưu tiên di chuyển, máy nhẹ và pin lâu, nên hệ thống ưu tiên CPU tiết kiệm điện, "
        "thiết kế mỏng nhẹ và cấu hình đủ tốt cho học tập hằng ngày."
    ),
    "cau_hinh_can_bang": (
        "Nhu cầu của người dùng ở mức tổng hợp hoặc có xung đột giữa hiệu năng, chi phí và tính di động, "
        "nên hệ thống đề xuất cấu hình cân bằng để dễ sử dụng lâu dài."
    ),
}
