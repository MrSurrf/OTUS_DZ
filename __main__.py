from src.app.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    print("Server is running on port 5000")