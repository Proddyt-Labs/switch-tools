"""Copy crates/labs-updater into each Proddyt Switch app and call it from eframe::App::logic.

Usage: python vendor-labs-updater.py <switch dir> [repo ...]   (idempotent)
"""
import os
import re
import shutil
import subprocess
import sys

NAMES = {
    "photo-labs": "Photo Labs", "vector-labs": "Vector Labs", "light-labs": "Light Labs", "film-labs": "Film Labs",
    "effect-labs": "Effect Labs", "design-labs": "Design Labs", "sound-labs": "Sound Labs", "word-labs": "Word Labs",
    "grid-labs": "Grid Labs", "deck-labs": "Deck Labs", "cad-labs": "CAD Labs",
}
LOGIC = re.compile(r"(\n(\s*)fn logic\(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame\) \{\n)")

root = sys.argv[1]
src = os.path.join(root, "_switch", "crates", "labs-updater")
for repo in sys.argv[2:] or NAMES:
    base = os.path.join(root, repo)
    dst = os.path.join(base, "crates", "labs-updater")
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    impl = None
    for top in ("crates", "apps"):
        for d, _, files in os.walk(os.path.join(base, top)):
            if "target" in d or "labs-updater" in d:
                continue
            for f in files:
                p = os.path.join(d, f)
                if f.endswith(".rs") and "impl eframe::App for" in open(p, encoding="utf8").read():
                    impl = impl or p
    s = open(impl, encoding="utf8").read()
    call = f'labs_updater::frame(ctx, "{repo}", "{NAMES[repo]}");'
    if call not in s:
        m = LOGIC.search(s)
        assert m, impl
        s = s[: m.end()] + f"{m.group(2)}    // Proddyt Switch: asks to update from the fork's releases (LABS-156).\n{m.group(2)}    {call}\n" + s[m.end():]
        open(impl, "w", encoding="utf8", newline="\n").write(s)
    crate_dir = impl
    while not os.path.exists(os.path.join(crate_dir, "Cargo.toml")):
        crate_dir = os.path.dirname(crate_dir)
    cargo = os.path.join(crate_dir, "Cargo.toml")
    c = open(cargo, encoding="utf8").read()
    if "labs-updater" not in c:
        rel = os.path.relpath(dst, crate_dir).replace("\\", "/")
        c = re.sub(r"(\[dependencies\]\n)", rf'\1labs-updater = {{ version = "0.1.0", path = "{rel}" }}\n', c, count=1)
        open(cargo, "w", encoding="utf8", newline="\n").write(c)
    subprocess.run(["cargo", "update", "--workspace", "-q"], cwd=base, check=True)
    subprocess.run(["cargo", "fmt", "--all"], cwd=base, check=True)
    print(repo, os.path.relpath(impl, base), os.path.relpath(cargo, base))
