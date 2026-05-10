from pydantic import BaseModel, Field


class ChildInfo(BaseModel):
    """Information about the child for personalized scenarios."""

    name: str = Field(..., min_length=1, description="Tên trẻ, để cá nhân hóa câu hỏi")
    age: int = Field(..., ge=5, le=16, description="Tuổi trẻ, 5-16")
    gender: str = Field("khác", description="Giới tính trẻ (nam/nữ/khác)")
    location: str = Field(..., min_length=1, description="Địa điểm, ảnh hưởng bối cảnh")
    notes: str | None = Field(None, description="Thông tin bổ sung (tùy chọn)")


class GenerateConfig(BaseModel):
    """Configuration for scenario generation."""

    total: int = Field(..., ge=1, le=10, description="Số câu hỏi muốn sinh, tối đa 10")
    difficulty: int = Field(
        ..., ge=1, description="Độ khó, 1 đến MAX_DIFFICULTY (cấu hình)"
    )


class GenerateBatchRequest(BaseModel):
    """Request body for POST /api/v1/scenarios/generate-batch."""

    child: ChildInfo
    config: GenerateConfig
