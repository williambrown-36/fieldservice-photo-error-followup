"""Decide technician follow-up and capture a photo-processing exception."""
import traceback

import infrai


def needs_follow_up(dispatch_status, photo_count):
    """A dispatched work order needs contact when it has no usable photo."""
    return dispatch_status == "dispatched" and photo_count == 0


def record_photo_failure(work_order_id, technician_id, dispatch_status, exc):
    """Capture one grouped event with the work-order context, then return the decision."""
    infrai.errors.capture(
        title="work-order photo processing failed",
        message=str(exc),
        level="error",
        fingerprint=["work-order-photo", type(exc).__name__],
        exception=traceback.format_exc(),
        context={
            "work_order_id": work_order_id,
            "technician_id": technician_id,
            "dispatch_status": dispatch_status,
        },
    )
    return needs_follow_up(dispatch_status, 0)


def run_example():
    work_order = {
        "id": "wo-1042",
        "technician_id": "tech-17",
        "dispatch_status": "dispatched",
        "photos": [],
    }
    try:
        raise ValueError("photo payload could not be decoded")
    except ValueError as exc:
        follow_up = record_photo_failure(
            work_order["id"], work_order["technician_id"],
            work_order["dispatch_status"], exc,
        )
    return {"work_order_id": work_order["id"], "technician_follow_up": follow_up}


if __name__ == "__main__":
    print(run_example())
