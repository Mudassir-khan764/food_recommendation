# AI Food Therapist Module

This module provides psychological support for users making healthy food choices, managing cravings, emotional eating, and staying motivated.

## Features

- **NLP Analysis**: Uses NLTK and TextBlob to analyze user input for emotions, intent, and food cravings
- **Intent Detection**: Identifies if eating is driven by hunger, boredom, stress, or emotions
- **Healthy Alternatives**: Maintains a database of nutritious food alternatives
- **Empathetic Responses**: Generates supportive, guilt-free motivational messages
- **Mindful Eating Tips**: Provides practical advice for better eating habits
- **Pattern Tracking**: Monitors user interactions to detect patterns and adjust suggestions

## Installation

```bash
pip install nltk textblob
```

The module will automatically download required NLTK data on first import.

## Usage

```python
from food_therapist import FoodTherapist

# Initialize the therapist
therapist = FoodTherapist()

# Process user input
user_message = "I really want to eat pizza, but I know it's unhealthy"
response = therapist.chat(user_message)
print(response)

# Get interaction patterns
patterns = therapist.get_patterns()
print(patterns)

# Get personalized suggestions based on history
suggestions = therapist.get_personalized_suggestions()
print(suggestions)
```

## Integration

This module can be easily integrated into larger food recommendation systems:

1. **Web Applications**: Use with Flask/Django for chat interfaces
2. **Mobile Apps**: Integrate via API endpoints
3. **Chatbots**: Combine with existing chatbot frameworks
4. **Meal Planning Systems**: Add psychological support to existing planners

## Example Interactions

- **User**: "I really want to eat pizza, but I know it's unhealthy"
- **AI**: "I hear that you're struggling with this choice. It's completely okay to have cravings - you're human! For your craving for pizza, you could try homemade veggie pizza with whole wheat crust. Balance is key - you don't have to be perfect! Celebrate your awareness and commitment to health. Mindful eating tip: Stop eating when you're 80% full to avoid overeating."

## Customization

- **Food Alternatives**: Modify the `food_alternatives` dictionary to add more options
- **Intent Keywords**: Update `intent_keywords` for better detection
- **Response Messages**: Customize `encouragements` and `mindful_tips` lists
- **NLP Models**: Extend analysis with additional sentiment or intent classification models

## Dependencies

- nltk
- textblob

## License

This module is part of the AI Meal Planner system.