from dataclasses import dataclass


@dataclass
class Deployment:

    namespace: str

    name: str

    replicas: int
