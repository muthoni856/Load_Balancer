from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashing
import logging

app = Flask(__name__)

# Initialize Consistent Hashing
hashing = ConsistentHashing()

# Predefined server replicas
server_replicas = ["server1", "server2", "server3"]
# Add the predefined server replicas to the consistent hashing ring
for server in server_replicas:
    hashing.add_node(server)


@app.route("/")
def home():
    """
    Root endpoint that returns a simple homepage message.
    """
    return "Homepage"


@app.route("/home")
def getname():
    """
    Endpoint to get a greeting message from a specific server.
    """
    # Get the node responsible for the hashed value of 'home'
    node_id = hashing.get_node(hash("home"))
    response_data = {"message": f"Hello from server: {node_id}", "status": "successful"}
    return jsonify(response_data), 200


@app.route("/heartbeat")
def heartbeat():
    """
    Endpoint to check if the server is alive.
    """
    return "", 200


def get_replicas():
    """
    Endpoint to get the list of current server replicas.
    """
    response_data = {
        "message": {
            "N": len(server_replicas),  # Number of replicas
            "replicas": server_replicas,  # List of replicas
        },
        "status": "successful",
    }
    return jsonify(response_data), 200


@app.route("/add", methods=["POST"])
def add_replica():
    """
    Endpoint to add new server replicas.
    """
    data = request.get_json()  # Get the JSON data from the request
    n = data.get("n")  # Number of replicas to add
    hostnames = data.get("hostnames")  # List of hostnames to add

    # Validate the input
    if len(hostnames) > n:
        return (
            jsonify(
                {
                    "message": "Error, number of hostnames is greater than newly added instances",
                    "status": "failure",
                }
            ),
            400,
        )
    else:
        # Add the new hostnames to the replicas and consistent hashing ring
        for hostname in hostnames:
            server_replicas.append(hostname)
            hashing.add_node(hostname)

        response_data = {
            "message": {
                "N": len(server_replicas),  # Updated number of replicas
                "replicas": server_replicas,  # Updated list of replicas
            },
            "status": "successful",
        }
        return jsonify(response_data), 200
