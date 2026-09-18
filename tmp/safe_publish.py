"""
safe_publish.py — riutilizzabile, STABILE
Pubblica un post su crazyweb con controlli automatici anti-errore:
1. Verifica che la categoria esista in _data/categorie.json — se manca, la aggiunge da sola
2. Verifica che _config.yml non sia corrotto (chiavi YAML vuote seguite da valore sulla riga dopo)
3. Scrive/aggiorna il post
4. git pull --rebase, add, commit, push
5. Aspetta il deploy su gh-pages e verifica che l'HTML compilato abbia il layout vero (contiene <head>)
   NON solo che risponda 200 — un 200 con body nudo (senza head/navbar) è comunque un fallimento.

USO:
    from safe_publish import safe_publish
    safe_publish(
        filename="2026-09-14-guida-di-prova.md",
        title="I nostri servizi",
        category="servizi",
        body="## Titolo\\n\\ntesto...",
        description="...",
    )
"""
import json
import re
import subprocess
import time
from pathlib import Path

PROJECT_PATH = Path(r"C:\Users\mirco\Desktop\crazyweb")
POSTS_DIR = PROJECT_PATH / "_posts"
CATEGORIE_JSON = PROJECT_PATH / "_data" / "categorie.json"
SITE_BASE = "https://cialdecompatibili-netizen.github.io/crazyweb"


def run(cmd, cwd=PROJECT_PATH):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    print(f"$ {cmd}\n{r.stdout}{r.stderr}")
    return r


def ensure_category(category, descrizione=None):
    """Aggiunge la categoria a _data/categorie.json se non esiste già."""
    data = json.loads(CATEGORIE_JSON.read_text(encoding="utf-8"))
    if any(c["nome"] == category for c in data):
        print(f"Categoria '{category}' già presente.")
        return
    data.append({"nome": category, "descrizione": descrizione or category.capitalize()})
    CATEGORIE_JSON.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"Categoria '{category}' aggiunta.")


def check_config_yaml_sanity():
    """Rileva il bug noto: chiave YAML vuota (es. 'last_name:') seguita da un
    valore YAML sulla riga successiva senza indentazione — segno di corruzione."""
    config = (PROJECT_PATH / "_config.yml").read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(config[:-1]):
        if re.match(r"^\w+:\s*$", line):  # chiave vuota tipo "last_name:"
            nxt = config[i + 1]
            if re.match(r"^\s{0,1}\w+:\s*\[", nxt) and not nxt.startswith("  "):
                raise RuntimeError(
                    f"_config.yml sembra corrotto vicino alla riga {i+1}: '{line}' seguita da '{nxt}'. "
                    "STOP — fixare manualmente prima di pubblicare."
                )
    print("_config.yml: nessuna corruzione nota rilevata.")


def write_post(filename, title, category, body, description=""):
    path = POSTS_DIR / filename
    date_str = filename[:10] + " 12:00:00"
    frontmatter = (
        "---\n"
        "layout: post\n"
        f"title: {title}\n"
        f"date: {date_str}\n"
        f"description: {description or title}\n"
        f"categories: {category}\n"
        "---\n\n"
    )
    path.write_text(frontmatter + body, encoding="utf-8")
    print(f"Post scritto: {path}")


def git_publish(message):
    run("git pull --rebase origin main")
    run("git add -A")
    run(f'git commit -m "{message}"')
    run("git pull --rebase origin main")  # ricontrolla nel caso siano arrivati commit nel frattempo
    r = run("git push origin main")
    if r.returncode != 0:
        raise RuntimeError("Push fallito — controllare l'output sopra.")


def verify_deploy(post_url_path, max_wait_s=180, interval_s=15):
    """Aspetta il deploy su gh-pages e verifica che l'HTML compilato abbia
    davvero il layout (contenga <head>), non solo che il branch sia aggiornato."""
    waited = 0
    while waited < max_wait_s:
        r = run(f"git ls-tree -r origin/gh-pages --name-only")
        run("git fetch origin gh-pages")
        r = run(f'git show origin/gh-pages:{post_url_path} 2>$null | Select-String "<head" -Quiet')
        if "True" in r.stdout:
            print(f"✅ Deploy OK: {post_url_path} ha il layout completo (<head> presente).")
            return True
        print(f"Non ancora pronto, attendo {interval_s}s... ({waited}/{max_wait_s}s)")
        time.sleep(interval_s)
        waited += interval_s
    print(f"⚠️ Timeout: {post_url_path} non ha ancora il layout dopo {max_wait_s}s. Verificare manualmente.")
    return False


def safe_publish(filename, title, category, body, description="", commit_msg=None):
    """Pipeline completa, con tutti i controlli. Da usare SEMPRE per pubblicare
    un post su crazyweb — mai scrivere/pushare a mano."""
    ensure_category(category)
    check_config_yaml_sanity()
    write_post(filename, title, category, body, description)
    git_publish(commit_msg or f"Aggiorna post: {title}")

    # slug reale nel gh-pages: dipende dall'estensione del file sorgente.
    # .md -> include la data nel permalink; .html -> senza data (comportamento
    # osservato empiricamente su questo tema/config, vedi CLAUDE.md).
    slug = filename.rsplit(".", 1)[0]
    if filename.endswith(".md"):
        url_path = f"blog/{slug}/index.html"
    else:
        # rimuove il prefisso data (YYYY-MM-DD-) per i file .html
        bare_slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
        url_path = f"blog/{bare_slug}/index.html"

    verify_deploy(url_path)
    print(f"URL pubblico atteso: {SITE_BASE}/{url_path.replace('index.html','')}")
