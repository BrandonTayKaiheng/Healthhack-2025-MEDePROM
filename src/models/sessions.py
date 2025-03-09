from dataclasses import dataclass, field
from typing import List
from models.questions import Question, QuestionOption


@dataclass
class Session:
    name: str
    sys_instruction: str
    questions: List[Question]
    answers: List[QuestionOption] = field(default_factory=list)
    history: List[str] = field(default_factory=list)
