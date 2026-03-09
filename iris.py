import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
iris = sns.load_dataset('iris')

st.title('IRIS 데이터 예제')
st.header('원본 데이터')
st.dataframe(iris)
st.header('sepal_width vs. sepal_length')
st.scatter_chart(iris, x="sepal_width", y="sepal_length")

st.header('Seaborn pairplot')
fig = sns.pairplot(iris, hue='species')
st.pyplot(fig)
plt.close()
