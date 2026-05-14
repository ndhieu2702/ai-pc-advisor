# ============================================================
# HE CHUYEN GIA TU VAN CAU HINH MAY TINH CHO SINH VIEN AI
# ============================================================

import csv
from datetime import datetime
import json
import os
import sys

from knowledge_base import (
    CPU_KB,
    GIAI_THICH_KB,
    GPU_KB,
    MAN_HINH_KB,
    RAM_KB,
    SSD_KB,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


class HeChuyenGiaTuVanMayTinhAI:
    def __init__(self):
        """Khởi tạo bộ nhớ làm việc và nạp cơ sở tri thức cấu hình."""
        self.known = {}
        self.cpu = CPU_KB
        self.ram = RAM_KB
        self.ssd = SSD_KB
        self.gpu = GPU_KB
        self.man_hinh = MAN_HINH_KB

    def hoi_yes_no(self, thuoc_tinh, cau_hoi):
        """Hỏi câu hỏi có/không và lưu câu trả lời vào self.known."""
        while True:
            tra_loi = input(f"{cau_hoi} (yes/no hoac co/khong): ").strip().lower()
            if tra_loi in ["yes", "y", "co", "có"]:
                self.known[thuoc_tinh] = True
                return True
            if tra_loi in ["no", "n", "khong", "không"]:
                self.known[thuoc_tinh] = False
                return False
            print("Gia tri khong hop le. Vui long nhap yes/no hoac co/khong.")

    def hoi_ngan_sach(self):
        """Hỏi mức ngân sách của người dùng và lưu vào self.known."""
        while True:
            print("\nNgan sach cua ban thuoc muc nao?")
            print("1. thap")
            print("2. trung_binh")
            print("3. cao")
            tra_loi = input("Nhap lua chon: ").strip().lower()

            if tra_loi in ["1", "thap", "thấp"]:
                self.known["ngan_sach"] = "thap"
                return "thap"
            if tra_loi in ["2", "trung_binh", "trung binh", "trung bình"]:
                self.known["ngan_sach"] = "trung_binh"
                return "trung_binh"
            if tra_loi in ["3", "cao"]:
                self.known["ngan_sach"] = "cao"
                return "cao"
            print("Gia tri khong hop le. Vui long nhap thap, trung_binh, cao hoac 1/2/3.")

    def thu_thap_du_lieu(self):
        """Thu thập toàn bộ thông tin đầu vào cần cho quá trình tư vấn."""
        self.hoi_yes_no("hoc_lap_trinh", "Ban co hoc lap trinh khong?")
        self.hoi_yes_no("hoc_machine_learning", "Ban co hoc Machine Learning khong?")
        self.hoi_yes_no("hoc_deep_learning", "Ban co hoc Deep Learning khong?")
        self.hoi_yes_no("xu_ly_anh_video", "Ban co xu ly anh/video hoac Computer Vision khong?")
        self.hoi_yes_no("choi_game_do_hoa", "Ban co choi game hoac lam do hoa khong?")
        self.hoi_yes_no("can_may_nhe_pin_lau", "Ban co can may nhe va pin lau khong?")
        self.hoi_yes_no("can_nang_cap", "Ban co muon may co kha nang nang cap RAM/SSD sau nay khong?")
        self.hoi_ngan_sach()

    def xac_dinh_nhom_nhu_cau(self):
        """Xác định nhóm nhu cầu theo tập luật điều kiện cũ."""
        k = self.known
        hoc_lap_trinh = k.get("hoc_lap_trinh", False)
        hoc_ml = k.get("hoc_machine_learning", False)
        hoc_dl = k.get("hoc_deep_learning", False)
        xu_ly_anh = k.get("xu_ly_anh_video", False)
        game_do_hoa = k.get("choi_game_do_hoa", False)
        may_nhe = k.get("can_may_nhe_pin_lau", False)
        ngan_sach = k.get("ngan_sach")

        if hoc_dl and xu_ly_anh:
            return "computer_vision"
        if hoc_ml and game_do_hoa:
            return "ai_game_do_hoa"
        if may_nhe and not hoc_dl and not game_do_hoa:
            return "may_mong_nhe_pin_lau"
        if hoc_lap_trinh and hoc_ml and hoc_dl:
            return "deep_learning"
        if hoc_lap_trinh and hoc_ml and not hoc_dl:
            return "machine_learning_co_ban"
        if hoc_lap_trinh and not hoc_ml and not hoc_dl:
            return "lap_trinh_co_ban"
        if hoc_ml and may_nhe and ngan_sach == "trung_binh":
            return "cau_hinh_can_bang"
        return "cau_hinh_can_bang"

    def suy_dien_nhom_chinh(self):
        """Chọn nhóm kết luận chính theo luật ưu tiên của hệ chuyên gia."""
        k = self.known
        hoc_lap_trinh = k.get("hoc_lap_trinh", False)
        hoc_ml = k.get("hoc_machine_learning", False)
        hoc_dl = k.get("hoc_deep_learning", False)
        xu_ly_anh = k.get("xu_ly_anh_video", False)
        game_do_hoa = k.get("choi_game_do_hoa", False)
        may_nhe = k.get("can_may_nhe_pin_lau", False)
        ngan_sach = k.get("ngan_sach")

        if ngan_sach == "thap" and (hoc_dl or xu_ly_anh or game_do_hoa):
            return "ai_tiet_kiem_cloud"
        if hoc_dl and xu_ly_anh and ngan_sach in ["trung_binh", "cao"]:
            return "computer_vision"
        if hoc_dl and ngan_sach in ["trung_binh", "cao"]:
            return "deep_learning"
        if hoc_ml and not hoc_dl:
            return "machine_learning_co_ban"
        if may_nhe and not hoc_dl and not game_do_hoa:
            return "may_mong_nhe_pin_lau"
        if hoc_lap_trinh and not hoc_ml and not hoc_dl:
            return "lap_trinh_co_ban"
        return "cau_hinh_can_bang"

    def tinh_diem(self):
        """Tính điểm phù hợp cho từng nhóm nhu cầu dựa trên dữ liệu đã biết."""
        k = self.known
        scores = {
            "lap_trinh_co_ban": 0,
            "machine_learning_co_ban": 0,
            "deep_learning": 0,
            "computer_vision": 0,
            "ai_game_do_hoa": 0,
            "may_mong_nhe_pin_lau": 0,
            "ai_tiet_kiem_cloud": 0,
            "cau_hinh_can_bang": 0,
        }

        if k.get("hoc_lap_trinh"):
            scores["lap_trinh_co_ban"] += 35
            scores["machine_learning_co_ban"] += 20
            scores["deep_learning"] += 15
            scores["cau_hinh_can_bang"] += 20
        else:
            scores["may_mong_nhe_pin_lau"] += 5

        if k.get("hoc_machine_learning"):
            scores["machine_learning_co_ban"] += 40
            scores["deep_learning"] += 25
            scores["computer_vision"] += 15
            scores["ai_game_do_hoa"] += 20
            scores["cau_hinh_can_bang"] += 20
        else:
            scores["lap_trinh_co_ban"] += 25

        if k.get("hoc_deep_learning"):
            scores["deep_learning"] += 45
            scores["computer_vision"] += 30
            scores["ai_game_do_hoa"] += 15
        else:
            scores["lap_trinh_co_ban"] += 25
            scores["machine_learning_co_ban"] += 25
            scores["may_mong_nhe_pin_lau"] += 20

        if k.get("xu_ly_anh_video"):
            scores["computer_vision"] += 50
        if k.get("choi_game_do_hoa"):
            scores["ai_game_do_hoa"] += 70
        else:
            scores["may_mong_nhe_pin_lau"] += 20
        if k.get("can_may_nhe_pin_lau"):
            scores["may_mong_nhe_pin_lau"] += 50
            scores["cau_hinh_can_bang"] += 20
        if k.get("can_nang_cap"):
            scores["cau_hinh_can_bang"] += 10

        ngan_sach = k.get("ngan_sach")
        if ngan_sach == "thap":
            scores["lap_trinh_co_ban"] += 15
            if k.get("hoc_deep_learning") or k.get("xu_ly_anh_video") or k.get("choi_game_do_hoa"):
                scores["ai_tiet_kiem_cloud"] += 100
                nhom_bi_phat = {
                    "deep_learning": 50,
                    "computer_vision": 50,
                    "deep_learning_hieu_nang": 50,
                    "computer_vision_hieu_nang": 50,
                    "ai_game_do_hoa": 40,
                }
                for ten_nhom, diem_tru in nhom_bi_phat.items():
                    if ten_nhom in scores:
                        scores[ten_nhom] = max(0, scores[ten_nhom] - diem_tru)
        elif ngan_sach == "trung_binh":
            scores["machine_learning_co_ban"] += 15
            scores["may_mong_nhe_pin_lau"] += 10
            scores["cau_hinh_can_bang"] += 30
        elif ngan_sach == "cao":
            scores["deep_learning"] += 15
            scores["computer_vision"] += 10
            scores["ai_game_do_hoa"] += 20

        return scores

    def phat_hien_xung_dot(self):
        """Phát hiện các xung đột lớn giữa nhu cầu và điều kiện sử dụng."""
        k = self.known
        xung_dot = []
        ngan_sach = k.get("ngan_sach")
        can_cau_hinh_cao = (
            k.get("hoc_deep_learning")
            or k.get("xu_ly_anh_video")
            or k.get("choi_game_do_hoa")
        )

        if ngan_sach == "thap" and can_cau_hinh_cao:
            xung_dot.append("Ngân sách thấp nhưng nhu cầu cần cấu hình cao")
        if k.get("can_may_nhe_pin_lau") and can_cau_hinh_cao:
            xung_dot.append("Nhu cầu máy nhẹ pin lâu xung đột với tác vụ hiệu năng cao")
        if k.get("choi_game_do_hoa") and ngan_sach == "thap":
            xung_dot.append("Game/đồ họa cần GPU nhưng ngân sách thấp")

        return xung_dot

    def tinh_muc_do_chac_chan(self, scores, nhom):
        """Tính độ tin cậy của kết luận dựa trên điểm, khoảng cách và xung đột."""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_score = scores.get(nhom, 0)
        second_score = 0

        for group, score in sorted_scores:
            if group != nhom:
                second_score = score
                break

        gap = top_score - second_score
        certainty = min(top_score, 90)

        if gap >= 25:
            certainty += 10
        elif gap >= 15:
            certainty += 5
        elif gap < 10:
            certainty -= 15

        conflicts = self.phat_hien_xung_dot()

        if conflicts:
            certainty = min(certainty, 85)

        if gap < 10:
            certainty = min(certainty, 75)

        if not conflicts and gap >= 25 and top_score >= 90:
            certainty = 100

        return max(0, min(100, round(certainty)))

    def danh_sach_gia_thuyet(self):
        """Trả về danh sách các nhóm có thể kiểm tra bằng suy diễn lùi."""
        return [
            "lap_trinh_co_ban",
            "machine_learning_co_ban",
            "ai_tiet_kiem_cloud",
            "deep_learning_co_ban",
            "deep_learning_hieu_nang",
            "computer_vision_hieu_nang",
            "ai_game_do_hoa",
            "may_mong_nhe_pin_lau",
            "cau_hinh_can_bang",
        ]

    def kiem_tra_gia_thuyet(self, nhom_gia_thuyet):
        """Kiểm tra một giả thuyết kết luận bằng suy diễn lùi."""
        k = self.known

        hoc_lap_trinh = bool(k.get("hoc_lap_trinh"))
        hoc_ml = bool(k.get("hoc_machine_learning"))
        hoc_dl = bool(k.get("hoc_deep_learning"))
        co_xu_ly_anh = bool(k.get("xu_ly_anh_video"))
        co_game_do_hoa = bool(k.get("choi_game_do_hoa"))
        co_may_nhe = bool(k.get("can_may_nhe_pin_lau"))
        ngan_sach = k.get("ngan_sach")
        co_nhu_cau_cao = hoc_dl or co_xu_ly_anh or co_game_do_hoa

        def mo_ta_boolean(value, co_text, khong_text):
            return f"Hiện tại: {co_text if value else khong_text}"

        def mo_ta_ngan_sach():
            labels = {
                "thap": "Ngân sách thấp",
                "trung_binh": "Ngân sách trung bình",
                "cao": "Ngân sách cao",
            }
            return f"Hiện tại: {labels.get(ngan_sach, 'Chưa có thông tin ngân sách')}"

        def mo_ta_nhu_cau_cao():
            nhu_cau = []
            if hoc_dl:
                nhu_cau.append("Deep Learning")
            if co_xu_ly_anh:
                nhu_cau.append("Computer Vision")
            if co_game_do_hoa:
                nhu_cau.append("Game/Đồ họa")
            if not nhu_cau:
                return "Hiện tại: Không có nhu cầu cấu hình cao"
            return "Hiện tại: Có nhu cầu " + ", ".join(nhu_cau)

        def tao_dieu_kien(dieu_kien_can, du_lieu_hien_tai, dat):
            return {
                "dieu_kien_can": dieu_kien_can,
                "du_lieu_hien_tai": du_lieu_hien_tai,
                "dat": bool(dat),
                "mo_ta": dieu_kien_can,
            }

        if nhom_gia_thuyet == "lap_trinh_co_ban":
            dieu_kien = [
                tao_dieu_kien("Người dùng có học lập trình", mo_ta_boolean(hoc_lap_trinh, "Có học lập trình", "Chưa học lập trình"), hoc_lap_trinh),
                tao_dieu_kien("Người dùng chưa học Machine Learning", mo_ta_boolean(hoc_ml, "Có học Machine Learning", "Chưa học Machine Learning"), not hoc_ml),
                tao_dieu_kien("Người dùng chưa học Deep Learning", mo_ta_boolean(hoc_dl, "Có học Deep Learning", "Chưa học Deep Learning"), not hoc_dl),
                tao_dieu_kien("Người dùng không xử lý ảnh / Computer Vision", mo_ta_boolean(co_xu_ly_anh, "Có xử lý ảnh / Computer Vision", "Không xử lý ảnh / Computer Vision"), not co_xu_ly_anh),
                tao_dieu_kien("Người dùng không chơi game / làm đồ họa", mo_ta_boolean(co_game_do_hoa, "Có chơi game / làm đồ họa", "Không chơi game / làm đồ họa"), not co_game_do_hoa),
            ]
        elif nhom_gia_thuyet == "machine_learning_co_ban":
            dieu_kien = [
                tao_dieu_kien("Người dùng có học Machine Learning", mo_ta_boolean(hoc_ml, "Có học Machine Learning", "Chưa học Machine Learning"), hoc_ml),
                tao_dieu_kien("Người dùng chưa học Deep Learning", mo_ta_boolean(hoc_dl, "Có học Deep Learning", "Chưa học Deep Learning"), not hoc_dl),
                tao_dieu_kien("Người dùng không xử lý ảnh / Computer Vision", mo_ta_boolean(co_xu_ly_anh, "Có xử lý ảnh / Computer Vision", "Không xử lý ảnh / Computer Vision"), not co_xu_ly_anh),
                tao_dieu_kien("Người dùng không chơi game / làm đồ họa nặng", mo_ta_boolean(co_game_do_hoa, "Có chơi game / làm đồ họa", "Không chơi game / làm đồ họa"), not co_game_do_hoa),
            ]
        elif nhom_gia_thuyet == "ai_tiet_kiem_cloud":
            dieu_kien = [
                tao_dieu_kien("Ngân sách hiện tại là thấp", mo_ta_ngan_sach(), ngan_sach == "thap"),
                tao_dieu_kien("Người dùng có ít nhất một nhu cầu cấu hình cao", mo_ta_nhu_cau_cao(), co_nhu_cau_cao),
            ]
        elif nhom_gia_thuyet == "deep_learning_co_ban":
            dieu_kien = [
                tao_dieu_kien("Người dùng có học Deep Learning", mo_ta_boolean(hoc_dl, "Có học Deep Learning", "Chưa học Deep Learning"), hoc_dl),
                tao_dieu_kien("Ngân sách hiện tại là trung bình", mo_ta_ngan_sach(), ngan_sach == "trung_binh"),
                tao_dieu_kien("Người dùng không xử lý ảnh / Computer Vision", mo_ta_boolean(co_xu_ly_anh, "Có xử lý ảnh / Computer Vision", "Không xử lý ảnh / Computer Vision"), not co_xu_ly_anh),
                tao_dieu_kien("Người dùng không chơi game / làm đồ họa", mo_ta_boolean(co_game_do_hoa, "Có chơi game / làm đồ họa", "Không chơi game / làm đồ họa"), not co_game_do_hoa),
            ]
        elif nhom_gia_thuyet == "deep_learning_hieu_nang":
            dieu_kien = [
                tao_dieu_kien("Người dùng có học Deep Learning", mo_ta_boolean(hoc_dl, "Có học Deep Learning", "Chưa học Deep Learning"), hoc_dl),
                tao_dieu_kien("Ngân sách hiện tại là cao", mo_ta_ngan_sach(), ngan_sach == "cao"),
                tao_dieu_kien("Người dùng không ưu tiên máy nhẹ, pin lâu", mo_ta_boolean(co_may_nhe, "Ưu tiên máy nhẹ, pin lâu", "Không ưu tiên máy nhẹ, pin lâu"), not co_may_nhe),
            ]
        elif nhom_gia_thuyet == "computer_vision_hieu_nang":
            dieu_kien = [
                tao_dieu_kien("Người dùng có học Machine Learning hoặc Deep Learning", mo_ta_boolean(hoc_ml or hoc_dl, "Có học Machine Learning hoặc Deep Learning", "Chưa học Machine Learning hoặc Deep Learning"), hoc_ml or hoc_dl),
                tao_dieu_kien("Người dùng có xử lý ảnh / Computer Vision", mo_ta_boolean(co_xu_ly_anh, "Có xử lý ảnh / Computer Vision", "Không xử lý ảnh / Computer Vision"), co_xu_ly_anh),
                tao_dieu_kien("Ngân sách hiện tại là trung bình hoặc cao", mo_ta_ngan_sach(), ngan_sach in ["trung_binh", "cao"]),
            ]
        elif nhom_gia_thuyet == "ai_game_do_hoa":
            dieu_kien = [
                tao_dieu_kien("Người dùng có chơi game hoặc làm đồ họa", mo_ta_boolean(co_game_do_hoa, "Có chơi game / làm đồ họa", "Không chơi game / làm đồ họa"), co_game_do_hoa),
                tao_dieu_kien("Ngân sách hiện tại là trung bình hoặc cao", mo_ta_ngan_sach(), ngan_sach in ["trung_binh", "cao"]),
            ]
        elif nhom_gia_thuyet == "may_mong_nhe_pin_lau":
            dieu_kien = [
                tao_dieu_kien("Người dùng cần máy nhẹ, pin lâu", mo_ta_boolean(co_may_nhe, "Cần máy nhẹ, pin lâu", "Không cần máy nhẹ, pin lâu"), co_may_nhe),
                tao_dieu_kien("Người dùng không học Deep Learning", mo_ta_boolean(hoc_dl, "Có học Deep Learning", "Chưa học Deep Learning"), not hoc_dl),
                tao_dieu_kien("Người dùng không xử lý ảnh / Computer Vision", mo_ta_boolean(co_xu_ly_anh, "Có xử lý ảnh / Computer Vision", "Không xử lý ảnh / Computer Vision"), not co_xu_ly_anh),
                tao_dieu_kien("Người dùng không chơi game / làm đồ họa", mo_ta_boolean(co_game_do_hoa, "Có chơi game / làm đồ họa", "Không chơi game / làm đồ họa"), not co_game_do_hoa),
            ]
        elif nhom_gia_thuyet == "cau_hinh_can_bang":
            nhu_cau_chinh = [
                hoc_lap_trinh,
                hoc_ml,
                hoc_dl,
                co_xu_ly_anh,
                co_game_do_hoa,
                co_may_nhe,
            ]
            so_nhu_cau = sum(bool(nhu_cau) for nhu_cau in nhu_cau_chinh)
            co_xung_dot = (
                (hoc_dl and co_may_nhe)
                or (co_game_do_hoa and co_may_nhe)
                or (co_xu_ly_anh and co_may_nhe)
            )
            mixed_need = so_nhu_cau >= 2
            if co_xung_dot:
                du_lieu_can_bang = "Hiện tại: Có xung đột giữa nhu cầu hiệu năng và tính di động"
            elif mixed_need:
                du_lieu_can_bang = f"Hiện tại: Có {so_nhu_cau} nhu cầu khác loại"
            else:
                du_lieu_can_bang = "Hiện tại: Chưa có nhu cầu pha trộn hoặc xung đột rõ"
            dieu_kien = [
                tao_dieu_kien(
                    "Người dùng có xung đột nhu cầu hoặc có từ 2 nhu cầu khác loại trở lên",
                    du_lieu_can_bang,
                    co_xung_dot or mixed_need,
                )
            ]
        else:
            dieu_kien = [
                tao_dieu_kien(
                    "Giả thuyết nằm trong danh sách hệ thống có thể kiểm tra",
                    "Hiện tại: Giả thuyết không có trong danh sách hỗ trợ",
                    False,
                )
            ]

        phu_hop = all(dieu_kien_item["dat"] for dieu_kien_item in dieu_kien)
        if phu_hop:
            ket_luan = "Giả thuyết phù hợp với dữ liệu hiện tại."
        else:
            ket_luan = "Giả thuyết chưa phù hợp vì một số điều kiện cần không khớp với dữ liệu hiện tại."

        return {
            "gia_thuyet": nhom_gia_thuyet,
            "phu_hop": phu_hop,
            "dieu_kien": dieu_kien,
            "ket_luan": ket_luan,
        }

    def tao_dau_vet_suy_luan(self):
        """Tạo danh sách giải thích các luật đã tác động đến điểm số."""
        k = self.known
        dau_vet = []

        if k.get("hoc_lap_trinh"):
            dau_vet.append("- Người dùng học lập trình -> tăng điểm cho nhóm lập trình cơ bản, Machine Learning cơ bản, Deep Learning và cấu hình cân bằng.")
        if k.get("hoc_machine_learning"):
            dau_vet.append("- Người dùng học Machine Learning -> tăng điểm cho nhóm Machine Learning cơ bản, Deep Learning, Computer Vision và AI kết hợp đồ họa.")
        if k.get("hoc_deep_learning"):
            dau_vet.append("- Người dùng học Deep Learning -> tăng điểm mạnh cho nhóm Deep Learning, Computer Vision và AI kết hợp đồ họa.")
        if k.get("xu_ly_anh_video"):
            dau_vet.append("- Người dùng xử lý ảnh/video -> tăng điểm mạnh cho nhóm Computer Vision.")
        if k.get("choi_game_do_hoa"):
            dau_vet.append("- Người dùng chơi game hoặc làm đồ họa -> tăng điểm mạnh cho nhóm AI kết hợp game/đồ họa.")
        if k.get("can_may_nhe_pin_lau"):
            dau_vet.append("- Người dùng cần máy nhẹ, pin lâu -> tăng điểm cho nhóm máy mỏng nhẹ và cấu hình cân bằng.")
        if k.get("can_nang_cap"):
            dau_vet.append("- Người dùng cần nâng cấp RAM/SSD -> tăng điểm cho nhóm cấu hình cân bằng.")

        ngan_sach = k.get("ngan_sach")
        if ngan_sach == "thap":
            dau_vet.append("- Ngân sách thấp -> ưu tiên nhóm lập trình cơ bản và cấu hình tiết kiệm.")
            if k.get("hoc_deep_learning") or k.get("xu_ly_anh_video") or k.get("choi_game_do_hoa"):
                dau_vet.append("- Ngân sách thấp nhưng có nhu cầu cấu hình cao -> chuyển hướng sang nhóm AI tiết kiệm + Cloud.")
        elif ngan_sach == "trung_binh":
            dau_vet.append("- Ngân sách trung bình -> tăng điểm cho nhóm Machine Learning cơ bản, máy mỏng nhẹ và cấu hình cân bằng.")
        elif ngan_sach == "cao":
            dau_vet.append("- Ngân sách cao -> tăng điểm cho nhóm Deep Learning, Computer Vision và AI kết hợp đồ họa.")

        return dau_vet

    def giai_thich(self, nhom):
        """Trả về giải thích ngắn gọn cho nhóm kết luận."""
        return GIAI_THICH_KB[nhom]

    def canh_bao_ngan_sach(self, nhom):
        """Tạo cảnh báo hoặc gợi ý điều chỉnh theo mức ngân sách."""
        ngan_sach = self.known.get("ngan_sach")
        if nhom == "ai_tiet_kiem_cloud":
            return "Ngân sách hiện tại chưa đủ để mua cấu hình AI hiệu năng cao có GPU RTX. Hệ thống đề xuất hướng học tập tiết kiệm hơn: ưu tiên RAM/SSD và sử dụng Google Colab, Kaggle Notebook hoặc máy phòng lab cho các mô hình nặng."
        if ngan_sach == "thap" and nhom in ["deep_learning", "computer_vision", "ai_game_do_hoa"]:
            return "Cảnh báo ngân sách: Nhu cầu của bạn cần cấu hình khá mạnh, nhưng ngân sách đang ở mức thấp. Nên ưu tiên RAM/SSD trước, có thể dùng Google Colab hoặc máy phòng lab để chạy mô hình nặng."
        if ngan_sach == "thap":
            return "Điều chỉnh ngân sách: Với ngân sách thấp, nên ưu tiên SSD và RAM trước, không bắt buộc GPU rời."
        if ngan_sach == "trung_binh":
            return "Điều chỉnh ngân sách: Với ngân sách trung bình, nên chọn RAM 16GB, SSD 512GB và CPU Core i5/Ryzen 5 trở lên."
        if ngan_sach == "cao":
            return "Điều chỉnh ngân sách: Với ngân sách cao, có thể ưu tiên CPU H-series, RAM 32GB, SSD 1TB và GPU RTX."
        return ""

    def luu_lich_su(self, nhom, diem):
        """Lưu kết quả tư vấn hiện tại vào file history.csv."""
        ten_file = "history.csv"
        fieldnames = [
            "time",
            "hoc_lap_trinh",
            "hoc_machine_learning",
            "hoc_deep_learning",
            "xu_ly_anh_video",
            "choi_game_do_hoa",
            "can_may_nhe_pin_lau",
            "can_nang_cap",
            "ngan_sach",
            "nhom_ket_luan",
            "muc_do_phu_hop",
            "cpu",
            "ram",
            "ssd",
            "gpu",
            "man_hinh",
        ]

        dong_du_lieu = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hoc_lap_trinh": self.known.get("hoc_lap_trinh", ""),
            "hoc_machine_learning": self.known.get("hoc_machine_learning", ""),
            "hoc_deep_learning": self.known.get("hoc_deep_learning", ""),
            "xu_ly_anh_video": self.known.get("xu_ly_anh_video", ""),
            "choi_game_do_hoa": self.known.get("choi_game_do_hoa", ""),
            "can_may_nhe_pin_lau": self.known.get("can_may_nhe_pin_lau", ""),
            "can_nang_cap": self.known.get("can_nang_cap", ""),
            "ngan_sach": self.known.get("ngan_sach", ""),
            "nhom_ket_luan": nhom,
            "muc_do_phu_hop": diem,
            "cpu": self.cpu[nhom],
            "ram": self.ram[nhom],
            "ssd": self.ssd[nhom],
            "gpu": self.gpu[nhom],
            "man_hinh": self.man_hinh[nhom],
        }

        can_ghi_header = not os.path.exists(ten_file) or os.path.getsize(ten_file) == 0
        encoding = "utf-8-sig" if can_ghi_header else "utf-8"
        with open(ten_file, "a", newline="", encoding=encoding) as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if can_ghi_header:
                writer.writeheader()
            writer.writerow(dong_du_lieu)

    def xuat_ket_qua_txt(self, nhom, diem, top_3):
        """Xuất kết quả tư vấn chi tiết ra file txt trong thư mục outputs."""
        thoi_gian = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ten_file = f"ket_qua_tu_van_{thoi_gian}.txt"
        thu_muc_outputs = "outputs"
        os.makedirs(thu_muc_outputs, exist_ok=True)
        duong_dan_file = os.path.join(thu_muc_outputs, ten_file)
        xung_dot = self.phat_hien_xung_dot()

        with open(duong_dan_file, "w", encoding="utf-8-sig") as file:
            file.write("KET QUA TU VAN CAU HINH MAY TINH\n")
            file.write("=================================\n")
            file.write(f"Nhom nhu cau: {nhom}\n")
            file.write(f"Mức độ chắc chắn theo luật: {diem}%\n")

            file.write("\nCau hinh khuyen nghi:\n")
            file.write(f"- CPU: {self.cpu[nhom]}\n")
            file.write(f"- RAM: {self.ram[nhom]}\n")
            file.write(f"- SSD: {self.ssd[nhom]}\n")
            file.write(f"- GPU: {self.gpu[nhom]}\n")
            file.write(f"- Man hinh: {self.man_hinh[nhom]}\n")

            file.write("\nCanh bao ngan sach:\n")
            file.write(f"{self.canh_bao_ngan_sach(nhom)}\n")

            file.write("\nCác xung đột nếu có:\n")
            if xung_dot:
                for dong in xung_dot:
                    file.write(f"- {dong}\n")
            else:
                file.write("- Không có xung đột lớn.\n")

            if self.known.get("can_nang_cap"):
                file.write("\nGoi y nang cap:\n")
                file.write("- Nen chon may co kha nang nang cap RAM hoac SSD de su dung lau dai.\n")

            file.write("\nGiai thich ket qua:\n")
            file.write(f"{self.giai_thich(nhom)}\n")

            file.write("\nDau vet suy luan:\n")
            for dong in self.tao_dau_vet_suy_luan():
                file.write(f"{dong}\n")

            file.write("\nDu lieu nguoi dung da cung cap:\n")
            for key, value in self.known.items():
                file.write(f"- {key}: {value}\n")

            file.write("\nTop 3 nhom nhu cau phu hop:\n")
            for ten_nhom, score in top_3:
                file.write(f"- {ten_nhom}: {max(0, min(score, 100))}%\n")

        return duong_dan_file.replace("\\", "/")

    def in_ket_qua(self):
        """In kết quả tư vấn, lưu lịch sử và xuất file báo cáo."""
        scores = self.tinh_diem()

        # Bộ suy diễn chọn nhóm theo luật ưu tiên và điểm phù hợp
        top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

        nhom = self.suy_dien_nhom_chinh()
        diem = self.tinh_muc_do_chac_chan(scores, nhom)
        xung_dot = self.phat_hien_xung_dot()

        print("\n================= KET QUA TU VAN =================")
        print(f"Nhom nhu cau cua ban: {nhom}")
        print(f"Muc do chac chan theo luat: {diem}%")
        print("\nCau hinh khuyen nghi:")
        print(f"- CPU: {self.cpu[nhom]}")
        print(f"- RAM: {self.ram[nhom]}")
        print(f"- SSD: {self.ssd[nhom]}")
        print(f"- GPU: {self.gpu[nhom]}")
        print(f"- Man hinh: {self.man_hinh[nhom]}")

        print("\n" + self.canh_bao_ngan_sach(nhom))

        if xung_dot:
            print("\nCanh bao xung dot:")
            for dong in xung_dot:
                print(f"- {dong}")

        if self.known.get("can_nang_cap"):
            print("- Goi y nang cap: Nen chon may co kha nang nang cap RAM hoac SSD de su dung lau dai.")

        print("\nGiai thich ket qua:")
        print(self.giai_thich(nhom))

        print("\nDau vet suy luan:")
        for dong in self.tao_dau_vet_suy_luan():
            print(dong)

        print("\nDu lieu nguoi dung da cung cap:")
        for key, value in self.known.items():
            print(f"- {key}: {value}")

        print("\nTop 3 nhom nhu cau phu hop:")
        for ten_nhom, score in top_3:
            print(f"- {ten_nhom}: {max(0, min(score, 100))}%")

        print("===================================================")
        self.luu_lich_su(nhom, diem)
        print("Da luu ket qua tu van vao file history.csv")
        ten_file = self.xuat_ket_qua_txt(nhom, diem, top_3)
        print(f"Da xuat ket qua tu van ra file: {ten_file}")
        print("Ket thuc tu van.")

    def bat_dau(self):
        """Chạy luồng tư vấn thủ công trên terminal."""
        print("====================================================")
        print(" HE CHUYEN GIA TU VAN CAU HINH MAY TINH CHO SINH VIEN AI")
        print("====================================================")
        print("Huong dan tra loi:")
        print("- Cau hoi co/khong: nhap yes/no hoac co/khong")
        print("- Ngan sach: nhap thap, trung_binh, cao hoac 1/2/3")
        print()
        self.thu_thap_du_lieu()
        self.in_ket_qua()

    def doc_sample_cases(self):
        """Đọc danh sách demo và test case từ file JSON."""
        duong_dan = os.path.join(os.path.dirname(__file__), "data", "sample_cases.json")
        if not os.path.exists(duong_dan):
            print("Khong tim thay file data/sample_cases.json")
            return None

        with open(duong_dan, "r", encoding="utf-8") as file:
            return json.load(file)

    def chay_demo_mau(self):
        """Cho người dùng chọn một demo mẫu và tự động tư vấn."""
        demos = self.doc_sample_cases()
        if demos is None:
            return

        while True:
            print("\n===== DEMO MAU =====")
            for index, demo in enumerate(demos, start=1):
                print(f"{index}. {demo['name']}")

            lua_chon = input("Nhap lua chon demo: ").strip()
            if lua_chon.isdigit() and 1 <= int(lua_chon) <= len(demos):
                demo = demos[int(lua_chon) - 1]
                self.known = demo["input"].copy()
                print(f"\nDang chay demo: {demo['name']}")
                self.in_ket_qua()
                return

            print(f"Lua chon khong hop le. Vui long nhap tu 1 den {len(demos)}.")

    def xem_lich_su(self):
        """Đọc và hiển thị 5 lần tư vấn gần nhất từ history.csv."""
        ten_file = "history.csv"
        if not os.path.exists(ten_file) or os.path.getsize(ten_file) == 0:
            print("Chua co lich su tu van.")
            return

        with open(ten_file, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            lich_su = list(reader)

        if not lich_su:
            print("Chua co lich su tu van.")
            return

        print("\n===== LICH SU TU VAN GAN NHAT =====")
        for dong in lich_su[-5:]:
            print(
                f"- {dong.get('time', '')} | "
                f"nhom: {dong.get('nhom_ket_luan', '')} | "
                f"do tin cay: {dong.get('muc_do_phu_hop', '')}% | "
                f"ngan sach: {dong.get('ngan_sach', '')}"
            )

    def kiem_thu_he_thong(self):
        """Chạy các test case mẫu để kiểm tra nhóm kết luận."""
        test_cases = self.doc_sample_cases()
        if test_cases is None:
            return

        known_cu = self.known.copy()
        so_dung = 0
        so_sai = 0

        print("\n===== KIEM THU HE THONG =====")
        for test_case in test_cases:
            self.known = test_case["input"].copy()
            self.tinh_diem()
            nhom_du_doan = self.suy_dien_nhom_chinh()
            expected = test_case["expected_group"]

            if nhom_du_doan == expected:
                so_dung += 1
                print(f"PASS: {test_case['name']} -> {nhom_du_doan}")
            else:
                so_sai += 1
                print(f"FAIL: {test_case['name']} | Expected: {expected} | Got: {nhom_du_doan}")

        self.known = known_cu

        print(f"\nTong so test: {len(test_cases)}")
        print(f"Dung: {so_dung}")
        print(f"Sai: {so_sai}")

    def kiem_thu_he_thong_data(self):
        """Trả về dữ liệu kiểm thử để giao diện web hiển thị PASS/FAIL rõ ràng."""
        test_cases = self.doc_sample_cases()
        if test_cases is None:
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "details": [],
            }

        known_cu = self.known.copy()
        details = []
        so_dung = 0
        so_sai = 0

        for test_case in test_cases:
            self.known = test_case["input"].copy()
            self.tinh_diem()
            nhom_du_doan = self.suy_dien_nhom_chinh()
            expected = test_case["expected_group"]
            passed = nhom_du_doan == expected

            if passed:
                so_dung += 1
            else:
                so_sai += 1

            details.append(
                {
                    "name": test_case["name"],
                    "expected": expected,
                    "got": nhom_du_doan,
                    "passed": passed,
                }
            )

        self.known = known_cu

        return {
            "total": len(test_cases),
            "passed": so_dung,
            "failed": so_sai,
            "details": details,
        }

    def ten_nhom_hien_thi(self, nhom):
        """Chuyển mã nhóm nội bộ thành tên dễ đọc trên terminal."""
        mapping = {
            "lap_trinh_co_ban": "Lap trinh co ban",
            "machine_learning_co_ban": "Machine Learning co ban",
            "ai_tiet_kiem_cloud": "AI tiet kiem + Cloud",
            "deep_learning_co_ban": "Deep Learning co ban",
            "deep_learning_hieu_nang": "Deep Learning hieu nang cao",
            "computer_vision_hieu_nang": "Computer Vision hieu nang cao",
            "ai_game_do_hoa": "AI + Game / Do hoa",
            "may_mong_nhe_pin_lau": "May mong nhe, pin lau",
            "cau_hinh_can_bang": "Cau hinh can bang",
        }
        return mapping.get(nhom, nhom)

    def kiem_tra_suy_dien_lui_terminal(self):
        """Chạy chức năng kiểm tra giả thuyết bằng suy diễn lùi trên terminal."""
        print("\n===== KIEM TRA SUY DIEN LUI =====")
        self.known.clear()
        self.thu_thap_du_lieu()

        danh_sach = self.danh_sach_gia_thuyet()
        print("\nDanh sach gia thuyet co the kiem tra:")
        for index, nhom in enumerate(danh_sach, start=1):
            print(f"{index}. {self.ten_nhom_hien_thi(nhom)}")

        while True:
            lua_chon = input("Nhap lua chon gia thuyet: ").strip()
            if lua_chon.isdigit() and 1 <= int(lua_chon) <= len(danh_sach):
                nhom_gia_thuyet = danh_sach[int(lua_chon) - 1]
                break
            print(f"Lua chon khong hop le. Vui long nhap tu 1 den {len(danh_sach)}.")

        ket_qua = self.kiem_tra_gia_thuyet(nhom_gia_thuyet)
        trang_thai = "Phu hop" if ket_qua["phu_hop"] else "Chua phu hop"

        print("\n===== KET QUA KIEM TRA GIA THUYET =====")
        print(f"Gia thuyet: {self.ten_nhom_hien_thi(ket_qua['gia_thuyet'])}")
        print(f"Ket luan: {trang_thai}")

        print("\nCac dieu kien he thong kiem tra:")
        for dieu_kien in ket_qua["dieu_kien"]:
            nhan = "[DAT]" if dieu_kien.get("dat") else "[CHUA DAT]"
            dieu_kien_can = dieu_kien.get("dieu_kien_can", dieu_kien.get("mo_ta", ""))
            du_lieu_hien_tai = dieu_kien.get("du_lieu_hien_tai", "")
            print(f"{nhan} Dieu kien can: {dieu_kien_can}")
            print(f"      Du lieu hien tai: {du_lieu_hien_tai}")

        print(f"\n{ket_qua['ket_luan']}")

    def menu(self):
        """Hiển thị menu terminal và điều hướng các chức năng chính."""
        while True:
            print("\n===== MENU HE CHUYEN GIA =====")
            print("1. Tu van thu cong")
            print("2. Chay demo mau")
            print("3. Thoat")
            print("4. Xem lich su tu van")
            print("5. Kiem thu he thong")
            print("6. Kiem tra suy dien lui")

            lua_chon = input("Nhap lua chon: ").strip()
            if lua_chon == "1":
                self.known.clear()
                self.bat_dau()
            elif lua_chon == "2":
                self.chay_demo_mau()
            elif lua_chon == "3":
                print("Ket thuc chuong trinh.")
                break
            elif lua_chon == "4":
                self.xem_lich_su()
            elif lua_chon == "5":
                self.kiem_thu_he_thong()
            elif lua_chon == "6":
                self.kiem_tra_suy_dien_lui_terminal()
            else:
                print("Vui long nhap 1, 2, 3, 4, 5 hoac 6.")
