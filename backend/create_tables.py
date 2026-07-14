from app.database import Base, engine

# Import models directly
from app.models.company import Company
from app.models.user import User

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")