# Dự án: Bé Ứng Biến
**Team: TungTungSahur**

## 📌 TÓM TẮT Ý TƯỞNG

### 🧠 Mô tả ngắn

Một **web app sử dụng LLM** để tạo chuỗi **tình huống trắc nghiệm cá nhân hóa**, giúp trẻ rèn luyện kỹ năng **bảo vệ bản thân trong cuộc sống đời thường và môi trường số**, có **yếu tố gamification** nhằm tăng trải nghiệm, và cung cấp phân tích cho phụ huynh sau khi hoàn thành.

---

## 🎯 Mục tiêu

* Giúp trẻ nhận diện và xử lý tình huống nguy cơ trong:

  * 🏫 Đời sống hằng ngày
  * 🌐 Môi trường số
* Đánh giá phản xạ ra quyết định của trẻ
* Hỗ trợ phụ huynh hiểu cách con suy nghĩ và hành động

---

## 👶 Input ban đầu

Phụ huynh nhập:

* Tuổi
* Giới tính
* Thông tin bổ sung (tuỳ chọn)

Thông tin này được dùng để điều chỉnh:

* Độ phức tạp tình huống
* Cách diễn đạt
* Bối cảnh phù hợp

---

## 🧩 Cách hoạt động

1. Hệ thống sinh ra chuỗi nhiều tình huống trắc nghiệm liên tiếp.
2. Mỗi tình huống:

   * Mô tả ngắn
   * 1 câu hỏi
   * 4 lựa chọn
   * Mỗi lựa chọn bao gồm:
     * **Trạng thái tương đối:** (Ví dụ: Rất tốt, Tốt, Tệ, Nguy hiểm...)
     * **Giải thích:** Lý do tại sao lựa chọn này lại có trạng thái như vậy.
   * Chỉ chọn 1 lần
3. Có yếu tố gamification để tăng engagement.
4. Sau khi hoàn thành:

   * Tổng điểm
   * Nhận xét chung về cách xử lý tình huống
   * Gợi ý phụ huynh cách hỗ trợ trẻ

Không lưu dữ liệu dài hạn.
Phụ huynh xem báo cáo ngay trên web sau khi kết thúc.

---

## 🌍 Phạm vi tình huống

### 🏫 Đời thường

* Người lạ tiếp cận
* Bị ép giữ bí mật
* Áp lực từ bạn bè
* Bị bắt nạt nhẹ

### 🌐 Môi trường số

* Xin thông tin cá nhân
* Rủ gặp ngoài đời
* Link lạ
* Lừa đảo trong game
* Áp lực xã hội online

---

## 🧠 Ví dụ minh họa

### Input:

* Tuổi: 10
* Giới tính: Nam
* Thông tin bổ sung: hay chơi game online

---

### 🌐 Tình huống

> Một người trong game nói rằng họ sẽ tặng con vật phẩm hiếm nếu con gửi số điện thoại để “xác nhận tài khoản”.

Con sẽ làm gì?

A. **Gửi số điện thoại** (Nguy hiểm: Tiết lộ thông tin cá nhân cho người lạ có thể dẫn đến lừa đảo hoặc quấy rối).
B. **Không trả lời và nói với ba mẹ** (Rất tốt: Bảo vệ thông tin cá nhân và tìm sự trợ giúp từ người lớn ngay lập tức).
C. **Hỏi thêm xem họ là ai** (Tệ: Tiếp tục giao tiếp với người lạ làm tăng rủi ro bị thao túng hoặc lừa đảo).
D. **Chặn người đó và báo cáo vi phạm** (Tốt: Chấm dứt sự tiếp cận của người lạ và giúp hệ thống loại bỏ kẻ xấu).

---

### 🏫 Tình huống khác

> Một bạn trong lớp yêu cầu con giữ bí mật một việc khiến con thấy lo lắng.

A. **Giữ bí mật** (Tệ: Một bí mật khiến con lo lắng thường là dấu hiệu của điều không ổn, không nên giữ một mình).
B. **Nói với người lớn con tin tưởng** (Rất tốt: Luôn chia sẻ những điều khiến con bất an với ba mẹ hoặc thầy cô).
C. **Tránh mặt bạn đó** (Bình thường: Chỉ là giải pháp tạm thời, không giải quyết được gốc rễ vấn đề lo lắng).
D. **Hỏi rõ bạn đó tại sao phải giữ bí mật** (Khá: Thể hiện sự chủ động nhưng vẫn nên chia sẻ với người lớn nếu cảm thấy lo lắng).

---

## 📊 Kết quả cuối

Phụ huynh sẽ thấy:

* Tổng điểm
* Nhận xét chung về khả năng nhận diện nguy cơ
* Gợi ý trao đổi thêm với trẻ

---

## 📌 Bản chất dự án

Đây là một:

> AI-driven interactive assessment web app giúp trẻ luyện phản xạ bảo vệ bản thân trong đời thực và môi trường số, có yếu tố gamification để tăng trải nghiệm, và hướng đến phụ huynh như người đồng hành.
