from dataclasses import dataclass


@dataclass
class Question:
    id: int
    name: str
    description: str | None


@dataclass
class QuestionOption:
    question_id: int
    id: int
    description: str
