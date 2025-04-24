from sqlalchemy import Column, String, create_engine, Integer, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()


class Product(Base):
    __tablename__ = 'Product_Information'

    id = Column(Integer, unique=True, primary_key=True, nullable=False)
    Product_Name = Column(String, nullable=False)
    Brand = Column(String, nullable=True)
    Category_Name = Column(String,)
    Current_Price = Column(String)
    Actual_Price = Column(String)
    Description = Column(String)
    Product_URL = Column(String)
    Category_URL = Column(String)


db_path = 'sqlite:///super_selectos.db'
engine = create_engine(url=db_path, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def insert_to_database(data: Product) -> None:
    """
    Inserting data to database
    :param data: Data to insert as Product class
    :return: None
    """
    session = Session()
    try:
        session.add(data)
        session.commit()
        print(f'{data.Product_Name} has added to database')
    except IntegrityError:
        session.rollback()
    finally:
        session.close()
