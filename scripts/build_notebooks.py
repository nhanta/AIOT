"""Generate curriculum notebooks as nbformat v4 JSON."""
from __future__ import annotations

import json
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def nb(cells: list[tuple[str, str]]) -> dict:
    out = []
    for ctype, src in cells:
        src = src.strip("\n") + "\n"
        lines = src.splitlines(keepends=True)
        cell_id = uuid.uuid4().hex[:8]
        if ctype == "md":
            out.append(
                {
                    "cell_type": "markdown",
                    "id": cell_id,
                    "metadata": {},
                    "source": lines,
                }
            )
        else:
            out.append(
                {
                    "cell_type": "code",
                    "id": cell_id,
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": lines,
                }
            )
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": out,
    }


def save(rel: str, cells: list[tuple[str, str]]) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb(cells), ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def build_00() -> None:
    save(
        "notebooks/00_setup_and_python/00_python_for_coders.ipynb",
        [
            (
                "md",
                """# 00 — Python cho người đã biết lập trình

## Mục tiêu
- Chạy được Jupyter notebook trong môi trường dự án.
- Map khái niệm từ ngôn ngữ cũ (JS/C#/Java…) sang Python.
- Thao tác DataFrame bằng Pandas ở mức tối thiểu.

## Kiến thức cần nhớ
- Python dùng thụt lề thay cho `{}`.
- `list` ≈ array, `dict` ≈ map/object.
- `pip` + `venv` quản lý thư viện theo dự án.
- Pandas: bảng dữ liệu (`DataFrame`) — chọn cột, lọc hàng, `describe()`.

## Checklist cuối bài
Bạn đã hiểu khi: tự chạy hết notebook, sửa 1 hàm, lọc được vài hàng CSV.""",
            ),
            ("md", "## 1. Kiểm tra môi trường"),
            (
                "code",
                """import sys
print("Python:", sys.version)
print("OK — nếu thấy 3.11+ là ổn.")""",
            ),
            (
                "md",
                """## 2. Biến, kiểu dữ liệu, f-string

Giống hầu hết ngôn ngữ: gán biến bằng `=`. Không cần khai báo kiểu.""",
            ),
            (
                "code",
                """ten = "An"
tuoi = 25
diem = 8.5
dang_hoc = True

# f-string ~ template string
msg = f"{ten} ({tuoi} tuoi) dat {diem} diem. Dang hoc? {dang_hoc}"
print(msg)
print(type(ten), type(tuoi), type(diem), type(dang_hoc))""",
            ),
            ("md", "## 3. List và dict"),
            (
                "code",
                """# list — thứ tự, có thể trùng
skills = ["python", "git", "sql"]
skills.append("pandas")
print(skills[0], skills[-1], len(skills))

# dict — key/value
hoc_vien = {"ten": "An", "ngon_ngu_cu": "C#", "muc_tieu": "AI"}
print(hoc_vien["ten"], hoc_vien.get("muc_tieu"))
print(list(hoc_vien.keys()))""",
            ),
            ("md", "## 4. Hàm, if, for"),
            (
                "code",
                """def chao(ten: str, lan: int = 1) -> str:
    \"\"\"Docstring: mo ta ham — tuong tu comment XML/JSDoc.\"\"\"
    if lan <= 0:
        return "(khong chao)"
    return " | ".join([f"Xin chao {ten}!" for _ in range(lan)])

print(chao("An"))
print(chao("An", 3))

for i, skill in enumerate(["python", "ml", "rag"], start=1):
    print(f"{i}. hoc {skill}")""",
            ),
            ("md", "## 5. Đọc / ghi file text"),
            (
                "code",
                """from pathlib import Path

sample = Path("../../data/_hello.txt")
sample.parent.mkdir(parents=True, exist_ok=True)
sample.write_text("dong 1\\ndong 2\\n", encoding="utf-8")
print(sample.read_text(encoding="utf-8"))
print("Ton tai?", sample.exists())""",
            ),
            (
                "md",
                """## 6. Import và hệ sinh thái pip

Trong terminal (đã activate `.venv`): `pip install pandas`

Trong notebook: import module đã cài.""",
            ),
            (
                "code",
                """import math
from statistics import mean

nums = [3, 5, 7, 9]
print("sqrt(16) =", math.sqrt(16))
print("mean =", mean(nums))""",
            ),
            (
                "md",
                """## 7. Pandas tối thiểu

Dataset mẫu: `data/nha_gia.csv` (sẽ dùng lại ở bài 01).""",
            ),
            (
                "code",
                """from pathlib import Path
import pandas as pd

# Notebook nam trong notebooks/00_..., len 2 cap ve goc repo
DATA = Path("../../data/nha_gia.csv")
df = pd.read_csv(DATA)

print("Shape:", df.shape)          # (so hang, so cot)
print("Cot:", list(df.columns))
df.head()""",
            ),
            (
                "code",
                """# Chon cot
print(df[["dien_tich_m2", "gia_trieu_vnd"]].head())

# Loc hang: nha >= 80 m2
lon = df[df["dien_tich_m2"] >= 80]
print("So nha >= 80m2:", len(lon))

# Thong ke nhanh
df[["dien_tich_m2", "gia_trieu_vnd"]].describe()""",
            ),
            (
                "md",
                """## Bài tập nhỏ

1. Lọc các căn có `so_phong_ngu >= 3` và in `shape`.
2. Tính giá trung bình (`mean`) theo từng `quan` — gợi ý: `df.groupby("quan")["gia_trieu_vnd"].mean()`.
3. Viết hàm `tom_tat(df)` trả về chuỗi gồm số hàng và giá max.""",
            ),
            (
                "code",
                """# TODO: lam bai tap o day
# lon_3pn = ...
# gia_theo_quan = ...
# def tom_tat(df): ...""",
            ),
            (
                "md",
                """## Checklist — đã hiểu khi…
- [ ] Chạy được cell theo thứ tự, không lỗi import
- [ ] Phân biệt `list` / `dict` / `DataFrame`
- [ ] Lọc được hàng bằng điều kiện Boolean trên cột
- [ ] Biết đường dẫn tương đối từ notebook về `data/`""",
            ),
        ],
    )


def build_01() -> None:
    save(
        "notebooks/01_house_price/01_train_and_predict.ipynb",
        [
            (
                "md",
                """# 01 — Dự đoán giá nhà (Supervised ML)

## Mục tiêu
- Hiểu pipeline: dữ liệu → feature/label → train/test → model → đánh giá → dự đoán mới.
- Dùng Scikit-learn trên bài toán hồi quy (regression).

## Kiến thức cần nhớ
- **Supervised learning**: có nhãn (ở đây là `gia_trieu_vnd`).
- **Feature** = đầu vào (diện tích, số phòng…); **label** = giá trị cần đoán.
- **Train/test split**: giữ một phần dữ liệu để kiểm tra model có bị nhớ máy không.
- **Overfitting**: điểm train rất tốt nhưng test kém — model “học thuộc” thay vì khái quát.

Công cụ: Pandas, Scikit-learn (Random Forest).""",
            ),
            ("md", "## 1. Load và xem dữ liệu"),
            (
                "code",
                """from pathlib import Path
import pandas as pd

DATA = Path("../../data/nha_gia.csv")
df = pd.read_csv(DATA)
print(df.shape)
df.head()""",
            ),
            (
                "code",
                """# EDA ngan
print(df["gia_trieu_vnd"].describe())
print("\\nTuong quan so voi gia:")
print(df.corr(numeric_only=True)["gia_trieu_vnd"].sort_values(ascending=False))""",
            ),
            (
                "md",
                """## 2. Chuẩn bị feature / label

Cột `quan` là categorical → one-hot encode. Các cột số giữ nguyên.""",
            ),
            (
                "code",
                """from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

feature_cols = ["dien_tich_m2", "so_phong_ngu", "so_phong_tam", "tuoi_nha_nam", "so_tang", "quan"]
label_col = "gia_trieu_vnd"

X = df[feature_cols]
y = df[label_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Train:", X_train.shape, "Test:", X_test.shape)""",
            ),
            ("md", "## 3. Pipeline: encode + Random Forest"),
            (
                "code",
                """numeric_features = ["dien_tich_m2", "so_phong_ngu", "so_phong_tam", "tuoi_nha_nam", "so_tang"]
categorical_features = ["quan"]

preprocess = ColumnTransformer(
    transformers=[
        ("num", "passthrough", numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

model = Pipeline(
    steps=[
        ("prep", preprocess),
        ("rf", RandomForestRegressor(n_estimators=200, random_state=42)),
    ]
)

model.fit(X_train, y_train)
print("Da train xong.")""",
            ),
            ("md", "## 4. Đánh giá MAE / RMSE"),
            (
                "code",
                """pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)
rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
print(f"MAE  = {mae:.2f} trieu VND  (sai so tuyet doi trung binh)")
print(f"RMSE = {rmse:.2f} trieu VND")

# So sanh nhanh 5 mau
so_sanh = X_test.copy()
so_sanh["gia_that"] = y_test.values
so_sanh["gia_du_doan"] = pred.round(1)
so_sanh.head()""",
            ),
            (
                "md",
                """## 5. Dự đoán căn nhà mới

Nhập số phòng ngủ, diện tích, quận… giống tính năng định giá.""",
            ),
            (
                "code",
                """nha_moi = pd.DataFrame(
    [
        {
            "dien_tich_m2": 72.0,
            "so_phong_ngu": 2,
            "so_phong_tam": 2,
            "tuoi_nha_nam": 5,
            "so_tang": 2,
            "quan": "Quan 7",
        }
    ]
)
gia_du_doan = model.predict(nha_moi)[0]
print(f"Gia du doan: {gia_du_doan:.1f} trieu VND")""",
            ),
            (
                "md",
                """## Giải thích cho bạn (đọc to)

1. Model **không** nhớ từng căn nhà; nó học quy luật từ feature → giá.
2. MAE ~ \"trung bình mỗi lần đoán lệch bao nhiêu triệu\".
3. Nếu train rất tốt mà test kém → nghi **overfitting** (thử model đơn giản hơn hoặc thêm data).""",
            ),
            (
                "md",
                """## Bài tập nhỏ

1. Đổi `RandomForestRegressor` sang `LinearRegression` (import từ `sklearn.linear_model`) và so sánh MAE.
2. Thử căn nhà ở `Go Vap`, 45m2, 1 phòng ngủ — giá dự đoán thay đổi thế nào?
3. Vẽ scatter `y_test` vs `pred` bằng matplotlib (tuỳ chọn).""",
            ),
            (
                "code",
                """# TODO: bai tap
# from sklearn.linear_model import LinearRegression
# ...""",
            ),
            (
                "md",
                """## Checklist — đã hiểu khi…
- [ ] Nói được feature / label / train-test trong bài này là gì
- [ ] Chạy được pipeline và đọc MAE
- [ ] Dự đoán được 1 căn nhà mới bằng `model.predict`
- [ ] Giải thích overfitting bằng 1 câu""",
            ),
        ],
    )


def build_02() -> None:
    save(
        "notebooks/02_sentiment/02_text_classify.ipynb",
        [
            (
                "md",
                """# 02 — Phân loại cảm xúc bình luận (NLP cổ điển)

## Mục tiêu
- Biến text thành số bằng **TF-IDF** (không dùng LLM).
- Train classifier (Logistic Regression) để gắn nhãn positive / negative / neutral.
- Chuẩn bị tư duy cho embedding ở bài RAG (vẫn là \"text → vector\", nhưng cách khác).

## Kiến thức cần nhớ
- Tabular ML dùng cột số; NLP cổ điển cần **vector hóa** câu trước.
- TF-IDF: từ xuất hiện nhiều trong 1 câu nhưng ít trong toàn corpus → quan trọng hơn.
- Accuracy / F1 đo chất lượng phân loại.

Dataset: `data/binh_luan.csv`.""",
            ),
            ("md", "## 1. Load dữ liệu"),
            (
                "code",
                """from pathlib import Path
import pandas as pd

DATA = Path("../../data/binh_luan.csv")
df = pd.read_csv(DATA)
print(df.shape)
print(df["label"].value_counts())
df.head()""",
            ),
            ("md", "## 2. Train/test + TF-IDF + Logistic Regression"),
            (
                "code",
                """from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
)

clf = Pipeline(
    steps=[
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("lr", LogisticRegression(max_iter=1000)),
    ]
)
clf.fit(X_train, y_train)

pred = clf.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred))""",
            ),
            ("md", "## 3. Thử vài câu mới"),
            (
                "code",
                """mau = [
    "San pham tot qua, se mua lai",
    "That vong, hang loi",
    "Tam on, khong co gi dac biet",
]
for c in mau:
    print(c, "->", clf.predict([c])[0])""",
            ),
            ("md", "## 4. Lưu model để FastAPI dùng"),
            (
                "code",
                """from pathlib import Path

MODEL_PATH = Path("../../data/sentiment_model.joblib")
joblib.dump(clf, MODEL_PATH)
print("Saved:", MODEL_PATH.resolve())""",
            ),
            (
                "md",
                """## 5. Gọi API (sau khi chạy uvicorn)

Trong terminal:

```powershell
cd notebooks\\02_sentiment
uvicorn api_predict:app --reload
```

Rồi test (terminal khác hoặc cell dưới với `httpx`/`requests`).""",
            ),
            (
                "code",
                """# Tuy chon: goi API neu dang chay
import json

try:
    import urllib.request

    body = json.dumps({"text": "Chat luong kem"}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000/predict",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=2) as resp:
        print(resp.read().decode("utf-8"))
except Exception as e:
    print("API chua chay hoac loi:", type(e).__name__, e)
    print("Bo qua cell nay neu ban chua mo uvicorn.")""",
            ),
            (
                "md",
                """## Bài tập nhỏ

1. Thêm 3 câu bình luận mới vào CSV (hoặc list), train lại, xem F1 có đổi không.
2. Đổi `LogisticRegression` sang `MultinomialNB` (`sklearn.naive_bayes`) và so sánh accuracy.
3. Giải thích khác biệt TF-IDF vs embedding (bài RAG) bằng 2–3 câu.""",
            ),
            (
                "code",
                """# TODO: bai tap
# from sklearn.naive_bayes import MultinomialNB""",
            ),
            (
                "md",
                """## Checklist — đã hiểu khi…
- [ ] Nói được vì sao text cần vector hóa trước khi đưa vào model
- [ ] Đọc được accuracy / F1 từ `classification_report`
- [ ] Lưu được model bằng `joblib`
- [ ] Biết chạy `uvicorn api_predict:app --reload`""",
            ),
        ],
    )


def build_03a() -> None:
    save(
        "notebooks/03_rag_chatbot/03a_load_split_pdf.ipynb",
        [
            (
                "md",
                """# 03a — Load PDF và cắt chunk

## Mục tiêu
- Đọc PDF bằng `PyPDFLoader`.
- Cắt văn bản thành chunk (~1000 ký tự) với overlap 200 để không đứt ý.

## Kiến thức cần nhớ
- LLM có **context window** giới hạn → không nhét cả cuốn sách mỗi lần hỏi.
- **Chunk + overlap**: giữ liên kết giữa các đoạn liền kề.
- Corpus demo: 2 file PDF trong `docs/`.

Bước tiếp: 03b (embedding + Chroma).""",
            ),
            ("md", "## 1. Tìm PDF trong docs/"),
            (
                "code",
                """from pathlib import Path

DOCS = Path("../../docs")
pdfs = sorted(DOCS.glob("*.pdf"))
print("Tim thay", len(pdfs), "file:")
for p in pdfs:
    print("-", p.name)""",
            ),
            ("md", "## 2. Load toàn bộ trang"),
            (
                "code",
                """from langchain_community.document_loaders import PyPDFLoader

docs = []
for pdf in pdfs:
    loader = PyPDFLoader(str(pdf))
    pages = loader.load()
    print(pdf.name, "->", len(pages), "trang")
    docs.extend(pages)

print("Tong so Document:", len(docs))
print("Mau 200 ky tu dau:\\n")
print(docs[0].page_content[:200])""",
            ),
            ("md", "## 3. Split với RecursiveCharacterTextSplitter"),
            (
                "code",
                """from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
print("So chunk:", len(chunks))
print("Do dai chunk[0]:", len(chunks[0].page_content))
print("---")
print(chunks[0].page_content[:400])""",
            ),
            (
                "md",
                """## Bài tập nhỏ

1. Thử `chunk_size=500` và so sánh số chunk.
2. In `metadata` của 1 chunk — nguồn PDF nào?""",
            ),
            (
                "code",
                """# TODO
# print(chunks[0].metadata)""",
            ),
            (
                "md",
                """## Checklist
- [ ] Load được PDF từ `docs/`
- [ ] Giải thích được vì sao cần overlap
- [ ] Biết biến `chunks` sẽ đưa sang bước embedding""",
            ),
        ],
    )


def build_03b() -> None:
    save(
        "notebooks/03_rag_chatbot/03b_embeddings_chroma.ipynb",
        [
            (
                "md",
                """# 03b — Embeddings + ChromaDB

## Mục tiêu
- Biến mỗi chunk thành vector (embedding).
- Lưu vào Chroma local và thử retrieve top-k đoạn liên quan.

## Kiến thức cần nhớ
- Embedding: câu gần nghĩa → vector gần nhau (dù khác từ).
- Vector DB giúp tìm đoạn liên quan nhanh hơn so khớp chuỗi thô.
- Cần `OPENAI_API_KEY` trong file `.env` ở gốc repo (xem `.env.example`).

**Không** hardcode API key trong notebook.""",
            ),
            ("md", "## 1. Load API key từ .env"),
            (
                "code",
                """import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path("../../").resolve()
load_dotenv(ROOT / ".env")

key = os.getenv("OPENAI_API_KEY", "")
if not key or key.startswith("sk-your"):
    raise EnvironmentError(
        "Chua co OPENAI_API_KEY hop le. Copy .env.example -> .env va dien key."
    )
print("API key: da load (do dai", len(key), "ky tu)")""",
            ),
            ("md", "## 2. Load + split lại (giống 03a)"),
            (
                "code",
                """from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

docs = []
for pdf in sorted((ROOT / "docs").glob("*.pdf")):
    docs.extend(PyPDFLoader(str(pdf)).load())

chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
print("chunks:", len(chunks))""",
            ),
            ("md", "## 3. Tạo Chroma từ embeddings"),
            (
                "code",
                """from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

persist_dir = str(ROOT / "data" / "chroma_db")
embeddings = OpenAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=persist_dir,
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
print("Da luu Chroma tai:", persist_dir)""",
            ),
            ("md", "## 4. Thử retrieve (chưa gọi LLM trả lời)"),
            (
                "code",
                """query = "Chatbot RAG dung cong cu gi?"
hits = retriever.invoke(query)
for i, doc in enumerate(hits, 1):
    src = doc.metadata.get("source", "?")
    print(f"\\n=== Hit {i} | {Path(src).name} ===")
    print(doc.page_content[:350])""",
            ),
            (
                "md",
                """## Checklist
- [ ] Key chỉ nằm trong `.env`
- [ ] Hiểu embedding khác TF-IDF chỗ nào (ngữ nghĩa vs đếm từ)
- [ ] Retrieve trả về chunk liên quan trước khi có LLM""",
            ),
        ],
    )


def build_03c() -> None:
    save(
        "notebooks/03_rag_chatbot/03c_rag_qa.ipynb",
        [
            (
                "md",
                """# 03c — Prompt + RAG hỏi đáp

## Mục tiêu
- Nối retriever + LLM thành chuỗi RAG.
- System prompt ép: chỉ trả lời theo ngữ cảnh, không bịa.
- So sánh câu hỏi **trong** tài liệu vs **ngoài** tài liệu.

Pipeline: câu hỏi → embedding → top-k chunk → nhét vào prompt → LLM.""",
            ),
            ("md", "## 1. Khởi tạo từ Chroma đã lưu + LLM"),
            (
                "code",
                """import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path("../../").resolve()
load_dotenv(ROOT / ".env")

if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError("Thieu OPENAI_API_KEY trong .env")

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
# LangChain 1.x: cac helper chain nam trong langchain_classic
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

persist_dir = str(ROOT / "data" / "chroma_db")
vectorstore = Chroma(
    persist_directory=persist_dir,
    embedding_function=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
print("Retriever + LLM san sang.")""",
            ),
            ("md", "## 2. System prompt chặt + tạo chain"),
            (
                "code",
                """system_prompt = (
    "Ban la tro ly AI huu ich. "
    "Su dung ngu canh duoi day de tra loi. "
    "Neu khong tim thay dap an, hay noi 'Toi khong biet', khong bia thong tin.\\n\\n"
    "Ngu canh:\\n{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, qa_chain)
print("RAG chain OK")""",
            ),
            ("md", "## 3. Câu hỏi trong tài liệu"),
            (
                "code",
                """question = "Nhung cong cu nao duoc dung de xay dung chatbot RAG trong tai lieu?"
response = rag_chain.invoke({"input": question})
print("Cau hoi:", question)
print("\\nTra loi:\\n", response["answer"])
print("\\nSo chunk context:", len(response.get("context", [])))""",
            ),
            ("md", "## 4. Câu hỏi ngoài tài liệu (kỳ vọng: không biết / không bịa)"),
            (
                "code",
                """question2 = "Gia Bitcoin ngay mai la bao nhieu theo tai lieu nay?"
response2 = rag_chain.invoke({"input": question2})
print("Cau hoi:", question2)
print("\\nTra loi:\\n", response2["answer"])""",
            ),
            (
                "md",
                """## Bài tập nhỏ

1. Đổi `k` retrieve từ 3 → 5, hỏi lại cùng câu — câu trả lời có dài/chi tiết hơn không?
2. Hỏi về Level 1 của lộ trình AI — model có trích đúng ý không?
3. (Tuỳ chọn) Thử temperature=0.7 và quan sát độ \"bay\" của câu trả lời.""",
            ),
            (
                "code",
                """# TODO: thu k=5
# retriever5 = vectorstore.as_retriever(search_kwargs={"k": 5})""",
            ),
            (
                "md",
                """## Checklist — đã hiểu khi…
- [ ] Vẽ được pipeline PDF → chunk → vector → retrieve → LLM
- [ ] Giải thích vì sao prompt cần câu \"không bịa\"
- [ ] Phân biệt được câu hỏi trong / ngoài corpus
- [ ] Sẵn sàng xem mỗi giai đoạn Jupyter như 1 module cho app Store sau này""",
            ),
        ],
    )


if __name__ == "__main__":
    build_00()
    build_01()
    build_02()
    build_03a()
    build_03b()
    build_03c()
    print("all notebooks built")
