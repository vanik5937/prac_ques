from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    region = Column(String, nullable=False)

    crop_batches = relationship(
        "CropBatches",
        back_populates= "farms"
    )



class CropBatches(Base):
    __tablename__ = "crop_batches"

    id = Column(Integer, primary_key=True, index= True)
    batch_name = Column(String, nullable=False)
    crop_type = Column(String, nullable=False)
    expected_yield_kg = Column(Integer, nullable=False)
    area_hectares = Column(Integer, nullable=False)

    farm_id = Column(
        Integer,
        ForeignKey("farms.id"),
        nullable= False
    )
    farms = relationship(
        "Farm",
        back_populates= "crop_batches"
    )


