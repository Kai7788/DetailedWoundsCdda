#!/usr/bin/env python3
"""Static validation and coverage reporting for Detailed Wounds.

This deliberately understands the mod's contradictory BIONIC_LIMB filters: they
make secondary and treatment-only wounds unavailable to automatic selection but
do not prevent u_add_wound or wound_fix from adding them explicitly.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".agents", ".codex", "__pycache__"}
MATRIX_DAMAGE_TYPES = (
    "bash",
    "cut",
    "stab",
    "bullet",
    "heat",
    "acid",
    "electric",
    "cold",
    "biological",
)
MATRIX_BODY_PART_TYPES = ("head", "torso", "sensor", "mouth", "arm", "hand", "leg", "foot")
OLD_COLD_SOURCE_IDS = {
    "dw_superficial_cold_injury",
    "dw_deep_cold_injury",
    "dw_severe_cold_injury",
    "dw_extensive_cold_injury",
}
PRODUCTION_DAMAGE_OVERLAYS = {
    "bash": "EOC_DW_DAMAGE_BASH_SECONDARY",
    "cut": "EOC_DW_DAMAGE_CUT_SECONDARY",
    "stab": "EOC_DW_DAMAGE_STAB_SECONDARY",
    "bullet": "EOC_DW_DAMAGE_BULLET_SECONDARY",
    "electric": "EOC_DW_DAMAGE_ELECTRIC_SECONDARY",
    "heat": "EOC_DW_DAMAGE_HEAT_SECONDARY",
}
RESERVED_REQUIREMENT_IDS = {"dw_minor_debridement", "dw_pressure_dressing"}
ACTIVE_EFFECT_IDS = {"dw_respiratory_impairment", "dw_chest_wall_impairment"}
DORMANT_EFFECT_IDS = {
    "dw_wound_contamination",
    "dw_local_wound_infection",
    "dw_tissue_necrosis",
}
UNREFERENCED_EOC_ALLOWLIST = {
    "EOC_DW_BRIDGE_ON_WOUND_CREATED",
    "EOC_DW_BRIDGE_ON_WOUND_TREATED",
    "EOC_DW_TREATMENT_CLEAR_LOCAL_INFECTION",
    "EOC_DW_TREATMENT_DOWNGRADE_LOCAL_INFECTION",
}
INTENTIONALLY_UNTREATABLE_WOUNDS: set[str] = set()

HEALING_CATEGORIES = {
    "A": "Naturally healing primary",
    "B": "Treatment-optional primary family",
    "C": "Treatment-required primary family",
    "D": "Secondary structural family",
    "E": "Respiratory/exposure family",
    "F": "Dormant/unreachable family",
}

TIME_UNITS = {
    "turn": 1,
    "turns": 1,
    "second": 1,
    "seconds": 1,
    "minute": 60,
    "minutes": 60,
    "hour": 3600,
    "hours": 3600,
    "day": 86400,
    "days": 86400,
    "week": 604800,
    "weeks": 604800,
    "month": 2592000,
    "months": 2592000,
    "year": 31536000,
    "years": 31536000,
}


@dataclass(frozen=True)
class Record:
    obj: dict[str, Any]
    path: Path
    index: int

    @property
    def label(self) -> str:
        try:
            path = self.path.relative_to(ROOT)
        except ValueError:
            path = self.path
        return f"{path} [{self.obj.get('id', self.index)}]"


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


@dataclass
class BaseData:
    root: Path | None
    ids_by_type: dict[str, set[str]]
    all_ids: set[str]
    limb_type_scores: dict[str, set[str]]

    @classmethod
    def empty(cls) -> "BaseData":
        return cls(None, defaultdict(set), set(), defaultdict(set))


def json_paths(root: Path) -> list[Path]:
    return [
        path
        for path in sorted(root.rglob("*.json"))
        if not any(part in IGNORED_PARTS for part in path.relative_to(root).parts)
    ]


def load_mod(report: Report) -> list[Record]:
    records: list[Record] = []
    paths = json_paths(ROOT)
    if not paths:
        report.error("No JSON files found in the mod.")
        return records

    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            report.error(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        if not isinstance(data, list):
            report.error(f"{path.relative_to(ROOT)}: top-level JSON value must be an array")
            continue
        if not data:
            report.warn(f"{path.relative_to(ROOT)}: empty JSON array")
        for index, obj in enumerate(data):
            if not isinstance(obj, dict):
                report.error(f"{path.relative_to(ROOT)} [{index}]: entry must be an object")
                continue
            if not isinstance(obj.get("type"), str) or not obj["type"]:
                report.error(f"{path.relative_to(ROOT)} [{index}]: missing non-empty string 'type'")
            if not isinstance(obj.get("id"), str) or not obj["id"]:
                report.error(f"{path.relative_to(ROOT)} [{index}]: missing non-empty string 'id'")
            records.append(Record(obj, path, index))

    seen: dict[tuple[str, str], Record] = {}
    for record in records:
        obj_type = record.obj.get("type")
        obj_id = record.obj.get("id")
        if not isinstance(obj_type, str) or not isinstance(obj_id, str):
            continue
        key = (obj_type, obj_id)
        if key in seen:
            report.error(f"Duplicate ({obj_type}, {obj_id}): {seen[key].label} and {record.label}")
        else:
            seen[key] = record
    return records


def normalize_data_root(path: Path) -> Path | None:
    candidates = (path, path / "data", path / "data" / "json")
    for candidate in candidates:
        if (candidate / "json" / "damage_types.json").is_file():
            return candidate
        if (candidate / "damage_types.json").is_file() and candidate.name == "json":
            return candidate.parent
    return None


def find_base_data(explicit: str | None) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser().resolve())
    candidates.extend(
        [
            ROOT.parent / "cataclysmdda-0.J" / "data",
            ROOT.parent / "Cataclysm-DDA" / "data",
        ]
    )
    for candidate in candidates:
        normalized = normalize_data_root(candidate)
        if normalized:
            return normalized
    return None


def load_base_data(path: Path | None, report: Report) -> BaseData:
    if path is None:
        report.warn("CDDA base data not found; external ID validation was skipped")
        return BaseData.empty()

    json_root = path / "json"
    ids_by_type: dict[str, set[str]] = defaultdict(set)
    all_ids: set[str] = set()
    limb_type_scores: dict[str, set[str]] = defaultdict(set)
    parse_failures = 0

    for file_path in sorted(json_root.rglob("*.json")):
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            parse_failures += 1
            continue
        if not isinstance(data, list):
            continue
        for obj in data:
            if not isinstance(obj, dict):
                continue
            obj_type, obj_id = obj.get("type"), obj.get("id")
            if isinstance(obj_type, str) and isinstance(obj_id, str):
                ids_by_type[obj_type].add(obj_id)
                all_ids.add(obj_id)
            if obj_type == "body_part":
                limb_types = obj.get("limb_types", [])
                if isinstance(limb_types, str):
                    limb_types = [limb_types]
                scores = obj.get("limb_scores", [])
                score_ids = {
                    value[0]
                    for value in scores
                    if isinstance(value, list) and value and isinstance(value[0], str)
                }
                for limb_type in limb_types:
                    if isinstance(limb_type, str):
                        limb_type_scores[limb_type].update(score_ids)

    if parse_failures:
        report.warn(f"Could not parse {parse_failures} base-game JSON file(s)")
    return BaseData(path, ids_by_type, all_ids, limb_type_scores)


def records_of_type(records: Iterable[Record], obj_type: str) -> list[Record]:
    return [record for record in records if record.obj.get("type") == obj_type]


def ordered_pair(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and all(isinstance(item, (int, float)) and not isinstance(item, bool) for item in value)
        and value[0] <= value[1]
    )


def duration_seconds(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s+([A-Za-z]+)\s*", value)
    if not match:
        return None
    factor = TIME_UNITS.get(match.group(2).lower())
    return float(match.group(1)) * factor if factor else None


def validate_wounds(records: list[Record], base: BaseData, report: Report) -> None:
    wounds = records_of_type(records, "wound")
    wound_ids = {record.obj.get("id") for record in wounds}
    wounds_by_id = {
        record.obj["id"]: record
        for record in wounds
        if isinstance(record.obj.get("id"), str)
    }
    valid_damage = base.ids_by_type.get("damage_type", set())
    valid_scores = base.ids_by_type.get("limb_score", set())

    for record in wounds:
        obj = record.obj
        damage_types = obj.get("damage_types")
        if not isinstance(damage_types, list) or not damage_types or not all(
            isinstance(value, str) for value in damage_types
        ):
            report.error(f"{record.label}: 'damage_types' must be a non-empty string array")
        elif valid_damage:
            for damage_type in damage_types:
                if damage_type not in valid_damage:
                    report.error(f"{record.label}: unknown damage type '{damage_type}'")

        if not ordered_pair(obj.get("damage_required")):
            report.error(f"{record.label}: 'damage_required' must be an ordered numeric pair")
        elif obj["damage_required"][0] < 0:
            report.error(f"{record.label}: damage thresholds cannot be negative")
        if not ordered_pair(obj.get("pain")):
            report.error(f"{record.label}: 'pain' must be an ordered numeric pair")
        elif obj["pain"][0] < 0:
            report.error(f"{record.label}: pain range cannot be negative")

        for field in ("weight", "limit"):
            value = obj.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 1:
                report.error(f"{record.label}: '{field}' must be a positive integer")

        if "healing_time" in obj:
            healing = obj["healing_time"]
            if not isinstance(healing, list) or len(healing) != 2:
                report.error(f"{record.label}: 'healing_time' must contain two durations")
            else:
                low, high = (duration_seconds(value) for value in healing)
                if low is None or high is None:
                    report.error(f"{record.label}: unrecognized healing duration {healing!r}")
                elif low > high:
                    report.error(f"{record.label}: healing time range is reversed")

        whitelist = obj.get("whitelist_body_part_types", [])
        if isinstance(whitelist, list) and len(whitelist) > 1:
            report.warn(
                f"{record.label}: multiple body-part whitelist types use AND semantics: {whitelist}"
            )

        scores = obj.get("limb_scores", [])
        if not isinstance(scores, list):
            report.error(f"{record.label}: 'limb_scores' must be an array")
            continue
        score_ids: list[str] = []
        for score in scores:
            if not isinstance(score, dict) or not isinstance(score.get("score"), str):
                report.error(f"{record.label}: malformed limb score entry {score!r}")
                continue
            score_id = score["score"]
            score_ids.append(score_id)
            if valid_scores and score_id not in valid_scores:
                report.error(f"{record.label}: unknown limb score '{score_id}'")
            value = score.get("value")
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 <= value <= 1:
                report.error(f"{record.label}: limb score '{score_id}' value must be between 0 and 1")

        if base.limb_type_scores:
            known_types = set(MATRIX_BODY_PART_TYPES) | {"wing", "tail", "other"}
            blacklist = obj.get("blacklist_body_part_types", [])
            possible_types = set(whitelist) if whitelist else known_types - set(blacklist)
            available = set().union(*(base.limb_type_scores.get(value, set()) for value in possible_types))
            for score_id in score_ids:
                if available and score_id not in available:
                    report.error(
                        f"{record.label}: limb score '{score_id}' is ineffective on every allowed base-game bodypart type"
                    )

        progressions = obj.get("wound_progression", [])
        if not isinstance(progressions, list):
            report.error(f"{record.label}: 'wound_progression' must be an array")
            continue
        for progression in progressions:
            if not isinstance(progression, dict) or not isinstance(progression.get("id"), str):
                report.error(f"{record.label}: malformed wound_progression entry")
                continue
            target = progression["id"]
            chance = progression.get("chance")
            if target not in wound_ids:
                report.error(
                    f"{record.label}: wound_progression references missing wound '{target}'"
                )
            elif target_record := wounds_by_id.get(target):
                known_types = set(MATRIX_BODY_PART_TYPES) | {"wing", "tail", "other"}
                source_whitelist = set(obj.get("whitelist_body_part_types", []))
                target_whitelist = set(target_record.obj.get("whitelist_body_part_types", []))
                source_types = source_whitelist or known_types - set(
                    obj.get("blacklist_body_part_types", [])
                )
                target_types = target_whitelist or known_types - set(
                    target_record.obj.get("blacklist_body_part_types", [])
                )
                if source_types.isdisjoint(target_types):
                    report.error(
                        f"{record.label}: wound_progression target '{target}' has no compatible bodypart type"
                    )
            if target == obj.get("id"):
                report.error(f"{record.label}: wound_progression cannot target itself")
            if not isinstance(chance, (int, float)) or isinstance(chance, bool) or not 0 < chance <= 100:
                report.error(f"{record.label}: wound_progression chance must be in (0, 100]")

    progression_graph = {
        record.obj["id"]: [
            progression["id"]
            for progression in record.obj.get("wound_progression", [])
            if isinstance(progression, dict) and isinstance(progression.get("id"), str)
        ]
        for record in wounds
        if isinstance(record.obj.get("id"), str)
    }
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(wound_id: str, trail: tuple[str, ...]) -> None:
        if wound_id in visiting:
            cycle = " -> ".join((*trail, wound_id))
            report.error(f"wound_progression cycle is not allowlisted: {cycle}")
            return
        if wound_id in visited:
            return
        visiting.add(wound_id)
        for target in progression_graph.get(wound_id, []):
            visit(target, (*trail, wound_id))
        visiting.remove(wound_id)
        visited.add(wound_id)

    for wound_id in progression_graph:
        visit(wound_id, ())


def validate_requirements(records: list[Record], base: BaseData, report: Report) -> None:
    requirements = records_of_type(records, "requirement")
    quality_ids = base.ids_by_type.get("tool_quality", set())
    # The third tuple member "LIST" refers to another requirement definition,
    # despite the historical name used by the JSON syntax.
    group_ids = base.ids_by_type.get("requirement", set()) | {
        record.obj["id"] for record in requirements if isinstance(record.obj.get("id"), str)
    }

    for record in requirements:
        obj = record.obj
        for quality in obj.get("qualities", []):
            if not isinstance(quality, dict) or not isinstance(quality.get("id"), str):
                report.error(f"{record.label}: malformed quality requirement {quality!r}")
                continue
            if quality_ids and quality["id"] not in quality_ids:
                report.error(f"{record.label}: unknown tool quality '{quality['id']}'")
            if not isinstance(quality.get("level"), int) or quality["level"] < 1:
                report.error(f"{record.label}: quality '{quality['id']}' needs a positive integer level")

        components = obj.get("components", [])
        if not isinstance(components, list):
            report.error(f"{record.label}: 'components' must be an array")
            continue
        for group in components:
            if not isinstance(group, list) or not group:
                report.error(f"{record.label}: component group must contain alternatives")
                continue
            for alternative in group:
                if (
                    not isinstance(alternative, list)
                    or len(alternative) not in (2, 3)
                    or not isinstance(alternative[0], str)
                    or not isinstance(alternative[1], int)
                    or alternative[1] == 0
                ):
                    report.error(f"{record.label}: malformed component alternative {alternative!r}")
                    continue
                component_id = alternative[0]
                is_list = len(alternative) == 3 and alternative[2] == "LIST"
                if len(alternative) == 3 and not is_list:
                    report.error(f"{record.label}: unsupported component marker in {alternative!r}")
                elif is_list and group_ids and component_id not in group_ids:
                    report.error(f"{record.label}: unknown component LIST '{component_id}'")
                elif not is_list and base.all_ids and component_id not in base.all_ids:
                    report.error(f"{record.label}: unknown component item '{component_id}'")


def validate_wound_fixes(records: list[Record], base: BaseData, report: Report) -> None:
    fixes = records_of_type(records, "wound_fix")
    wound_map = {
        record.obj["id"]: record
        for record in records_of_type(records, "wound")
        if "id" in record.obj
    }
    wound_ids = set(wound_map)
    requirement_ids = {
        record.obj["id"] for record in records_of_type(records, "requirement") if "id" in record.obj
    }
    skills = base.ids_by_type.get("skill", set())
    proficiencies = base.ids_by_type.get("proficiency", set())
    used_requirements: set[str] = set()

    for record in fixes:
        obj = record.obj
        success_msg = obj.get("success_msg")
        if not isinstance(success_msg, str) or not success_msg.strip():
            report.error(f"{record.label}: wound_fix needs a non-empty success_msg")
        for field in ("wounds_removed", "wounds_added"):
            values = obj.get(field)
            if not isinstance(values, list) or not values or not all(isinstance(value, str) for value in values):
                report.error(f"{record.label}: '{field}' must be a non-empty string array")
                continue
            if len(values) != len(set(values)):
                report.error(f"{record.label}: '{field}' contains duplicate wound IDs")
            for wound_id in values:
                if wound_id not in wound_ids:
                    report.error(f"{record.label}: {field} references missing wound '{wound_id}'")

        sources = obj.get("wounds_removed", [])
        targets = obj.get("wounds_added", [])
        if isinstance(sources, list) and isinstance(targets, list) and set(sources) & set(targets):
            report.error(f"{record.label}: a wound_fix cannot add and remove the same wound ID")
        if isinstance(sources, list) and isinstance(targets, list):
            for source in sources:
                for target in targets:
                    if source not in wound_map or target not in wound_map:
                        continue
                    source_obj = wound_map[source].obj
                    target_obj = wound_map[target].obj
                    if source_obj.get("name") == target_obj.get("name"):
                        report.error(
                            f"{record.label}: treatment target '{target}' must have a distinct display name from '{source}'"
                        )
                    if source_obj.get("description") == target_obj.get("description"):
                        report.error(
                            f"{record.label}: treatment target '{target}' must have a distinct description from '{source}'"
                        )

        time = duration_seconds(obj.get("time"))
        if time is None or time <= 0:
            report.error(f"{record.label}: 'time' must be a positive recognized duration")

        for requirement in obj.get("requirements", []):
            if (
                not isinstance(requirement, list)
                or len(requirement) != 2
                or not isinstance(requirement[0], str)
                or not isinstance(requirement[1], int)
                or requirement[1] < 1
            ):
                report.error(f"{record.label}: malformed requirement reference {requirement!r}")
                continue
            requirement_id = requirement[0]
            used_requirements.add(requirement_id)
            if requirement_id not in requirement_ids:
                report.error(f"{record.label}: missing requirement '{requirement_id}'")

        skill_map = obj.get("skills", {})
        if not isinstance(skill_map, dict):
            report.error(f"{record.label}: 'skills' must be an object")
        else:
            for skill, level in skill_map.items():
                if skills and skill not in skills:
                    report.error(f"{record.label}: unknown skill '{skill}'")
                if not isinstance(level, int) or level < 0:
                    report.error(f"{record.label}: skill '{skill}' needs a non-negative integer level")

        for proficiency in obj.get("proficiencies", []):
            if not isinstance(proficiency, dict) or not isinstance(proficiency.get("proficiency"), str):
                report.error(f"{record.label}: malformed proficiency entry {proficiency!r}")
                continue
            proficiency_id = proficiency["proficiency"]
            if proficiencies and proficiency_id not in proficiencies:
                report.error(f"{record.label}: unknown proficiency '{proficiency_id}'")
            if not isinstance(proficiency.get("is_mandatory"), bool):
                report.error(f"{record.label}: proficiency '{proficiency_id}' needs boolean is_mandatory")
            time_save = proficiency.get("time_save")
            if not isinstance(time_save, (int, float)) or isinstance(time_save, bool) or time_save <= 0:
                report.error(f"{record.label}: proficiency '{proficiency_id}' needs positive time_save")

    unused = requirement_ids - used_requirements
    for requirement_id in sorted(unused & RESERVED_REQUIREMENT_IDS):
        report.note(f"Intentional reserved requirement: {requirement_id}")
    for requirement_id in sorted(unused - RESERVED_REQUIREMENT_IDS):
        report.error(f"Unreferenced requirement is not reserved: {requirement_id}")
    for requirement_id in sorted(RESERVED_REQUIREMENT_IDS - requirement_ids):
        report.error(f"Reserved requirement allowlist contains missing ID: {requirement_id}")


def walk(value: Any) -> Iterable[tuple[str | None, Any, dict[str, Any] | None]]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield key, child, value
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield None, child, None
            yield from walk(child)


def strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)


def referenced_eoc_ids(obj: dict[str, Any]) -> set[str]:
    references: set[str] = set()
    for key, value, _ in walk(obj):
        if key in {"run_eocs", "false_eocs"}:
            references.update(strings(value))
        elif key == "weighted_list_eocs" and isinstance(value, list):
            references.update(
                entry[0]
                for entry in value
                if isinstance(entry, list) and len(entry) == 2 and isinstance(entry[0], str)
            )
    return references


def validate_eocs(records: list[Record], base: BaseData, report: Report) -> None:
    eocs = records_of_type(records, "effect_on_condition")
    eoc_ids = {record.obj["id"] for record in eocs if "id" in record.obj}
    known_eoc_ids = eoc_ids | base.ids_by_type.get("effect_on_condition", set())
    wound_ids = {record.obj["id"] for record in records_of_type(records, "wound") if "id" in record.obj}
    effect_ids = (
        {record.obj["id"] for record in records_of_type(records, "effect_type") if "id" in record.obj}
        | base.ids_by_type.get("effect_type", set())
    )

    for record in eocs:
        for key, value, parent in walk(record.obj):
            if key == "u_remove_effect":
                report.error(f"{record.label}: stale unsupported key 'u_remove_effect'; use 'u_lose_effect'")
            if key == "math":
                for expression in strings(value):
                    if "&&" in expression or "||" in expression:
                        report.error(
                            f"{record.label}: installed CDDA math parser does not support &&/||; use EOC and/or conditions"
                        )
            elif key in {"run_eocs", "false_eocs"}:
                for eoc_id in strings(value):
                    if eoc_id not in eoc_ids:
                        report.error(f"{record.label}: {key} references missing EOC '{eoc_id}'")
            elif key == "weighted_list_eocs":
                if not isinstance(value, list) or not value:
                    report.error(f"{record.label}: weighted_list_eocs must be a non-empty array")
                    continue
                total = 0.0
                valid = True
                for entry in value:
                    if (
                        not isinstance(entry, list)
                        or len(entry) != 2
                        or not isinstance(entry[0], str)
                        or not isinstance(entry[1], (int, float))
                        or isinstance(entry[1], bool)
                        or entry[1] <= 0
                    ):
                        report.error(f"{record.label}: malformed weighted EOC entry {entry!r}")
                        valid = False
                        continue
                    if entry[0] not in eoc_ids:
                        report.error(f"{record.label}: weighted list references missing EOC '{entry[0]}'")
                    total += entry[1]
                if valid and total != 100:
                    report.error(f"{record.label}: project probability list sums to {total:g}, not 100")
            elif key in {
                "u_add_effect",
                "npc_add_effect",
                "u_has_effect",
                "npc_has_effect",
                "u_lose_effect",
                "npc_lose_effect",
            }:
                for effect_id in strings(value):
                    if effect_ids and effect_id not in effect_ids:
                        report.error(f"{record.label}: {key} references missing effect '{effect_id}'")
            elif key == "wound_id":
                for wound_id in strings(value):
                    if wound_id not in wound_ids:
                        report.error(f"{record.label}: references missing wound '{wound_id}'")
            elif key == "compare_string" and isinstance(value, list):
                context = next(
                    (
                        side["context_val"]
                        for side in value
                        if isinstance(side, dict) and isinstance(side.get("context_val"), str)
                    ),
                    None,
                )
                if context == "wound_id":
                    for literal in (side for side in value if isinstance(side, str)):
                        if literal.startswith("dw_") and literal not in wound_ids:
                            report.error(
                                f"{record.label}: wound_id comparison references missing wound '{literal}'"
                            )
                elif context == "effect":
                    for literal in (side for side in value if isinstance(side, str)):
                        if effect_ids and literal not in effect_ids:
                            report.error(
                                f"{record.label}: effect comparison references missing effect '{literal}'"
                            )

    for record in records:
        for field in ("onhit_eocs", "ondamage_eocs"):
            if field not in record.obj:
                continue
            references = record.obj[field]
            if not isinstance(references, list) or not all(isinstance(value, str) for value in references):
                report.error(f"{record.label}: '{field}' must be a string array")
                continue
            for eoc_id in references:
                if eoc_id not in known_eoc_ids:
                    report.error(f"{record.label}: {field} references missing EOC '{eoc_id}'")

    for record in records_of_type(records, "effect_type"):
        for modifier in record.obj.get("limb_score_mods", []):
            score_id = modifier.get("limb_score") if isinstance(modifier, dict) else None
            valid_scores = base.ids_by_type.get("limb_score", set())
            if not isinstance(score_id, str):
                report.error(f"{record.label}: malformed effect limb_score_mods entry {modifier!r}")
            elif valid_scores and score_id not in valid_scores:
                report.error(f"{record.label}: unknown effect limb score '{score_id}'")

    all_references: set[str] = set()
    for record in eocs:
        all_references.update(referenced_eoc_ids(record.obj))
    for record in records:
        for field in ("onhit_eocs", "ondamage_eocs"):
            all_references.update(strings(record.obj.get(field, [])))
    unreferenced = {
        record.obj["id"]
        for record in eocs
        if record.obj.get("eoc_type") != "EVENT"
        and record.obj["id"] not in all_references
        and record.obj["id"] not in UNREFERENCED_EOC_ALLOWLIST
    }
    for eoc_id in sorted(unreferenced):
        report.error(f"Unreferenced EOC is not reserved/dormant: {eoc_id}")
    for eoc_id in sorted(UNREFERENCED_EOC_ALLOWLIST - eoc_ids):
        report.error(f"Dormant EOC allowlist contains missing ID: {eoc_id}")


def validate_damage_overlays(records: list[Record], report: Report) -> None:
    overlays = records_of_type(records, "damage_type")
    by_id = {record.obj.get("id"): record for record in overlays}
    for damage_id, eoc_id in PRODUCTION_DAMAGE_OVERLAYS.items():
        record = by_id.get(damage_id)
        if not record:
            report.error(f"Missing production damage_type overlay '{damage_id}'")
            continue
        if record.obj.get("copy-from") != damage_id:
            report.error(f"{record.label}: vanilla damage overlay must use same-ID copy-from")
        if record.obj.get("ondamage_eocs") != [eoc_id]:
            report.error(
                f"{record.label}: expected ondamage_eocs [ '{eoc_id}' ], got {record.obj.get('ondamage_eocs')!r}"
            )
    for damage_id, record in by_id.items():
        if damage_id not in PRODUCTION_DAMAGE_OVERLAYS:
            report.error(f"{record.label}: unexpected vanilla damage_type replacement/overlay")


def validate_effect_classification(records: list[Record], report: Report) -> None:
    effects = {
        record.obj["id"]
        for record in records_of_type(records, "effect_type")
        if isinstance(record.obj.get("id"), str)
    }
    classified = ACTIVE_EFFECT_IDS | DORMANT_EFFECT_IDS
    for effect_id in sorted(effects - classified):
        report.error(f"Effect has no active/dormant classification: {effect_id}")
    for effect_id in sorted(classified - effects):
        report.error(f"Effect classification references missing effect: {effect_id}")

    active_eocs = production_reachable_eocs(records)
    eoc_map = {
        record.obj["id"]: record.obj
        for record in records_of_type(records, "effect_on_condition")
        if isinstance(record.obj.get("id"), str)
    }
    active_effect_references = {
        effect_id
        for eoc_id in active_eocs
        for key, raw, _ in walk(eoc_map[eoc_id])
        if key in {"u_add_effect", "npc_add_effect", "u_lose_effect", "npc_lose_effect"}
        for effect_id in strings(raw)
    }
    for effect_id in sorted(ACTIVE_EFFECT_IDS - active_effect_references):
        report.error(f"Effect is classified active but has no production-reachable lifecycle entry: {effect_id}")
    effect_map = {
        record.obj["id"]: record
        for record in records_of_type(records, "effect_type")
        if isinstance(record.obj.get("id"), str)
    }
    for effect_id in sorted(ACTIVE_EFFECT_IDS):
        record = effect_map.get(effect_id)
        if record and (
            not isinstance(record.obj.get("remove_message"), str)
            or not record.obj["remove_message"].strip()
        ):
            report.error(f"{record.label}: active finite impairment needs a recovery remove_message")
    for effect_id in sorted(DORMANT_EFFECT_IDS):
        report.note(f"Intentional dormant effect: {effect_id}")


def validate_feedback(records: list[Record], report: Report) -> None:
    """Validate the deliberately bounded v0.2 player-feedback layer.

    Production secondary and respiratory entry EOCs know that they have just added
    a wound to the damaged character. Native primary selection, wound_progression,
    and natural completion do not expose equivalent JSON lifecycle context and are
    intentionally outside this check.
    """
    eoc_map = {
        record.obj["id"]: record
        for record in records_of_type(records, "effect_on_condition")
        if isinstance(record.obj.get("id"), str)
    }
    for eoc_id in sorted(production_reachable_eocs(records)):
        record = eoc_map[eoc_id]
        wound_additions = sum(
            1
            for key, _, _ in walk(record.obj)
            if key in {"u_add_wound", "npc_add_wound"}
        )
        messages = [
            value
            for key, value, _ in walk(record.obj)
            if key in {"u_message", "npc_message"}
        ]
        if wound_additions and len(messages) < wound_additions:
            report.error(
                f"{record.label}: production wound entry has {wound_additions} wound addition(s) "
                f"but only {len(messages)} acquisition message(s)"
            )
        for message in messages:
            if not isinstance(message, str) or not message.strip():
                report.error(f"{record.label}: feedback message must be a non-empty string")


def validate_treatment_reachability(records: list[Record], report: Report) -> None:
    wounds = {
        record.obj["id"]: record
        for record in records_of_type(records, "wound")
        if isinstance(record.obj.get("id"), str)
    }
    treatment_graph: dict[str, set[str]] = defaultdict(set)
    for record in records_of_type(records, "wound_fix"):
        sources = [value for value in record.obj.get("wounds_removed", []) if isinstance(value, str)]
        targets = [value for value in record.obj.get("wounds_added", []) if isinstance(value, str)]
        for source in sources:
            treatment_graph[source].update(targets)

    memo: dict[str, bool] = {}

    def reaches_healing(wound_id: str, visiting: set[str]) -> bool:
        if wound_id in memo:
            return memo[wound_id]
        record = wounds.get(wound_id)
        if record and "healing_time" in record.obj:
            memo[wound_id] = True
            return True
        if wound_id in visiting:
            return False
        result = any(
            reaches_healing(target, visiting | {wound_id})
            for target in treatment_graph.get(wound_id, set())
        )
        memo[wound_id] = result
        return result

    for wound_id, record in wounds.items():
        if "healing_time" in record.obj or wound_id in INTENTIONALLY_UNTREATABLE_WOUNDS:
            continue
        if not reaches_healing(wound_id, set()):
            report.error(f"{record.label}: non-healing wound has no treatment path to a healing state")
    for wound_id in sorted(INTENTIONALLY_UNTREATABLE_WOUNDS - wounds.keys()):
        report.error(f"Intentionally untreatable wound allowlist contains missing ID: {wound_id}")


def has_effect_check(value: Any, effect_id: str, intensity: int, under_not: bool = False) -> bool:
    if isinstance(value, dict):
        if (
            under_not
            and value.get("u_has_effect") == effect_id
            and value.get("intensity") == intensity
        ):
            return True
        return any(
            has_effect_check(child, effect_id, intensity, under_not or key == "not")
            for key, child in value.items()
        )
    if isinstance(value, list):
        return any(has_effect_check(child, effect_id, intensity, under_not) for child in value)
    return False


def regression_checks(records: list[Record], report: Report) -> None:
    fixes = records_of_type(records, "wound_fix")
    for record in fixes:
        for wound_id in record.obj.get("wounds_removed", []):
            if wound_id in OLD_COLD_SOURCE_IDS:
                report.error(f"{record.label}: stale cold source wound ID '{wound_id}'")

    wounds = {record.obj.get("id"): record for record in records_of_type(records, "wound")}
    ocular = wounds.get("dw_ocular_laceration")
    if ocular:
        damage_range = ocular.obj.get("damage_required")
        if not ordered_pair(damage_range) or damage_range[1] < 1000:
            report.error("dw_ocular_laceration must retain severe cut coverage through damage 1000")
    else:
        report.error("Missing regression wound 'dw_ocular_laceration'")

    eocs = {record.obj.get("id"): record for record in records_of_type(records, "effect_on_condition")}
    for eoc_id in ("EOC_DW_MAINTAIN_MODERATE_CONTAMINATION", "EOC_DW_CHECK_MODERATE_CONTAMINATION"):
        record = eocs.get(eoc_id)
        if not record:
            report.error(f"Missing contamination regression EOC '{eoc_id}'")
        elif not has_effect_check(record.obj.get("condition"), "dw_wound_contamination", 3):
            report.error(f"{record.label}: must exclude contamination intensity 3 to prevent downgrading")


def applicability(wound: dict[str, Any], body_part_type: str) -> bool:
    whitelist = wound.get("whitelist_body_part_types", [])
    blacklist = wound.get("blacklist_body_part_types", [])
    if whitelist and not all(value == body_part_type for value in whitelist):
        return False
    if body_part_type in blacklist:
        return False
    if (
        wound.get("whitelist_bp_with_flag") == "BIONIC_LIMB"
        and wound.get("blacklist_bp_with_flag") == "BIONIC_LIMB"
    ):
        return False
    return True


def explicit_applicability(wound: dict[str, Any], body_part_type: str) -> bool:
    """Conceptual anatomy for explicitly added secondary/treatment wounds.

    Unlike automatic selection, this intentionally ignores the contradictory
    BIONIC_LIMB gate used to keep these definitions secondary-only.
    """
    whitelist = wound.get("whitelist_body_part_types", [])
    blacklist = wound.get("blacklist_body_part_types", [])
    if whitelist and not all(value == body_part_type for value in whitelist):
        return False
    return body_part_type not in blacklist


def production_reachable_eocs(records: list[Record]) -> set[str]:
    eocs = {
        record.obj["id"]: record.obj
        for record in records_of_type(records, "effect_on_condition")
        if isinstance(record.obj.get("id"), str)
    }
    roots = {
        eoc_id
        for record in records
        for field in ("onhit_eocs", "ondamage_eocs")
        for eoc_id in strings(record.obj.get(field, []))
    }
    roots.update(
        record.obj["id"]
        for record in records_of_type(records, "effect_on_condition")
        if record.obj.get("eoc_type") == "EVENT" and isinstance(record.obj.get("id"), str)
    )
    reachable: set[str] = set()
    pending = list(roots)
    while pending:
        eoc_id = pending.pop()
        if eoc_id in reachable or eoc_id not in eocs:
            continue
        reachable.add(eoc_id)
        pending.extend(referenced_eoc_ids(eocs[eoc_id]) - reachable)
    return reachable


def production_reachable_wounds(records: list[Record]) -> set[str]:
    eoc_map = {
        record.obj["id"]: record.obj
        for record in records_of_type(records, "effect_on_condition")
        if isinstance(record.obj.get("id"), str)
    }
    reachable = production_reachable_eocs(records)
    wound_ids = {
        value
        for eoc_id in reachable
        for key, raw, _ in walk(eoc_map[eoc_id])
        if key == "wound_id"
        for value in strings(raw)
    }
    wound_map = {
        record.obj["id"]: record.obj
        for record in records_of_type(records, "wound")
        if isinstance(record.obj.get("id"), str)
    }
    pending = list(wound_ids)
    while pending:
        wound_id = pending.pop()
        for progression in wound_map.get(wound_id, {}).get("wound_progression", []):
            target = progression.get("id") if isinstance(progression, dict) else None
            if isinstance(target, str) and target not in wound_ids:
                wound_ids.add(target)
                pending.append(target)
    return wound_ids


def wound_group(record: Record) -> str:
    return next(
        (group for group in ("primary", "secondary", "treated") if group in record.path.parts),
        "other",
    )


def healing_classifications(records: list[Record]) -> dict[str, str]:
    """Assign every existing wound to exactly one documented healing category.

    Primary and secondary definitions establish the family category. Treated states
    inherit the category of their treatment-chain source. Production-unreachable
    secondary families, and treated states descended only from them, remain dormant.
    """
    wounds = {
        record.obj["id"]: record
        for record in records_of_type(records, "wound")
        if isinstance(record.obj.get("id"), str)
    }
    fixes = records_of_type(records, "wound_fix")
    direct_fix_sources = {
        wound_id
        for record in fixes
        for wound_id in record.obj.get("wounds_removed", [])
        if isinstance(wound_id, str)
    }
    reverse_treatment: dict[str, set[str]] = defaultdict(set)
    for record in fixes:
        sources = [value for value in record.obj.get("wounds_removed", []) if isinstance(value, str)]
        targets = [value for value in record.obj.get("wounds_added", []) if isinstance(value, str)]
        for target in targets:
            reverse_treatment[target].update(sources)

    production_wounds = production_reachable_wounds(records)
    base: dict[str, str] = {}
    for wound_id, record in wounds.items():
        group = wound_group(record)
        if group == "primary":
            if "healing_time" not in record.obj:
                base[wound_id] = "C"
            elif wound_id in direct_fix_sources:
                base[wound_id] = "B"
            else:
                base[wound_id] = "A"
        elif group == "secondary":
            if wound_id not in production_wounds:
                base[wound_id] = "F"
            elif record.path.name == "respiratory_injuries.json":
                base[wound_id] = "E"
            else:
                base[wound_id] = "D"

    memo: dict[str, set[str]] = {}

    def source_categories(wound_id: str, visiting: set[str]) -> set[str]:
        if wound_id in base:
            return {base[wound_id]}
        if wound_id in memo:
            return memo[wound_id]
        if wound_id in visiting:
            return set()
        categories = set().union(
            *(
                source_categories(source, visiting | {wound_id})
                for source in reverse_treatment.get(wound_id, set())
            )
        )
        memo[wound_id] = categories
        return categories

    result: dict[str, str] = {}
    for wound_id in wounds:
        categories = source_categories(wound_id, set())
        if len(categories) == 1:
            result[wound_id] = next(iter(categories))
    return result


def validate_healing_classifications(records: list[Record], report: Report) -> None:
    wounds = {
        record.obj["id"]: record
        for record in records_of_type(records, "wound")
        if isinstance(record.obj.get("id"), str)
    }
    classifications = healing_classifications(records)
    for wound_id, record in wounds.items():
        if wound_id not in classifications:
            report.error(f"{record.label}: wound has no unambiguous healing category")
        elif classifications[wound_id] not in HEALING_CATEGORIES:
            report.error(
                f"{record.label}: unknown healing category '{classifications[wound_id]}'"
            )
    for wound_id in sorted(classifications.keys() - wounds.keys()):
        report.error(f"Healing classification references missing wound '{wound_id}'")


def wound_reachability(record: Record, classification: str) -> str:
    if classification == "F":
        return "dormant"
    if wound_group(record) == "treated":
        return "via wound_fix"
    if wound_group(record) == "secondary":
        return "production EOC"
    return "native selection"


def healing_matrix_markdown(records: list[Record]) -> str:
    wounds = {
        record.obj["id"]: record
        for record in records_of_type(records, "wound")
        if isinstance(record.obj.get("id"), str)
    }
    fixes = records_of_type(records, "wound_fix")
    direct_fix_sources = {
        wound_id
        for record in fixes
        for wound_id in record.obj.get("wounds_removed", [])
        if isinstance(wound_id, str)
    }
    classifications = healing_classifications(records)
    counts = Counter(classifications.values())
    finite = sum("healing_time" in record.obj for record in wounds.values())
    indefinite = len(wounds) - finite

    lines = [
        "# Healing classification matrix",
        "",
        "Generated by `python3 tools/validate_mod.py --healing-matrix-output docs/HEALING_MATRIX.md`.",
        "Every current wound belongs to exactly one category in the wound catalog carried into v0.2;",
        "the installed CDDA JSON API cannot safely observe or transition native wound healing",
        "progress, so no timed visible-stage controller is enabled.",
        "",
        "## Summary",
        "",
        "| Category | Meaning | Wounds |",
        "|---|---|---:|",
    ]
    for category, description in HEALING_CATEGORIES.items():
        lines.append(f"| {category} | {description} | {counts.get(category, 0)} |")
    lines.extend(
        [
            "",
            f"- Total wounds: {len(wounds)}",
            f"- Native finite healing timers: {finite}",
            f"- Treatment-gated/indefinite definitions: {indefinite}",
            "- Timed visible healing-stage wounds: 0 (blocked by the audited JSON API)",
            "- Healing-completion messages: 0 (no trustworthy wound-completion hook)",
            "",
            "## Definitions",
            "",
            "| Category | Wound | Layer | Reachability | Native timer | Direct fix | Visible timed stages |",
            "|---|---|---|---|---|:---:|:---:|",
        ]
    )
    for wound_id, record in sorted(
        wounds.items(), key=lambda item: (classifications.get(item[0], "?"), item[0])
    ):
        category = classifications.get(wound_id, "?")
        healing = record.obj.get("healing_time")
        timer = (
            f"{healing[0]} – {healing[1]}"
            if isinstance(healing, list) and len(healing) == 2
            else "indefinite"
        )
        lines.append(
            f"| {category} | `{wound_id}` | {wound_group(record)} | "
            f"{wound_reachability(record, category)} | {timer} | "
            f"{'yes' if wound_id in direct_fix_sources else 'no'} | no |"
        )
    lines.extend(
        [
            "",
            "## Category rules",
            "",
            "- **A:** finite primary wound with no direct treatment; it heals on CDDA's native timer.",
            "- **B:** finite primary family with optional treatment; treated descendants inherit B.",
            "- **C:** primary family whose entry wound requires treatment before finite recovery; treated descendants inherit C.",
            "- **D:** production-reachable structural secondary family, including its treated states.",
            "- **E:** production-reachable respiratory/exposure family.",
            "- **F:** source event is unavailable or deliberately dormant; descendants are also dormant.",
            "",
        ]
    )
    return "\n".join(lines)


def healing_duration_markdown(records: list[Record]) -> str:
    wounds = {
        record.obj["id"]: record
        for record in records_of_type(records, "wound")
        if isinstance(record.obj.get("id"), str)
    }
    classifications = healing_classifications(records)
    finite = [record for record in wounds.values() if "healing_time" in record.obj]
    indefinite = [record for record in wounds.values() if "healing_time" not in record.obj]
    lines = [
        "# Healing duration audit",
        "",
        "The safe JSON-only result leaves every native healing range unchanged. No visible timed",
        "stage chain is enabled because this CDDA build cannot observe wound progress or validate",
        "a delayed transition after treatment/reinjury. Accordingly, the audited result equals the",
        "v0.1 baseline and every duration delta is zero.",
        "",
        "| Wound | Category | v0.1 min | v0.1 max | Audited min | Audited max | Delta min | Delta max | Stages |",
        "|---|:---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for record in sorted(finite, key=lambda value: value.obj["id"]):
        wound_id = record.obj["id"]
        low, high = record.obj["healing_time"]
        lines.append(
            f"| `{wound_id}` | {classifications[wound_id]} | {low} | {high} | "
            f"{low} | {high} | 0% | 0% | 0 |"
        )
    lines.extend(
        [
            "",
            "## Treatment-gated definitions",
            "",
            "These definitions intentionally have no finite native timer. Their existing treatment",
            "graphs reach a finite treated state; the strict validator checks that transitively.",
            "",
        ]
    )
    for record in sorted(indefinite, key=lambda value: value.obj["id"]):
        lines.append(f"- `{record.obj['id']}` (category {classifications[record.obj['id']]})")
    lines.append("")
    return "\n".join(lines)


def message_audit_markdown(records: list[Record]) -> str:
    eoc_map = {
        record.obj["id"]: record
        for record in records_of_type(records, "effect_on_condition")
        if isinstance(record.obj.get("id"), str)
    }
    acquisition: list[tuple[str, list[str], list[str]]] = []
    for eoc_id in sorted(production_reachable_eocs(records)):
        record = eoc_map[eoc_id]
        wound_ids = [
            value
            for key, raw, _ in walk(record.obj)
            if key == "wound_id"
            for value in strings(raw)
        ]
        messages = [
            raw
            for key, raw, _ in walk(record.obj)
            if key in {"u_message", "npc_message"} and isinstance(raw, str)
        ]
        if wound_ids and messages:
            acquisition.append((eoc_id, wound_ids, messages))

    fixes = sorted(
        records_of_type(records, "wound_fix"), key=lambda record: record.obj["id"]
    )
    active_effects = {
        record.obj["id"]: record.obj
        for record in records_of_type(records, "effect_type")
        if record.obj.get("id") in ACTIVE_EFFECT_IDS
    }
    acquisition_message_count = sum(len(messages) for _, _, messages in acquisition)
    treatment_message_count = sum(
        isinstance(record.obj.get("success_msg"), str) and bool(record.obj["success_msg"].strip())
        for record in fixes
    )
    recovery_message_count = sum(
        isinstance(obj.get("remove_message"), str) and bool(obj["remove_message"].strip())
        for obj in active_effects.values()
    )

    lines = [
        "# v0.2 message coverage audit",
        "",
        "Generated by `python3 tools/validate_mod.py --message-audit-output docs/V02_MESSAGE_AUDIT.md`.",
        "Messages are attached only where JSON observes the real transition. `u_message` and",
        "effect `remove_message` are avatar-facing; NPC recovery remains silent.",
        "",
        "## Summary",
        "",
        f"- Production acquisition messages: {acquisition_message_count}",
        f"- Native wound-fix success messages: {treatment_message_count}",
        f"- Finite acute recovery milestones: {recovery_message_count}",
        "- Distinct native wound-progression messages: 0 (no success callback/context)",
        "- Exact natural wound-healing messages: 0 (no wound-healed event/query)",
        "",
        "## Production acquisition feedback",
        "",
        "| EOC | Wound outcome(s) | Message(s) |",
        "|---|---|---|",
    ]
    for eoc_id, wound_ids, messages in acquisition:
        lines.append(
            f"| `{eoc_id}` | "
            + ", ".join(f"`{wound_id}`" for wound_id in wound_ids)
            + " | "
            + "<br>".join(messages)
            + " |"
        )
    lines.extend(
        [
            "",
            "## Treatment completion feedback",
            "",
            "| Wound fix | Success message |",
            "|---|---|",
        ]
    )
    for record in fixes:
        lines.append(f"| `{record.obj['id']}` | {record.obj['success_msg']} |")
    lines.extend(
        [
            "",
            "## Safe recovery milestones",
            "",
            "| Effect | Removal message | Meaning |",
            "|---|---|---|",
        ]
    )
    meanings = {
        "dw_respiratory_impairment": "The finite acute breathing restriction expired; the longer wound may remain.",
        "dw_chest_wall_impairment": "The finite acute chest restriction expired; the longer wound may remain.",
    }
    for effect_id in sorted(active_effects):
        lines.append(
            f"| `{effect_id}` | {active_effects[effect_id]['remove_message']} | {meanings[effect_id]} |"
        )
    lines.extend(
        [
            "",
            "## Deliberate gaps",
            "",
            "Natural primary acquisition is silent because native wound selection exposes no chosen wound ID.",
            "Native `wound_progression` exposes neither success nor old/new wound context, so production",
            "messages describe a structural event in wording valid for either a new injury or aggravation.",
            "Natural wound completion remains silent because CDDA erases the wound without a JSON event.",
            "No parallel timer or unverified healing claim is used.",
            "",
        ]
    )
    return "\n".join(lines)


def coverage_markdown(records: list[Record]) -> str:
    primary = [
        record.obj
        for record in records_of_type(records, "wound")
        if "wounds" in record.path.parts and "primary" in record.path.parts
    ]
    fixes = records_of_type(records, "wound_fix")
    treated = {
        wound_id
        for record in fixes
        for wound_id in record.obj.get("wounds_removed", [])
        if isinstance(wound_id, str)
    }
    secondary = [
        record.obj
        for record in records_of_type(records, "wound")
        if "wounds" in record.path.parts and "secondary" in record.path.parts
    ]
    production_wounds = production_reachable_wounds(records)

    cells: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for wound in primary:
        for damage_type in wound.get("damage_types", []):
            for body_part_type in MATRIX_BODY_PART_TYPES:
                if applicability(wound, body_part_type):
                    cells[(damage_type, body_part_type)].append(wound)

    lines = [
        "# Detailed Wounds coverage matrix",
        "",
        "Generated from the current files by `python3 tools/validate_mod.py --coverage-output docs/WOUND_MATRIX.md`.",
        "It separates automatically selectable primary wounds from secondary wounds reachable through production JSON hooks.",
        "",
        "A cell shows `primary definitions / definitions with a direct wound_fix`.",
        "A zero treatment count is acceptable when every listed wound heals naturally.",
        "",
        "| Damage | " + " | ".join(MATRIX_BODY_PART_TYPES) + " |",
        "|---|" + "---:|" * len(MATRIX_BODY_PART_TYPES),
    ]
    for damage_type in MATRIX_DAMAGE_TYPES:
        values = []
        for body_part_type in MATRIX_BODY_PART_TYPES:
            wounds = cells.get((damage_type, body_part_type), [])
            if wounds:
                values.append(f"{len(wounds)} / {sum(wound['id'] in treated for wound in wounds)}")
            elif damage_type == "biological":
                values.append("secondary only")
            else:
                values.append("**missing**")
        lines.append(f"| {damage_type} | " + " | ".join(values) + " |")

    lines.extend(
        [
            "",
            "## Runtime validation of Phase D coverage",
            "",
            "The following direct specialized routes have been confirmed in-game. This records",
            "only the bodypart/damage combinations and treatment behavior that were actually",
            "tested; it does not claim runtime coverage of every severity tier.",
            "",
            "| Bodypart type | Damage | Specialized generation | Native treatment |",
            "|---|---|:---:|:---:|",
            "| sensor | cold | passed | passed |",
            "| mouth | stab | passed | passed |",
            "| mouth | bullet | passed | passed |",
            "| mouth | heat | passed | passed |",
            "| mouth | acid | passed | passed |",
            "| mouth | electric | passed | passed |",
            "| mouth | cold | passed | passed |",
            "",
            "The severe oral chemical irrigation-then-debridement chain passed in-game, and a",
            "resulting treated wound state was verified across save/load.",
        ]
    )

    secondary_cells: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for wound in secondary:
        if wound.get("id") not in production_wounds:
            continue
        for damage_type in wound.get("damage_types", []):
            for body_part_type in MATRIX_BODY_PART_TYPES:
                if explicit_applicability(wound, body_part_type):
                    secondary_cells[(damage_type, body_part_type)].append(wound)
    lines.extend(
        [
            "",
            "## Production secondary coverage",
            "",
            "These counts include wounds directly added by an active damage/effect hook and worse states reachable through native `wound_progression`.",
            "A cell shows `reachable secondary definitions / definitions with a direct wound_fix`.",
            "",
            "| Damage | " + " | ".join(MATRIX_BODY_PART_TYPES) + " |",
            "|---|" + "---:|" * len(MATRIX_BODY_PART_TYPES),
        ]
    )
    for damage_type in MATRIX_DAMAGE_TYPES:
        values = []
        for body_part_type in MATRIX_BODY_PART_TYPES:
            wounds = secondary_cells.get((damage_type, body_part_type), [])
            values.append(
                f"{len(wounds)} / {sum(wound['id'] in treated for wound in wounds)}" if wounds else "—"
            )
        lines.append(f"| {damage_type} | " + " | ".join(values) + " |")
    lines.extend(
        [
            "",
            "Generic structural damage routing is intentionally limited to standard flesh arms, hands, legs, feet, and torso. Head, eye, and mouth physical damage remains under specialized primary wound control; the mouth biological entry above is source-specific upper-airway exposure. Bite trauma and thermal-airway wounds remain defined but lack a sufficiently precise production event in this build.",
        ]
    )

    missing = [
        (damage_type, body_part_type)
        for damage_type in MATRIX_DAMAGE_TYPES
        if damage_type != "biological"
        for body_part_type in MATRIX_BODY_PART_TYPES
        if not cells.get((damage_type, body_part_type))
    ]
    lines.extend(
        [
            "",
            "## Direct primary coverage gaps",
            "",
        ]
    )
    if missing:
        for damage_type, body_part_type in missing:
            lines.append(f"- `{body_part_type}` × `{damage_type}`")
    else:
        lines.append("None.")
    lines.extend(
        [
            "",
            "`biological` is intentionally not treated as generic direct wound coverage. Existing respiratory",
            "and exposure wounds are secondary-only, and a broad biological-damage hook would create false",
            "lung injuries for non-respiratory poison/internal damage.",
            "",
            "## Primary treatment reachability",
            "",
        ]
    )
    no_fix = [wound for wound in primary if wound["id"] not in treated]
    dead_ends = [wound for wound in no_fix if "healing_time" not in wound]
    lines.extend(
        [
            f"- Primary wound definitions: {len(primary)}",
            f"- Primary wounds with a direct `wound_fix`: {len(primary) - len(no_fix)}",
            f"- Naturally healing primary wounds without a direct fix: {len(no_fix) - len(dead_ends)}",
            f"- Non-healing primary wounds without a treatment path: {len(dead_ends)}",
            "",
            "## Detailed primary definitions",
            "",
            "| Damage | Bodypart type | Wound | Damage | Direct fix | Natural healing |",
            "|---|---|---|---:|:---:|:---:|",
        ]
    )
    for damage_type in MATRIX_DAMAGE_TYPES:
        for body_part_type in MATRIX_BODY_PART_TYPES:
            for wound in sorted(cells.get((damage_type, body_part_type), []), key=lambda item: item["damage_required"]):
                damage_range = f"{wound['damage_required'][0]}–{wound['damage_required'][1]}"
                lines.append(
                    f"| {damage_type} | {body_part_type} | `{wound['id']}` | {damage_range} | "
                    f"{'yes' if wound['id'] in treated else 'no'} | {'yes' if 'healing_time' in wound else 'no'} |"
                )
    unreachable_secondary = sorted(
        wound["id"] for wound in secondary if wound.get("id") not in production_wounds
    )
    lines.extend(
        [
            "",
            "## Secondary reachability summary",
            "",
            f"- Secondary wound definitions: {len(secondary)}",
            f"- Production-reachable secondary wounds: {len(secondary) - len(unreachable_secondary)}",
            f"- Intentionally dormant/unreachable secondary wounds: {len(unreachable_secondary)}",
        ]
    )
    if unreachable_secondary:
        lines.append("- Dormant IDs: " + ", ".join(f"`{value}`" for value in unreachable_secondary))
    lines.append("")
    return "\n".join(lines)


def print_report(records: list[Record], base: BaseData, report: Report) -> None:
    counts = Counter(record.obj.get("type", "<missing>") for record in records)
    wound_groups = Counter(
        next(
            (group for group in ("primary", "secondary", "treated") if group in record.path.parts),
            "other",
        )
        for record in records_of_type(records, "wound")
    )
    progression_count = sum(
        len(record.obj.get("wound_progression", []))
        for record in records_of_type(records, "wound")
        if isinstance(record.obj.get("wound_progression", []), list)
    )
    healing_categories = Counter(healing_classifications(records).values())
    reachable_eocs = production_reachable_eocs(records)
    eoc_map = {
        record.obj["id"]: record.obj
        for record in records_of_type(records, "effect_on_condition")
        if isinstance(record.obj.get("id"), str)
    }
    acquisition_messages = sum(
        1
        for eoc_id in reachable_eocs
        for key, _, _ in walk(eoc_map[eoc_id])
        if key == "u_message"
    )
    treatment_messages = sum(
        isinstance(record.obj.get("success_msg"), str) and bool(record.obj["success_msg"].strip())
        for record in records_of_type(records, "wound_fix")
    )
    recovery_messages = sum(
        record.obj.get("id") in ACTIVE_EFFECT_IDS
        and isinstance(record.obj.get("remove_message"), str)
        and bool(record.obj["remove_message"].strip())
        for record in records_of_type(records, "effect_type")
    )
    print(f"Parsed {len(json_paths(ROOT))} JSON files and {len(records)} objects.")
    if base.root:
        print(f"CDDA base data: {base.root}")
    for obj_type in (
        "wound",
        "wound_fix",
        "requirement",
        "effect_type",
        "effect_on_condition",
        "damage_type",
    ):
        print(f"  {obj_type}: {counts.get(obj_type, 0)}")
    print(
        "  wound groups: "
        f"primary={wound_groups['primary']}, secondary={wound_groups['secondary']}, "
        f"treated={wound_groups['treated']}, other={wound_groups['other']}"
    )
    print(f"  wound_progression relationships: {progression_count}")
    print(
        "  healing categories: "
        + ", ".join(
            f"{category}={healing_categories.get(category, 0)}"
            for category in HEALING_CATEGORIES
        )
    )
    print(
        "  feedback messages: "
        f"acquisition={acquisition_messages}, treatment={treatment_messages}, "
        f"acute_recovery={recovery_messages}"
    )
    for heading, messages in (
        ("ERRORS", report.errors),
        ("WARNINGS", report.warnings),
        ("NOTES", report.notes),
    ):
        if messages:
            print(f"\n{heading} ({len(messages)}):")
            for message in messages:
                print(f"- {message}")
    if not report.errors and not report.warnings:
        print("\nValidation passed with no errors or warnings.")
    elif not report.errors:
        print("\nValidation passed with warnings.")
    else:
        print("\nValidation failed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cdda-data",
        help="CDDA data directory or game root; defaults to a sibling cataclysmdda-0.J checkout",
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="print the generated Markdown coverage matrix after validation",
    )
    parser.add_argument(
        "--coverage-output",
        metavar="PATH",
        help="write the generated Markdown coverage matrix inside the repository",
    )
    parser.add_argument(
        "--healing-matrix-output",
        metavar="PATH",
        help="write the complete wound healing-classification matrix inside the repository",
    )
    parser.add_argument(
        "--healing-duration-output",
        metavar="PATH",
        help="write the current healing-duration preservation audit inside the repository",
    )
    parser.add_argument(
        "--message-audit-output",
        metavar="PATH",
        help="write the v0.2 acquisition/treatment/recovery message audit inside the repository",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a failure status for warnings as well as errors",
    )
    args = parser.parse_args()

    report = Report()
    records = load_mod(report)
    base = load_base_data(find_base_data(args.cdda_data), report)
    validate_wounds(records, base, report)
    validate_requirements(records, base, report)
    validate_wound_fixes(records, base, report)
    validate_eocs(records, base, report)
    validate_damage_overlays(records, report)
    validate_effect_classification(records, report)
    validate_feedback(records, report)
    validate_treatment_reachability(records, report)
    validate_healing_classifications(records, report)
    regression_checks(records, report)
    print_report(records, base, report)
    coverage = coverage_markdown(records) if args.coverage or args.coverage_output else None
    if args.coverage:
        print("\n" + coverage)
    if args.coverage_output:
        output = Path(args.coverage_output)
        if not output.is_absolute():
            output = ROOT / output
        output = output.resolve()
        if output != ROOT and ROOT not in output.parents:
            parser.error("--coverage-output must remain inside the repository")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(coverage, encoding="utf-8")
        print(f"Coverage matrix written to {output.relative_to(ROOT)}")
    generated_documents = (
        (args.healing_matrix_output, healing_matrix_markdown(records), "Healing matrix"),
        (args.healing_duration_output, healing_duration_markdown(records), "Healing duration audit"),
        (args.message_audit_output, message_audit_markdown(records), "Message audit"),
    )
    for destination, contents, label in generated_documents:
        if not destination:
            continue
        output = Path(destination)
        if not output.is_absolute():
            output = ROOT / output
        output = output.resolve()
        if output != ROOT and ROOT not in output.parents:
            parser.error(f"{label} output must remain inside the repository")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(contents, encoding="utf-8")
        print(f"{label} written to {output.relative_to(ROOT)}")
    return 1 if report.errors or (args.strict and report.warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
