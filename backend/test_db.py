from app.database import engine
from sqlalchemy.exc import SQLAlchemyError

try:
    connection = engine.connect()
    print("✅ Database connected successfully!")
    connection.close()

except SQLAlchemyError as e:
    print("❌ Connection failed!")
    print(e)
