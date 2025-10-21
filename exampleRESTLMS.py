import requests
import json

# API endpoint
API_URL = "http://localhost:1234/v1/chat/completions"

FAQS="""
How do I connect to the IxNetwork Web UI — should I use HTTP or HTTPS? This addresses 
SSL issues and emphasizes how to enable HTTP usage or stick with secure HTTPS through API keys. 
How do I set up licensing in IxNetwork and check license features? Covers installing licenses on the chassis, 
adjusting license mode (Perpetual vs. Subscription), and troubleshooting missing feature errors.
Why can't I open the IxNetwork packet capture — Wireshark shows an error? Often caused by missing or 
incompatible integrated Wireshark versions, and explains how to resolve by installing the correct compatible version.
How do I install IxNetwork API libraries for automation — on Windows vs. Linux? Details downloading and 
installing appropriate API packages, version compatibility, and path locations on both platforms. 
What are the main use cases for IxNetwork VE (Virtual Edition)? Explores how organizations leverage IxNetwork VE, 
with discussion in community Q&A spaces. What needs improvement in IxNetwork VE? Community-driven feedback highlights 
limitations or suggestions for future development. What is IxNetwork used for and what are its key features? 
IxNetwork delivers performance testing under the most challenging conditions. Capable of generating multiple 
terabytes of data and analyzing up to 4 million traffic flows simultaneously, IxNetwork scales to handle t
he most powerful devices and the largest networks. With its enhanced real-time analysis and statistics, 
this powerful solution emulates everything from routing and switching, data center Ethernet and SDN to 
broadband access and industrial Ethernet for comprehensive testing. And graphical user interface (GUI) 
wizards make it easier for our customers to meet a wide range of performance requirements with minimal resources.

"""
    # System prompt (you can paste your IxNetwork FAQs here)
system_prompt = (
    "You are a helpful assistant. Here are IxNetwork FAQ’s" + FAQS +
    "DO NOT MAKE UP ANSWERS"
)

# Model to use
MODEL = "llama-3.2-1b-instruct"

# Initialize conversation
messages = [
    {"role": "system", "content": system_prompt}
]

print("🤖 IxNetwork Chatbot (type 'exit' or 'quit' to stop)")
print("--------------------------------------------------")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Append user message
    messages.append({"role": "user", "content": user_input})

    # Prepare request payload
    payload = {
        "model": MODEL,
        "messages": messages
    }

    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code != 200:
            print(f"⚠️ Error: {response.status_code} - {response.text}")
            continue

        result = response.json()

        # Extract assistant's reply
        assistant_message = result["choices"][0]["message"]["content"].strip()

        # Display assistant response
        print(f"Assistant: {assistant_message}\n")

        # Add assistant message to conversation history
        messages.append({"role": "assistant", "content": assistant_message})

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
