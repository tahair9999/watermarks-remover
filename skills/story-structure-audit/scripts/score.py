#!/usr/bin/env python3
"""Turn twelve StoryScope checkpoint scores into a structural profile.

The arithmetic here is deliberately simple. Its job is not to be a classifier --
StoryScope's own classifier used 304 features and an XGBoost model -- but to stop
the audit from drifting toward whatever impression formed while reading. Scoring
first and computing second keeps the ranking honest.

Every checkpoint is normalized to a 0.0-1.0 "lean" where 1.0 is the pole the paper
found more often in machine-written fiction and 0.0 the pole more common in its
human corpus (published novels). The mean is reported as an index.

An index is not a verdict. It says how many structural choices went the
conventional way, which is a craft observation about defaults, not evidence of
authorship.

Usage:
    python3 score.py --interactive
    python3 score.py --scores 5,yes,protagonist_choice,1,4,sympathetic,flat,1,2,physical,vague,no
    python3 score.py --scores ... --json
"""

from __future__ import annotations

import argparse
import json
import sys


def scale(lo_is_ai: bool):
    """A 1-5 rubric scale. lo_is_ai=True means 1 is the machine-typical pole."""

    def parse(raw: str) -> float:
        value = int(raw)
        if not 1 <= value <= 5:
            raise ValueError("expected 1-5")
        lean = (5 - value) / 4 if lo_is_ai else (value - 1) / 4
        return lean

    return parse


def choice(mapping: dict[str, float]):
    def parse(raw: str) -> float:
        key = raw.strip().lower().replace("-", "_").replace(" ", "_")
        if key not in mapping:
            raise ValueError(f"expected one of: {', '.join(sorted(mapping))}")
        return mapping[key]

    return parse


BINARY_AI_YES = {"yes": 1.0, "y": 1.0, "no": 0.0, "n": 0.0}
BINARY_AI_NO = {"no": 1.0, "n": 1.0, "yes": 0.0, "y": 0.0}

# (key, label, dimension, parser, prompt shown in interactive mode)
CHECKPOINTS = [
    (
        "thematic_explicitness",
        "Thematic explicitness",
        "Situatedness",
        scale(False),
        "How explicitly is the theme articulated? 1=wholly implicit, 5=stated and underlined",
    ),
    (
        "narratorial_commentary",
        "Narratorial thematic commentary",
        "Situatedness",
        choice(BINARY_AI_YES),
        "Does the narrator step outside the characters to gloss the theme? yes/no",
    ),
    (
        "agency_in_resolution",
        "Agency in resolution",
        "Plot",
        choice({"protagonist_choice": 1.0, "mixed": 0.5, "external_fate": 0.0}),
        "What drives the resolution? protagonist_choice / mixed / external_fate",
    ),
    (
        "plot_tracks",
        "Plot track count",
        "Plot",
        scale(True),
        "How many plot lines stay live? 1=single track nothing loose, 5=several open threads",
    ),
    (
        "ending_tidiness",
        "Ending tidiness",
        "Plot",
        scale(False),
        "How completely does the ending resolve? 1=abrupt/open, 5=all resolved + denouement",
    ),
    (
        "moral_position",
        "Protagonist moral position",
        "Agents",
        choice({"sympathetic": 1.0, "mixed": 0.5, "ambivalent": 0.0}),
        "Protagonist's moral position? sympathetic / mixed / ambivalent",
    ),
    (
        "escalation",
        "Event escalation curve",
        "Events",
        choice({"flat": 1.0, "even_steps": 0.75, "uneven": 0.25, "spiked": 0.0}),
        "Event intensity curve? flat / even_steps / uneven / spiked",
    ),
    (
        "chronology",
        "Chronological discontinuity",
        "Temporal structure",
        scale(True),
        "How often does the narrative jump in time? 1=strict forward, 5=heavily discontinuous",
    ),
    (
        "recontextualization",
        "Recontextualization depth",
        "Revelation",
        scale(True),
        "Do reveals reframe earlier scenes? 1=only add information, 5=force complete re-reading",
    ),
    (
        "emotion_channel",
        "Emotion channel",
        "Agents",
        choice({"physical": 1.0, "mixed": 0.5, "named": 0.0}),
        "How is emotion mainly conveyed? physical / mixed / named",
    ),
    (
        "intertextuality",
        "Intertextual strategy",
        "Situatedness",
        choice(
            {
                "vague": 1.0,
                "vague_allusion": 1.0,
                "none": 0.6,
                "explicit_named": 0.0,
                "retelling": 0.0,
                "pastiche": 0.0,
                "myth_religion": 0.0,
                "self_referential": 0.0,
            }
        ),
        "Intertextual strategy? vague / none / explicit_named / retelling / pastiche / "
        "myth_religion / self_referential",
    ),
    (
        "reader_address",
        "Reader address / frame breaking",
        "Perspective",
        choice(BINARY_AI_NO),
        "Does the narration ever acknowledge the reader or itself as a telling? yes/no",
    ),
]

BAR_WIDTH = 20


def bar(lean: float) -> str:
    filled = round(lean * BAR_WIDTH)
    return "#" * filled + "." * (BAR_WIDTH - filled)


def collect_interactive() -> list[float]:
    leans = []
    print("Twelve checkpoints. See references/core-features.md for the full rubric.\n")
    for index, (_key, label, dimension, parser, prompt) in enumerate(CHECKPOINTS, 1):
        while True:
            raw = input(f"{index:2}. {label} [{dimension}]\n    {prompt}\n    > ").strip()
            try:
                leans.append(parser(raw))
                break
            except (ValueError, KeyError) as error:
                print(f"    -- {error}, try again")
        print()
    return leans


def collect_from_arg(argument: str) -> list[float]:
    parts = [part.strip() for part in argument.split(",")]
    if len(parts) != len(CHECKPOINTS):
        raise SystemExit(
            f"error: expected {len(CHECKPOINTS)} comma-separated scores, got {len(parts)}.\n"
            f"Order: {', '.join(key for key, *_ in CHECKPOINTS)}"
        )
    leans = []
    for (key, label, _dimension, parser, _prompt), raw in zip(CHECKPOINTS, parts, strict=True):
        try:
            leans.append(parser(raw))
        except (ValueError, KeyError) as error:
            raise SystemExit(f"error: {label} ({key}): {raw!r} -- {error}") from error
    return leans


def build_profile(leans: list[float]) -> dict:
    rows = [
        {
            "key": key,
            "label": label,
            "dimension": dimension,
            "lean": lean,
        }
        for (key, label, dimension, _parser, _prompt), lean in zip(CHECKPOINTS, leans, strict=True)
    ]
    index = sum(leans) / len(leans) * 100

    by_dimension: dict[str, list[float]] = {}
    for row in rows:
        by_dimension.setdefault(row["dimension"], []).append(row["lean"])
    dimensions = {name: sum(values) / len(values) for name, values in by_dimension.items()}

    ranked = sorted(rows, key=lambda row: row["lean"], reverse=True)
    return {
        "index": round(index, 1),
        "checkpoints": rows,
        "dimensions": {k: round(v, 3) for k, v in dimensions.items()},
        "priorities": [row["key"] for row in ranked if row["lean"] >= 0.75][:3],
        "already_human_typical": [row["key"] for row in rows if row["lean"] <= 0.25],
    }


def report(profile: dict) -> None:
    print(f"\nStructural profile\n{'=' * 52}")
    print(f"Conventional-default index: {profile['index']}/100")
    print("(share of structural choices that went the machine-typical way --")
    print(" a craft observation about defaults, not a judgment of authorship)\n")

    print("Checkpoints, most machine-typical first")
    print("-" * 52)
    for row in sorted(profile["checkpoints"], key=lambda r: r["lean"], reverse=True):
        print(f"  {bar(row['lean'])}  {row['lean']:.2f}  {row['label']}")

    print("\nBy dimension")
    print("-" * 52)
    for name, value in sorted(profile["dimensions"].items(), key=lambda kv: -kv[1]):
        print(f"  {bar(value)}  {value:.2f}  {name}")

    labels = {key: label for key, label, *_ in CHECKPOINTS}

    print("\nWork on these first (lean >= 0.75)")
    print("-" * 52)
    if profile["priorities"]:
        for key in profile["priorities"]:
            print(f"  - {labels[key]}")
        print("\n  Read references/revision-moves.md for structural moves on each.")
    else:
        print("  Nothing above the threshold. Say so plainly rather than")
        print("  manufacturing three findings.")

    print("\nLeave alone (lean <= 0.25)")
    print("-" * 52)
    if profile["already_human_typical"]:
        for key in profile["already_human_typical"]:
            print(f"  - {labels[key]}")
    else:
        print("  (none)")

    print(
        "\nReminder: there is no target profile to aim for. The paper's human corpus is"
        "\ndispersed across narrative space -- prescribing a shape reproduces exactly the"
        "\nconvergence it measures. Use this to find choices made by default, then let the"
        "\nauthor decide which defaults were wrong.\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--interactive", action="store_true", help="prompt for each checkpoint")
    group.add_argument("--scores", help="twelve comma-separated scores, in checkpoint order")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    parser.add_argument("--list", action="store_true", help="print checkpoint order and exit")
    args = parser.parse_args(argv)

    if args.list:
        for index, (key, label, dimension, *_rest) in enumerate(CHECKPOINTS, 1):
            print(f"{index:2}. {key:24} {label} [{dimension}]")
        return 0

    if not args.interactive and args.scores is None:
        parser.error("one of --interactive, --scores or --list is required")

    leans = collect_interactive() if args.interactive else collect_from_arg(args.scores)
    profile = build_profile(leans)

    if args.json:
        json.dump(profile, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        report(profile)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # Piping into head/less closes stdout early; that is not an error. Redirect
        # the remaining buffered write to devnull so Python does not report it.
        import os

        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
