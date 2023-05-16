# Import required libraries
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
from snowflake.snowpark.functions import call_udf
import plotly.express as px
import pandas as pd
import streamlit as st

# Create Session object
# @st.cache_resource
def create_session():
    connection_parameters = {
        "account": "xxx.ap-southeast-1",
        "user"        :"",
        "host": "xxx.ap-southeast-1.snowflakecomputing.com", # e.g. "sn00111.snowflakecomputing.com",
        "password"    :"",
        "role": "SYSADMIN",
        "database": "HOL_DB",
        "schema": "PUBLIC",
        "warehouse": "HOL_WH"
        }
    session = Session.builder.configs(connection_parameters).create()
    return session


# Create Snowpark DataFrames that loads data
# Create Sliders
# @st.cache_data
def load_data(_session):

    maint_df = session.table("PUBLIC.MAINTENANCE_HUM")
    maint_df = maint_df.describe().sort(col("SUMMARY").desc()).filter("SUMMARY = 'max' or SUMMARY = 'mean' or SUMMARY = 'min'").drop(col("TYPE")).collect()

    return maint_df


def draw_sliders(session, m_df):
    st.header("Machine Predictive Maintenance Classification Dataset")

    with st.expander("See Synosis"):
        st.write("""
        In this use case you will build a binary model based on the 'Machine Predictive Maintenance Classification' dataset from Kaggle. We supplement this dataset with data from the Snowflake data marketplace.

        The use case uses information related to machine diagnostics (torque, rotational speed) and environmental features (air temperature, humidity) to predict the likelihood of a failure.

        https://www.kaggle.com/datasets/shivamb/machine-predictive-maintenance-classification
        
        """
        )
    st.subheader("Snowpark Dataframe fetched from MAINTENANCE_HUM table")
    with st.expander("See Dataframe"):
        st.dataframe(m_df)

    st.subheader("Select your What-If values")

    with st.expander("See Sliders (Defaulted to the mean values)"):
        col1, col2, col3 = st.columns(3)
        with st.container():
            with col1:
                feature_1 = st.slider('Air Temperature K', m_df[0][1], m_df[2][1], m_df[1][1], key='feature_1', on_change=None)
                feature_2 = st.slider('Process Temperature K', m_df[0][2], m_df[2][2], m_df[1][2], key='feature_2')
            with col2:
                feature_3 = st.slider('Rotational Speed RPM', m_df[0][3], m_df[2][3], m_df[1][3], key='feature_3')
                feature_4 = st.slider('Torque Nm', m_df[0][4], m_df[2][4], m_df[1][4], key='feature_4')
            with col3:
                feature_5 = st.slider('Tool Wear Min', m_df[0][5], m_df[2][5], m_df[1][5], key='feature_5')
                feature_6 = st.slider('Relative Humidity', m_df[0][6], m_df[2][6], m_df[1][6], key='feature_6')


    plotly_df = pd.DataFrame(dict(
        r=[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6],
        theta=['Air Temperature K','Process Temperature K','Rotational Speed RPM',
            'Torque Nm', 'Tool Wear Min', 'Relative Humidity']))

    fig = px.line_polar(plotly_df, r='r', theta='theta', line_close=True)
    # fig.show()
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    st.subheader('Probability of Machine Failure')

    if st.button('Predict Machine Failure'):
        features_df = session.create_dataframe([[feature_1, feature_2, feature_3, feature_4, feature_5, feature_6]], schema=["A", "B", "C", "D", "E", "F"])
        machine_failure = round(features_df.select(call_udf("predict_failure", col("A"),col("B"),col("C"),col("D"),col("E"),col("F"))).collect()[0][0], 3)

        st.write('The probability of Machine Failure:', machine_failure)
    else:
        st.write('Click Predict after selecting values')

if __name__ == "__main__":
    session = create_session()
    df = load_data(session)
    draw_sliders(session, df)
