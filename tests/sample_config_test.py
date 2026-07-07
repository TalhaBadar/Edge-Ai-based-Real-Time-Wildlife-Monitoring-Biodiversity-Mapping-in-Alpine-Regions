from utils.common import load_yaml


def test_config_loads():
    cfg = load_yaml("configs/config.yaml")
    assert "paths" in cfg
    assert "training" in cfg
    assert "edge" in cfg
    print("Config loaded successfully")


if __name__ == "__main__":
    test_config_loads()
