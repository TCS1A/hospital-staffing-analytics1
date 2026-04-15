import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='Hospital Staffing Analytics',
    page_icon='🏥',
    layout='wide'
)

# ── Load Data ──
@st.cache_data
def load_data():
    df = pd.read_csv('data/PBJ_Daily_Nurse_Staffing_Q2_2024.csv',
                     encoding='latin-1',
                     low_memory=False)
    df['total_nurse_hrs'] = df['Hrs_RN'] + df['Hrs_LPN'] + df['Hrs_CNA']
    df['nurse_patient_ratio'] = df['total_nurse_hrs'] / df['MDScensus'].replace(0, pd.NA)
    df['emp_hrs_total'] = df['Hrs_RN_emp'] + df['Hrs_LPN_emp'] + df['Hrs_CNA_emp']
    df['ctr_hrs_total'] = df['Hrs_RN_ctr'] + df['Hrs_LPN_ctr'] + df['Hrs_CNA_ctr']
    df['WorkDate'] = pd.to_datetime(df['WorkDate'].astype(str))
    df['Month'] = df['WorkDate'].dt.to_period('M').astype(str)
    return df

with st.spinner('Loading 1.3 million records...'):
    df = load_data()

# ── Header ──
st.title('🏥 Hospital Staffing Analytics')
st.markdown('**Q2 2024 — CMS Payroll-Based Journal (PBJ) Data**')
st.divider()

# ── Sidebar Filters ──
st.sidebar.header('Filters')
states = ['All States'] + sorted(df['STATE'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox('Select State', states)

if selected_state != 'All States':
    filtered = df[df['STATE'] == selected_state]
else:
    filtered = df

# ── KPI Cards ──
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    '🏨 Total Facilities',
    f"{filtered['PROVNUM'].nunique():,}"
)
col2.metric(
    '👥 Avg Patients/Day',
    f"{filtered['MDScensus'].mean():.1f}"
)
col3.metric(
    '⏱️ Avg Nurse Hours/Day',
    f"{filtered['total_nurse_hrs'].mean():.1f}"
)
col4.metric(
    '📊 Avg Nurse:Patient Ratio',
    f"{filtered['nurse_patient_ratio'].mean():.2f}"
)

st.divider()

# ── Row 1: Two charts side by side ──
col_left, col_right = st.columns(2)

with col_left:
    st.subheader('Nurse-to-Patient Ratio by State')
    ratio_state = filtered.groupby('STATE')['nurse_patient_ratio'] \
                          .mean().round(2) \
                          .sort_values(ascending=False) \
                          .reset_index()
    ratio_state.columns = ['State', 'Ratio']
    fig1 = px.bar(
        ratio_state.head(20),
        x='State', y='Ratio',
        color='Ratio',
        color_continuous_scale='Blues',
        labels={'Ratio': 'Nurse:Patient Ratio'}
    )
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader('Total Nursing Hours by State')
    hours_state = filtered.groupby('STATE')['total_nurse_hrs'] \
                          .sum().round(0) \
                          .sort_values(ascending=False) \
                          .reset_index()
    hours_state.columns = ['State', 'Total Hours']
    fig2 = px.bar(
        hours_state.head(20),
        x='State', y='Total Hours',
        color='Total Hours',
        color_continuous_scale='Teal',
        labels={'Total Hours': 'Total Nurse Hours'}
    )
    fig2.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Row 2: Map + Pie ──
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader('Nurse-to-Patient Ratio Map')
    map_data = df.groupby('STATE')['nurse_patient_ratio'] \
                 .mean().round(2).reset_index()
    map_data.columns = ['State', 'Ratio']
    fig3 = px.choropleth(
        map_data,
        locations='State',
        locationmode='USA-states',
        color='Ratio',
        scope='usa',
        color_continuous_scale='RdYlGn',
        labels={'Ratio': 'Nurse:Patient Ratio'}
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader('Employee vs Contract Staff Hours')
    total_emp = filtered['emp_hrs_total'].sum()
    total_ctr = filtered['ctr_hrs_total'].sum()
    pie_data = pd.DataFrame({
        'Type': ['Employee', 'Contract'],
        'Hours': [total_emp, total_ctr]
    })
    fig4 = px.pie(
        pie_data,
        names='Type',
        values='Hours',
        color_discrete_sequence=['#2E75B6', '#1E8449'],
        hole=0.4
    )
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ── Row 3: Census Trend + Understaffed Table ──
col_left3, col_right3 = st.columns(2)

with col_left3:
    st.subheader('Patient Census Trend Over Time')
    trend = filtered.groupby('Month').agg(
        Avg_Patients=('MDScensus', 'mean')
    ).round(1).reset_index()
    fig5 = px.line(
        trend,
        x='Month', y='Avg_Patients',
        markers=True,
        labels={'Avg_Patients': 'Avg Patients', 'Month': 'Month'},
        color_discrete_sequence=['#2E75B6']
    )
    fig5.update_layout(height=400)
    st.plotly_chart(fig5, use_container_width=True)

with col_right3:
    st.subheader('Most Understaffed Facilities')
    understaffed = filtered.groupby('PROVNUM').agg(
        Facility=('PROVNAME', 'first'),
        State=('STATE', 'first'),
        Avg_Patients=('MDScensus', 'mean'),
        Avg_Nurse_Hrs=('total_nurse_hrs', 'mean')
    ).reset_index()
    understaffed['Ratio'] = (
        understaffed['Avg_Nurse_Hrs'] /
        understaffed['Avg_Patients'].replace(0, pd.NA)
    ).round(2)
    understaffed = understaffed.dropna(subset=['Ratio']) \
                               .sort_values('Ratio') \
                               .head(10)
    st.dataframe(
        understaffed[['Facility', 'State', 'Avg_Patients', 'Ratio']],
        use_container_width=True,
        height=380
    )

st.divider()
st.caption('Data source: CMS Payroll-Based Journal (PBJ) Q2 2024 | Built with Streamlit & Plotly')