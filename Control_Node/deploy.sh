#!/bin/bash

TMUX_SESSION="my_session"
SCRIPTS=("startplay.py" "terra.py" "tvars.py" "port.py")
SCRIPT_PATHS=("/scripts/startplay.py" "/scripts/terra.py" "/scripts/tvars.py" "/scripts/port.py")
TMUX_WINDOWS=("window1" "window2" "window3" "window4")

# Check if tmux session exists
tmux has-session -t $TMUX_SESSION 2>/dev/null
if [ $? != 0 ]; then
    tmux new-session -d -s $TMUX_SESSION
fi

for i in "${!SCRIPTS[@]}"; do
    SCRIPT_NAME=${SCRIPTS[$i]}
    NEW_SCRIPT_PATH=${SCRIPT_PATHS[$i]}
    TMUX_WINDOW=${TMUX_WINDOWS[$i]}

    # Kill the current running script
    tmux send-keys -t $TMUX_SESSION:$TMUX_WINDOW C-c
    sleep 2

    # Start the new script version
    tmux send-keys -t $TMUX_SESSION:$TMUX_WINDOW " sudo python3 $NEW_SCRIPT_PATH" C-m
done
