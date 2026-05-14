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
    elif ngan_sach == "trung_binh":
        traces.append("Ngân sách trung bình -> tăng điểm cho nhóm Machine Learning cơ bản, máy mỏng nhẹ và cấu hình cân bằng.")
    elif ngan_sach == "cao":
        traces.append("Ngân sách cao -> tăng điểm cho nhóm Deep Learning, Computer Vision và AI kết hợp đồ họa.")

    return traces

DEMO_DEEP_LEARNING = {
    "hoc_lap_trinh": True,
    "hoc_machine_learning": True,
    "hoc_deep_learning": True,
    "xu_ly_anh_video": False,
    "choi_game_do_hoa": False,
    "can_may_nhe_pin_lau": False,
    "can_nang_cap": True,
    "ngan_sach": "cao",
}


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
            border-right: 1px solid var(--border);
            box-shadow: 8px 0 30px rgba(15, 23, 42, 0.04);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 2rem 1.4rem;
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
            height: 3.35rem;
            border-radius: 0.7rem;
            border: 1px solid var(--border);
            background: #ffffff;
            color: var(--text);
            font-weight: 700;
            justify-content: flex-start;
            padding-left: 1rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2563eb 0%, #0f6bff 100%);
            color: #ffffff;
            border: 1px solid #2563eb;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.28);
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

        .small-alert {
            background: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 14px;
            margin-top: 12px;
        }

        .footer {
            text-align: center;
            color: var(--muted);
            border-top: 1px solid var(--border);
            margin-top: 1.3rem;
            padding: 1rem 0 0.25rem 0;
            font-size: 0.92rem;
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
    nhom = top_3[0][0]
    diem = min(top_3[0][1], 100)
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
    header_cols[2].markdown("**Mức độ phù hợp**")

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
        scores = he.tinh_diem()
        predicted = max(scores, key=scores.get)
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
        <div class="header-row">
            <div>
                <h1 class="main-title">AI PC Advisor</h1>
                <div class="sub-title">HỆ CHUYÊN GIA TƯ VẤN CẤU HÌNH MÁY TÍNH CHO SINH VIÊN AI</div>
            </div>
            <div class="robot-badge">🤖</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(result):
    nhom = result["nhom"]
    diem = result["diem"]
    group_name = pretty_group(nhom)
    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">🏆 <span>Kết quả tư vấn</span></div>
            <div class="result-line">
                <span>Nhóm nhu cầu phù hợp nhất:</span>
                <span class="result-group">{html_escape(group_name)}</span>
            </div>
            <div class="result-progress-row">
                <div>Mức độ phù hợp:</div>
                <div class="progress-bg"><div class="progress-fill" style="width:{diem}%;"></div></div>
                <div class="score-badge">{diem}%</div>
            </div>
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
        percent = min(score, 100)
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
    lines, passed, failed = run_system_tests()
    result_lines = "<br>".join(html_escape(line) for line in lines)
    st.markdown(
        f"""
        <div class="card">
            <div class="section-title">🛡️ Kiểm thử hệ thống</div>
            <div class="notice">Chức năng kiểm thử hệ thống hiện chạy tốt nhất ở bản terminal bằng menu số 5. Bản web vẫn chạy lại các test case từ <b>data/sample_cases.json</b>.</div>
            <div class="explain-text">{result_lines}</div>
            <br>
            <div class="explain-text"><b>Tổng số test:</b> {passed + failed} &nbsp; | &nbsp; <b>Đúng:</b> {passed} &nbsp; | &nbsp; <b>Sai:</b> {failed}</div>
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


def build_known_from_inputs():
    budget_map = {"Thấp": "thap", "Trung bình": "trung_binh", "Cao": "cao"}
    return {
        "hoc_lap_trinh": st.session_state.get("hoc_lap_trinh", True),
        "hoc_machine_learning": st.session_state.get("hoc_ml", True),
        "hoc_deep_learning": st.session_state.get("hoc_dl", True),
        "xu_ly_anh_video": st.session_state.get("xu_ly_anh", False),
        "choi_game_do_hoa": st.session_state.get("game_do_hoa", False),
        "can_may_nhe_pin_lau": st.session_state.get("may_nhe", False),
        "can_nang_cap": st.session_state.get("can_nang_cap", True),
        "ngan_sach": budget_map.get(st.session_state.get("ngan_sach_label", "Cao"), "cao"),
    }


def initialize_state():
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "result" not in st.session_state:
        st.session_state.result = infer_result(DEMO_DEEP_LEARNING, save_outputs=False)
    if "export_message" not in st.session_state:
        st.session_state.export_message = ""
    if "export_path" not in st.session_state:
        st.session_state.export_path = ""
    defaults = {
        "hoc_lap_trinh": True,
        "hoc_ml": True,
        "hoc_dl": True,
        "xu_ly_anh": False,
        "game_do_hoa": False,
        "may_nhe": False,
        "can_nang_cap": True,
        "ngan_sach_label": "Cao",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_sidebar():
    def run_demo_callback():
        st.session_state.hoc_lap_trinh = True
        st.session_state.hoc_ml = True
        st.session_state.hoc_dl = True
        st.session_state.xu_ly_anh = False
        st.session_state.game_do_hoa = False
        st.session_state.may_nhe = False
        st.session_state.can_nang_cap = True
        st.session_state.ngan_sach_label = "Cao"
        st.session_state.result = infer_result(DEMO_DEEP_LEARNING, save_outputs=True)
        st.session_state.page = "dashboard"
        st.session_state.export_message = "Đã xuất kết quả tư vấn"
        st.session_state.export_path = st.session_state.result["txt_path"] or ""
        st.toast("Đã xuất kết quả tư vấn", icon="✅")

    st.sidebar.markdown("## 📋 Thông tin đầu vào")
    st.sidebar.checkbox("Học lập trình", key="hoc_lap_trinh")
    st.sidebar.checkbox("Machine Learning", key="hoc_ml")
    st.sidebar.checkbox("Deep Learning", key="hoc_dl")
    st.sidebar.checkbox("Xử lý ảnh / Computer Vision", key="xu_ly_anh")
    st.sidebar.checkbox("Game / Đồ họa", key="game_do_hoa")
    st.sidebar.checkbox("Máy nhẹ, pin lâu", key="may_nhe")
    st.sidebar.checkbox("Cần nâng cấp RAM/SSD", key="can_nang_cap")
    st.sidebar.selectbox("Ngân sách", ["Thấp", "Trung bình", "Cao"], key="ngan_sach_label")

    st.sidebar.write("")
    consult_clicked = st.sidebar.button("⚡  Tư vấn cấu hình", type="primary", use_container_width=True)
    st.sidebar.button("📦  Chạy demo mẫu", use_container_width=True, on_click=run_demo_callback)
    history_clicked = st.sidebar.button("🕘  Xem lịch sử", use_container_width=True)
    test_clicked = st.sidebar.button("🛡️  Kiểm thử hệ thống", use_container_width=True)

    if consult_clicked:
        known = build_known_from_inputs()
        st.session_state.result = infer_result(known, save_outputs=True)
        st.session_state.page = "dashboard"
        st.session_state.export_message = "Đã xuất kết quả tư vấn"
        st.session_state.export_path = st.session_state.result["txt_path"] or ""
        st.toast("Đã xuất kết quả tư vấn", icon="✅")

    if history_clicked:
        st.session_state.page = "history"

    if test_clicked:
        st.session_state.page = "test"


def main():
    initialize_state()
    inject_css()
    render_sidebar()
    render_header()

    if st.session_state.page == "history":
        render_history_page()
    elif st.session_state.page == "test":
        render_test_page()
    else:
        render_dashboard(st.session_state.result)

    st.markdown(
        '<div class="footer">AI PC Advisor © 2026 | Hệ chuyên gia tư vấn cấu hình máy tính cho sinh viên AI</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
