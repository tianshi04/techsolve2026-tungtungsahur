# API Documentation - TungTungSahur

Hệ thống cung cấp hai phương thức chính để sinh các tình huống đánh giá kỹ năng bảo vệ bản thân cho trẻ em: **Batch** (trả về toàn bộ một lần) và **Stream** (trả về từng câu theo thời gian thực).

---

## 1. POST /api/v1/scenarios/generate-batch

Sinh một **chuỗi nhiều tình huống** cùng lúc. Phù hợp khi muốn nhận toàn bộ dữ liệu trước khi hiển thị.

### Request Body

```json
{
  "child": {
    "name": "Minh",
    "age": 10,
    "gender": "nam",
    "location": "TP.HCM",
    "notes": "hay chơi game online"
  },
  "config": {
    "total": 5,
    "difficulty": 3
  }
}
```

| Field | Loại | Bắt buộc | Mô tả |
|-------|------|----------|---------|
| `child.name` | string | ✅ | Tên trẻ (để cá nhân hóa) |
| `child.age` | integer | ✅ | Độ tuổi (5-16) |
| `child.gender` | string | ❌ | Giới tính (`nam`, `nữ`, `khác`). Mặc định: `khác` |
| `child.location` | string | ✅ | Địa điểm (ảnh hưởng bối cảnh) |
| `child.notes` | string | ❌ | Thông tin bổ sung |
| `config.total` | integer | ✅ | Số lượng câu hỏi (1-10) |
| `config.difficulty` | integer | ✅ | Độ khó (1 - MAX_DIFFICULTY) |

### Response Body

```json
{
  "scenarios": [
    {
      "type": "digital",
      "question": "Minh đang chơi game thì một người lạ đề nghị tặng skin miễn phí nếu Minh gửi số điện thoại của mẹ. Minh nên làm gì?",
      "choices": {
        "A": { "text": "Gửi ngay để lấy skin", "status": "Nguy hiểm", "explain": "Lừa đảo lấy thông tin cá nhân", "score": 0 },
        "B": { "text": "Hỏi ý kiến mẹ trước", "status": "Rất tốt", "explain": "Luôn chia sẻ với người lớn", "score": 10 },
        "C": { "text": "Từ chối và báo cáo người đó", "status": "Tốt", "explain": "Hành động đúng để bảo vệ mình", "score": 8 },
        "D": { "text": "Im lặng và tiếp tục chơi", "status": "Tệ", "explain": "Cần hành động để ngăn chặn rủi ro", "score": 3 }
      }
    }
    // ...
  ]
}
```

---

## 2. POST /api/v1/scenarios/generate-stream

Sinh tình huống theo dạng **Streaming (SSE)**. Khuyên dùng để cải thiện trải nghiệm người dùng (UX) khi chờ LLM phản hồi.

### Request Body
Giống hệt endpoint `/generate-batch`.

### Response Format
`Content-Type: text/event-stream`

Hệ thống sẽ trả về các sự kiện theo định dạng Server-Sent Events:

- **event: scenario**: Trả về một object tình huống duy nhất ngay khi nó vừa được sinh ra.
- **event: done**: Thông báo quá trình sinh đã hoàn tất.
- **event: error**: Thông báo lỗi nếu có vấn đề xảy ra trong quá trình stream.

#### Ví dụ luồng dữ liệu (Raw SSE):
```text
event: scenario
data: {"type": "digital", "question": "...", "choices": {...}}

event: scenario
data: {"type": "daily", "question": "...", "choices": {...}}

event: done
data: {}
```

---

## Dữ liệu Models (Pydantic)

### Scenario Object
| Field | Loại | Mô tả |
|-------|------|---------|
| `type` | string | `digital` (môi trường mạng) hoặc `daily` (đời thực) |
| `question` | string | Nội dung tình huống và câu hỏi cụ thể |
| `choices` | object | Chứa 4 key `A`, `B`, `C`, `D` |

### Choice Object
| Field | Loại | Mô tả |
|-------|------|---------|
| `text` | string | Nội dung câu trả lời |
| `status` | string | Đánh giá (e.g., "Rất tốt", "Nguy hiểm", "Tệ") |
| `explain` | string | Giải thích tại sao lựa chọn đó lại có trạng thái như vậy |
| `score` | integer | Điểm số (0-10) |

---

## Lưu ý kỹ thuật

- **Stateless**: Backend không lưu trữ trạng thái vào Database. Client cần quản lý session và lịch sử chơi.
- **LLM Structured Output**: Sử dụng Gemini Flash 2.0 với JSON Schema để đảm bảo dữ liệu trả về luôn đúng cấu trúc.
- **Retry Logic**: Backend tự động thử lại tối đa 2 lần nếu LLM trả về dữ liệu lỗi format.
- **Health Check**: Có thể kiểm tra trạng thái server tại `GET /health`.
