import streamlit as st
import time
import requests
import re
import plotly.express as px
import pandas as pd
from config import servers, monitoring_config

st.set_page_config(
    page_title="Server Monitoring",
    layout="wide"
    )

def read_logs_from_file(log_file):
    with open(log_file, 'r', encoding='utf-8') as file:
        logs = file.readlines()
    return logs

def read_logs_from_url(log_url):
    response = requests.get(log_url)
    if response.status_code == 200:
        logs = response.content.decode('utf-8').splitlines()
        return logs
    return []

def display_sys_log(log_file_or_url):
    logs = []
    if log_file_or_url.startswith("http://") or log_file_or_url.startswith("https://"):
        logs = read_logs_from_url(log_file_or_url)
    else:
        logs = read_logs_from_file(log_file_or_url)
    
    sys_log_list = []
    for log in reversed(logs[-monitoring_config['MAX_LOG_COUNT']:]):
        split_log = log.split('|')
        
        # 로그를 표시해주는 경우 
        if len(split_log) == 3:
            time = f":red[{split_log[0]}]"
            status = f":blue[{split_log[1]}]"
            messages = split_log[2]
            sys_log_list.append(f"{time}{status}{messages}")

        # 실행 시간을 같이 표기해주는 경우
        elif len(split_log) == 4:
            time = f":red[{split_log[0]}]"
            status = f":blue[{split_log[1]}]"
            function = f":green[{split_log[2]}]"
            messages = split_log[3]
            sys_log_list.append(f"{time}{status}{function}{messages}")
        else:
            sys_log_list.append(f"{log}")
    
    return sys_log_list

def display_hw_logs(log_file_or_url):
    logs = []
    if log_file_or_url.startswith("http://") or log_file_or_url.startswith("https://"):
        logs = read_logs_from_url(log_file_or_url)
    else:
        logs = read_logs_from_file(log_file_or_url)
    time_list, cpu_list, ram_list, ssd_list = [],[],[],[]
    for log in logs[-monitoring_config['MAX_LOG_COUNT']:]:  # 최신 로그 300개만 표시
        split_log = log.split('|')
        time_list.append(split_log[0][6:-2])
        cpu_list.append(extract_percentage(split_log[1][4:]))
        ram_list.append(extract_percentage(split_log[2][4:]))
        ssd_list.append(extract_percentage(split_log[3][4:]))
    return time_list, cpu_list, ram_list, ssd_list

def extract_percentage(s):
    """ 문자열에서 백분율 값만 추출 함수 """
    match = re.search(r'(\d+(\.\d+)?)', s)
    if match:
        return float(match.group(1))
    return None

  
def display_server_dashboard(hw_log_url: str, sys_log_url: str, server_name: str):
    time_list, cpu_list, ram_list, hdd_list = display_hw_logs(hw_log_url)
    data = {
        'Time': time_list,
        'CPU': cpu_list,
        'RAM': ram_list,
        'HDD': hdd_list
    }
    df = pd.DataFrame(data)

    st.title(f'{server_name} Server')
    st.subheader('Hardware Logs')
    
    placeholder = st.empty()
    with placeholder.container():
        sec1, sec2, sec3 = st.columns(3)
        sec1.metric(label="CPU", value=f'{cpu_list[-1]}%')  
        sec2.metric(label="RAM", value=f'{ram_list[-1]}%')
        sec3.metric(label="HDD", value=f'{hdd_list[-1]}%')

    fig = px.line(df, x='Time', y=df.columns[1:])
    fig.update_layout(autosize=True)
    fig.update_yaxes(range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader('Application Logs')
    sys_log = display_sys_log(sys_log_url)
    st.markdown("\n  \n".join(sys_log))
    time.sleep(5)
    st.rerun()


if 'selected_server' not in st.session_state:
    st.session_state.selected_server = servers[0]['name']  # 기본값 설정

# Sidebar Configuration
for server in servers:
    if st.sidebar.button(server['name']):
        st.session_state.selected_server = server['name']

selected_server_config = next(server for server in servers if server['name'] == st.session_state.selected_server)

display_server_dashboard(
    selected_server_config['hw_log_url'], 
    selected_server_config['sys_log_url'], 
    selected_server_config['name']
)