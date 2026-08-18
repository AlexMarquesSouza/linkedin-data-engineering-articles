import argparse,json
from pathlib import Path

def analyze(p):
    total=sum(x["cost"] for x in p["usage"]); allocated=sum(x["cost"] for x in p["usage"] if x.get("tags"))
    return {"total_cost":total,"allocated_cost":allocated,"unallocated_cost":total-allocated,"coverage_percent":round(100*allocated/total,1)}

def main():
    q=argparse.ArgumentParser(); q.add_argument("input",nargs="?",default="data/scenario.json"); q.add_argument("--output",default="data/output/report.json"); a=q.parse_args(); report=analyze(json.loads(Path(a.input).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
