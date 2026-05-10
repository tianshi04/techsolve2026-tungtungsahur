from pydantic import BaseModel, Field


class Choice(BaseModel):
    """A single answer choice for a scenario."""

    text: str = Field(..., description="Nội dung lựa chọn")
    status: str = Field(
        ..., description="Trạng thái: Nguy hiểm, Rất tốt, Tệ, Tốt, etc."
    )
    explain: str = Field(..., description="Giải thích lý do")
    score: int = Field(..., ge=0, le=10, description="Điểm cho lựa chọn, 0-10")


class Choices(BaseModel):
    """Fixed set of choices A, B, C, D."""

    A: Choice
    B: Choice
    C: Choice
    D: Choice


class Scenario(BaseModel):
    """A single scenario with question and choices."""

    type: str = Field(..., description="Loại: digital hoặc daily")
    question: str = Field(..., description="Nội dung tình huống và câu hỏi")
    choices: Choices = Field(..., description="Các lựa chọn A, B, C, D")


class GenerateBatchResponse(BaseModel):
    """Response body for POST /api/v1/scenarios/generate-batch."""

    scenarios: list[Scenario] = Field(..., description="Danh sách tình huống")
