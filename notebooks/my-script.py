class PointV2:
    """Representation of a two-dimensional point coordinate."""

    def __init__(self, x: float, y: float) -> None:
        """Initializes a PointV2 with the given coordinates."""
        self.x = x
        self.y = y

    def distance_to(self, other: "PointV2") -> float:
        """Computes the distance to another `PointV2`."""
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx**2 + dy**2) ** 0.5


p1 = PointV2(x="5", y="7")
p2 = PointV2(x=5, y=7)
