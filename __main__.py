from src.app.app import create_app
from src.app_editor.app_editor import editor_app

if __name__ == '__main__':
    app = create_app()
    app_editor = editor_app()
    app.run(debug=True)
    app_editor.run(debug=True,port=5001)
