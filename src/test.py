import toml

config = toml.load(open("config.toml"))
print(config)