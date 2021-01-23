import datetime
import pandas as pd
import sys
import streamlit as st
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
stockfromcsv=pd.read_csv('https://raw.githubusercontent.com/kennyko2002/ptt_hot_stock/master/pttstock2',parse_dates=['日期'],infer_datetime_format='%Y-%M-%D')
stockfromcsv['推文數']=stockfromcsv['推文數'].replace(regex=r'^X',value=0)
stockfromcsv['推文數']=stockfromcsv['推文數'].replace(regex=r'^爆',value=100)
stockfromcsv=stockfromcsv.fillna(value=0)
stockfromcsv=stockfromcsv.astype({"股名":str, "主旨":str,"推文數": int})
x=stockfromcsv.groupby(['日期','股名'])['推文數'].sum().unstack().sort_index(ascending=False)
last_seven_day=[x.iloc[num,:].sort_values(ascending=False).index[0:6] for num in range(7)]
topfivestock=pd.DataFrame(last_seven_day,index=x.iloc[0:7,:].index)
last_seven_day_hot=[x.iloc[num,:].sort_values(ascending=False)[0:6].tolist() for num in range(7)]
topfivestock_hotindex=pd.DataFrame(last_seven_day_hot,index=x.iloc[0:7,:].index)

st.title("PTT 熱門討論股")
st.table(topfivestock+'('+topfivestock_hotindex.astype(int).astype(str) +')')
pyplot.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
pyplot.rcParams['axes.unicode_minus'] = False
st.title("PTT 討論熱度趨勢")
#fig,axes=pyplot.subplots(3,2,sharex=True,sharey=True)
fig,axes=pyplot.subplots(3,2,sharex=True)
for i in range(3):
    for j in range(2):
        yy=topfivestock[2*i+j][0]
        axes[i,j].bar(x[yy].index ,x[yy],align='edge',)
        axes[i,j].set_title(yy)
        axes[i,j].tick_params(labelrotation=45)
st.pyplot(fig)

