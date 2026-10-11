# Curriculum AI thực chiến (Jupyter)

Chương trình dạy AI bằng Jupyter Notebook cho người **đã biết lập trình ngôn ngữ khác**, Python gần như mới.

Thứ tự: nền tảng Python/data → dự đoán giá nhà → phân loại cảm xúc → chatbot RAG.

## Yêu cầu

- Windows 10/11
- Python 3.11+ (`python --version`)
- (Tuỳ chọn, cho bài RAG) API key OpenAI — xem `.env.example`

## Cài môi trường

Mở PowerShell tại thư mục gốc dự án:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements\rag.txt
python -m ipykernel install --user --name python3 --display-name "Python 3 (AIOT)"
```

Chỉ học đến bài ML (chưa RAG) thì có thể dùng:

```powershell
pip install -r requirements\ml.txt
```

## Chạy Jupyter

```powershell
.\.venv\Scripts\Activate.ps1
jupyter lab
```

Trong Jupyter, chọn kernel **Python 3 (AIOT)** (hoặc Python 3 từ `.venv`).

## Thứ tự học

| # | Notebook | Mục tiêu |
|---|----------|----------|
| 0 | `notebooks/00_setup_and_python/00_python_for_coders.ipynb` | Python + Pandas tối thiểu |
| 1 | `notebooks/01_house_price/01_train_and_predict.ipynb` | Supervised ML tabular |
| 2 | `notebooks/02_sentiment/02_text_classify.ipynb` | NLP cổ điển (TF-IDF) |
| 2b | `notebooks/02_sentiment/api_predict.py` | FastAPI `POST /predict` |
| 3a | `notebooks/03_rag_chatbot/03a_load_split_pdf.ipynb` | Load PDF + chunk |
| 3b | `notebooks/03_rag_chatbot/03b_embeddings_chroma.ipynb` | Embedding + Chroma |
| 3c | `notebooks/03_rag_chatbot/03c_rag_qa.ipynb` | Prompt + hỏi đáp RAG |

Tài liệu gốc nằm trong `docs/`. Dataset mẫu nằm trong `data/`.

## API key cho RAG

```powershell
copy .env.example .env
# Mở .env và dán OPENAI_API_KEY
```

Notebook RAG đọc key từ biến môi trường / file `.env` ở thư mục gốc — **không** ghi key vào cell.

## Chạy FastAPI (sau bài sentiment)

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn notebooks.02_sentiment.api_predict:app --reload --app-dir .
```

Hoặc từ thư mục `notebooks/02_sentiment`:

```powershell
uvicorn api_predict:app --reload
```

## Smoke-test (offline)

Không cần API key — chạy notebook 00 → 03a + kiểm tra import RAG:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts\smoke_test.py
```

Notebook `03b` / `03c` cần `OPENAI_API_KEY` trong `.env`.

## Ghi chú

- YOLO, recommendation, app Microsoft Store: **chưa** thuộc giai đoạn này.
- Mỗi notebook có: mục tiêu → kiến thức cần nhớ → code chú thích → bài tập → checklist.
- LangChain 1.x: helper `create_retrieval_chain` nằm trong `langchain_classic` (đã ghi trong notebook 03c).
- Tái tạo notebook từ script: `python scripts\build_notebooks.py`
