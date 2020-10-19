import os


class InitProject:
    def __init__(self):
        self.project = os.getcwd().replace(os.path.basename(os.getcwd()), 'project')

    def __call__(self, *args, **kwargs):
        self.init_users_folder()

    def init_users_folder(self):
        if not os.path.exists(os.path.join(self.project, 'mediacontent/users/')):
            os.makedirs(os.path.join(self.project, 'mediacontent/users/'))


def main():
    init = InitProject()
    init()


if __name__ == "__main__":
    main()
