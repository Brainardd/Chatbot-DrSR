import random
import json
import numpy as np
import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE, map_location=device)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "NexxusBot"

def get_response(msg):
    sentence = tokenize(msg)
    X = np.array(bag_of_words(sentence, all_words), dtype=np.float32)
    X = torch.tensor(X, dtype=torch.float32).unsqueeze(0).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.95:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    return "I'm sorry, but I don't have information about that. I'm an AI assistant focused on Nexxus Lab's services. Is there anything specific about our services, quoting process, project initiation, or SEO offerings that I can help you with?"


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)
