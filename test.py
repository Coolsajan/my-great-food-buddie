import gradio as gr
from app.recommender import retrive_generate, check_dB_data
import time

# Core logic function

def respond(user_message, state):
    # Unpack state
    place, location, question, retriever, step = state

    # First message initialization
    if step == 0:
        messages = [("assistant", "👋 Hello! I'm your Food Buddy AI assistant. I can help you find information about restaurants or food places. What restaurant would you like to know about?")]
        state = ("", "", "", None, 1)
        return messages, state

    # Handle user input
    messages = []
    if step == 1:
        place = user_message
        response = f"Great! '{place}' sounds delicious. Where is it located?"
        step = 2
        state = (place, location, question, retriever, step)
        return [("user", user_message), ("assistant", response)], state

    elif step == 2:
        location = user_message
        step = 3
        foodPlace = f"{place}_{location}"
        # Simulate DB check
        retriever = check_dB_data(foodPlace=foodPlace)
        response = f"I've found information about {place} in {location}. What would you like to know about it?"
        state = (place, location, question, retriever, step)
        return [("user", user_message), ("assistant", response)], state

    else:
        question = user_message
        step = 4
        # Generate answer
        _, answer = retrive_generate(retriever=retriever, question=question)
        state = (place, location, question, retriever, step)
        return [("user", user_message), ("assistant", answer)], state

# Initialize Gradio app
with gr.Blocks() as demo:
    state = gr.State(("", "", "", None, 0))  # place, location, question, retriever, step
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message here...", show_label=False)
    send = gr.Button("Send")

    def user_interact(user_message, state):
        messages, new_state = respond(user_message, state)
        return messages, new_state

    send.click(user_interact, inputs=[msg, state], outputs=[chatbot, state])
    msg.submit(user_interact, inputs=[msg, state], outputs=[chatbot, state])

if __name__ == "__main__":
    demo.launch()
