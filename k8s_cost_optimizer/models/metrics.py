from dataclasses import dataclass


@dataclass
class ResourceMetrics:

    cpu_average: float = 0.0

    cpu_peak: float = 0.0

    memory_average: float = 0.0

    memory_peak: float = 0.0
