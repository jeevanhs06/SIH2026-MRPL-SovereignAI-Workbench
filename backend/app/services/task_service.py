import asyncio
from datetime import UTC, datetime
from uuid import uuid4

from app.schemas import TaskCreateRequest, TaskEvent, TaskResponse, TaskReviewRequest, TaskStatus
from app.services.audit import AuditLogger
from app.services.model_gateway import LocalModelGateway
from app.services.output_generator import OutputGenerator


class TaskService:
    def __init__(self) -> None:
        self.tasks: dict[str, TaskResponse] = {}
        self.gateway = LocalModelGateway()
        self.output_generator = OutputGenerator()
        self.audit = AuditLogger()

    def list_tasks(self) -> list[TaskResponse]:
        return sorted(self.tasks.values(), key=lambda t: t.created_at, reverse=True)

    def get_task(self, task_id: str) -> TaskResponse:
        task = self.tasks.get(task_id)
        if task is None:
            raise KeyError(task_id)
        return task

    def create_task(self, payload: TaskCreateRequest) -> TaskResponse:
        now = datetime.now(UTC)
        task = TaskResponse(
            task_id=str(uuid4()),
            title=payload.title,
            prompt=payload.prompt,
            status=TaskStatus.created,
            document_ids=payload.document_ids,
            requires_review=payload.requires_review,
            output_files=[],
            created_at=now,
            updated_at=now,
            events=[TaskEvent(timestamp=now, event="task_created", details={"title": payload.title})],
        )
        self.tasks[task.task_id] = task
        self.audit.log_event(
            "task_created",
            {"task_id": task.task_id, "title": task.title, "document_ids": task.document_ids},
        )
        return task

    async def execute_task(self, task_id: str) -> None:
        task = self.get_task(task_id)
        await self._transition(task, TaskStatus.queued, "task_queued")
        await asyncio.sleep(0)
        await self._transition(task, TaskStatus.running, "task_running")

        result = self.gateway.run_task(prompt=task.prompt, task_type="analysis")
        result_payload = {
            "task_id": task.task_id,
            "title": task.title,
            "provider": result.provider,
            "summary": result.output_text,
            "documents": task.document_ids,
        }

        json_file = self.output_generator.generate_json(task.task_id, result_payload)
        docx_file = self.output_generator.generate_docx_placeholder(task.task_id, result.output_text)
        xlsx_file = self.output_generator.generate_xlsx_placeholder(task.task_id, result.output_text)
        pdf_file = self.output_generator.generate_pdf_placeholder(task.task_id, result.output_text)
        task.output_files = [json_file, docx_file, xlsx_file, pdf_file]

        self.audit.log_event("task_outputs_generated", {"task_id": task.task_id, "output_files": task.output_files})
        terminal_state = TaskStatus.waiting_for_review if task.requires_review else TaskStatus.completed
        await self._transition(task, terminal_state, "task_finished")

    async def review_task(self, task_id: str, review: TaskReviewRequest) -> TaskResponse:
        task = self.get_task(task_id)
        if task.status != TaskStatus.waiting_for_review:
            raise ValueError("Task is not waiting for review")

        next_status = TaskStatus.completed if review.approved else TaskStatus.rejected
        await self._transition(
            task,
            next_status,
            "task_reviewed",
            {"approved": str(review.approved), "notes": review.notes},
        )
        return task

    async def _transition(
        self,
        task: TaskResponse,
        status: TaskStatus,
        event: str,
        details: dict[str, str] | None = None,
    ) -> None:
        now = datetime.now(UTC)
        task.status = status
        task.updated_at = now
        task.events.append(TaskEvent(timestamp=now, event=event, details=details or {}))
        self.audit.log_event(
            "task_transition",
            {"task_id": task.task_id, "status": status.value, "event": event, "details": details or {}},
        )
