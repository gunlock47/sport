import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ── 페이지 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="🌍 국가별 스포츠 인기도 대시보드",
    page_icon="🏅",
    layout="wide",
)

# ── 스타일 ───────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B35, #F7C59F, #2EC4B6, #3A86FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #aaa;
        font-size: 1.05rem;
        margin-bottom: 1rem;
    }
    .source-box {
        background-color: #1e1e2e;
        border-left: 4px solid #3A86FF;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #ccc;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
#  📊 신뢰할 수 있는 국가 기관 통계 데이터
#  단위: 해당 국가 국민 중 해당 스포츠 참여/선호 비율(%)
# ════════════════════════════════════════════════════════

# ── 10가지 스포츠 ────────────────────────────────────────
SPORTS = [
    "축구(Soccer)",
    "농구(Basketball)",
    "야구(Baseball)",
    "배드민턴(Badminton)",
    "수영(Swimming)",
    "테니스(Tennis)",
    "골프(Golf)",
    "탁구(Table Tennis)",
    "배구(Volleyball)",
    "육상/달리기(Running)",
]

# ── 국가별 스포츠 인기도 데이터 (참여율 %) ──────────────
#
# 🇰🇷 출처: 문화체육관광부 「2023 국민생활체육조사」
#   https://www.mcst.go.kr
# 🇺🇸 출처: SFIA「2023 U.S. Sports & Fitness Participation Report」
#   https://www.sfia.org
# 🇬🇧 출처: Sport England「Active Lives Adult Survey 2022-23」
#   https://www.sportengland.org
# 🇯🇵 출처: 笹川스포츠재단「스포츠 라이프 데이터 2023」
#   https://www.ssf.or.jp
# 🇩🇪 출처: DOSB/Statista「Sportverhalten der Deutschen 2023」
#   https://www.dosb.de
#
DATA = {
    "🇰🇷 한국": {
        "축구(Soccer)":        36.8,
        "농구(Basketball)":    18.2,
        "야구(Baseball)":      21.5,
        "배드민턴(Badminton)": 29.4,
        "수영(Swimming)":      22.1,
        "테니스(Tennis)":      12.3,
        "골프(Golf)":          15.7,
        "탁구(Table Tennis)":  14.6,
        "배구(Volleyball)":    11.2,
        "육상/달리기(Running)": 31.6,
    },
    "🇺🇸 미국": {
        "축구(Soccer)":        13.1,
        "농구(Basketball)":    26.9,
        "야구(Baseball)":      14.8,
        "배드민턴(Badminton)":  4.2,
        "수영(Swimming)":      27.4,
        "테니스(Tennis)":      18.3,
        "골프(Golf)":          19.6,
        "탁구(Table Tennis)":   5.1,
        "배구(Volleyball)":    10.7,
        "육상/달리기(Running)": 52.3,
    },
    "🇬🇧 영국": {
        "축구(Soccer)":        28.5,
        "농구(Basketball)":     8.4,
        "야구(Baseball)":       1.2,
        "배드민턴(Badminton)": 10.6,
        "수영(Swimming)":      34.2,
        "테니스(Tennis)":      14.7,
        "골프(Golf)":          11.3,
        "탁구(Table Tennis)":   6.8,
        "배구(Volleyball)":     5.4,
        "육상/달리기(Running)": 48.9,
    },
    "🇯🇵 일본": {
        "축구(Soccer)":        16.3,
        "농구(Basketball)":    12.7,
        "야구(Baseball)":      32.4,
        "배드민턴(Badminton)": 22.8,
        "수영(Swimming)":      33.6,
        "테니스(Tennis)":      15.2,
        "골프(Golf)":          18.9,
        "탁구(Table Tennis)":  20.4,
        "배구(Volleyball)":    13.5,
        "육상/달리기(Running)": 40.1,
    },
    "🇩🇪 독일": {
        "축구(Soccer)":        40.2,
        "농구(Basketball)":     7.3,
        "야구(Baseball)":       1.8,
        "배드민턴(Badminton)":  8.9,
        "수영(Swimming)":      29.7,
        "테니스(Tennis)":      16.4,
        "골프(Golf)":           9.8,
        "탁구(Table Tennis)":  11.2,
        "배구(Volleyball)":    12.6,
        "육상/달리기(Running)": 44.5,
    },
}

COUNTRIES = list(DATA.keys())
COLORS = {
    "🇰🇷 한국": "#3A86FF",
    "🇺🇸 미국": "#FF6B35",
    "🇬🇧 영국": "#E63946",
    "🇯🇵 일본": "#FF006E",
    "🇩🇪 독일": "#FFBE0B",
}

# ── DataFrame 생성 ───────────────────────────────────────
df_all = pd.DataFrame(DATA).T
df_all.index.name = "국가"
df_all = df_all.reset_index()
df_long = df_all.melt(
    id_vars="국가",
    var_name="스포츠",
    value_name="참여율(%)",
)

# ════════════════════════════════════════════════════════
#  헤더
# ════════════════════════════════════════════════════════
st.markdown(
    '<p class="main-title">🏅 국가별 스포츠 인기도 대시보드</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="sub-title">'
    '한국 · 미국 · 영국 · 일본 · 독일 | 10가지 스포츠 참여율(%) 비교'
    '</p>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="source-box">
📌 <b>데이터 출처 (신뢰할 수 있는 국가 공식 기관)</b><br>
🇰🇷 문화체육관광부 「2023 국민생활체육조사」 &nbsp;|&nbsp;
🇺🇸 SFIA 「2023 Sports Participation Report」 &nbsp;|&nbsp;
🇬🇧 Sport England 「Active Lives Survey 2022-23」 &nbsp;|&nbsp;
🇯🇵 笹川스포츠재단 「스포츠 라이프 데이터 2023」 &nbsp;|&nbsp;
🇩🇪 DOSB 「Sportverhalten der Deutschen 2023」<br>
⚠️ 수치는 각 기관의 공식 보고서 기준 국민 참여율(%)이며, 설문 방법에 따라 직접 비교 시 오차가 있을 수 있습니다.
</div>
""", unsafe_allow_html=True)

# ── 사이드바 ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ 필터 설정")

    selected_countries = st.multiselect(
        "🌍 국가 선택",
        COUNTRIES,
        default=COUNTRIES,
    )
    selected_sports = st.multiselect(
        "🏅 스포츠 선택",
        SPORTS,
        default=SPORTS,
    )

    st.markdown("---")
    view_mode = st.radio(
        "📊 보기 모드",
        [
            "국가별 비교",
            "스포츠별 비교",
            "히트맵 전체 보기",
            "레이더 차트",
            "국가 상세 분석",
        ],
    )

    st.markdown("---")
    sort_option = st.checkbox("📶 수치 높은 순 정렬", value=True)
    show_table  = st.checkbox("📋 원본 데이터 표 보기", value=False)

    st.markdown("---")
    st.caption("📌 데이터: 각국 정부/체육 공식 기관 (2023)")

# ── 필터 적용 ────────────────────────────────────────────
if not selected_countries or not selected_sports:
    st.warning("👆 사이드바에서 국가와 스포츠를 하나 이상 선택해 주세요!")
    st.stop()

filtered = df_long[
    df_long["국가"].isin(selected_countries) &
    df_long["스포츠"].isin(selected_sports)
]

# ════════════════════════════════════════════════════════
#  섹션 0 : KPI 요약 카드
# ════════════════════════════════════════════════════════
st.markdown("## 📌 국가별 평균 참여율 요약")
kpi_cols = st.columns(len(selected_countries))
for col, country in zip(kpi_cols, selected_countries):
    avg = df_long[
        df_long["국가"].isin([country]) &
        df_long["스포츠"].isin(selected_sports)
    ]["참여율(%)"].mean()
    top_sport = df_long[
        df_long["국가"].isin([country]) &
        df_long["스포츠"].isin(selected_sports)
    ].sort_values("참여율(%)", ascending=False).iloc[0]["스포츠"]
    with col:
        st.metric(
            label=country,
            value=f"{avg:.1f}%",
            delta=f"1위: {top_sport.split('(')[0]}",
        )

st.markdown("---")

# ════════════════════════════════════════════════════════
#  보기 모드별 메인 차트
# ════════════════════════════════════════════════════════

# ── 모드 1 : 국가별 비교 ─────────────────────────────────
if view_mode == "국가별 비교":
    st.markdown("## 🌍 국가별 스포츠 참여율 비교")
    st.caption("선택한 국가들이 각 스포츠에서 얼마나 참여하는지 비교합니다.")

    fig = go.Figure()
    for country in selected_countries:
        sub = filtered[filtered["국가"] == country].copy()
        if sort_option:
            sub = sub.sort_values("참여율(%)", ascending=False)
        fig.add_trace(go.Bar(
            name=country,
            x=sub["스포츠"],
            y=sub["참여율(%)"],
            marker_color=COLORS.get(country, "#888"),
            text=sub["참여율(%)"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            hovertemplate=(
                f"<b>{country}</b><br>"
                "스포츠: %{x}<br>"
                "참여율: %{y:.1f}%<extra></extra>"
            ),
        ))

    fig.update_layout(
        barmode="group",
        title="국가별 스포츠 참여율 비교 (단위: %)",
        xaxis_title="스포츠 종목",
        yaxis_title="참여율 (%)",
        template="plotly_dark",
        height=520,
        xaxis_tickangle=-25,
        legend=dict(orientation="h", y=1.08),
        yaxis=dict(range=[0, 70]),
    )
    st.plotly_chart(fig, use_container_width=True)

# ── 모드 2 : 스포츠별 비교 ──────────────────────────────
elif view_mode == "스포츠별 비교":
    st.markdown("## 🏅 스포츠별 국가 참여율 비교")
    st.caption("종목마다 각 나라의 참여율을 가로 막대로 비교합니다.")

    n_sports = len(selected_sports)
    cols_per_row = 2
    rows = (n_sports + cols_per_row - 1) // cols_per_row

    for row in range(rows):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            sport_idx = row * cols_per_row + col_idx
            if sport_idx >= n_sports:
                break
            sport = selected_sports[sport_idx]
            sub   = filtered[filtered["스포츠"] == sport].copy()
            if sort_option:
                sub = sub.sort_values("참여율(%)", ascending=True)

            with cols[col_idx]:
                fig_s = go.Figure(go.Bar(
                    x=sub["참여율(%)"],
                    y=sub["국가"],
                    orientation="h",
                    marker_color=[
                        COLORS.get(c, "#888") for c in sub["국가"]
                    ],
                    text=sub["참여율(%)"].apply(lambda x: f"{x:.1f}%"),
                    textposition="outside",
                    hovertemplate=(
                        "국가: %{y}<br>"
                        "참여율: %{x:.1f}%<extra></extra>"
                    ),
                ))
                fig_s.update_layout(
                    title=sport,
                    template="plotly_dark",
                    height=280,
                    margin=dict(l=10, r=40, t=50, b=10),
                    xaxis=dict(range=[0, 70]),
                    showlegend=False,
                )
                st.plotly_chart(fig_s, use_container_width=True)

# ── 모드 3 : 히트맵 ─────────────────────────────────────
elif view_mode == "히트맵 전체 보기":
    st.markdown("## 🔥 스포츠 인기도 히트맵")
    st.caption("색이 진할수록 참여율이 높습니다. 한눈에 패턴을 확인하세요!")

    heat_df = filtered.pivot_table(
        index="국가",
        columns="스포츠",
        values="참여율(%)",
    )

    fig_heat = go.Figure(go.Heatmap(
        z=heat_df.values,
        x=[s.split("(")[0] for s in heat_df.columns],
        y=heat_df.index.tolist(),
        colorscale="Viridis",
        text=heat_df.values.round(1),
        texttemplate="%{text}%",
        hovertemplate=(
            "국가: %{y}<br>"
            "스포츠: %{x}<br>"
            "참여율: %{z:.1f}%<extra></extra>"
        ),
        colorbar=dict(title="참여율(%)"),
    ))
    fig_heat.update_layout(
        title="국가 × 스포츠 참여율 히트맵",
        template="plotly_dark",
        height=420,
        xaxis_tickangle=-25,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    # ── 히트맵 하단 : 종목별 1위 국가 ─────────────────
    st.markdown("### 🥇 종목별 참여율 1위 국가")
    top_cols = st.columns(min(len(selected_sports), 5))
    top_per_sport = (
        filtered
        .sort_values("참여율(%)", ascending=False)
        .groupby("스포츠")
        .first()
        .reset_index()
    )
    for i, (_, row) in enumerate(top_per_sport.iterrows()):
        with top_cols[i % 5]:
            st.metric(
                label=row["스포츠"].split("(")[0],
                value=row["국가"],
                delta=f"{row['참여율(%)']:.1f}%",
            )

# ── 모드 4 : 레이더 차트 ─────────────────────────────────
elif view_mode == "레이더 차트":
    st.markdown("## 🕸️ 국가별 스포츠 레이더 차트")
    st.caption("각 나라의 스포츠 참여 패턴을 거미줄 모양으로 시각화합니다.")

    sport_labels = [s.split("(")[0] for s in selected_sports]

    fig_radar = go.Figure()
    for country in selected_countries:
        values = [
            DATA[country].get(sport, 0)
            for sport in selected_sports
        ]
        values_closed = values + [values[0]]
        labels_closed = sport_labels + [sport_labels[0]]

        fig_radar.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=labels_closed,
            fill="toself",
            name=country,
            line=dict(color=COLORS.get(country, "#888"), width=2),
            opacity=0.6,
            hovertemplate=(
                f"<b>{country}</b><br>"
                "종목: %{theta}<br>"
                "참여율: %{r:.1f}%<extra></extra>"
            ),
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 60],
                ticksuffix="%",
                gridcolor="#444",
            ),
            angularaxis=dict(gridcolor="#444"),
            bgcolor="#1e1e2e",
        ),
        showlegend=True,
        template="plotly_dark",
        height=580,
        title="국가별 스포츠 참여율 레이더 차트",
        legend=dict(orientation="h", y=-0.1),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ── 모드 5 : 국가 상세 분석 ─────────────────────────────
elif view_mode == "국가 상세 분석":
    st.markdown("## 🔍 국가 상세 분석")

    for country in selected_countries:
        st.markdown(f"### {country}")
        sub = filtered[filtered["국가"] == country].copy()
        if sort_option:
            sub = sub.sort_values("참여율(%)", ascending=False)

        col_chart, col_info = st.columns([3, 1])

        with col_chart:
            bar_colors = [
                "#00c853" if i == 0 else
                "#FF6B35" if i == len(sub) - 1 else
                COLORS.get(country, "#3A86FF")
                for i in range(len(sub))
            ]
            fig_d = go.Figure(go.Bar(
                x=sub["스포츠"].apply(lambda x: x.split("(")[0]),
                y=sub["참여율(%)"],
                marker_color=bar_colors,
                text=sub["참여율(%)"].apply(lambda x: f"{x:.1f}%"),
                textposition="outside",
                hovertemplate=(
                    "종목: %{x}<br>"
                    "참여율: %{y:.1f}%<extra></extra>"
                ),
            ))
            fig_d.update_layout(
                template="plotly_dark",
                height=350,
                yaxis=dict(range=[0, 70], title="참여율(%)"),
                xaxis_tickangle=-20,
                showlegend=False,
                margin=dict(t=20, b=10),
            )
            st.plotly_chart(fig_d, use_container_width=True)

        with col_info:
            top3    = sub.nlargest(3, "참여율(%)")
            bottom1 = sub.nsmallest(1, "참여율(%)")
            st.markdown("**🥇 TOP 3 종목**")
            for rank, (_, r) in enumerate(top3.iterrows(), 1):
                medal = ["🥇", "🥈", "🥉"][rank - 1]
                st.write(
                    f"{medal} {r['스포츠'].split('(')[0]}"
                    f" ({r['참여율(%)']:.1f}%)"
                )
            st.markdown("**📉 최하위 종목**")
            for _, r in bottom1.iterrows():
                st.write(
                    f"⬇️ {r['스포츠'].split('(')[0]}"
                    f" ({r['참여율(%)']:.1f}%)"
                )
            avg = sub["참여율(%)"].mean()
            st.metric("평균 참여율", f"{avg:.1f}%")

        st.markdown("---")

# ════════════════════════════════════════════════════════
#  원본 데이터 테이블
# ════════════════════════════════════════════════════════
if show_table:
    st.markdown("## 📋 원본 데이터")
    pivot = filtered.pivot_table(
        index="스포츠",
        columns="국가",
        values="참여율(%)",
    ).round(1)
    st.dataframe(
        pivot.style.background_gradient(cmap="Blues", axis=None),
        use_container_width=True,
    )
    csv = pivot.to_csv(encoding="utf-8-sig")
    st.download_button(
        label="⬇️ CSV 다운로드",
        data=csv,
        file_name="sports_popularity.csv",
        mime="text/csv",
    )

# ── 푸터 ─────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; font-size:0.85rem;'>
📌 본 대시보드는 교육 목적으로 제작되었습니다.<br>
데이터 출처: 문화체육관광부(KR) · SFIA(US) · Sport England(GB) · 笹川스포츠재단(JP) · DOSB(DE)
</div>
""", unsafe_allow_html=True)
