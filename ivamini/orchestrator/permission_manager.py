from ivamini.orchestrator.permission_request import PermissionRequest
from ivamini.logs.logger import log_event

class PermissionManager:

    def request_permission(self, task_id: str, level: str, reason: str):
        req = PermissionRequest(
            task_id=task_id,
            requested_level=level,
            reason=reason
        )

        log_event("PERMISSION_REQUESTED", {
            "task_id": task_id,
            "requested_level": level,
            "reason": reason,
            "status": req.status
        })

        return req

    def approve(self, req: PermissionRequest):
        req.status = "APPROVED"

        log_event("PERMISSION_APPROVED", {
            "task_id": req.task_id,
            "level": req.requested_level
        })

        return req

    def deny(self, req: PermissionRequest, reason: str):
        req.status = "DENIED"

        log_event("PERMISSION_DENIED", {
            "task_id": req.task_id,
            "reason": reason
        })

        return req
