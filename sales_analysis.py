import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="Sales Data Analysis", layout="wide")
st.title('📊 Sales 데이터 요약 및 시각화')

@st.cache_data
def load_sales_data(file_path):
    try:
        # 모든 시트를 딕셔너리 형태로 로드 (sheet_name=None)
        return pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

file_path = 'sales.xlsx'
all_sheets = load_sales_data(file_path)

if all_sheets is not None:
    # 사이드바에서 분석할 시트 선택
    sheet_names = list(all_sheets.keys())
    selected_sheet = st.sidebar.selectbox('분석할 시트를 선택하세요:', sheet_names)
    df = all_sheets[selected_sheet]

    st.info(f"현재 분석 중인 시트: **{selected_sheet}**")

    # 1. 데이터 요약 정보
    st.header('📈 데이터 요약')
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('기본 통계량')
        st.dataframe(df.describe())

    with col2:
        st.subheader('데이터 정보')
        info_df = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.values,
            'Non-Null Count': df.notnull().sum().values
        })
        st.table(info_df)

    # 2. 시각화 섹션
    st.header('📊 데이터 시각화')
    
    # 숫자형 컬럼 추출
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    
    if numeric_columns:
        selected_col = st.selectbox('시각화할 항목을 선택하세요:', numeric_columns)
        
        st.subheader(f'[{selected_col}] 분포 및 추이')
        st.line_chart(df[selected_col])
        
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(df[selected_col], kde=True, ax=ax, color='skyblue')
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning('시각화할 수 있는 숫자형 데이터가 없습니다.')

    # 3. 카테고리별 합계 분석
    st.header('📂 카테고리별 합계 분석')
    cat_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if cat_columns and numeric_columns:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            selected_cat = st.selectbox('기준 카테고리 컬럼을 선택하세요:', cat_columns)
        with col_c2:
            selected_val = st.selectbox('합계를 계산할 수치 컬럼을 선택하세요:', numeric_columns)

        # 그룹화 및 합계 계산
        category_sum = df.groupby(selected_cat)[selected_val].sum().reset_index()

        col_res1, col_res2 = st.columns([1, 2])
        with col_res1:
            st.subheader('집계 결과 테이블')
            st.dataframe(category_sum, use_container_width=True)
        with col_res2:
            st.subheader('카테고리별 합계 차트')
            st.bar_chart(data=category_sum, x=selected_cat, y=selected_val)
    else:
        st.info('카테고리 분석을 위한 문자열(Object) 컬럼 또는 수치 데이터가 부족합니다.')

    # 4. 원본 데이터 확인
    st.divider()
    if st.checkbox('원본 데이터프레임 보기'):
        st.dataframe(df)
else:
    st.info('`sales.xlsx` 파일을 찾을 수 없습니다. 파일이 스크립트와 같은 경로에 있는지 확인해주세요.')