# CrateJuice — Easy Drop Pack (Hybrid)
- PWA gift splash + player (v3/frontend/public)
- CLI player (tools/cjplay.py)
- Gift packer (tools/cjpack.py) with themes: 4boss, 4mmi, 4cbo, dan, danfun, opal
- Default tagline: Cbo Mmi- JuiceLuv (auto unless --tagline passed)
- Taglines pool in content/data/taglines.json (last line is default)

## Quick start
./crate_run.sh
python3 tools/cjplay.py --surprise 12 --rate 1.00

## Freeze a gift (PWA + export zip)
python3 tools/cjpack.py --tag gift-dan-01 --to "Dan" --theme danfun --note "Weird, pastel, fun — just like you"
