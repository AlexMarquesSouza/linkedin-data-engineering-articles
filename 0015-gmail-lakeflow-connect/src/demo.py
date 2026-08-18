import argparse,json
from pathlib import Path

def analyze(p):
    latest={}
    for x in p["messages"]:
        if x["day"]>=p["cursor_day"] and (x["id"] not in latest or x["day"]>latest[x["id"]]): latest[x["id"]]=x["day"]
    return {"ingested":sorted(latest),"new_cursor_day":max(latest.values(),default=p["cursor_day"])}

def main():
    q=argparse.ArgumentParser(); q.add_argument("input",nargs="?",default="data/scenario.json"); q.add_argument("--output",default="data/output/report.json"); a=q.parse_args(); report=analyze(json.loads(Path(a.input).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
