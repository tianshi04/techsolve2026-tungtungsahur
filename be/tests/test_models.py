import pytest
from pydantic import ValidationError
from app.models.request import ChildInfo, GenerateConfig, GenerateBatchRequest
from app.models.response import Choice, Scenario, Choices


# --- Request Models ---


class TestChildInfo:
    def test_valid(self, sample_child_info):
        child = ChildInfo(**sample_child_info())
        assert child.name == "Minh"
        assert child.age == 10

    def test_age_too_low(self, sample_child_info):
        with pytest.raises(ValidationError):
            ChildInfo(**sample_child_info(age=3))

    def test_age_too_high(self, sample_child_info):
        with pytest.raises(ValidationError):
            ChildInfo(**sample_child_info(age=20))

    def test_empty_name(self, sample_child_info):
        with pytest.raises(ValidationError):
            ChildInfo(**sample_child_info(name=""))


class TestGenerateConfig:
    def test_valid(self, sample_generate_config):
        config = GenerateConfig(**sample_generate_config())
        assert config.total == 2

    def test_total_too_high(self, sample_generate_config):
        with pytest.raises(ValidationError):
            GenerateConfig(**sample_generate_config(total=11))


class TestGenerateBatchRequest:
    def test_valid(self, valid_request):
        req = GenerateBatchRequest(**valid_request())
        assert req.child.name == "Minh"
        assert req.config.total == 2


# --- Response Models ---


class TestChoice:
    def test_valid(self):
        choice = Choice(
            text="Gửi số điện thoại",
            status="Nguy hiểm",
            explain="Tiết lộ thông tin",
            score=0,
        )
        assert choice.score == 0

    def test_score_too_high(self):
        with pytest.raises(ValidationError):
            Choice(text="...", status="...", explain="...", score=11)


class TestScenario:
    def test_valid(self):
        scenario = Scenario(
            type="digital",
            question="Minh sẽ làm gì?",
            choices=Choices(
                A={"text": "...", "status": "Nguy hiểm", "explain": "...", "score": 0},
                B={"text": "...", "status": "Rất tốt", "explain": "...", "score": 10},
                C={"text": "...", "status": "Tệ", "explain": "...", "score": 2},
                D={"text": "...", "status": "Tốt", "explain": "...", "score": 7},
            ),
        )
        assert scenario.type == "digital"
