"""Application entry point"""
from Climber_Carabiner import create_app
from flask import render_template

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
