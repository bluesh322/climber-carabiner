"""Application entry point"""
from Climber_Carabiner import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

@app.errorhandler(404)
def page_not_found(e):
    """404 Not Found"""
    return render_template('/Climber_Carabiner/templates/404.html')