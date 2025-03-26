# ProcLens.ai

ProcLens.ai is a **Streamlit-based** system monitoring and AI-powered assistant that provides **real-time process insights** using Ollama's AI models. This tool helps analyze system processes, detect anomalies, and answer user queries about running applications.

## 🚀 Features

- **Real-time System Process Monitoring**
- **AI-powered Insights using Ollama**
- **Interactive User Interface with Streamlit**
- **Background Process Updates**
- **Aesthetic UI with Smooth Animations**

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Ollama AI](https://ollama.ai/)
- `psutil`, `pandas`, `requests`

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/your-repo/proclens-ai.git
cd proclens-ai

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run Ollama locally
ollama serve &  # Ensure Ollama is running in the background

# Start the application
streamlit run app.py
```

## 📌 Usage

1. **Launch the application** with `streamlit run app.py`.
2. **View real-time processes** and their CPU/memory usage.
3. **Ask about a process** in the input box (e.g., *"Tell me about chrome.exe"*).
4. **Ollama provides insights** about the process using AI analysis.

## 🎨 Customization

- Modify `` in `app.py` to change the AI model (e.g., use `mistral` or `phi`).
- Adjust the **CSS in **`` to customize the UI.
- Set `refresh_interval` in `update_processes()` to control update frequency.

## 🛡️ Security Notes

- The tool **only reads system processes**; it does **not** modify or kill them.
- For advanced security, integrate with an antivirus API for malware detection.

## 🤖 API Integration

Ollama is queried using:

```python
api_url = "http://localhost:11434/api/generate"
payload = {
    "model": "mistral",
    "prompt": f"Tell me about {process_name}",
    "stream": False,
    "options": {"temperature": 0.7, "max_tokens": 256}
}
```

## 🏗️ Future Enhancements

- **Process Termination Feature** *(Admin only)*
- **Malware Process Detection** using threat intelligence databases
- **Resource Usage Graphs** for better visualization

## 📜 License

This project is **open-source** under the MIT License.

## 🤝 Contributing

1. Fork the repo 🍴
2. Create a feature branch 🔧 (`git checkout -b feature-name`)
3. Commit changes ✍️ (`git commit -m "Added new feature"`)
4. Push to the branch 🚀 (`git push origin feature-name`)
5. Open a PR on GitHub 🎉

## 💡 Credits

- **Ollama AI** for text-based insights
- **Streamlit** for UI framework
- **psutil** for system monitoring

👨‍💻 Developed by **[Your Name]**

