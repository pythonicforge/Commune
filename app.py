from src import create_app
# create app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)