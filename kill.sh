# LINCOLNNGUYEN18.COM
# DEMO3

if ! screen -list | grep -q d1; then
    echo "d1 already killed"
    exit 1
else
    echo "killing d1"
fi

# Screen names
# react='l18-demo3-react'
# uvicorn='l18-demo3-uvicorn'
uvicorn='e1'
# node_dev='l18-demo3-node-dev'
# node_pub='l18-demo3-node-pub'
node_pub='d1'

# Ports
node_port=7001
# react_port=8006
# uvicorn_port=8007
uvicorn_port=8000

# Kill node server
sudo kill $(sudo lsof -t -i:$node_port) &>/dev/null
screen -S $node_pub -X quit
# screen -S $node_dev -X quit

# # Kill react client
# sudo kill $(sudo lsof -t -i:$react_port) &>/dev/null
# screen -S $react -X quit

# Kill uvicorn
sudo kill $(sudo lsof -t -i:$uvicorn_port) &>/dev/null
screen -S $uvicorn -X quit

# Confirm killed
echo "Checking if uvicorn is still alive..."
sudo lsof -i :$uvicorn_port
echo "Checking if node is still alive..."
sudo lsof -i :$node_port
# echo "Checking if react is still alive..."
# sudo lsof -i :$react_port