/
├── apps/                    # ripper + future engines
├── content/                 # crate data + seeds
├── cratejuice/              # main shared code
├── v3/                      # frontend bundle (public UI)
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── health/              # frontend health path
│   └── assets/              # images, icons, cards
├── backend/                 # FastAPI backend
│   ├── main.py
│   ├── requirements.txt
│   ├── verify.sh
│   ├── health/
│   └── render_deploy.sh
├── bash/                    # scripts
├── deploy.sh                # primary deploy script
├── netlify.toml             # frontend routing + health
├── render.yaml              # backend config
├── Dockerfile               # backend container
├── Dockerfile.frontend
└── README.md                # this file
