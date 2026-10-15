from typing import Self


class BoundingBox(tuple[int, int, int, int]):
    """Immutable Rich Value Object encapsulating (x1, y1, x2, y2) bounding box geometry."""

    def __new__(cls, x1: int, y1: int, x2: int, y2: int) -> Self:
        return super().__new__(cls, (int(x1), int(y1), int(x2), int(y2)))

    @property
    def x1(self) -> int:
        return self[0]

    @property
    def y1(self) -> int:
        return self[1]

    @property
    def x2(self) -> int:
        return self[2]

    @property
    def y2(self) -> int:
        return self[3]

    @property
    def area(self) -> int:
        return max(0, self[2] - self[0]) * max(0, self[3] - self[1])

    @property
    def aspect_ratio(self) -> float:
        return (self[2] - self[0]) / max(1, self[3] - self[1])

    def contains(self, other: tuple[int, int, int, int], threshold: float = 0.80) -> bool:
        ix1, iy1 = max(self[0], other[0]), max(self[1], other[1])
        ix2, iy2 = min(self[2], other[2]), min(self[3], other[3])
        if ix2 <= ix1 or iy2 <= iy1:
            return False
        inter = (ix2 - ix1) * (iy2 - iy1)
        other_area = max(1, (other[2] - other[0]) * (other[3] - other[1]))
        return (inter / other_area) >= threshold

    def iou(self, other: tuple[int, int, int, int]) -> float:
        ix1, iy1 = max(self[0], other[0]), max(self[1], other[1])
        ix2, iy2 = min(self[2], other[2]), min(self[3], other[3])
        if ix2 <= ix1 or iy2 <= iy1:
            return 0.0
        inter = (ix2 - ix1) * (iy2 - iy1)
        union = self.area + max(0, other[2] - other[0]) * max(0, other[3] - other[1]) - inter
        return inter / max(1, union)
