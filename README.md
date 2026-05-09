# Bé Ứng Biến — AI-Powered Child Safety Assessment

Phát triển bởi Team **TungTungSahur**

**Bé Ứng Biến** là một nền tảng web sử dụng trí tuệ nhân tạo (LLM) để tạo ra các tình huống trắc nghiệm cá nhân hóa, giúp trẻ em rèn luyện kỹ năng bảo vệ bản thân trong cả môi trường đời thực và không gian mạng.

## 🚀 Giới thiệu dự án

Dự án hướng tới việc thay đổi cách giáo dục về an toàn cho trẻ em bằng cách biến các bài học khô khan thành các trải nghiệm tương tác (Gamification). Hệ thống sử dụng mô hình Google Gemini để sinh ra các tình huống thực tế, phù hợp với độ tuổi và sở thích của từng trẻ.

### ✨ Các tính năng chính

- **Cá nhân hóa tình huống:** AI tự động điều chỉnh nội dung dựa trên độ tuổi, giới tính và sở thích của trẻ.
- **Tình huống thực tế:** Bao gồm cả rủi ro đời thường (người lạ, bí mật nguy hiểm) và rủi ro mạng (lừa đảo game, thông tin cá nhân).
- **Gamification:** Tăng tính hấp dẫn thông qua hệ thống điểm và phản hồi tương tác.
- **Báo cáo cho phụ huynh:** Cung cấp phân tích về cách con xử lý tình huống và gợi ý hướng dẫn thêm.

## 📂 Cấu trúc dự án

```text
techsolve2026-tungtungsahur/
├── be/               # Backend API (FastAPI + Gemini SDK)
├── fe/               # Frontend App (Đang phát triển)
├── docs/             # Tài liệu dự án (Ý tưởng, API, Quy tắc)
└── README.md         # Tài liệu hướng dẫn chính
```

## 🛠 Công nghệ sử dụng

- **Backend:** FastAPI, Python 3.12+
- **AI Engine:** Google Gemini (Gemini 3 Flash)
- **Validation:** Pydantic
- **Package Manager:** uv / pip

## 🚦 Bắt đầu

Để cài đặt và chạy thử hệ thống, vui lòng xem hướng dẫn chi tiết tại:

1. **Backend:** [Hướng dẫn cài đặt Backend](./be/README.md)
2. **Frontend:** [Hướng dẫn cài đặt Frontend](./fe/README.md) (Sắp ra mắt)

---

## 📄 Tài liệu tham khảo

- [Tóm tắt ý tưởng](./docs/idea.md)
- [Tài liệu API](./docs/api.md)
- [Khái niệm Frontend](./docs/fe_concept.md)
