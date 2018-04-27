from flask import json

def format_data(data):
    return json.dumps(data, indent=4)

def find_context_by_name(contexts, name):
    for context in contexts:
        if context["name"] == name:
            return context
    else:
        return None

def find_contexts_by_name(contexts, name):
    context_list = []
    for context in contexts:
        if context["name"] == name:
            context_list.append(context)
    return context_list