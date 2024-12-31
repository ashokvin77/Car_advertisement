import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
veh_ad = pd.read_csv('vehicles_us.csv')

# Create derived columns
veh_ad['brand'] = veh_ad['model'].str.split().str[0]
veh_ad['vehicle_age'] = 2019 - veh_ad['model_year']

# Title for the app
st.title("Vehicle Advertisement Data Analysis")

# Section 1: Scatter Plot - Price vs Mileage by Brand
st.header("Price vs Mileage by Brand")
price_mileage_scatter = px.scatter(
    veh_ad,
    x='odometer',
    y='price',
    color='brand',
    title='Vehicle Price vs. Mileage by Brand',
    opacity=0.4,
    template='seaborn'
)
price_mileage_scatter.update_layout(title={'x': 0.2})
st.plotly_chart(price_mileage_scatter)

# Section 2: Checkbox - Top Brands Filter
st.header("Distribution of Vehicle Types Across Top 10 Brands")
if st.checkbox("Show Top 10 Brands Only"):
    top_brands = veh_ad['brand'].value_counts().head(10).index
    filtered_veh_ad = veh_ad[veh_ad['brand'].isin(top_brands)]
    brand_type_counts = filtered_veh_ad.groupby(['brand', 'type']).size().reset_index(name='count')
    top_brands_bar = px.bar(
        brand_type_counts,
        x='brand',
        y='count',
        color='type',
        title='Distribution of Vehicle Types Across Top 10 Brands',
        labels={'brand': 'Brand', 'count': 'Number of Vehicles', 'type': 'Vehicle Type'},
        template='seaborn'
    )
    top_brands_bar.update_layout(
        xaxis_title='Brand',
        yaxis_title='Number of Vehicles',
        barmode='stack',
        title={'x': 0.2}
    )
    st.plotly_chart(top_brands_bar)

# Section 3: High Mileage Vehicles Bar Plot
st.header("High Mileage Vehicles")
if st.checkbox("Show Vehicles with Odometer > 200,000"):
    high_mileage_vehicles = veh_ad[veh_ad['odometer'] > 200000]
    type_counts = high_mileage_vehicles['type'].value_counts().reset_index()
    type_counts.columns = ['vehicle_type', 'vehicle_count']
    high_mileage_bar = px.bar(
        type_counts,
        x='vehicle_type',
        y='vehicle_count',
        title='Most Prevalent Vehicle Types for Mileage > 200,000',
        labels={'vehicle_type': 'Vehicle Type', 'vehicle_count': 'Number of Vehicles'},
        template='seaborn',
        color_discrete_sequence=['#636EFA']
    )
    high_mileage_bar.update_layout(
        xaxis_title='Vehicle Type',
        yaxis_title='Number of Vehicles',
        showlegend=False,
        title={'x': 0.2}
    )
    st.plotly_chart(high_mileage_bar)

# Section 4: Average Price by Color
st.header("Average Price by Vehicle Color")
price_color = px.bar(
    veh_ad.groupby('paint_color')['price'].mean().reset_index(),
    x='paint_color',
    y='price',
    title='Average Price of Vehicles by Color',
    labels={'paint_color': 'Vehicle Color', 'price': 'Average Price ($)'},
    template='seaborn',
    color_discrete_sequence=['#636EFA']
)
price_color.update_layout(
    xaxis_title='Vehicle Color',
    yaxis_title='Average Price ($)',
    showlegend=False,
    title={'x': 0.2}
)
st.plotly_chart(price_color)

# Section 5: Histogram - Vehicle Distribution by Condition and Year
st.header("Vehicle Distribution by Condition and Year")
pivot_year_condition = veh_ad.pivot_table(
    index='model_year', 
    columns='condition', 
    values='price', 
    aggfunc='count'
)
pivot_year_condition_reset = pivot_year_condition.reset_index().melt(
    id_vars='model_year',
    var_name='condition',
    value_name='count'
)
year_hist = px.histogram(
    pivot_year_condition_reset,
    x='model_year',
    y='count',
    color='condition',
    title='Vehicle Distribution by Condition and Year',
    opacity=0.7,
    template='seaborn'
)
year_hist.update_layout(
    xaxis_title='Model Year',
    yaxis_title='Count of Vehicles',
    title={'x': 0.2}
)
st.plotly_chart(year_hist)

# Section 6: Number of Vehicles by Color
st.header("Number of Vehicles by Color")
color_frequency = veh_ad['paint_color'].value_counts().reset_index()
color_frequency.columns = ['paint_color', 'vehicle_count']
color_bar = px.bar(
    color_frequency,
    x='paint_color',
    y='vehicle_count',
    title='Number of Vehicles by Color',
    labels={'paint_color': 'Vehicle Color', 'vehicle_count': 'Number of Vehicles'},
    template='seaborn',
    color_discrete_sequence=['#636EFA']
)
color_bar.update_layout(
    xaxis_title='Vehicle Color',
    yaxis_title='Number of Vehicles',
    showlegend=False,
    title={'x': 0.2}
)
st.plotly_chart(color_bar)

# Section 7: Average Mileage for Vehicles < 10 Years Old by Brand
st.header("Average Mileage for Vehicles < 10 Years Old by Brand")
recent_vehicles = veh_ad[veh_ad['vehicle_age'] < 10]
average_mileage_by_brand = recent_vehicles.groupby('brand').agg(
    avg_mileage=('odometer', 'mean'),
    std_mileage=('odometer', 'std'),
    vehicle_count=('odometer', 'size')
).reset_index()
average_mileage_by_brand = average_mileage_by_brand.sort_values(by='avg_mileage', ascending=False)
recent_veh_bar = px.bar(
    average_mileage_by_brand,
    x='brand',
    y='avg_mileage',
    error_y='std_mileage',
    title='Average Mileage for Vehicles < 10 Years Old by Brand',
    labels={'brand': 'Brand', 'avg_mileage': 'Average Mileage (miles)'},
    hover_data={'vehicle_count': True},
    template='seaborn',
    color_discrete_sequence=['#636EFA']
)
recent_veh_bar.update_layout(
    xaxis_title='Brand',
    yaxis_title='Average Mileage (miles)',
    showlegend=False,
    title={'x': 0.2}
)
st.plotly_chart(recent_veh_bar)
