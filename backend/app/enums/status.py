from enum import Enum


class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"
