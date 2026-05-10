from unittest.mock import patch, MagicMock
from app.models.response import Choice, Scenario, Choices, GenerateBatchResponse
from app.services.llm_service import ScenariosOutput


MOCK_SCENARIOS = ScenariosOutput(
    scenarios=[
        Scenario(
            type="digital",
            question="Một người lạ trong game online nhắn tin cho Minh. Minh sẽ làm gì?",
            choices=Choices(
                A=Choice(
                    text="Gửi số điện thoại",
                    status="Nguy hiểm",
                    explain="Tiết lộ thông tin cá nhân",
                    score=0,
                ),
                B=Choice(
                    text="Nói với ba mẹ",
                    status="Rất tốt",
                    explain="Tìm sự trợ giúp",
                    score=10,
                ),
                C=Choice(
                    text="Hỏi thêm",
                    status="Tệ",
                    explain="Tiếp tục nói chuyện nguy hiểm",
                    score=2,
                ),
                D=Choice(
                    text="Chặn và báo cáo",
                    status="Tốt",
                    explain="Chấm dứt tiếp cận",
                    score=7,
                ),
            ),
        ),
        Scenario(
            type="daily",
            question="Một người lạ hỏi đường và muốn Minh dẫn đi. Minh sẽ làm gì?",
            choices=Choices(
                A=Choice(
                    text="Dẫn người đó đi",
                    status="Nguy hiểm",
                    explain="Đi theo người lạ rất nguy hiểm",
                    score=0,
                ),
                B=Choice(
                    text="Từ chối và đi về",
                    status="Rất tốt",
                    explain="Giữ khoảng cách an toàn",
                    score=10,
                ),
                C=Choice(
                    text="Chỉ đường bằng lời",
                    status="Tốt",
                    explain="Giúp đỡ nhưng giữ khoảng cách",
                    score=7,
                ),
                D=Choice(
                    text="Gọi điện cho ba mẹ",
                    status="Tốt",
                    explain="Nhờ người lớn hỗ trợ",
                    score=8,
                ),
            ),
        ),
    ]
)


def _create_mock_response(parsed: ScenariosOutput):
    """Create a mock Gemini API response with structured output."""
    mock = MagicMock()
    mock.parsed = parsed
    return mock


class TestGenerateBatchEndpoint:
    """Tests for POST /api/v1/scenarios/generate-batch."""

    @patch("app.services.llm_service.client")
    def test_success(self, mock_genai_client, client, valid_request):
        """Test successful scenario generation with structured output."""
        mock_genai_client.models.generate_content.return_value = _create_mock_response(
            MOCK_SCENARIOS
        )

        response = client.post("/api/v1/scenarios/generate-batch", json=valid_request())

        assert response.status_code == 200
        # Validate using Pydantic model - if this succeeds, the structure is correct
        data = GenerateBatchResponse(**response.json())
        assert len(data.scenarios) == 2

    def test_missing_child_name(self, client, valid_request):
        """Test validation: missing required field child.name."""
        bad_req = valid_request()
        # Remove name entirely to trigger Pydantic missing field error
        del bad_req["child"]["name"]

        response = client.post("/api/v1/scenarios/generate-batch", json=bad_req)
        assert response.status_code == 422

    def test_age_out_of_range(self, client, valid_request):
        """Test validation: age outside 5-16 range."""
        bad_req = valid_request(child_kwargs={"age": 3})
        response = client.post("/api/v1/scenarios/generate-batch", json=bad_req)
        assert response.status_code == 422

    def test_total_exceeds_max(self, client, valid_request):
        """Test validation: total > 10."""
        bad_req = valid_request(config_kwargs={"total": 15})
        response = client.post("/api/v1/scenarios/generate-batch", json=bad_req)
        assert response.status_code == 422

    @patch("app.services.llm_service.client")
    def test_llm_failure(self, mock_genai_client, client, valid_request):
        """Test that LLM failure results in 422 after retries."""
        mock_genai_client.models.generate_content.side_effect = Exception("API error")
        response = client.post("/api/v1/scenarios/generate-batch", json=valid_request())
        assert response.status_code == 422

    def test_empty_body(self, client):
        """Test validation: empty request body."""
        response = client.post("/api/v1/scenarios/generate-batch", json={})
        assert response.status_code == 422


class TestGenerateStreamEndpoint:
    """Tests for POST /api/v1/scenarios/generate-stream."""

    @patch("app.services.llm_service.client")
    def test_stream_success(self, mock_genai_client, client, valid_request):
        """Test successful streaming with SSE format."""
        # Setup mock for async stream chunks
        chunk1 = MagicMock()
        chunk1.text = '{"scenarios": [{"type": "digital", "question": "Q1", "choices": '
        chunk2 = MagicMock()
        chunk2.text = '{"A": {"text": "T1", "status": "S1", "explain": "E1", "score": 10}, "B": {"text": "T2", "status": "S2", "explain": "E2", "score": 0}, "C": {"text": "T3", "status": "S3", "explain": "E3", "score": 0}, "D": {"text": "T4", "status": "S4", "explain": "E4", "score": 0}}'
        chunk3 = MagicMock()
        chunk3.text = '}, {"type": "daily", "question": "Q2", "choices": {"A": {"text": "T1", "status": "S1", "explain": "E1", "score": 10}, "B": {"text": "T2", "status": "S2", "explain": "E2", "score": 0}, "C": {"text": "T3", "status": "S3", "explain": "E3", "score": 0}, "D": {"text": "T4", "status": "S4", "explain": "E4", "score": 0}}}]}'

        async def mock_async_gen():
            yield chunk1
            yield chunk2
            yield chunk3

        async def mock_stream_call(*args, **kwargs):
            return mock_async_gen()

        mock_genai_client.aio.models.generate_content_stream.side_effect = (
            mock_stream_call
        )

        response = client.post(
            "/api/v1/scenarios/generate-stream", json=valid_request()
        )

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/event-stream")

        content = response.text
        assert "event: scenario" in content
        assert "event: done" in content

    @patch("app.services.llm_service.client")
    def test_stream_error(self, mock_genai_client, client, valid_request):
        """Test streaming error handling."""
        mock_genai_client.aio.models.generate_content_stream.side_effect = Exception(
            "API fail"
        )
        response = client.post(
            "/api/v1/scenarios/generate-stream", json=valid_request()
        )
        assert "event: error" in response.text


class TestHealthCheck:
    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
