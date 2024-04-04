import altair as alt
import pandas as pd
import streamlit as st


df2 = pd.read_excel("CanesPHRevenue.xlsx")
discounts = pd.read_excel("CanesDiscounts.xlsx")
cluster = pd.read_csv("PlansSold.csv")

st.sidebar.write("Cluster One Loyalty Discount: Pure Hockey Plan Holder 0-9 Years")
st.sidebar.write("Cluster Two Loyalty Discount: Pure Hockey Plan Holder 10-14 Years")
st.sidebar.write("Cluster Three Loyalty Discount: Pure Hockey Plan Holder 15-19 Years")
st.sidebar.write("Cluster Four Loyalty Discount: Pure Hockey Plan Holder 20+ Years")
discounts['Discount'] = (discounts['Discount'] * 100).astype(str) + '%'
st.sidebar.dataframe(discounts)

selected_renewal = st.selectbox(
    "Please select an expected Pure Hockey->Regular Season Ticket Member upgrade percentage.",
    [100, 75, 50, 25],
)


df2["Projected Revenue"]= df2['ProjectUpgradeRevenue'] * (selected_renewal / 100.0)
df2["Projected Revenue with Discount"]= df2['DiscountProfit'] * (selected_renewal / 100.0)

df3 = df2[["Clusters","Projected Revenue","Projected Revenue with Discount"]]
#df3['Projected Revenue'] = df3['Projected Revenue'].apply(lambda x: f"${x:,.2f}")
#df3['Projected Revenue with Discount'] = df3['Projected Revenue with Discount'].apply(lambda x: f"${x:,.2f}")

# Calculate the subtotal of the 'Amount' column
subtotal = df3['Projected Revenue'].sum()
subtotal2 = df3['Projected Revenue with Discount'].sum()

# Append a new row with the subtotal. Assign a specific value (like 'Total') to the other columns if necessary
subtotal_row = pd.DataFrame({'Projected Revenue': [subtotal], 'Projected Revenue with Discount': [subtotal2]})

# Append subtotal_row to the original df3
df3_with_total = pd.concat([df3, subtotal_row], ignore_index=True)

# Optional: If displaying as currency, format the 'Amount' column, including the new subtotal row
df3_with_total['Projected Revenue'] = df3_with_total['Projected Revenue'].apply(lambda x: f"${x:,.2f}")
df3_with_total['Projected Revenue with Discount'] = df3_with_total['Projected Revenue with Discount'].apply(lambda x: f"${x:,.2f}")
df3_with_total.loc[4, 'Clusters'] = 'Totals'
st.dataframe(df3_with_total)

cluster.rename(columns={'Clust1': 'Clusters'}, inplace=True)
cluster.rename(columns={'Num Seats': 'Number of Seats'}, inplace=True)
cluster.rename(columns={'Years Since': 'Years Since Buying Pure Hockey Plan'}, inplace=True)

categories_of_interest = ['New Pure Hockey', 'Renew PH Platinum','Renew PH Upgrade','Renew Pure Hockey','Sideline PH Renewal','Sponsor PH Full Season','Updated PH Renew','Updated Pure Hockey']

# Filter the DataFrame based on categories
filtered_df = cluster.loc[cluster['Ticket Type'].isin(categories_of_interest)]

alt_chart = (
    alt.Chart(filtered_df, title="Pure Hockey Loyalty Clusters")
    .mark_circle()
    .encode(
        x='Years Since Buying Pure Hockey Plan',
        y='Number of Seats',
        color=alt.Color("Clusters", scale=alt.Scale(range=['orange', 'blue', 'red', 'green'])),
    )
    .interactive()
)

st.altair_chart(alt_chart, use_container_width=True)
#x_val = st.sidebar.selectbox("Pick your x-axis",who_data.select_dtypes(include=np.number).columns.tolist())
#y_val = st.sidebar.selectbox("Pick your y-axis",who_data.select_dtypes(include=np.number).columns.tolist())


#barchart = alt.Chart(df, title = "Bar chart").mark_bar().encode(
#    x='Cluster Number:N',
#    y='OG PH Base Price'
#)

#bchart = alt.Chart(df).mark_bar().encode(
#    x='Cluster Number:N',  # Treat 'Value' as nominal (categorical) data
#    y=alt.Y('sum(OG PH Base Price):Q', axis=alt.Axis(title='Total Amount')),
#)

#st.altair_chart(barchart,use_container_width=True)
#st.altair_chart(bchart,use_container_width=True)