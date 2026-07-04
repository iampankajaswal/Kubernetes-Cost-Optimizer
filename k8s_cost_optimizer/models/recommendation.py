from dataclasses import dataclass


@dataclass
class Recommendation:

    namespace: str

    deployment: str

    current_cpu: float

    recommended_cpu: float

    current_memory: float

    recommended_memory: float

    monthly_saving: float
