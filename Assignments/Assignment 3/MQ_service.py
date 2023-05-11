from fastapi import FastAPI, HTTPException
import os
import yaml
import logging
import requests
from schemas import Message, Queue

app = FastAPI()

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

max_queue_size = config["max_queue_size"]
creation_permission = config["creation_role"]
manipulation_permission = config["manipulation_role"]
port = config["port"]
config_ = config["logging"]

queues:list[Queue] = []


def save_queues() -> None:
    """
    Saves the queues in a persistent storage
    """
    pass

def get_queue(queue_id:str) -> Queue:
    """
    Returns the queue with the specified id.

    Args:
        queue_id (str): queue id

    Returns:
        Queue: queue with the specified id
    """
    for queue in queues:
        if queue.queue_id == queue_id:
            return queue
    return None

def get_user_role(token: str) -> list[str]:
    """
    Sends a request to the authentication service to get the user's role.

    Args:
        token (str): user's token

    Returns:
        list[str]: username and role
    """
    response = requests.get(
        url="http://localhost:8000/auth/role/?token=" + token
    ).content
    response = eval(response.decode("utf-8"))
    role = response[1]
    username = response[0]
    return username, role


def create_log_file():
    # Check if the log file exists
    if not os.path.exists("log.txt"):
        # If it doesn't exist, create a new file
        with open("log.txt", "w") as f:
            f.write("")  # it just doesn't work without this line
            # Configure the logging module
            write_log("Log file created", 200)


def write_log(message:str, code:int) -> None:
    """
    Writes a message to the log file.

    Args:
        message (str): message to write
        code (int): code of the message
    """
    
    code = str(code)
    # Configure the logging module
    logging.basicConfig(
                filename=config_["file_path"],
                format=config_["format"],
                level=config_["level"]
            )
    if code[0] == "2" or code[0] == "1":
        logging.info(f'{code} - {message}')
    elif code[0] == "3":
        logging.warning(f'{code} - {message}')
    elif code[0] == "4":
        logging.error(f'{code} - {message}')
    elif code[0] == "5":
        logging.critical(f'{code} - {message}')
        
def check_exist(queue_id: str) -> bool:
    """
    Checks if the queue exists.

    Args:
        queue_id (str): queue's id

    Returns:
        bool: True if the queue exists, False otherwise
    """
    pass
        

@app.post("/queue/create")
def create_queue(token: str, queue_id: str):
    user, role = get_user_role(token)
    if role != creation_permission:
        write_log(f"User {user} tried to create a queue", 403)
        raise HTTPException(status_code=403, detail="You don't have permission to create a queue")
    # Check if the queue already exists
    if check_exist(queue_id):
        write_log(f"User {user} tried to create a queue that already exists", 409)
        raise HTTPException(status_code=409, detail="The queue already exists")
    # Create the queue
    queue = Queue(max_queue_size, queue_id)
    queues.append(queue)
    # save the queue
    write_log(f"User {user} created a queue {queue_id}", 201)

@app.delete("/queue/{queue_id}/delete")
def delete_queue(token: str, queue_id: str):
    user, role = get_user_role(token)
    if role != creation_permission:
        write_log(f"User {user} tried to delete a queue", 403)
        raise HTTPException(status_code=403, detail="You don't have permission to delete a queue")
    # Check if the queue exists
    if not check_exist(queue_id):
        write_log(f"User {user} tried to delete a queue that doesn't exist", 404)
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    # Delete the queue
    # save the changes
    pass

@app.post("/queue/{queue_id}/push")
def push(token: str, queue_id: str, message: Message):
    username, role = get_user_role(token)
    if role != manipulation_permission:
        write_log(f"User {username} tried to push a message", 403)
        raise HTTPException(status_code=403, detail="You don't have permission to push a message")
    # Check if the queue exists
    if not check_exist(queue_id):
        write_log(f"User {username} tried to push a message to a queue that doesn't exist", 404)
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    # Check if the queue is full
    queue = get_queue(queue_id)
    if queue.size() == queue.max_size:
        write_log(f"User {username} tried to push a message to a full queue", 403)
        raise HTTPException(status_code=403, detail="The queue is full")
    # Push the message
    # save the changes
    # return the message id
    # write_log(f"User {username} pushed a message to the queue {queue_id}", 201)
    

        
    

@app.post("/queue/{queue_id}/pull")
def pull(token: str, queue_id: str):
    username, role = get_user_role(token)
    if role != manipulation_permission:
        write_log(f"User {username} tried to pull a message", 403)
        raise HTTPException(status_code=403, detail="You don't have permission to pull a message")
    # Check if the queue exists
    if not check_exist(queue_id):
        write_log(f"User {username} tried to pull a message from a queue that doesn't exist", 404)
        raise HTTPException(status_code=404, detail="The queue doesn't exist")
    # Check if the queue is empty
    queue = get_queue(queue_id)
    if queue.size() == 0:
        write_log(f"User {username} tried to pull a message from an empty queue", 403)
        raise HTTPException(status_code=403, detail="The queue is empty")
    # Pull the message
    message = queue.dequeue()
    # save the changes
    # return the message
    write_log(f"User {username} pulled a message from the queue {queue_id}", 200)
    return message



if __name__ == "__main__":
    import uvicorn
    create_log_file()
    uvicorn.run(app, host="127.0.0.1", port=port)
        