"""
update_post.py — riutilizzabile
Aggiorna un post esistente in _posts/ (frontmatter + corpo) e pubblica
(git pull --rebase, add, commit, push) sul repo crazyweb.

USO:
    python update_post.py <nome_file_in_posts> "<titolo>" "<categoria>" "<corpo_markdown>"

Esempio:
    python update_post.py 2026-09-14-guida-di-prova.md "I nostri servizi" "servizi" "testo..."
"""
import sys
import subprocess
from pathlib import Path

PROJECT_PATH = Path(r"C:\Users\mirco\Desktop\crazyweb")
POSTS_DIR = PROJECT_PATH / "_posts"


def update_post(filename, title, category, body, description=""):
    path = POSTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Post non trovato: {path}")

    # Mantiene la data originale dal filename (YYYY-MM-DD-slug.md)
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
    print(f"Aggiornato: {path}")


def publish(message):
    def run(cmd):
        r = subprocess.run(cmd, cwd=PROJECT_PATH, capture_output=True, text=True, shell=True)
        print(r.stdout, r.stderr)
        return r

    run("git pull --rebase origin main")
    run("git add -A")
    run(f'git commit -m "{message}"')
    run("git push origin main")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python update_post.py <file> <titolo> <categoria> <corpo>")
        sys.exit(1)
    _, filename, title, category, body = sys.argv[:5]
    update_post(filename, title, category, body)
    publish(f"Aggiorna post: {title}")
