import pandas as pd
import plotly.express as pe

def Unemployment(list_countries, df_full_country_list):
    df_GER_CHIL_USA=df_full_country_list[df_full_country_list["Country Name"].isin(list_countries)]
    df_GER_CHIL_USA
    df_GER_CHIL_USA[df_GER_CHIL_USA["Indicator Name"]=="Unemployment levels (%)"]
    fig=pe.line(df_GER_CHIL_USA[df_GER_CHIL_USA["Indicator Name"]=="Unemployment levels (%)"],
    x="Year",
    y="Value",
    color="Country Name",
    title="Unemployment levels (%) over Time"
    )
    return fig