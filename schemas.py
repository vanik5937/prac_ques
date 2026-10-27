from pydantic import Field, BaseModel, ConfigDict


class ParentCreate(BaseModel):
    name: str = Field(min_length=1)
    region: str = Field(min_length=1)

class ParentOut(BaseModel):
    id: int
    name: str
    region: str

    model_config = ConfigDict(from_attributes=True)

class ChildCreate(BaseModel):
    batch_name: str = Field(min_length=1)
    crop_type: str = Field(min_length=1)
    expected_yield_kg: int = Field(ge=0)
    area_hectares: int = Field(ge = 1)

class ChildOut(BaseModel):
    id: int
    batch_name: str
    crop_type: str
    expected_yield_kg: int
    area_hectares: int

    model_config = ConfigDict(from_attributes=True)


class ChildUpdate(BaseModel):
    batch_name: str | None =  Field(default=None,min_length=1)
    crop_type: str | None = Field(default=None,min_length=1)
    excepted_yield_kg: int | None = Field(default=None, ge=0)
    area_hectares: int | None = Field(default = None, ge = 1)


class ParentWithChildren(ParentOut):
    children : list[ChildOut]