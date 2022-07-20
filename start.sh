#!/usr/bin/env bash

echo "Servern werden gestartet"

tmux new-session -d -s services -n as ./as.py
tmux new-window -t services -n vst ./vst.py
tmux new-window -t services -n fdz ./fdz.py
tmux new-window -t services -n bash /bin/bash

#tmux new-session as -d -s services 'uvicorn as:app --port 20001'
#tmux new-window vst -s services 'uvicorn vst:app --port 20002'

cat <<'EOF'

Je nach Umgebung (Rechner) muss man den drei HTTP-Servern zwei bis fünf
Sekunden zum Start-Up Zeit lassen, bis man mit 
    ./epa-fdv.py
die Anfrage starten.

mit 

    tmux at -t services

kann man sich zur Session verbinden.

EOF

sleep 10

echo "Anfrage wird gestartet"
./epa-fdv.py