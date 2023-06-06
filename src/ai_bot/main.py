with open('context.txt', 'r') as f:
    context = f.read()
    print(context)


import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

# Load the pre-trained model and tokenizer
model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

previous_answers = []

# context = "The Apollo program was a series of space missions"

# Answer a question based on the provided context and previous answers


def answer_question(context, previous_answers, question):
    # Concatenate the context, previous answers, and question
    context = context + " " + " ".join(previous_answers)

    # Tokenize the input text
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True,
                                   return_tensors="pt", truncation=True, padding="max_length", max_length=512)

    # Perform question answering
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the start and end positions of the answer
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    # Decode and return the answer
    answer = tokenizer.decode(
        inputs.input_ids[0][start_index:end_index+1], skip_special_tokens=True)
    return answer


# Chat with the question-answering model
while True:
    user_input = input("User: ")

    # Assume the user input is a question
    question = user_input

    # Answer the question based on the context and previous answers
    answer = answer_question(context, previous_answers, question)

    # Update the previous answers with the new answer
    previous_answers.append(answer)

    print("Bot:", answer)
