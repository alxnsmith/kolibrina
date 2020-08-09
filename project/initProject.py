import os


def main():
    cwd = os.getcwd()
    if not os.path.exists(os.path.join(cwd, 'static/mediacontent/users/')):
        os.makedirs('static/mediacontent/users/')


if __name__ == "__main__":
    main()
