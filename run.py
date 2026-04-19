from app import create_app

print(">>> STO PARTENDO CON RUN.PY")

app = create_app()

if __name__ == '__main__':
    print(">>> PRIMA DI RUN")

    # app.run(host="0.0.0.0", port=5000, debug=True) ## PER DOCKER
    app.run(debug=True)