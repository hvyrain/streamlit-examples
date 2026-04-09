import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return sns.load_dataset('iris') 
iris = load_data()

st.title('IRIS 데이터 예제')
st.html(
'''    
<h2>작성 : 서대우 교수</h2>
<div style="border:1px dotted blue">
    이 예제는 seaborn iris 데이터를 다양한 형식으로 보여주는 것입니다.
</div>
''')
# 탭 생성
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "원본 데이터", 
    "종별 평균", 
    "Box Plot",
    "Scatter Chart",
    "Pairplot",
    "히트맵"
])

with tab1:
    st.header('원본 데이터')
    st.dataframe(iris)

with tab2:
    st.header("종별 평균")
    st.dataframe(iris.groupby('species').mean())
    st.bar_chart(iris.groupby('species').mean())

with tab3:
    st.header('Box Plot 예제')
    fig, ax = plt.subplots()
    sns.boxenplot(data=iris[["sepal_length","sepal_width","petal_length","petal_width"]], ax=ax)
    st.pyplot(fig)
    plt.close(fig)

with tab4:
    st.header('Scatter Chart - Species별 분류')
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Sepal: Width vs Length')
        st.scatter_chart(iris, x="sepal_width", y="sepal_length", color="species")
    
    with col2:
        st.subheader('Petal: Width vs Length')
        st.scatter_chart(iris, x="petal_width", y="petal_length", color="species")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader('Sepal vs Petal Length')
        st.scatter_chart(iris, x="sepal_length", y="petal_length", color="species")
    
    with col4:
        st.subheader('Sepal vs Petal Width')
        st.scatter_chart(iris, x="sepal_width", y="petal_width", color="species")

with tab5:
    st.header('Seaborn pairplot')
    pair = sns.pairplot(iris, hue='species')
    st.pyplot(pair.figure)
    plt.close(pair.figure)

with tab6:
    st.header('상관계수 히트맵')
    fig2, ax = plt.subplots()
    sns.heatmap(iris.corr(numeric_only=True), annot=True, ax=ax)
    st.pyplot(fig2)
    plt.close(fig2)
