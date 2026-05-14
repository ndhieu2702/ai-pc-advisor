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
        self.known = {}
        self.cpu = CPU_KB
        self.ram = RAM_KB
        self.ssd = SSD_KB
        self.gpu = GPU_KB
        self.man_hinh = MAN_HINH_KB

    def hoi_yes_no(self, thuoc_tinh, cau_hoi):
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
        self.hoi_yes_no("hoc_lap_trinh", "Ban co hoc lap trinh khong?")
        self.hoi_yes_no("hoc_machine_learning", "Ban co hoc Machine Learning khong?")
        self.hoi_yes_no("hoc_deep_learning", "Ban co hoc Deep Learning khong?")
        self.hoi_yes_no("xu_ly_anh_video", "Ban co xu ly anh/video hoac Computer Vision khong?")
        self.hoi_yes_no("choi_game_do_hoa", "Ban co choi game hoac lam do hoa khong?")
        self.hoi_yes_no("can_may_nhe_pin_lau", "Ban co can may nhe va pin lau khong?")
        self.hoi_yes_no("can_nang_cap", "Ban co muon may co kha nang nang cap RAM/SSD sau nay khong?")
        self.hoi_ngan_sach()

    def xac_dinh_nhom_nhu_cau(self):
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

    def tinh_diem(self):
        k = self.known
        scores = {
            "lap_trinh_co_ban": 0,
            "machine_learning_co_ban": 0,
            "deep_learning": 0,
            "computer_vision": 0,
            "ai_game_do_hoa": 0,
            "may_mong_nhe_pin_lau": 0,
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
            scores["ai_game_do_hoa"] += 45
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
        elif ngan_sach == "trung_binh":
            scores["machine_learning_co_ban"] += 15
            scores["may_mong_nhe_pin_lau"] += 10
            scores["cau_hinh_can_bang"] += 30
        elif ngan_sach == "cao":
            scores["deep_learning"] += 15
            scores["computer_vision"] += 10
            scores["ai_game_do_hoa"] += 20

        return scores

    def tao_dau_vet_suy_luan(self):
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
        elif ngan_sach == "trung_binh":
            dau_vet.append("- Ngân sách trung bình -> tăng điểm cho nhóm Machine Learning cơ bản, máy mỏng nhẹ và cấu hình cân bằng.")
        elif ngan_sach == "cao":
            dau_vet.append("- Ngân sách cao -> tăng điểm cho nhóm Deep Learning, Computer Vision và AI kết hợp đồ họa.")

        return dau_vet

    def giai_thich(self, nhom):
        return GIAI_THICH_KB[nhom]

    def canh_bao_ngan_sach(self, nhom):
        ngan_sach = self.known.get("ngan_sach")
        if ngan_sach == "thap" and nhom in ["deep_learning", "computer_vision", "ai_game_do_hoa"]:
            return "Canh bao ngan sach: Nhu cau cua ban can cau hinh kha manh, nhung ngan sach dang o muc thap. Nen uu tien RAM/SSD truoc, co the dung Google Colab hoac may phong lab de chay mo hinh nang."
        if ngan_sach == "thap":
            return "Dieu chinh ngan sach: Voi ngan sach thap, nen uu tien SSD va RAM truoc, khong bat buoc GPU roi."
        if ngan_sach == "trung_binh":
            return "Dieu chinh ngan sach: Voi ngan sach trung binh, nen chon RAM 16GB, SSD 512GB va CPU Core i5/Ryzen 5 tro len."
        if ngan_sach == "cao":
            return "Dieu chinh ngan sach: Voi ngan sach cao, co the uu tien CPU H-series, RAM 32GB, SSD 1TB va GPU RTX."
        return ""

    def luu_lich_su(self, nhom, diem):
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
        thoi_gian = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ten_file = f"ket_qua_tu_van_{thoi_gian}.txt"
        thu_muc_outputs = "outputs"
        os.makedirs(thu_muc_outputs, exist_ok=True)
        duong_dan_file = os.path.join(thu_muc_outputs, ten_file)

        with open(duong_dan_file, "w", encoding="utf-8-sig") as file:
            file.write("KET QUA TU VAN CAU HINH MAY TINH\n")
            file.write("=================================\n")
            file.write(f"Nhom nhu cau: {nhom}\n")
            file.write(f"Muc do phu hop: {diem}%\n")

            file.write("\nCau hinh khuyen nghi:\n")
            file.write(f"- CPU: {self.cpu[nhom]}\n")
            file.write(f"- RAM: {self.ram[nhom]}\n")
            file.write(f"- SSD: {self.ssd[nhom]}\n")
            file.write(f"- GPU: {self.gpu[nhom]}\n")
            file.write(f"- Man hinh: {self.man_hinh[nhom]}\n")

            file.write("\nCanh bao ngan sach:\n")
            file.write(f"{self.canh_bao_ngan_sach(nhom)}\n")

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
                file.write(f"- {ten_nhom}: {min(score, 100)}%\n")

        return duong_dan_file.replace("\\", "/")

    def in_ket_qua(self):
        scores = self.tinh_diem()

        # Bộ suy diễn chọn nhóm có điểm phù hợp cao nhất
        top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

        nhom = top_3[0][0]
        diem = min(top_3[0][1], 100)

        print("\n================= KET QUA TU VAN =================")
        print(f"Nhom nhu cau cua ban: {nhom}")
        print(f"Muc do phu hop: {diem}%")
        print("\nCau hinh khuyen nghi:")
        print(f"- CPU: {self.cpu[nhom]}")
        print(f"- RAM: {self.ram[nhom]}")
        print(f"- SSD: {self.ssd[nhom]}")
        print(f"- GPU: {self.gpu[nhom]}")
        print(f"- Man hinh: {self.man_hinh[nhom]}")

        print("\n" + self.canh_bao_ngan_sach(nhom))

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
            print(f"- {ten_nhom}: {min(score, 100)}%")

        print("===================================================")
        self.luu_lich_su(nhom, diem)
        print("Da luu ket qua tu van vao file history.csv")
        ten_file = self.xuat_ket_qua_txt(nhom, diem, top_3)
        print(f"Da xuat ket qua tu van ra file: {ten_file}")
        print("Ket thuc tu van.")

    def bat_dau(self):
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
        duong_dan = os.path.join(os.path.dirname(__file__), "data", "sample_cases.json")
        if not os.path.exists(duong_dan):
            print("Khong tim thay file data/sample_cases.json")
            return None

        with open(duong_dan, "r", encoding="utf-8") as file:
            return json.load(file)

    def chay_demo_mau(self):
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
                f"phu hop: {dong.get('muc_do_phu_hop', '')}% | "
                f"ngan sach: {dong.get('ngan_sach', '')}"
            )

    def kiem_thu_he_thong(self):
        test_cases = self.doc_sample_cases()
        if test_cases is None:
            return

        known_cu = self.known.copy()
        so_dung = 0
        so_sai = 0

        print("\n===== KIEM THU HE THONG =====")
        for test_case in test_cases:
            self.known = test_case["input"].copy()
            scores = self.tinh_diem()
            nhom_du_doan = max(scores, key=scores.get)
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

    def menu(self):
        while True:
            print("\n===== MENU HE CHUYEN GIA =====")
            print("1. Tu van thu cong")
            print("2. Chay demo mau")
            print("3. Thoat")
            print("4. Xem lich su tu van")
            print("5. Kiem thu he thong")

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
            else:
                print("Vui long nhap 1, 2, 3, 4 hoac 5.")
