from app import app, db

# ------------ For executing 'python run.py' ------------
# Create an application context
with app.app_context():
    # Initialize the database
    db.create_all()

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
