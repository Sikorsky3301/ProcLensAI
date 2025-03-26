import streamlit as st
import psutil
import pandas as pd
import time
import requests
import threading
import subprocess

OLLAMA_PORT = "11434"

def load_css():
    """Load custom CSS from external file."""
    with open("style.css", "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def is_ollama_running():
    try:
        response = requests.get(f"http://localhost:{OLLAMA_PORT}/api/tags", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_ollama():
    if not is_ollama_running():
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)

def get_system_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_times', 'memory_info']):
        try:
            process_info = proc.info
            cpu_time = process_info['cpu_times'].user + process_info['cpu_times'].system
            memory_info = process_info['memory_info']
            processes.append({
                'pid': process_info['pid'],
                'name': process_info['name'],
                'status': process_info['status'],
                'cpu_kb': cpu_time / 1000,
                'memory_kb': memory_info.rss / 1024
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    processes.sort(key=lambda x: x['memory_kb'], reverse=True)
    return processes[:50]

def query_ollama(user_query, context):
    api_url = f"http://localhost:{OLLAMA_PORT}/api/generate"
    payload = {
        "model": "phi",
        "prompt": context + "\n" + user_query,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "max_tokens": 256
        }
    }

    with st.spinner("Generating response..."):
        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                return response.json().get("response", "No response from Ollama.")
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Failed to connect to Ollama: {e}"

def update_processes():
    while True:
        st.session_state.processes = get_system_processes()
        time.sleep(5)

def main():
    st.set_page_config(page_title="ProcLens.ai", page_icon="🖥️", layout="wide")
    load_css()

    st.markdown('<h1 class="big-title">ProcLens.ai 🖥️</h1>', unsafe_allow_html=True)
    start_ollama()

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'processes' not in st.session_state:
        with st.spinner("Fetching system processes..."):
            st.session_state.processes = get_system_processes()

    if 'thread' not in st.session_state:
        st.session_state.thread = threading.Thread(target=update_processes)
        st.session_state.thread.daemon = True
        st.session_state.thread.start()

    with st.expander("🔍 **System Processes**", expanded=True):
        if st.session_state.processes:
            df = pd.DataFrame(st.session_state.processes)
            df['cpu_kb'] = df['cpu_kb'].map(lambda x: f"{x:.2f} K")
            df['memory_kb'] = df['memory_kb'].map(lambda x: f"{x:.2f} K")
            st.dataframe(df, width=1200)
        else:
            st.warning("No processes found or insufficient permissions.")

    st.subheader("🧠 Ask Ollama about System Processes")
    user_query = st.text_input("Enter your question here:")

    if user_query:
        context = "System processes: " + ", ".join(
            [f"PID: {proc['pid']}, Name: {proc['name']}, Status: {proc['status']}, CPU KB: {proc['cpu_kb']}, Memory KB: {proc['memory_kb']}"
             for proc in st.session_state.processes]
        )

        response = query_ollama(user_query, context)
        st.session_state.chat_history.append(response)

        st.subheader("🤖 Ollama Response")
        st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
