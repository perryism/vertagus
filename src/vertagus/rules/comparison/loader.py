import typing as T
from . import library
from vertagus.core.rule_bases import VersionComparisonRule


def load_rules():
    _rules = []
    for obj in dir(library):
        if issubclass(getattr(library, obj), VersionComparisonRule):
            obj: T.Type[VersionComparisonRule] = obj
            if obj.name != "base":
                _rules.append(getattr(library, obj))
    return _rules


def get_rules(rule_names) -> list[T.Type[VersionComparisonRule]]:
    rules = load_rules()
    rules: list[T.Type[VersionComparisonRule]] = rules
    rules_d = {rule.name: rule for rule in rules if rule.name in rule_names}
    return [rules_d[rule_name] for rule_name in rule_names]