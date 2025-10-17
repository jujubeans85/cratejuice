# CrateJuice — Turbo Scaffold

Run `./crate_run.sh examples/mycrates.txt chill stabilize 0.5`.
cd cratejuice_turbo_repo
ls -1chmod +x crate_run.sh
mkdir -p examples
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > examples/mycrates.txt
./crate_run.sh examples/mycrates.txt chill stabilize 0.5
cat >> ~/.bashrc <<'EOF'
cjgo() { 
  cd /workspaces/cratejuice/cratejuice_turbo_repo 2>/dev/null || cd ~/workspaces/cratejuice/cratejuice_turbo_repo 2>/dev/null || pwd; ls -1
}
cjrun() {
  cjgo || return 1
  chmod +x crate_run.sh 2>/dev/null || true
  export CRATE_DIR=/workspaces/cratejuice/offgrid-crates
  mkdir -p "$CRATE_DIR" examples
  [ -s examples/mycrates.txt ] || echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" > examples/mycrates.txt
  echo "🎛  Running CJ chain → $CRATE_DIR"
  ./crate_run.sh examples/mycrates.txt chill stabilize 0.5
}
cjreset() {
  set -e
  cd /workspaces
  rm -rf cratejuice
  git clone https://github.com/jujubeans85/cratejuice.git
  echo "✅ Fresh clone at /workspaces/cratejuice"
}
EOF
source ~/.bashrc
