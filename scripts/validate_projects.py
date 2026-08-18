from pathlib import Path
import subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
PATTERN='[0-9][0-9][0-9][0-9]-*'
HEADINGS=("Ferramentas","Passo a passo","Conceitos","Pré-requisitos","O que foi validado","Solução de problemas","Checklist","Tecnologias relacionadas","Referências oficiais")

def validate():
    errors=[]; projects=sorted(ROOT.glob(PATTERN)); setup=ROOT/"000-configuracao-ambiente"
    if setup.exists() and setup not in projects: projects.insert(0,setup)
    if not projects: errors.append("Nenhum projeto numerado encontrado")
    for project in projects:
        readme=project/"README.md"
        if not readme.exists(): errors.append(f"{project.name}: README ausente"); continue
        text=readme.read_text(encoding="utf-8")
        for heading in HEADINGS:
            if heading.lower() not in text.lower(): errors.append(f"{project.name}: seção ausente: {heading}")
        if "/Users/alexmarques" in text: errors.append(f"{project.name}: caminho local absoluto")
        if not list((project/"docs").glob("*.svg")): errors.append(f"{project.name}: diagrama SVG ausente")
        if (project/"tests").is_dir():
            run=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=project,text=True,capture_output=True)
            if run.returncode: errors.append(f"{project.name}: testes falharam\n{run.stdout}{run.stderr}")
    return projects,errors

if __name__=="__main__":
    projects,errors=validate()
    if errors: print("\n".join(errors)); raise SystemExit(1)
    print(f"{len(projects)} projetos validados em linkedin-data-engineering-articles.")
