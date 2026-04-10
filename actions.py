from transformers import pipeline
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Text, Dict, List
import random

# this is for Loading  emotion detection model
classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

class ActionDetectEmotion(Action):

    def name(self) -> Text:
        return "action_detect_emotion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text")

        # Detect emotion
        result = classifier(user_message)[0]
        emotion = result["label"]
        score = result["score"]

        # Get previous emotion (memory back)
        previous_emotion = tracker.get_slot("user_emotion")

        #  RESPONSE VARIATIONS

        sad_responses = [
            "I'm really sorry you're feeling this way 💙",
            "That sounds really tough… I'm here for you",
            "I understand… want to talk about it?"
        ]

        joy_responses = [
            "That's amazing to hear! 😊",
            "I'm really happy for you!",
            "That’s great news! Keep it up!"
        ]

        anger_responses = [
            "I understand you're upset.",
            "That sounds frustrating.",
            "It's okay to feel angry sometimes."
        ]

        fear_responses = [
            "It sounds like you're feeling anxious.",
            "That must be stressful.",
            "I'm here with you, you're not alone 💙"
        ]

        # CONFIDENCE CHECK
        if score < 0.6:
            dispatcher.utter_message(
                text="I'm not completely sure how you're feeling, but I'm here to listen 💙"
            )
            return [SlotSet("user_emotion", emotion)]

        # EMOTION TRANSITION
        if previous_emotion == "sadness" and emotion == "joy":
            dispatcher.utter_message(
                text="I'm really glad to see you're feeling better now 💙"
            )

        #  MAIN RESPONSE LOGIC

        if emotion == "sadness":
            if previous_emotion == "sadness":
                dispatcher.utter_message(
                    text="I remember you've been feeling down 💙 I'm here with you."
                )

            dispatcher.utter_message(
                text=random.choice(sad_responses)
            )

            dispatcher.utter_message(
                text="Maybe try:\n- Taking a short walk 🚶\n- Listening to music 🎧\n- Talking to someone you trust ❤️"
            )

        elif emotion == "joy":
            dispatcher.utter_message(
                text=random.choice(joy_responses)
            )

            dispatcher.utter_message(
                text="What's making you feel this way?"
            )

        elif emotion == "anger":
            dispatcher.utter_message(
                text=random.choice(anger_responses)
            )

            dispatcher.utter_message(
                text="Try this:\n- Take a deep breath 🌬️\n- Step away for a moment\n- Talk it out calmly"
            )

        elif emotion == "fear":
            dispatcher.utter_message(
                text=random.choice(fear_responses)
            )

            dispatcher.utter_message(
                text="Try:\n- Deep breathing\n- Grounding yourself\n- Talking to someone you trust"
            )

        else:
            dispatcher.utter_message(
                text="Thank you for sharing 💙 I'm here to listen."
            )

        #FOLLOW-UP
        dispatcher.utter_message(
            text="Do you want to tell me more about what's going on?"
        )

        # Save emotion in memory
        return [SlotSet("user_emotion", emotion)]