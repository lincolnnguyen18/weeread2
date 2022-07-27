# LINCOLNNGUYEN18.COM
# DEMO3

if screen -list | grep -q "d1|e1"; then
    echo "d1 already started"
    exit 1
else
    echo "starting d1"
fi

. /mnt/sda1/deployment/ports.sh
# Start uvicorn
screen -dmS 'e1'
screen -S 'e1' -X stuff "cd python && uvicorn --reload --port 8000 app:app\n"

echo "Checking if uvicorn started..."
lsof -i:$e1

# Start node server
screen -dmS 'd1'
screen -S 'd1' -X stuff "cd server && npm run pub\n"

echo "Checking if node started..."
lsof -i:$d1

# Build react client
# (cd client && npm run build)