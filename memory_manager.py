conversation_memory = []

MAX_MEMORY = 5

def add_message(role, content):
    conversation_memory.append({
        "role": role,
        "content": content
    })

    if len(conversation_memory) > MAX_MEMORY:
        conversation_memory.pop(0)


def get_memory():
    return conversation_memory