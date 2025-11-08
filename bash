cd cratejuice

# Backup old frontend just in case
mv frontend frontend_old_$(date +%Y%m%d%H%M)

# Move demo into place
mv demo frontend

# Stage everything
git add .

# Clean commit message (keeps history clear)
git commit -m "☮️ CrateJuice: clean base commit — backend/health + frontend/demo merged"

# Push it live
git push origin main