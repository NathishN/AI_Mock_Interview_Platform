from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RubricDimension(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    weight: float = Field(gt=0, le=100)


class RubricIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    dimensions: list[RubricDimension] = Field(min_length=1, max_length=12)
    is_active: bool = True

    @model_validator(mode="after")
    def _weights_sum_to_100(self):
        total = sum(d.weight for d in self.dimensions)
        if abs(total - 100) > 1e-6:
            raise ValueError(f"Dimension weights must sum to 100 (got {total:g})")
        names = [d.name.lower() for d in self.dimensions]
        if len(set(names)) != len(names):
            raise ValueError("Dimension names must be unique")
        return self


class RubricOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    name: str
    dimensions: list[RubricDimension]
    is_active: bool
    updated_at: datetime
