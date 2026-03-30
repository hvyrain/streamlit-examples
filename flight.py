import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

# matplotlib에서 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

@st.cache_data
def load_data():
    try:
        flights = sns.load_dataset('flights')
        flights['month_no'] = pd.to_datetime(flights['month'], format='%b').dt.month
        return flights
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return None

@st.cache_resource
def load_animation():
    """Lottie 애니메이션 로드"""
    try:
        # 비행기 애니메이션 URL
        url = "https://lottie.host/4db176db-8fef-4db7-920d-e71d8d0e5e54/h3VxPZsKa7.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"애니메이션 로드 실패: {e}")
        return None

flights = load_data()
if flights is None:
    st.stop()

st.title('Flights 데이터 분석')

def plot_trend_chart(data):
    """시계열 데이터 트렌드 차트"""
    flights_sorted = data.sort_values(['year', 'month_no']).reset_index(drop=True)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    x = np.arange(len(flights_sorted))
    y = flights_sorted['passengers'].values
    ax.plot(x, y, label='승객 수', linewidth=2)
    
    coeffs = np.polyfit(x, y, 1)
    trend = np.polyval(coeffs, x)
    ax.plot(x, trend, 'r--', label='추세선', linewidth=2)
    
    ax.set_xlabel('기간')
    ax.set_ylabel('승객 수')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig

# 탭 생성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 추세 분석",
    "📊 월별 비교", 
    "📉 월별 상세분석",
    "📋 통계 분석",
    "📂 데이터 확인"
])

# Tab 1: 추세 분석
with tab1:
    st.header('📊 대시보드')
    
    # 비행기 애니메이션 - 사인곡선 경로 (파란 배경 내 제한)
    animation_html = """
    <style>
        .airplane-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-radius: 10px;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }
        
        @keyframes sine-wave {
            0% {
                left: 0%;
                top: 50%;
                opacity: 0;
            }
            12.5% {
                left: 12.5%;
                top: 30%;
                opacity: 1;
            }
            25% {
                left: 25%;
                top: 20%;
                opacity: 1;
            }
            37.5% {
                left: 37.5%;
                top: 30%;
                opacity: 1;
            }
            50% {
                left: 50%;
                top: 50%;
                opacity: 1;
            }
            62.5% {
                left: 62.5%;
                top: 70%;
                opacity: 1;
            }
            75% {
                left: 75%;
                top: 80%;
                opacity: 1;
            }
            87.5% {
                left: 87.5%;
                top: 70%;
                opacity: 1;
            }
            100% {
                left: 100%;
                top: 50%;
                opacity: 0;
            }
        }
        
        .airplane {
            font-size: 60px;
            animation: sine-wave 4s ease-in-out infinite;
            position: absolute;
            transform: translate(-50%, -50%);
        }
    </style>
    
    <div class="airplane-container">
        <div class="airplane">✈️</div>
    </div>
    """
    st.markdown(animation_html, unsafe_allow_html=True)
    
    st.divider()
    
    # KPI 메트릭 (상단)
    col1, col2, col3, col4 = st.columns(4)
    
    avg_passengers = flights['passengers'].mean()
    max_passengers = flights['passengers'].max()
    min_passengers = flights['passengers'].min()
    
    # 첫 연도와 마지막 연도의 평균 비교
    first_year_avg = flights[flights['year'] == flights['year'].min()]['passengers'].mean()
    last_year_avg = flights[flights['year'] == flights['year'].max()]['passengers'].mean()
    growth_rate = ((last_year_avg - first_year_avg) / first_year_avg) * 100
    
    with col1:
        st.metric('📈 전체 평균', f"{avg_passengers:.0f}")
    with col2:
        st.metric('🔝 최고값', f"{max_passengers}")
    with col3:
        st.metric('🔻 최저값', f"{min_passengers}")
    with col4:
        st.metric('📊 연도별 성장률', f"{growth_rate:.1f}%")
    
    st.divider()
    
    # 트렌드 라인 차트 (중간)
    st.subheader('시계열 추이 분석')
    fig = plot_trend_chart(flights)
    st.pyplot(fig)
    plt.close(fig)
    
    st.divider()
    
    # 계절성 분석 (하단)
    st.subheader('계절성 분석')
    
    col_season1, col_season2, col_season3 = st.columns(3)
    
    # 월별 평균 계산
    monthly_avg = flights.groupby('month_no')['passengers'].mean()
    peak_month = monthly_avg.idxmax()
    lowest_month = monthly_avg.idxmin()
    
    month_names = ['1월', '2월', '3월', '4월', '5월', '6월', 
                   '7월', '8월', '9월', '10월', '11월', '12월']
    
    with col_season1:
        st.metric('🌞 가장 붐비는 달', f"{month_names[peak_month-1]} ({monthly_avg[peak_month]:.0f}명)")
    
    with col_season2:
        st.metric('❄️ 가장 한산한 달', f"{month_names[lowest_month-1]} ({monthly_avg[lowest_month]:.0f}명)")
    
    with col_season3:
        diff = monthly_avg[peak_month] - monthly_avg[lowest_month]
        st.metric('📍 최고-최저 차이', f"{diff:.0f}명 ({(diff/monthly_avg[lowest_month]*100):.1f}%)")
    
    # 주요 인사이트
    st.info(f"""
    **주요 인사이트:**
    - 📈 {flights['year'].min()}년 대비 {flights['year'].max()}년 성장률: **{growth_rate:.1f}%**
    - 🌞 **여름철({month_names[peak_month-1]})**에 승객이 가장 많음
    - ❄️ **겨울철({month_names[lowest_month-1]})**에 승객이 가장 적음
    - 📊 전체 승객 수는 **지속적으로 증가**하는 추세를 보임
    """)

# Tab 2: 월별 비교
with tab2:
    st.header('연도별 월별 승객 수')
    pivot_data = flights.pivot_table(values='passengers', index='month_no', columns='year')
    st.bar_chart(pivot_data)
    st.info('💡 각 연도별로 월별 승객수를 비교할 수 있습니다.')

# Tab 3: 월별 상세분석
with tab3:
    st.header('월별 상세분석')
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader('월별 승객수 분포 (Box Plot)')
        fig, ax = plt.subplots(figsize=(10, 5))
        flights_for_box = flights.copy()
        sns.boxplot(data=flights_for_box, x='month_no', y='passengers', ax=ax, palette='Set2')
        ax.set_xlabel('월')
        ax.set_ylabel('승객 수')
        ax.set_title('월별 승객수 분포')
        st.pyplot(fig)
        plt.close(fig)
    
    with col2:
        st.subheader('월별 연도별 승객수 히트맵')
        pivot_heatmap = flights.pivot_table(values='passengers', index='month_no', columns='year')
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot_heatmap, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': '승객 수'})
        ax.set_xlabel('연도')
        ax.set_ylabel('월')
        ax.set_title('월별 연도별 승객수 히트맵')
        st.pyplot(fig)
        plt.close(fig)

# Tab 4: 통계 분석
with tab4:
    st.header('월별 승객수 분석 결과')
    
    # 주요 지표
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('전체 평균', f"{flights['passengers'].mean():.0f}")
    with col2:
        st.metric('최고 승객수', f"{flights['passengers'].max()}")
    with col3:
        st.metric('최저 승객수', f"{flights['passengers'].min()}")
    
    # 월별 통계
    st.subheader('월별 평균 승객수')
    monthly_avg = flights.groupby('month_no')['passengers'].agg(['mean', 'min', 'max', 'std']).round(0)
    monthly_avg.columns = ['평균', '최소', '최대', '표준편차']
    st.dataframe(monthly_avg, use_container_width=True)
    
    # 월별 세부 통계
    st.subheader('월별 세부 통계')
    monthly_stats = flights.groupby('month_no').agg({
        'passengers': ['mean', 'std'],
        'year': 'count'
    }).round(0)
    monthly_stats.columns = ['평균', '표준편차', '데이터 수']
    st.dataframe(monthly_stats, use_container_width=True)
    
    # 연도별 총 승객수
    st.subheader('연도별 총 승객수')
    yearly_total = flights.groupby('year')['passengers'].sum().reset_index()
    yearly_total.columns = ['연도', '총 승객수']
    st.bar_chart(yearly_total.set_index('연도'))

# Tab 5: 데이터 확인
with tab5:
    st.header('데이터 확인')
    st.subheader('원본 데이터')
    st.dataframe(flights, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric('총 데이터 행 수', len(flights))
    with col2:
        st.metric('데이터 기간', f"{flights['year'].min()}~{flights['year'].max()}")

st.info('✓ Flights 데이터는 1949년부터 1960년까지의 국제 항공 승객 데이터입니다.')
