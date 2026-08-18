import json,platform,shutil,sys
from pathlib import Path
def inspect(): return {"python":platform.python_version(),"supported":sys.version_info>=(3,10),"tools":{x:shutil.which(x) for x in ("python3","code","git")}}
def main():
    r=inspect(); out=Path("data/output/environment.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(r,indent=2)+"\n"); print(json.dumps(r,indent=2)); raise SystemExit(0 if r["supported"] else 1)
if __name__=="__main__": main()
