def build_prompt(
    name: str,
    age: int,
    location: str,
    notes: str | None,
    total: int,
    difficulty: int,
    max_difficulty: int,
) -> str:
    """Build the LLM prompt for generating scenario batches.

    Since structured output handles JSON formatting, this prompt
    focuses purely on content quality and requirements.
    """

    notes_text = f"\n- Thông tin bổ sung: {notes}" if notes else ""

    return f"""Bạn là chuyên gia giáo dục hàng đầu về an toàn cho trẻ em.
Nhiệm vụ của bạn là tạo ra {total} tình huống trắc nghiệm thực tế, kịch tính và có tính giáo dục cao cho trẻ em.

THÔNG TIN TRẺ:
- Tên: {name}
- Tuổi: {age}
- Địa điểm/Bối cảnh: {location}{notes_text}

ĐỘ KHÓ: {difficulty}/{max_difficulty}
- Mức 1-2: Tình huống rõ ràng, dễ nhận biết đúng sai.
- Mức 3-4: Tình huống tinh vi hơn, cần suy luận.
- Mức 5+: Tình huống cực kỳ phức tạp, đánh vào tâm lý hoặc sự cả tin.

YÊU CẦU NỘI DUNG:
1. Mỗi tình huống phải được trình bày TRONG CÙNG MỘT TRƯỜNG "question" (bao gồm cả mô tả bối cảnh dẫn dắt và câu hỏi thực tế).
2. Đan xen giữa "digital" (an toàn mạng, lừa đảo game, mạng xã hội) và "daily" (người lạ, bắt nạt, bí mật xấu).
3. Luôn dùng tên "{name}" trong câu hỏi để tăng tính tương tác.
4. Mỗi lựa chọn phải có cấu trúc:
   - text: Hành động cụ thể của trẻ.
   - status: Chọn 1 trong: "Rất tốt", "Tốt", "Khá", "Bình thường", "Tệ", "Nguy hiểm".
   - explain: Giải thích ngắn gọn tại sao hành động đó lại dẫn đến trạng thái như vậy.
   - score: Điểm số từ 0 đến 10.
5. QUY TẮC ĐÁP ÁN:
   - Phải có DUY NHẤT 1 lựa chọn là 10 điểm ("Rất tốt").
   - 3 lựa chọn còn lại phải có số điểm thấp hơn (vd: 0, 3, 7) tùy theo mức độ an toàn.
   - Các lựa chọn phải có vẻ ngoài hợp lý, không quá ngớ ngẩn.

ĐỊNH DẠNG ĐẦU RA:
- type: "digital" hoặc "daily".
- question: Nội dung tình huống và câu hỏi.
- choices: Gồm A, B, C, D.

PHẠM VI CHUYÊN MÔN:
- Daily: Quy tắc 5 ngón tay, đụng chạm không an toàn, đi lạc, người lạ tặng quà, bị ép làm việc xấu.
- Digital: Bảo mật mật khẩu, không chia sẻ ảnh cá nhân, nhận diện link lừa đảo, ứng xử văn minh trên mạng."""
