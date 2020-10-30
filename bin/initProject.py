import os


class InitProject:
    def __init__(self):
        self.project = os.getcwd().replace(os.path.basename(os.getcwd()), 'project')

    def __call__(self, *args, **kwargs):
        self.init_users_folder()
        self.init_banners_folder()

    def init_banners_folder(self):
        path = os.path.join(self.project, 'mediacontent/banners/')
        if not os.path.exists(path):
            os.makedirs(path)

    def init_users_folder(self):
        path = os.path.join(self.project, 'mediacontent/users/')
        if not os.path.exists(path):
            os.makedirs(path)


def main():
    init = InitProject()
    init()


if __name__ == "__main__":
    main()
