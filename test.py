
from app import app

def test_home():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    
    with app.app_context():
        from app import db
        db.create_all()
        
        client = app.test_client()
        response = client.get("/")
        
        assert response.status_code == 200
