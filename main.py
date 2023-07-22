from app import app, database
from configuration import insert_data

# Create a new database and put in some data.
database.create_all()
insert_data()


if __name__ == "__main__":
    app.run(debug=True, port=8484)
