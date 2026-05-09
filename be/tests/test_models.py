import pytest
from pydantic import ValidationError

from app.models.request import ChildInfo, GenerateConfig, GenerateBatchRequest
from app.models.response import Choice, Scenario, GenerateBatchResponse, Choices


# --- Request Models ---

class TestChildInfo:
    def test_valid(self):
        child = ChildInfo(name="Minh", age=10, gender="nam", location="TP.HCM")
        assert child.name == "Minh"
        assert child.age == 10
        assert child.gender == "nam"
        assert child.location == "TP.HCM"
        assert child.notes is None

    def test_valid_with_notes(self):
        child = ChildInfo(name="Minh", age=10, location="TP.HCM", notes="hay chơi game")
        assert child.notes == "hay chơi game"

    def test_age_too_low(self):
        with pytest.raises(ValidationError):
            ChildInfo(name="Minh", age=3, location="TP.HCM")

    def test_age_too_high(self):
        with pytest.raises(ValidationError):
            ChildInfo(name="Minh", age=20, location="TP.HCM")

    def test_missing_name(self):
        with pytest.raises(ValidationError):
            ChildInfo(age=10, location="TP.HCM")

    def test_empty_name(self):
        with pytest.raises(ValidationError):
            ChildInfo(name="", age=10, location="TP.HCM")

    def test_missing_location(self):
        with pytest.raises(ValidationError):
            ChildInfo(name="Minh", age=10)


class TestGenerateConfig:
    def test_valid(self):
        config = GenerateConfig(total=5, difficulty=3)
        assert config.total == 5
        assert config.difficulty == 3

    def test_total_too_low(self):
        with pytest.raises(ValidationError):
            GenerateConfig(total=0, difficulty=3)

    def test_total_too_high(self):
        with pytest.raises(ValidationError):
            GenerateConfig(total=11, difficulty=3)

    def test_difficulty_too_low(self):
        with pytest.raises(ValidationError):
            GenerateConfig(total=5, difficulty=0)


class TestGenerateBatchRequest:
    def test_valid(self):
        req = GenerateBatchRequest(
            child={"name": "Minh", "age": 10, "location": "TP.HCM"},
            config={"total": 5, "difficulty": 3},
        )
        assert req.child.name == "Minh"
        assert req.config.total == 5


# --- Response Models ---

class TestChoice:
    def test_valid(self):
        choice = Choice(text="Gửi số điện thoại", status="Nguy hiểm", explain="Tiết lộ thông tin", score=0)
        assert choice.score == 0

    def test_score_too_high(self):
        with pytest.raises(ValidationError):
            Choice(text="...", status="...", explain="...", score=11)

    def test_score_negative(self):
        with pytest.raises(ValidationError):
            Choice(text="...", status="...", explain="...", score=-1)


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
        assert scenario.choices.A.score == 0


class TestGenerateBatchResponse:
    def test_valid(self):
        resp = GenerateBatchResponse(
            scenarios=[
                {
                    "type": "digital",
                    "question": "...",
                    "choices": Choices(
                        A={"text": "...", "status": "...", "explain": "...", "score": 0},
                        B={"text": "...", "status": "...", "explain": "...", "score": 10},
                        C={"text": "...", "status": "...", "explain": "...", "score": 2},
                        D={"text": "...", "status": "...", "explain": "...", "score": 7},
                    ),
                }
            ],
        )
        assert len(resp.scenarios) == 1
