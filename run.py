from app import create_app
from app.tasks import celery

app = create_app()
celery.conf.update(app.config)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
