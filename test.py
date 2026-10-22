
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db

def test_home():
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()

        try:
            client = app.test_client()
            response = client.get("/")
            assert response.status_code == 200
        finally:
            db.session.remove()
            db.drop_all()
