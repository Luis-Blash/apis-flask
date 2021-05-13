from app import create_app

app = create_app()

if __name__ and '__main__':
    app.run(debug=True, host='0.0.0.0')
