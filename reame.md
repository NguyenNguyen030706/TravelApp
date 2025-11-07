
## ✅ 1. Chuẩn bị
- Cài **Ollama**: https://ollama.com/download
- Python 3.9+
- VSCode
## ✅ 2. Kiểm tra Ollama
```powershell
ollama list
```
## ✅ 3. Tải model nhẹ nhất
```powershell
ollama pull phi3:mini
```
## ✅ 4. Cài thư viện Python
```powershell
pip install streamlit ollama
```
## ✅ 5. Chạy ứng dụng
```powershell
python -m streamlit run app.py
```
Sau đó mở: `http://localhost:8501`
## ✅ 6. Cấu hình model trong app.py
```python
model="phi3:mini"
```
