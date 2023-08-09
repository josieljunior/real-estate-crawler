from sqlalchemy import create_engine
from .models import Base

engine = create_engine("mysql://root:secret@db/real_estate_crawler",
                       pool_size=40,  
                       max_overflow=10)

Base.metadata.create_all(engine)
