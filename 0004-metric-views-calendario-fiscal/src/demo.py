import argparse,json
from pathlib import Path

def analyze(p):
    rows=sorted(p["periods"],key=lambda x:x["index"]); out=[]
    for i,x in enumerate(rows): out.append({"index":x["index"],"average":round(sum(y["value"] for y in rows[max(0,i-1):i+1])/len(rows[max(0,i-1):i+1]),1)})
    return {"trailing_2":out}

def main():
    q=argparse.ArgumentParser(); q.add_argument("input",nargs="?",default="data/scenario.json"); q.add_argument("--output",default="data/output/report.json"); a=q.parse_args(); report=analyze(json.loads(Path(a.input).read_text())); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n"); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
