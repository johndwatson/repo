import streamlit as st
import snowflake.connector


snw_conn = {'user': 'john.watson@uscca.com',
            'password': '25AfT4ccTbdSFJcaSF',
            'account': 'deltadefense-analytics',
            'warehouse': 'compute_wh'}

# Connect to Snowflake and configure
print("Connecting to Snowflake")
snw_conn = snowflake.connector.connect(**snw_conn)
snw_curs = snw_conn.cursor(snowflake.connector.DictCursor)

# Set roles
snw_curs.execute("use role sysadmin")
snw_curs.execute("use database domo_dev")
snw_curs.execute("use schema lk")

st.write("# 2022 Registrants per month :memo:")

snw_curs.execute("Select count(distinct registrant_id) as registrants_per_month, date_part(month, created_at) as month_created from DOMO_DEV.LK_TRAINING.REGISTRANTS where created_at >= '2022-01-01' group by date_part(month, created_at) order by 2")
df = snw_curs.fetch_pandas_all()
st.dataframe(df.style.highlight_max(axis=0))

st.line_chart(df)
