MODRINTH_API_URL = "https://api.modrinth.com/v2"
MOD_LIST = [
    # base mods
    "fabric-api",
    "cloth-config",
    "sodium",
    "nvidium",
    "lithium",
    "indium",
    "ferrite-core",
    "immediatelyfast",
    "modernfix",
    "moreculling",
    "ebe",
    # optional
    # "sodium-extra",
    # "iris",
    # "debugify",
    # "language-reload",
    # "betterf3",
    # optifine replacements
    # "fabric-language-kotlin",
    # "yacl",
     "obsidianui",
    # "animatica",
    # "optigui",
     "ryoamiclights",
    # "fabricbettergrass",
    # "capes",
     "ok-zoomer",
    # "continuity",
    # "entitytexturefeatures",
    # "entity-model-features",
    # "polytone",
    # "puzzle",
    # Add more mod slugs as needed
]
MINECRAFT_VERSIONS = [
    {"version": "1.21.1", "compatible": ["1.21"]},
    {"version": "1.21", "compatible": ["1.21.1"]},
    {"version": "1.20.6", "compatible": ["1.20.5"]},
    {"version": "1.20.5", "compatible": ["1.20.6"]},
    {"version": "1.20.4", "compatible": ["1.20.3"]},
    {"version": "1.20.3", "compatible": ["1.20.4"]},
    {"version": "1.20.2", "compatible": []},
    {"version": "1.20.1", "compatible": ["1.20"]},
    {"version": "1.20", "compatible": ["1.20.1"]},
    {"version": "1.19.4", "compatible": []},
    {"version": "1.19.3", "compatible": []},
    {"version": "1.19.2", "compatible": ["1.19.1"]},
    {"version": "1.19.1", "compatible": ["1.19.2"]},
    {"version": "1.19", "compatible": []},
    {"version": "1.18.2", "compatible": []},
    {"version": "1.18.1", "compatible": ["1.18"]},
    {"version": "1.18", "compatible": ["1.18.1"]},
    {"version": "1.17.1", "compatible": []},
    {"version": "1.17", "compatible": []},
    {"version": "1.16.5", "compatible": ["1.16.4"]},
    {"version": "1.16.4", "compatible": ["1.16.5"]},
]
MINECRAFT_VERSION = MINECRAFT_VERSIONS[0]["version"]  # Default to the first version in the list
FABRIC_VERSION = "0.16.0"  # Update this to the latest Fabric version
FABRIC_INSTALLER_URL = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.jar"
GITHUB_API_URL = "https://api.github.com"
LITHIUM_REPO = "CaffeineMC/lithium-fabric"
GITHUB_TOKEN = "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"