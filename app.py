import json
import os

import pandas as pd
import streamlit as st

from expert_system import HeChuyenGiaTuVanMayTinhAI


st.set_page_config(
    page_title="AI PC Advisor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


GROUP_LABELS = {
    "lap_trinh_co_ban": "Lập trình cơ bản",
    "machine_learning_co_ban": "Machine Learning cơ bản",
    "deep_learning": "Deep Learning",
    "computer_vision": "Computer Vision",
    "ai_game_do_hoa": "AI + Game / Đồ họa",
    "may_mong_nhe_pin_lau": "Máy mỏng nhẹ, pin lâu",
    "ai_tiet_kiem_cloud": "AI tiết kiệm + Cloud",
    "deep_learning_co_ban": "Deep Learning cơ bản",
    "deep_learning_hieu_nang": "Deep Learning hiệu năng",
    "computer_vision_hieu_nang": "Computer Vision hiệu năng",
    "cau_hinh_can_bang": "Cấu hình cân bằng",
}

BUDGET_LABELS = {
    "thap": "Thấp",
    "trung_binh": "Trung bình",
    "cao": "Cao",
}


def pretty_group(name):
    mapping = {
        "lap_trinh_co_ban": "Lập trình cơ bản",
        "machine_learning_co_ban": "Machine Learning cơ bản",
        "deep_learning": "Deep Learning",
        "computer_vision": "Computer Vision",
        "ai_game_do_hoa": "AI + Game / Đồ họa",
        "may_mong_nhe_pin_lau": "Máy mỏng nhẹ, pin lâu",
        "ai_tiet_kiem_cloud": "AI tiết kiệm + Cloud",
        "deep_learning_co_ban": "Deep Learning cơ bản",
        "deep_learning_hieu_nang": "Deep Learning hiệu năng",
        "computer_vision_hieu_nang": "Computer Vision hiệu năng",
        "cau_hinh_can_bang": "Cấu hình cân bằng",
    }
    return mapping.get(name, name)


def format_config_text(text):
    replacements = {
        "Toi thieu": "Tối thiểu",
        "khuyen nghi": "khuyến nghị",
        "Khong bat buoc": "Không bắt buộc",
        "khong bat buoc": "không bắt buộc",
        "Nen co": "Nên có",
        "Can": "Cần",
        "GPU roi": "GPU rời",
        "hoac": "hoặc",
        "tro len": "trở lên",
        "hieu nang": "hiệu năng",
        "uu tien": "ưu tiên",
        "dong": "dòng",
        "tiet kiem dien": "tiết kiệm điện",
        "trong luong": "trọng lượng",
        "mau sac": "màu sắc",
        "tan so quet": "tần số quét",
        "neu co dieu kien": "nếu có điều kiện",
        "neu can": "nếu cần",
        "lam viec": "làm việc",
        "lau": "lâu",
        "tuy": "tùy",
        "ngan sach": "ngân sách",
        "Toi": "Tối",
        "manh": "mạnh",
        "lon": "lớn",
        "xu ly": "xử lý",
        "anh": "ảnh",
        "mo hinh": "mô hình",
        "chat luong": "chất lượng",
        "hien thi": "hiển thị",
        " va ": " và ",
        " de ": " để ",
        "tot": "tốt",
        "may": "máy",
    }
    text = str(text)
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def format_explanation_text(nhom, text):
    explanations = {
        "lap_trinh_co_ban": "Bạn chủ yếu học lập trình cơ bản, không yêu cầu huấn luyện mô hình AI nặng, nên cấu hình vừa phải là phù hợp.",
        "machine_learning_co_ban": "Bạn có học Machine Learning, cần CPU tốt và RAM đủ lớn để xử lý dữ liệu, chạy Python và các mô hình ML cơ bản.",
        "deep_learning": "Bạn có học Deep Learning, nên hệ thống ưu tiên CPU mạnh, RAM lớn và GPU rời để hỗ trợ huấn luyện mô hình.",
        "computer_vision": "Bạn có xử lý ảnh/video hoặc Computer Vision, nên cần GPU rời, RAM lớn và màn hình có chất lượng hiển thị tốt.",
        "ai_game_do_hoa": "Bạn vừa học AI vừa có nhu cầu game/đồ họa, nên cần GPU rời và tản nhiệt tốt để đảm bảo hiệu năng.",
        "may_mong_nhe_pin_lau": "Bạn ưu tiên di chuyển, máy nhẹ và pin lâu, nên hệ thống ưu tiên CPU tiết kiệm điện và thiết kế mỏng nhẹ.",
        "ai_tiet_kiem_cloud": "Người dùng có nhu cầu học AI/Deep Learning/Computer Vision nhưng ngân sách thấp chưa phù hợp để mua laptop GPU mạnh. Hệ thống đề xuất cấu hình vừa đủ để học lập trình, xử lý dữ liệu và chạy mô hình nhỏ; với mô hình nặng nên dùng Google Colab, Kaggle Notebook hoặc máy phòng lab.",
        "cau_hinh_can_bang": "Nhu cầu của bạn ở mức tổng hợp, nên hệ thống đề xuất cấu hình cân bằng giữa hiệu năng, chi phí và tính di động.",
    }
    return explanations.get(nhom, format_config_text(text))


def pretty_reasoning_traces(he):
    k = he.known
    traces = []

    if k.get("hoc_lap_trinh"):
        traces.append("Người dùng học lập trình -> tăng điểm cho nhóm lập trình cơ bản, Machine Learning cơ bản, Deep Learning và cấu hình cân bằng.")
    if k.get("hoc_machine_learning"):
        traces.append("Người dùng học Machine Learning -> tăng điểm cho nhóm Machine Learning cơ bản, Deep Learning, Computer Vision và AI kết hợp đồ họa.")
    if k.get("hoc_deep_learning"):
        traces.append("Người dùng học Deep Learning -> tăng điểm mạnh cho nhóm Deep Learning, Computer Vision và AI kết hợp đồ họa.")
    if k.get("xu_ly_anh_video"):
        traces.append("Người dùng xử lý ảnh/video -> tăng điểm mạnh cho nhóm Computer Vision.")
    if k.get("choi_game_do_hoa"):
        traces.append("Người dùng chơi game hoặc làm đồ họa -> tăng điểm mạnh cho nhóm AI kết hợp game/đồ họa.")
    if k.get("can_may_nhe_pin_lau"):
        traces.append("Người dùng cần máy nhẹ, pin lâu -> tăng điểm cho nhóm máy mỏng nhẹ và cấu hình cân bằng.")
    if k.get("can_nang_cap"):
        traces.append("Người dùng cần nâng cấp RAM/SSD -> tăng điểm cho nhóm cấu hình cân bằng.")

    ngan_sach = k.get("ngan_sach")
    if ngan_sach == "thap":
        traces.append("Ngân sách thấp -> ưu tiên nhóm lập trình cơ bản và cấu hình tiết kiệm.")
        if k.get("hoc_deep_learning") or k.get("xu_ly_anh_video") or k.get("choi_game_do_hoa"):
            traces.append("Ngân sách thấp nhưng có nhu cầu cấu hình cao -> chuyển hướng sang nhóm AI tiết kiệm + Cloud.")
    elif ngan_sach == "trung_binh":
        traces.append("Ngân sách trung bình -> tăng điểm cho nhóm Machine Learning cơ bản, máy mỏng nhẹ và cấu hình cân bằng.")
    elif ngan_sach == "cao":
        traces.append("Ngân sách cao -> tăng điểm cho nhóm Deep Learning, Computer Vision và AI kết hợp đồ họa.")

    return traces


def pretty_demo_name(name):
    mapping = {
        "Lap trinh co ban": "Lập trình cơ bản",
        "Machine Learning co ban": "Machine Learning cơ bản",
        "Deep Learning": "Deep Learning",
        "Computer Vision": "Computer Vision",
        "May mong nhe pin lau": "Máy mỏng nhẹ, pin lâu",
        "AI tiet kiem + Cloud": "AI tiết kiệm + Cloud",
        "AI tiết kiệm + Cloud": "AI tiết kiệm + Cloud",
    }
    return mapping.get(name, name)


def load_sample_cases():
    path = os.path.join(os.path.dirname(__file__), "data", "sample_cases.json")
    if not os.path.exists(path):
        return [], "Không tìm thấy file data/sample_cases.json"

    try:
        with open(path, "r", encoding="utf-8") as file:
            cases = json.load(file)
    except Exception:
        return [], "Không đọc được dữ liệu demo mẫu"

    if not isinstance(cases, list):
        return [], "Không đọc được dữ liệu demo mẫu"

    return cases, ""


def inject_css():
    st.markdown(
        """
        <style>
        :root {
            --primary: #2563eb;
            --primary-light: #dbeafe;
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #0f172a;
            --muted: #64748b;
            --border: #e2e8f0;
        }

        html, body, [data-testid="stAppViewContainer"] {
            background: var(--bg);
            color: var(--text);
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        [data-testid="stHeader"] {
            display: none;
        }

        .block-container {
            padding: 2.4rem 1.15rem 1.25rem 1.15rem;
            max-width: 1350px;
            margin-left: auto;
            margin-right: auto;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e2e8f0;
            box-shadow: 8px 0 30px rgba(15, 23, 42, 0.04);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 1.35rem 1.2rem;
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span {
            color: var(--text);
            font-size: 0.98rem;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
            font-size: 1.1rem;
            margin-bottom: 1.1rem;
            color: var(--text);
            font-weight: 800;
        }

        [data-testid="stCheckbox"] {
            margin-bottom: 0.45rem;
        }

        [data-testid="stCheckbox"] label {
            gap: 0.6rem;
        }

        [data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p {
            font-size: 0.98rem;
            line-height: 1.2;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            height: 46px;
            border-radius: 14px !important;
            border: 1px solid #e2e8f0 !important;
            background: #ffffff !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            text-align: left !important;
            justify-content: flex-start;
            padding-left: 14px !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
            margin-bottom: 8px;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #eff6ff !important;
            border-color: #93c5fd !important;
            color: #2563eb !important;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: #2563eb !important;
            border-color: #2563eb !important;
            color: #ffffff !important;
            box-shadow: 0 10px 22px rgba(37, 99, 235, 0.22) !important;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] p,
        [data-testid="stSidebar"] .stButton > button[kind="primary"] span {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stButton > button:not([kind="primary"]) p,
        [data-testid="stSidebar"] .stButton > button:not([kind="primary"]) span {
            color: #0f172a !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover p,
        [data-testid="stSidebar"] .stButton > button:hover span {
            color: #2563eb !important;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover p,
        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover span {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] .stSelectbox > div > div {
            border-radius: 0.7rem;
            border-color: var(--border);
            min-height: 3rem;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.03);
        }

        .main-title {
            font-size: 3rem;
            line-height: 1.05;
            font-weight: 900;
            color: var(--text);
            letter-spacing: 0;
            margin: 0;
        }

        .sub-title {
            color: var(--muted);
            font-size: 1.04rem;
            margin-top: 0.55rem;
        }

        .header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.45rem;
        }

        .robot-badge {
            width: 4.25rem;
            height: 4.25rem;
            border-radius: 999px;
            background: var(--primary-light);
            border: 1px solid #bfdbfe;
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.15rem;
            box-shadow: 0 14px 34px rgba(37, 99, 235, 0.13);
            flex: 0 0 auto;
        }

        .header-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 22px 26px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        }

        .sidebar-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 8px 20px 8px;
            border-bottom: 1px solid #e2e8f0;
            margin-bottom: 18px;
        }

        .logo-icon {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            background: #dbeafe;
            color: #2563eb;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
        }

        .logo-title {
            font-size: 18px;
            font-weight: 900;
            color: #0f172a;
            line-height: 1.15;
        }

        .logo-subtitle {
            font-size: 12px;
            color: #64748b;
            margin-top: 2px;
        }

        .sidebar-section-title {
            color: #64748b;
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            margin: 12px 0 8px 0;
        }

        .active-mode-card {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 14px;
            padding: 12px 14px;
            color: #1d4ed8;
            font-weight: 700;
            margin-top: 16px;
        }

        .result-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 1.15rem;
            padding: 1.45rem 1.55rem 1.25rem 1.55rem;
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
            margin-bottom: 1.25rem;
        }

        .result-title {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            color: var(--text);
            font-size: 1.45rem;
            font-weight: 850;
            margin-bottom: 1.25rem;
        }

        .result-line {
            display: flex;
            align-items: center;
            gap: 0.9rem;
            font-size: 1.16rem;
            margin-bottom: 1.05rem;
        }

        .result-group {
            color: var(--primary);
            font-size: 1.34rem;
            font-weight: 900;
        }

        .result-progress-row {
            display: grid;
            grid-template-columns: 10rem 1fr 8rem;
            gap: 1rem;
            align-items: center;
        }

        .score-badge {
            text-align: center;
            padding: 0.65rem 0.5rem;
            border: 1px solid var(--border);
            border-radius: 0.6rem;
            color: var(--primary);
            background: #f8fbff;
            font-size: 1.75rem;
            font-weight: 900;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1.35rem 1.3rem;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.07);
            height: 100%;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 1rem !important;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.07) !important;
            padding: 1.15rem 1.2rem !important;
        }

        .metric-box {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1.45rem 1.15rem 1.35rem 1.15rem;
            min-height: 11.25rem;
            text-align: center;
            box-shadow: 0 10px 22px rgba(15, 23, 42, 0.07);
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
        }

        .metric-icon {
            width: 3.15rem;
            height: 3.15rem;
            border-radius: 0.85rem;
            background: var(--primary-light);
            color: var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            margin-bottom: 0.75rem;
            border: 1px solid #bfdbfe;
        }

        .metric-title {
            font-size: 1.03rem;
            font-weight: 850;
            color: var(--text);
            margin-bottom: 0.55rem;
        }

        .metric-text {
            color: var(--text);
            font-size: 0.96rem;
            line-height: 1.46;
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            font-weight: 850;
            color: var(--text);
            font-size: 1.15rem;
            margin-bottom: 1rem;
        }

        .rank-row {
            display: grid;
            grid-template-columns: 2rem 1fr 36% 3.2rem;
            gap: 0.75rem;
            align-items: center;
            margin: 0.75rem 0;
        }

        .rank-num {
            width: 1.75rem;
            height: 1.75rem;
            border-radius: 999px;
            background: var(--primary);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 0.86rem;
        }

        .progress-bg {
            height: 0.58rem;
            background: #e8eef7;
            border-radius: 999px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #2563eb, #60a5fa);
            border-radius: 999px;
        }

        .percent {
            color: var(--text);
            font-weight: 850;
            text-align: right;
        }

        .explain-text {
            color: var(--text);
            font-size: 1rem;
            line-height: 1.65;
        }

        .trace-list {
            margin: 0;
            padding-left: 1rem;
        }

        .trace-list li {
            margin-bottom: 0.72rem;
            color: var(--text);
            line-height: 1.45;
        }

        .trace-list li::marker {
            color: var(--primary);
        }

        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            color: #0f172a !important;
        }

        div[data-baseweb="select"] span {
            color: #0f172a !important;
        }

        div[data-baseweb="popover"] {
            background-color: #ffffff !important;
        }

        ul[role="listbox"] {
            background-color: #ffffff !important;
        }

        li[role="option"] {
            color: #0f172a !important;
            background-color: #ffffff !important;
        }

        li[role="option"]:hover {
            background-color: #dbeafe !important;
        }

        .notice {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1e3a8a;
            padding: 0.95rem 1rem;
            border-radius: 0.9rem;
            margin-bottom: 1rem;
            font-weight: 650;
        }

        .warning-list {
            margin: 0.45rem 0 0 1.15rem;
            padding: 0;
        }

        .warning-list li {
            margin: 0.2rem 0;
        }

        .small-alert {
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 14px;
            margin-top: 12px;
        }

        .stCheckbox label,
        .stRadio label,
        .stSelectbox label,
        .stTextInput label,
        .stNumberInput label,
        [data-testid="stWidgetLabel"],
        [data-testid="stMarkdownContainer"],
        label,
        p,
        span {
            color: #0f172a !important;
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] p {
            color: #0f172a !important;
        }

        .stButton > button {
            border-radius: 12px !important;
            font-weight: 700 !important;
            padding: 0.65rem 1.1rem !important;
        }

        button[kind="primary"],
        .main .stButton button {
            background-color: #2563eb !important;
            border: 1px solid #2563eb !important;
            color: #ffffff !important;
        }

        button[kind="primary"] p,
        button[kind="primary"] span,
        .main .stButton button p,
        .main .stButton button span {
            color: #ffffff !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 12px !important;
            color: #0f172a !important;
        }

        div[data-baseweb="select"] span {
            color: #0f172a !important;
        }

        .page-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            margin-bottom: 20px;
        }

        .page-card .section-title {
            font-size: 22px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 10px;
        }

        .section-desc {
            color: #475569;
            font-size: 15px;
            margin-bottom: 16px;
            line-height: 1.55;
        }

        .test-pass {
            background: #ecfdf5;
            color: #166534;
            border: 1px solid #bbf7d0;
            border-radius: 12px;
            padding: 10px 14px;
            margin: 8px 0;
            font-weight: 700;
        }

        .test-fail {
            background: #fef2f2;
            color: #991b1b;
            border: 1px solid #fecaca;
            border-radius: 12px;
            padding: 10px 14px;
            margin: 8px 0;
            font-weight: 700;
        }

        .condition-ok {
            background: #ecfdf5;
            color: #166534;
            border: 1px solid #bbf7d0;
            border-radius: 12px;
            padding: 12px 14px;
            margin: 8px 0;
        }

        .condition-bad {
            background: #fef2f2;
            color: #991b1b;
            border: 1px solid #fecaca;
            border-radius: 12px;
            padding: 12px 14px;
            margin: 8px 0;
        }

        .summary-box {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
        }

        .summary-value {
            color: #2563eb;
            font-size: 28px;
            font-weight: 900;
            line-height: 1;
        }

        .summary-label {
            color: #475569;
            font-size: 14px;
            font-weight: 700;
            margin-top: 8px;
        }

        .result-group {
            color: #2563eb !important;
        }

        .robot-badge,
        .metric-icon {
            color: #2563eb !important;
        }

        .footer {
            text-align: center;
            color: var(--muted);
            border-top: 1px solid var(--border);
            margin-top: 1.3rem;
            padding: 1rem 0 0.25rem 0;
            font-size: 0.92rem;
        }

        .main .block-container {
            max-width: 1280px !important;
            padding-top: 2rem !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
            min-height: 90vh;
        }

        @media (min-width: 1400px) {
            .main .block-container {
                max-width: 1400px !important;
            }
        }

        .page-card,
        .card,
        .result-card {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 22px !important;
            padding: 30px 34px !important;
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08) !important;
            margin-bottom: 24px !important;
        }

        .header-card {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 24px !important;
            padding: 34px 38px !important;
            box-shadow: 0 14px 36px rgba(15, 23, 42, 0.08) !important;
            margin-bottom: 24px !important;
        }

        .header-row {
            margin-bottom: 0 !important;
        }

        .main-title {
            font-size: 44px !important;
            font-weight: 900 !important;
            color: #0f172a !important;
            margin: 0 !important;
        }

        .sub-title {
            font-size: 17px !important;
            color: #64748b !important;
            margin-top: 10px !important;
        }

        .robot-badge {
            width: 74px !important;
            height: 74px !important;
            border-radius: 999px !important;
            background: #dbeafe !important;
            color: #2563eb !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-size: 30px !important;
            box-shadow: 0 16px 36px rgba(37, 99, 235, 0.18) !important;
        }

        .stCheckbox label p,
        .stCheckbox label,
        [data-testid="stWidgetLabel"] p {
            font-size: 16px !important;
            color: #0f172a !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="select"] {
            font-size: 16px !important;
        }

        .main .stButton > button {
            height: 52px !important;
            border-radius: 16px !important;
            font-size: 16px !important;
            font-weight: 800 !important;
            padding: 0 22px !important;
            background: #2563eb !important;
            color: #ffffff !important;
            border: 1px solid #2563eb !important;
            box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24) !important;
        }

        .main .stButton > button:hover {
            background: #1d4ed8 !important;
            border-color: #1d4ed8 !important;
        }

        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 320px !important;
            background: #ffffff !important;
            border-right: 1px solid #e2e8f0 !important;
        }

        [data-testid="stSidebar"] .stButton > button {
            height: 50px !important;
            border-radius: 14px !important;
            font-size: 15px !important;
        }

        .metric-box {
            min-height: 190px !important;
            padding: 24px 20px !important;
            border-radius: 20px !important;
        }

        .metric-icon {
            font-size: 38px !important;
        }

        .metric-title {
            font-size: 18px !important;
        }

        .metric-text {
            font-size: 15px !important;
            line-height: 1.55 !important;
        }

        .mini-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 22px 24px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
            min-height: 120px;
        }

        .mini-card-title {
            color: #0f172a;
            font-size: 17px;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .mini-card-text {
            color: #64748b;
            font-size: 15px;
            line-height: 1.5;
        }

        .footer {
            margin-top: 32px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def html_escape(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def create_expert(known):
    he = HeChuyenGiaTuVanMayTinhAI()
    he.known = known.copy()
    return he


def infer_result(known, save_outputs=False):
    he = create_expert(known)
    scores = he.tinh_diem()
    top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
    nhom = he.suy_dien_nhom_chinh()
    diem = he.tinh_muc_do_chac_chan(scores, nhom)
    conflicts = he.phat_hien_xung_dot()
    txt_path = None

    if save_outputs:
        he.luu_lich_su(nhom, diem)
        txt_path = he.xuat_ket_qua_txt(nhom, diem, top_3)

    return {
        "he": he,
        "scores": scores,
        "top_3": top_3,
        "nhom": nhom,
        "diem": diem,
        "conflicts": conflicts,
        "txt_path": txt_path,
    }


def read_history(limit=5):
    if not os.path.exists("history.csv") or os.path.getsize("history.csv") == 0:
        return pd.DataFrame()

    try:
        df = pd.read_csv("history.csv")
    except Exception:
        return pd.DataFrame()

    columns = ["time", "nhom_ket_luan", "muc_do_phu_hop"]
    existing = [col for col in columns if col in df.columns]
    return df.tail(limit)[existing] if existing else pd.DataFrame()


def render_history_table(limit=5):
    if not os.path.exists("history.csv") or os.path.getsize("history.csv") == 0:
        st.info("Chưa có lịch sử tư vấn.")
        return

    try:
        df = pd.read_csv("history.csv")
    except Exception:
        st.warning("Không đọc được file history.csv.")
        return

    if df.empty:
        st.info("Chưa có lịch sử tư vấn.")
        return

    required_columns = ["time", "nhom_ket_luan", "muc_do_phu_hop"]
    if not all(column in df.columns for column in required_columns):
        st.warning("File history.csv thiếu cột dữ liệu cần thiết.")
        return

    df = df.tail(limit).copy()
    df["nhom_ket_luan"] = df["nhom_ket_luan"].apply(lambda group: pretty_group(str(group)))
    df["muc_do_phu_hop"] = (
        df["muc_do_phu_hop"]
        .astype(str)
        .str.replace("%", "", regex=False)
        + "%"
    )

    header_cols = st.columns([1.4, 1.4, 1])
    header_cols[0].markdown("**Thời gian**")
    header_cols[1].markdown("**Nhóm phù hợp nhất**")
    header_cols[2].markdown("**Độ tin cậy tư vấn**")

    st.divider()

    for _, row in df.iterrows():
        cols = st.columns([1.4, 1.4, 1])
        cols[0].write(row.get("time", ""))
        cols[1].markdown(f"**:blue[{row.get('nhom_ket_luan', '')}]**")
        cols[2].markdown(f"✅ **{row.get('muc_do_phu_hop', '')}**")


def run_system_tests():
    he = HeChuyenGiaTuVanMayTinhAI()
    cases = he.doc_sample_cases()
    if cases is None:
        return ["Khong tim thay file data/sample_cases.json"], 0, 0

    lines = []
    passed = 0
    failed = 0
    for case in cases:
        he.known = case["input"].copy()
        he.tinh_diem()
        predicted = he.suy_dien_nhom_chinh()
        expected = case["expected_group"]
        if predicted == expected:
            passed += 1
            lines.append(f"PASS: {case['name']} -> {pretty_group(predicted)}")
        else:
            failed += 1
            lines.append(
                f"FAIL: {case['name']} | Expected: {pretty_group(expected)} | Got: {pretty_group(predicted)}"
            )

    return lines, passed, failed


def render_header():
    st.markdown(
        """
        <div class="header-card">
            <div class="header-row">
                <div>
                    <h1 class="main-title">AI PC Advisor</h1>
                    <div class="sub-title">Hệ chuyên gia tư vấn cấu hình máy tính cho sinh viên AI</div>
                </div>
                <div class="robot-badge">🤖</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(result):
    nhom = result["nhom"]
    diem = result["diem"]
    he = result["he"]
    conflicts = result.get("conflicts", [])
    group_name = pretty_group(nhom)
    warning_blocks = []
    if nhom == "ai_tiet_kiem_cloud":
        warning_blocks.append(
            f'<div class="notice">{html_escape(he.canh_bao_ngan_sach(nhom))}</div>'
        )
    if conflicts:
        conflict_items = "".join(
            f"<li>{html_escape(conflict)}</li>"
            for conflict in conflicts
        )
        warning_blocks.append(
            f'<div class="notice"><b>Cảnh báo:</b><ul class="warning-list">{conflict_items}</ul></div>'
        )
    warning_html = "".join(warning_blocks)
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">🏆 <span>Kết quả tư vấn</span></div>
            <div class="result-line">
                <span>Nhóm nhu cầu phù hợp nhất:</span>
                <span class="result-group">{html_escape(group_name)}</span>
            </div>
            <div class="result-progress-row">
                <div>Độ tin cậy tư vấn:</div>
                <div class="progress-bg"><div class="progress-fill" style="width:{diem}%;"></div></div>
                <div class="score-badge">{diem}%</div>
            </div>
            {warning_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(result):
    he = result["he"]
    nhom = result["nhom"]
    metrics = [
        ("▣", "CPU", format_config_text(he.cpu[nhom])),
        ("▤", "RAM", format_config_text(he.ram[nhom])),
        ("▥", "SSD", format_config_text(he.ssd[nhom])),
        ("▦", "GPU", format_config_text(he.gpu[nhom])),
        ("▭", "Màn hình", format_config_text(he.man_hinh[nhom])),
    ]

    st.markdown('<div class="section-title">Cấu hình khuyến nghị</div>', unsafe_allow_html=True)
    cols = st.columns(5, gap="small")
    for col, (icon, title, text) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-icon">{icon}</div>
                    <div class="metric-title">{html_escape(title)}</div>
                    <div class="metric-text">{html_escape(text)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_top3_and_explanation(result):
    he = result["he"]
    top_3 = result["top_3"]
    nhom = result["nhom"]
    left, right = st.columns([1, 1], gap="large")

    rows = []
    for index, (group_id, score) in enumerate(top_3, start=1):
        percent = max(0, min(score, 100))
        rows.append(
            f"""
            <div class="rank-row">
                <div class="rank-num">{index}</div>
                <div>{html_escape(pretty_group(group_id))}</div>
                <div class="progress-bg"><div class="progress-fill" style="width:{percent}%;"></div></div>
                <div class="percent">{percent}%</div>
            </div>
            """
        )

    with left:
        st.markdown(
            f"""
            <div class="card">
                <div class="section-title">Top 3 nhóm nhu cầu phù hợp</div>
                {''.join(rows)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="card">
                <div class="section-title">💡 Giải thích kết quả</div>
                <div class="explain-text">{html_escape(format_explanation_text(nhom, he.giai_thich(nhom)))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_trace_and_history(result):
    he = result["he"]
    left, right = st.columns([1, 1], gap="large")

    traces = "".join(
        f"<li>{html_escape(line)}</li>"
        for line in pretty_reasoning_traces(he)
    )

    with left:
        st.markdown(
            f"""
            <div class="card">
                <div class="section-title">🔗 Dấu vết suy luận</div>
                <ul class="trace-list">{traces}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        with st.container(border=True):
            st.markdown('<div class="section-title">🕘 Lịch sử gần đây</div>', unsafe_allow_html=True)
            render_history_table()


def render_history_page():
    with st.container(border=True):
        st.markdown('<div class="section-title">🕘 Lịch sử tư vấn</div>', unsafe_allow_html=True)
        render_history_table(limit=100)


def render_test_page():
    he = HeChuyenGiaTuVanMayTinhAI()
    ket_qua = he.kiem_thu_he_thong_data()
    st.markdown(
        """
        <div class="page-card">
            <div class="section-title">🛡️ Kiểm thử hệ thống</div>
            <div class="section-desc">
                Tự động chạy các test case trong data/sample_cases.json để kiểm tra bộ suy diễn.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_total, col_passed, col_failed = st.columns(3, gap="large")
    summary_items = [
        (col_total, "Tổng số test", ket_qua["total"]),
        (col_passed, "Đúng", ket_qua["passed"]),
        (col_failed, "Sai", ket_qua["failed"]),
    ]
    for col, label, value in summary_items:
        with col:
            st.markdown(
                f"""
                <div class="summary-box">
                    <div class="summary-value">{value}</div>
                    <div class="summary-label">{html_escape(label)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    for detail in ket_qua["details"]:
        class_name = "test-pass" if detail["passed"] else "test-fail"
        status = "PASS" if detail["passed"] else "FAIL"
        st.markdown(
            f"""
            <div class="{class_name}">
                {status}: {html_escape(detail["name"])} |
                Expected: {html_escape(pretty_group(detail["expected"]))} |
                Got: {html_escape(pretty_group(detail["got"]))}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_dashboard(result):
    render_result_card(result)
    render_metric_cards(result)
    st.write("")
    render_top3_and_explanation(result)
    st.write("")
    render_trace_and_history(result)
    if st.session_state.get("export_message"):
        st.markdown(
            f"<div class='small-alert'>✅ {html_escape(st.session_state.export_message)}</div>",
            unsafe_allow_html=True,
        )
        if st.session_state.get("export_path"):
            with st.expander("Xem đường dẫn file xuất"):
                st.text_input("Đường dẫn", value=st.session_state.export_path, disabled=True)


def budget_label_to_value(label):
    mapping = {"Thấp": "thap", "Trung bình": "trung_binh", "Cao": "cao"}
    return mapping.get(label, "thap")


def budget_index(value):
    values = ["thap", "trung_binh", "cao"]
    return values.index(value) if value in values else 0


def render_input_form(prefix, defaults=None):
    defaults = defaults or {}
    left, right = st.columns(2, gap="large")

    with left:
        hoc_lap_trinh = st.checkbox(
            "Học lập trình",
            value=defaults.get("hoc_lap_trinh", True),
            key=f"{prefix}_hoc_lap_trinh",
        )
        hoc_ml = st.checkbox(
            "Machine Learning",
            value=defaults.get("hoc_machine_learning", False),
            key=f"{prefix}_hoc_ml",
        )
        hoc_dl = st.checkbox(
            "Deep Learning",
            value=defaults.get("hoc_deep_learning", False),
            key=f"{prefix}_hoc_dl",
        )
        xu_ly_anh = st.checkbox(
            "Xử lý ảnh / Computer Vision",
            value=defaults.get("xu_ly_anh_video", False),
            key=f"{prefix}_xu_ly_anh",
        )

    with right:
        game_do_hoa = st.checkbox(
            "Game / Đồ họa",
            value=defaults.get("choi_game_do_hoa", False),
            key=f"{prefix}_game_do_hoa",
        )
        may_nhe = st.checkbox(
            "Máy nhẹ, pin lâu",
            value=defaults.get("can_may_nhe_pin_lau", False),
            key=f"{prefix}_may_nhe",
        )
        can_nang_cap = st.checkbox(
            "Cần nâng cấp RAM/SSD",
            value=defaults.get("can_nang_cap", True),
            key=f"{prefix}_can_nang_cap",
        )
        ngan_sach_label = st.selectbox(
            "Ngân sách",
            ["Thấp", "Trung bình", "Cao"],
            index=budget_index(defaults.get("ngan_sach", "thap")),
            key=f"{prefix}_ngan_sach_label",
        )

    return {
        "hoc_lap_trinh": hoc_lap_trinh,
        "hoc_machine_learning": hoc_ml,
        "hoc_deep_learning": hoc_dl,
        "xu_ly_anh_video": xu_ly_anh,
        "choi_game_do_hoa": game_do_hoa,
        "can_may_nhe_pin_lau": may_nhe,
        "can_nang_cap": can_nang_cap,
        "ngan_sach": budget_label_to_value(ngan_sach_label),
    }


def render_consultation_page():
    st.markdown(
        """
        <div class="page-card">
            <div class="section-title">⚡ Tư vấn cấu hình</div>
            <div class="section-desc">
                Nhập nhu cầu học tập và ngân sách, hệ chuyên gia sẽ suy diễn nhóm nhu cầu phù hợp và đề xuất cấu hình.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="section-title">Thông tin đầu vào</div>', unsafe_allow_html=True)
        known = render_input_form("consultation")

        if st.button("⚡ Tư vấn cấu hình", type="primary", key="consultation_submit"):
            st.session_state.consultation_result = infer_result(known, save_outputs=True)
            st.session_state.export_message = "Đã xuất kết quả tư vấn"
            st.session_state.export_path = st.session_state.consultation_result["txt_path"] or ""
            st.toast("Đã xuất kết quả tư vấn", icon="✅")

    if st.session_state.get("consultation_result"):
        st.write("")
        render_dashboard(st.session_state.consultation_result)
    else:
        st.write("")
        cols = st.columns(3, gap="large")
        guide_cards = [
            ("1. Nhập dữ liệu", "Chọn nhu cầu học tập, tác vụ AI và mức ngân sách hiện tại."),
            ("2. Hệ thống suy diễn", "Bộ luật và điểm phù hợp sẽ được tính để chọn nhóm nhu cầu chính."),
            ("3. Nhận cấu hình", "Xem CPU, RAM, SSD, GPU, màn hình và giải thích kết luận."),
        ]
        for col, (title, text) in zip(cols, guide_cards):
            with col:
                st.markdown(
                    f"""
                    <div class="mini-card">
                        <div class="mini-card-title">{html_escape(title)}</div>
                        <div class="mini-card-text">{html_escape(text)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_demo_page():
    st.markdown(
        """
        <div class="page-card">
            <div class="section-title">📦 Chạy demo mẫu</div>
            <div class="section-desc">Chọn một bộ dữ liệu mẫu từ data/sample_cases.json để chạy thử hệ chuyên gia.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    demo_cases, demo_error = load_sample_cases()
    if demo_error:
        st.error(demo_error)
        return
    if not demo_cases:
        st.warning("Không đọc được dữ liệu demo mẫu")
        return

    demo_names = [
        case.get("name", f"Demo {index}")
        for index, case in enumerate(demo_cases, start=1)
    ]
    selected_demo_name = st.selectbox(
        "Chọn demo mẫu",
        demo_names,
        key="demo_page_case",
        format_func=pretty_demo_name,
    )

    if st.button("📦 Chạy demo", type="primary", key="demo_page_submit"):
        selected_case = next(
            (case for case in demo_cases if case.get("name") == selected_demo_name),
            None,
        )
        if selected_case is None:
            st.error("Không đọc được dữ liệu demo mẫu")
        else:
            st.session_state.demo_result = infer_result(selected_case["input"], save_outputs=True)
            st.session_state.export_message = "Đã xuất kết quả tư vấn"
            st.session_state.export_path = st.session_state.demo_result["txt_path"] or ""
            st.toast(f"Đã chạy demo: {pretty_demo_name(selected_demo_name)}", icon="✅")

    if st.session_state.get("demo_result"):
        st.write("")
        render_dashboard(st.session_state.demo_result)


def render_backward_chaining_page():
    st.markdown(
        """
        <div class="page-card">
            <div class="section-title">🔎 Kiểm tra suy diễn lùi</div>
            <div class="section-desc">
                Chọn một giả thuyết kết luận, hệ thống sẽ kiểm tra ngược lại các điều kiện cần.
            </div>
            <div class="section-desc">
                Suy diễn lùi bắt đầu từ một giả thuyết kết luận, sau đó hệ thống kiểm tra ngược lại các điều kiện cần để xem giả thuyết đó có phù hợp với dữ liệu hiện tại hay không.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<div class="section-title">Dữ kiện kiểm tra</div>', unsafe_allow_html=True)
        known = render_input_form("backward")
        he = HeChuyenGiaTuVanMayTinhAI()
        he.known = known

        gia_thuyet = st.selectbox(
            "Chọn giả thuyết cần kiểm tra",
            he.danh_sach_gia_thuyet(),
            format_func=pretty_group,
            key="gia_thuyet_suy_dien_lui",
        )

        kiem_tra = st.button("🔎 Kiểm tra giả thuyết", type="primary", key="kiem_tra_gia_thuyet_btn")

    if kiem_tra:
        ket_qua = he.kiem_tra_gia_thuyet(gia_thuyet)
        ten_gia_thuyet = pretty_group(ket_qua["gia_thuyet"])
        trang_thai = (
            f"✅ Kết luận: Giả thuyết '{ten_gia_thuyet}' phù hợp với dữ liệu hiện tại."
            if ket_qua["phu_hop"]
            else f"❌ Kết luận: Giả thuyết '{ten_gia_thuyet}' chưa phù hợp với dữ liệu hiện tại."
        )
        cach_suy_luan = (
            f"Hệ thống giả định trước kết luận là '{ten_gia_thuyet}', sau đó kiểm tra các điều kiện cần. Vì tất cả điều kiện đều đạt nên giả thuyết được chấp nhận."
            if ket_qua["phu_hop"]
            else f"Hệ thống giả định trước kết luận là '{ten_gia_thuyet}', nhưng một số điều kiện chưa đạt nên giả thuyết bị bác bỏ."
        )

        st.markdown(
            f"""
            <div class="page-card">
                <div class="section-title">Kết quả kiểm tra giả thuyết</div>
                <div class="section-desc"><b>Giả thuyết:</b> {html_escape(ten_gia_thuyet)}</div>
                <div class="section-desc">{html_escape(trang_thai)}</div>
                <div class="section-title" style="font-size: 18px; margin-top: 10px;">Các điều kiện hệ thống kiểm tra</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for dieu_kien in ket_qua["dieu_kien"]:
            dat = dieu_kien.get("dat", False)
            dieu_kien_can = dieu_kien.get("dieu_kien_can", dieu_kien.get("mo_ta", ""))
            du_lieu_hien_tai = dieu_kien.get("du_lieu_hien_tai", "")
            css_class = "condition-ok" if dat else "condition-bad"
            icon = "✅" if dat else "❌"
            condition_html = f"""
            <div class="{css_class}">
                <div><b>{icon} Điều kiện cần:</b> {html_escape(dieu_kien_can)}</div>
                <div style="margin-top: 4px; font-weight: 600;">{html_escape(du_lieu_hien_tai)}</div>
            </div>
            """
            st.markdown(condition_html, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="page-card">
                <div class="section-title" style="font-size: 18px; margin-bottom: 8px;">Cách hệ thống suy luận</div>
                <div class="section-desc">{html_escape(cach_suy_luan)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def initialize_state():
    if "mode" not in st.session_state:
        st.session_state.mode = "Tư vấn cấu hình"
    if "export_message" not in st.session_state:
        st.session_state.export_message = ""
    if "export_path" not in st.session_state:
        st.session_state.export_path = ""
    if "consultation_result" not in st.session_state:
        st.session_state.consultation_result = None
    if "demo_result" not in st.session_state:
        st.session_state.demo_result = None


def sidebar_button(label, icon, mode_name):
    active = st.session_state.mode == mode_name
    if st.sidebar.button(
        f"{icon}  {label}",
        key=f"nav_{mode_name}",
        type="primary" if active else "secondary",
        use_container_width=True,
    ):
        st.session_state.mode = mode_name


def render_sidebar():
    st.sidebar.markdown(
        """
        <div class="sidebar-logo">
            <div class="logo-icon">🤖</div>
            <div>
                <div class="logo-title">AI PC Advisor</div>
                <div class="logo-subtitle">Expert System</div>
            </div>
        </div>
        <div class="sidebar-section-title">Chức năng</div>
        """,
        unsafe_allow_html=True,
    )
    sidebar_button("Tư vấn cấu hình", "⚡", "Tư vấn cấu hình")
    sidebar_button("Chạy demo mẫu", "📦", "Chạy demo mẫu")
    sidebar_button("Xem lịch sử", "🕘", "Xem lịch sử")
    sidebar_button("Kiểm thử hệ thống", "🛡️", "Kiểm thử hệ thống")
    sidebar_button("Kiểm tra suy diễn lùi", "🔎", "Kiểm tra suy diễn lùi")
    st.sidebar.markdown(
        f"""
        <div class="active-mode-card">
            Đang mở: <b>{html_escape(st.session_state.mode)}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    initialize_state()
    inject_css()
    render_sidebar()
    mode = st.session_state.mode
    render_header()

    if mode == "Tư vấn cấu hình":
        render_consultation_page()
    elif mode == "Chạy demo mẫu":
        render_demo_page()
    elif mode == "Xem lịch sử":
        render_history_page()
    elif mode == "Kiểm thử hệ thống":
        render_test_page()
    elif mode == "Kiểm tra suy diễn lùi":
        render_backward_chaining_page()

    st.markdown(
        '<div class="footer">AI PC Advisor © 2026 | Hệ chuyên gia tư vấn cấu hình máy tính cho sinh viên AI</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
