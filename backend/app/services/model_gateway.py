from dataclasses import dataclass

from app.config import get_settings


@dataclass(slots=True)
class ModelResult:
    provider: str
    output_text: str


class LocalModelGateway:
    def __init__(self) -> None:
        self.settings = get_settings()

    def run_task(self, prompt: str, task_type: str) -> ModelResult:
        return ModelResult(
            provider="mock-local-provider",
            output_text=(
                f"Placeholder local-model response for task_type={task_type}. "
                f"Prompt length={len(prompt)}. Configure a local model runtime to replace this provider."
            ),
        )
