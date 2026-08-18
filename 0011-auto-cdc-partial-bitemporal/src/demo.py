import argparse,json
from pathlib import Path

def analyze(p):
    state=dict(p["initial"]); order=[]
    for e in sorted(p["events"],key=lambda x:x["sequence"]): state.update(e["changes"]); order.append(e["sequence"])
    return {"current":state,"applied_sequence":order}

def main():
    q=argparse.ArgumentParser(); q.add_argument("input",nargs="?",default="data/scenario.json"); q.add_argument("--output",default="data/output/report.json"); a=q.parse_args(); report=analyze(json.loads(Path(a.input).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
