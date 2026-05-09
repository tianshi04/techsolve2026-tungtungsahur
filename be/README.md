# TungTungSahur — Backend API

Backend API cho ứng dụng AI đánh giá kỹ năng bảo vệ bản thân cho trẻ em. Sử dụng Google Gemini để sinh chuỗi tình huống trắc nghiệm cá nhân hóa.

## Tech Stack

- **Python 3.12+**
- **FastAPI** — Web framework
- **Google Gemini** — LLM (structured output)
- **Pydantic** — Validation
- **uv** — Package manager

## Cài đặt

Dự án hỗ trợ cả **uv** (khuyên dùng) và **pip** truyền thống.

### Cách 1: Sử dụng uv (Nhanh & Quản lý virtualenv tự động)

1. **Cài đặt uv** (nếu chưa có):
   ```bash
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   # macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Cài đặt dependencies**:
   ```bash
   cd be
   uv sync
   ```

### Cách 2: Sử dụng pip truyền thống

1. **Tạo virtual environment**:
   ```bash
   cd be
   python -m venv .venv
   ```

2. **Kích hoạt virtual environment**:
   ```bash
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Cài đặt dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Cấu hình .env

```bash
cp .env.example .env
```

Mở `.env` và điền API key:

```env
LLM_API_KEY=your-gemini-api-key
LLM_MODEL=gemini-3-flash-preview
MAX_DIFFICULTY=5
HOST=127.0.0.1
PORT=8000
```

| Biến | Mô tả | Mặc định |
|------|--------|----------|
| `LLM_API_KEY` | Google Gemini API key | (bắt buộc) |
| `LLM_MODEL` | Model Gemini | `gemini-3-flash-preview` |
| `MAX_DIFFICULTY` | Độ khó tối đa cho tình huống | `5` |
| `HOST` | Host để chạy server | `127.0.0.1` |
| `PORT` | Port để chạy server | `8000` |

**Sử dụng uv:**
```bash
uv run python main.py
```

**Sử dụng pip (sau khi đã activate venv):**
```bash
python main.py
```

*Hoặc chạy trực tiếp bằng uvicorn:*
```bash
uvicorn app.main:app --reload
```

Server chạy tại `http://localhost:8000`

- **API docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## API

### `POST /api/v1/scenarios/generate-stream`

Sinh chuỗi tình huống trắc nghiệm (Streaming SSE).

**Request:**

```json
{
  "child": {
    "name": "Minh",
    "age": 10,
    "location": "TP.HCM",
    "notes": "hay chơi game online"
  },
  "config": {
    "total": 5,
    "difficulty": 3
  }
}
```

**Response (SSE Stream):**
Mỗi event trả về một object Scenario:
```text
event: scenario
data: {"id": "scn_1", ...}

event: scenario
data: {"id": "scn_2", ...}

event: done
data: [hoàn tất]
```

## Chạy tests

**Sử dụng uv:**
```bash
uv run pytest -v
```

**Sử dụng pip:**
```bash
pytest -v
```

## Cấu trúc dự án

```
be/
├── pyproject.toml
├── .env.example
├── main.py                  # Entry point chính
├── app/
│   ├── main.py              # FastAPI app definition
│   ├── config.py            # Settings (.env)
│   ├── models/
│   │   ├── request.py       # Request validation
│   │   └── response.py      # Response schema
│   ├── services/
│   │   └── llm_service.py   # Gemini structured output
│   ├── routers/
│   │   └── scenarios.py     # API endpoint
│   └── prompts/
│       └── scenario_prompt.py
└── tests/
    ├── test_models.py
    └── test_scenarios.py
```
