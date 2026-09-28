# -*- coding: utf-8 -*-
"""The client's editorial decisions on the survey half of guide-data.json, in one place.

    python3 idbc-salary-guide/data/survey_edits.py    # apply to data/guide-data.json (safe to re-run)

build-guide-data.py applies the same edits every time the survey is rebuilt from the research
workbook, so a rebuild cannot undo them. Salary data is not touched (build-salary-data.py owns it).
"""
import io, json, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent

# Questions the client asked to see in a topic (2026-09-25, D40). Their figures are in the
# workbook for every dataset; the workbook's topic sheet left them out. Appended in this order.
ADD_TO_TOPIC = [
    ("Home office", "Általános", "Munkáltatók",
     "Milyen hatással van a jelenlegi home office policy a toborzás sikerességére?"),
    ("Home office", "IT + Contracting", "Munkáltatók",
     "Milyen hatással van a jelenlegi home office policy a toborzás sikerességére?"),
    ("AI", "Általános", "Munkáltatók",
     "Rendelkezik a vállalatod dedikált költségkerettel AI fejlesztésekre vagy kezdeményezésekre?"),
    ("AI", "Általános", "Munkáltatók",
     "Mire használja a vállalatod AI eszközöket a toborzási folyamat során?"),
]
SIDE = {"Munkavállalók": "employee", "Munkáltatók": "employer"}


def apply(guide, areas):
    """Name and order the datasets as the area tiles do (the client's Piaci trendek names, D31),
    and add the questions above to their topics. Stops on anything it cannot place."""
    ds = guide["datasets"]
    order = [guide["totalKey"]]
    for a in areas["areas"]:
        if a["dataKey"] not in ds:
            sys.exit(f"survey_edits: no dataset '{a['dataKey']}' for area '{a['name']}'")
        ds[a["dataKey"]]["label"] = a["name"]
        order.append(a["dataKey"])
    order += [k for k in ds if k not in order]
    guide["datasets"] = {k: ds[k] for k in order}

    topics = {t["topic"]: t for t in guide["topics"]}
    for topic, qset, side, question in ADD_TO_TOPIC:
        lst = topics[topic]["questionSets"][qset][side]
        for k, d in guide["datasets"].items():
            if d["questionSet"] == qset and question not in d[SIDE[side]]["base"]:
                sys.exit(f"survey_edits: '{question[:50]}…' has no figures in dataset '{k}'")
        if question not in lst:
            lst.append(question)
    return guide


if __name__ == "__main__":
    path = HERE / "guide-data.json"
    guide = json.load(io.open(path, encoding="utf-8"))
    areas = json.load(io.open(HERE / "areas.json", encoding="utf-8"))
    before = json.dumps(guide, ensure_ascii=False, separators=(",", ":"))
    after = json.dumps(apply(guide, areas), ensure_ascii=False, separators=(",", ":"))
    if after != before:
        io.open(path, "w", encoding="utf-8").write(after)
    print("survey_edits:", "guide-data.json updated" if after != before else "nothing to change")
