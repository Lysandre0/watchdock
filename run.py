from app import create_app, run_proxy

if __name__ == "__main__":
    # Démarre l'application Flask
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port=5000)

    # Démarre le proxy en parallèle
    run_proxy()
