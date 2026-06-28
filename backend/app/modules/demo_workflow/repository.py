from __future__ import annotations

from app.modules.demo_workflow.schemas import DemoRunSummary


class DemoWorkflowRepository:
    _runs: list[DemoRunSummary] = []

    def save(self, run: DemoRunSummary) -> DemoRunSummary:
        self._runs.insert(0, run)
        del self._runs[25:]
        return run

    def list_runs(self) -> list[DemoRunSummary]:
        return list(self._runs)

    def clear(self) -> None:
        self._runs.clear()
