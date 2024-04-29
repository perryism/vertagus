import typing as T
from dataclasses import dataclass, field, asdict

class ScmConfigBase(T.TypedDict):
    scm_type: str


ScmConfig: T.TypeAlias = T.Union[ScmConfigBase, dict]


class ProjectConfig(T.TypedDict):
    manifests: list[T.Type["ManifestConfig"]]
    rules: "RulesConfig"
    stages: dict[str, "StageConfig"]


class ManifestConfig(T.TypedDict):
    type: str
    path: str
    loc: T.Optional[str]


class ManifestComparisonConfig(T.TypedDict):
    manifests: list[str]


class RulesConfig(T.TypedDict):
    current: list[str]
    increment: list[str]
    manifest_comparisons: list[ManifestComparisonConfig]


class StageConfig(T.TypedDict):
    name: str
    manifests: T.Optional[list[str]]
    rules: T.Optional["RulesConfig"]
    aliases: T.Optional[list[str]]


class MasterConfig(T.TypedDict):
    project: ProjectConfig
    scm: T.Union[ScmConfigBase, dict]


@dataclass
class RulesData:
    current: list[str] = field(default_factory=list)
    increment: list[str] = field(default_factory=list)
    manifest_comparisons: list[ManifestComparisonConfig] = field(default_factory=list)


@dataclass
class ManifestData:
    name: str
    type: str
    path: str
    loc: str = field(default=None)

    def config(self):
        return dict(name=self.name, path=self.path, loc=self.loc)



class StageData:

    def __init__(self,
                 name: str,
                 manifests: list[ManifestData],
                 rules: RulesData,
                 aliases: list[str] = None
                 ):
        self.name: str = name
        self.manifests: list[ManifestData] = manifests
        self.rules: RulesData = rules
        self.aliases: list[str] = aliases

    @classmethod
    def from_stage_config(cls, name: str, config: StageConfig):
        return cls(
            name=name,
            manifests=[ManifestData(**m) for m in config.get("manifests", [])],
            rules=RulesData(
                current=config.get("rules", {}).get("current", []),
                increment=config.get("rules").get("increment", []),
                manifest_comparisons=config.get("rules").get("manifest_comparisons", []),
            ),
            aliases=config.get("aliases", []),
        )

    def config(self):
        return dict(
            name=self.name,
            manifests=[m.config() for m in self.manifests],
            current_version_rules=self.rules.current,
            version_increment_rules=self.rules.increment,
            manifest_versions_comparison_rules=self.rules.manifest_comparisons,
            aliases=self.aliases,
        )


class ProjectData:
    
    def __init__(self,
                 manifests: list[ManifestData],
                 rules: RulesData,
                 stages: list[StageData]
                 ):
        self.manifests: list[ManifestData] = manifests
        self.rules: RulesData = rules
        self.stages: list[StageData] = stages

    def config(self):
        return dict(
            manifests=[m.config() for m in self.manifests],
            stages = [stage.config() for stage in self.stages.values()],
            current_version_rules=self.rules.current,
            version_increment_rules=self.rules.increment,
            manifest_versions_comparison_rules=self.rules.manifest_comparisons,
        )
    
    @classmethod
    def from_project_config(cls, config: ProjectConfig):
        return cls(
            manifests=[ManifestData(**m) for m in config.get("manifests", [])],
            rules=RulesData(
                current=config.get("rules", {}).get("current", []),
                increment=config.get("rules").get("increment", []),
                manifest_comparisons=config.get("rules").get("manifest_comparisons", []),
            ),
            stages=[StageData.from_stage_config(name, data) for name, data in config["stages"].items()],
        )


class ScmData:
    
    def __init__(self, type, **kwargs):
        self.scm_type = type
        self.kwargs = kwargs

    def config(self):
        return self.kwargs