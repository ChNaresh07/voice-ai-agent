conversation_memory = {}

def save_context(user_id, data):
    conversation_memory[user_id] = data

def get_context(user_id):
    return conversation_memory.get(user_id)