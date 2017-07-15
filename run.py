from app.app import Runner
from config import Config


if __name__ == '__main__':
    cfg = Config()
    data = cfg.read()

    Runner.run(cfg, data)
