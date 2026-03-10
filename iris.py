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
<div style="border:1px dotted blue">
    이 예제는 seaborn iris 데이터를 다양한 형식으로 보여주는 것입니다.
</div>
''')
st.header('원본 데이터')
if st.checkbox('데이터프레임 보기'):
    st.dataframe(iris)

st.header("종별 평균")
if st.checkbox('종별 평균값 보기'):
    st.dataframe(iris.groupby('species').mean())
    st.bar_chart(iris.groupby('species').mean())

st.header('Box Plot 예제')
fig, ax = plt.subplots()
sns.boxenplot(data=iris[["sepal_length","sepal_width","petal_length","petal_width"]], ax=ax)
st.pyplot(fig)
plt.close(fig)

st.header('sepal_width vs. sepal_length')
st.scatter_chart(iris, x="sepal_width", y="sepal_length")

st.header('Seaborn pairplot')

pair = sns.pairplot(iris, hue='species')
st.pyplot(pair.figure)
plt.close(pair.figure)


st.header('상관계수 히트맵')

fig2, ax = plt.subplots()
sns.heatmap(iris.corr(numeric_only=True), annot=True, ax=ax)

st.pyplot(fig2)
plt.close(fig2)
