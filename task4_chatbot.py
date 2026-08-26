"""
TASK 4: Mini Project - Production-Ready Multi-Intent Rule-Based Chatbot
---------------------------------------------------------------------------
Objective : A terminal-based conversational bot that:
    - Normalizes user text (lowercasing, stripping punctuation/whitespace)
    - Uses nested if-elif-else logic combined with a dictionary-based
      intent map to route user messages
    - Handles multiple "help trees" (topics): greetings, support, orders,
      account help, and small talk
    - Maintains simple session state (e.g. user's name, last topic)
    - Gracefully falls back on unrecognized input
"""

import re
import sys


class ChatSession:
    """Holds simple conversational state for the current session."""

    def __init__(self):
        self.user_name = None
        self.last_topic = None
        self.order_id = None
        self.turns = 0


def normalize_text(text: str) -> str:
    """Lowercase, strip punctuation and extra whitespace from user input."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)   # remove punctuation
    text = re.sub(r"\s+", " ", text)      # collapse whitespace
    return text


# ------------------------------------------------------------------
# Intent detection: keyword -> intent name
# ------------------------------------------------------------------
INTENT_KEYWORDS = {
    "greeting": ["hi", "hello", "hey", "salam", "assalamualaikum"],
    "farewell": ["bye", "goodbye", "exit", "quit", "see you"],
    "set_name": ["my name is", "i am", "im", "call me"],
    "order_status": ["order", "tracking", "shipment", "delivery"],
    "account_help": ["password", "account", "login", "reset"],
    "support": ["help", "support", "problem", "issue", "complaint"],
    "thanks": ["thanks", "thank you", "shukriya"],
    "smalltalk": ["how are you", "whats up", "what is up"],
}


def detect_intent(normalized_text: str) -> str:
    """
    Route the normalized text to an intent using nested if-elif-else logic
    layered on top of the keyword dictionary map above.
    """
    if not normalized_text:
        return "empty"

    # Priority ordering matters -> check specific intents before generic ones
    if any(kw in normalized_text for kw in INTENT_KEYWORDS["farewell"]):
        return "farewell"
    elif any(kw in normalized_text for kw in INTENT_KEYWORDS["set_name"]):
        return "set_name"
    elif any(kw in normalized_text for kw in INTENT_KEYWORDS["order_status"]):
        return "order_status"
    elif any(kw in normalized_text for kw in INTENT_KEYWORDS["account_help"]):
        return "account_help"
    elif any(kw in normalized_text for kw in INTENT_KEYWORDS["support"]):
        return "support"
    elif any(kw in normalized_text for kw in INTENT_KEYWORDS["thanks"]):
        return "thanks"
    elif any(kw in normalized_text for kw in INTENT_KEYWORDS["smalltalk"]):
        return "smalltalk"
    elif any(kw in normalized_text for kw in INTENT_KEYWORDS["greeting"]):
        return "greeting"
    else:
        return "fallback"


# ------------------------------------------------------------------
# Intent handlers (each returns a bot reply string)
# ------------------------------------------------------------------
def handle_greeting(session: ChatSession, text: str) -> str:
    session.last_topic = "greeting"
    if session.user_name:
        return f"Hello again, {session.user_name}! How can I help you today?"
    return "Hi there! I'm your assistant bot. What's your name?"


def handle_farewell(session: ChatSession, text: str) -> str:
    name = f", {session.user_name}" if session.user_name else ""
    return f"Goodbye{name}! Have a great day."


def handle_set_name(session: ChatSession, text: str) -> str:
    # crude name extraction after known trigger phrases
    for trigger in INTENT_KEYWORDS["set_name"]:
        if trigger in text:
            name_part = text.split(trigger, 1)[1].strip()
            if name_part:
                session.user_name = name_part.split()[0].capitalize()
                break
    session.last_topic = "set_name"
    if session.user_name:
        return f"Nice to meet you, {session.user_name}! How can I help — orders, account, or general support?"
    return "I couldn't quite catch your name — could you repeat it?"


def handle_order_status(session: ChatSession, text: str) -> str:
    session.last_topic = "order_status"
    match = re.search(r"\b\d{4,}\b", text)
    if match:
        session.order_id = match.group()
        return f"Checking status for order #{session.order_id}... it's currently in transit and expected soon."
    return "Sure, I can check that. Could you share your order ID (numbers only)?"


def handle_account_help(session: ChatSession, text: str) -> str:
    session.last_topic = "account_help"
    if "reset" in text or "password" in text:
        return "To reset your password, go to Settings > Security > Reset Password, and check your email for the link."
    return "I can help with account/login issues. Are you trying to log in or reset your password?"


def handle_support(session: ChatSession, text: str) -> str:
    session.last_topic = "support"
    return "I'm sorry you're facing an issue. Could you describe the problem in a bit more detail?"


def handle_thanks(session: ChatSession, text: str) -> str:
    return "You're welcome! Let me know if there's anything else I can help with."


def handle_smalltalk(session: ChatSession, text: str) -> str:
    return "I'm just a bunch of if-elif statements, but I'm doing great! How can I assist you?"


def handle_empty(session: ChatSession, text: str) -> str:
    return "I didn't catch that — could you type something?"


def handle_fallback(session: ChatSession, text: str) -> str:
    if session.last_topic:
        return (f"Hmm, I'm not sure I understood that. "
                f"We were just talking about {session.last_topic.replace('_', ' ')} — "
                f"want to continue with that, or ask something else?")
    return "I'm not sure I understood. You can ask me about orders, account help, or general support."


# Dictionary-based functional map: intent name -> handler function
INTENT_HANDLERS = {
    "greeting": handle_greeting,
    "farewell": handle_farewell,
    "set_name": handle_set_name,
    "order_status": handle_order_status,
    "account_help": handle_account_help,
    "support": handle_support,
    "thanks": handle_thanks,
    "smalltalk": handle_smalltalk,
    "empty": handle_empty,
    "fallback": handle_fallback,
}


def process_message(session: ChatSession, raw_text: str) -> str:
    """Full pipeline: normalize -> detect intent -> route -> respond."""
    session.turns += 1
    normalized = normalize_text(raw_text)
    intent = detect_intent(normalized)
    handler = INTENT_HANDLERS.get(intent, handle_fallback)
    return handler(session, normalized)


def run_chat_loop():
    """Main terminal conversational loop."""
    session = ChatSession()
    print("Bot: Hi! Type 'bye' anytime to exit.")

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Session ended. Goodbye!")
            break

        reply = process_message(session, user_input)
        print(f"Bot: {reply}")

        if detect_intent(normalize_text(user_input)) == "farewell":
            break


if __name__ == "__main__":
    run_chat_loop()
