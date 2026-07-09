from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    app_name: str = "Sentinel - Agent of Agents"
    tagline: str = "Observe. Audit. Trust. Optimize."
    demo_mode: bool = True
    database_path: Path = PROJECT_ROOT / "data" / "sentinel.db"
    chroma_path: Path = PROJECT_ROOT / "data" / "chroma"
    model_name: str = "gpt-4o-mini"

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.database_path}"


settings = Settings()
