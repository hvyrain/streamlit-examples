import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
iris = sns.load_dataset('iris')

st.dataframe(iris.groupby('species').mean())

st.title('IRIS 데이터 예제')
"이 예제는 seaborn iris 데이터를 다양한 형식으로 보여주는 것입니다."
st.header('원본 데이터')
st.dataframe(iris)
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
