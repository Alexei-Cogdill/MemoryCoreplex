from app import app
import os

#Runs the app 
port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    app.run(debug=True)
