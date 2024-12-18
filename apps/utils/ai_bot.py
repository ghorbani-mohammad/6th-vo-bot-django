from django.conf import settings


def generate_horoscope(
    user_personality: str, prompts: dict, temperature: float, max_tokens: int
) -> dict:
    client = settings.AZURE_CLIENT

    # Construct the messages with clear instructions for each horoscope type
    messages = [
        {
            "role": "user",
            "content": "These are some Questions and Answers that the user has provided. \
                Please provide some horoscope based on this personality."
            + user_personality,
        },
        {
            "role": "system",
            "content": "Provide the following horoscopes and please separate them with '---'.",
        },
    ]
    for horoscope_type, prompt in prompts.items():
        messages.append(
            {
                "role": "system",
                "content": f"{horoscope_type.capitalize()} Horoscope: {prompt}",
            }
        )

    # Call Azure OpenAI's chat completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the deployment name of your Azure model
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Split the response content by type for each horoscope
    horoscopes = (
        response.choices[0].message.content.strip().replace("\n", "").split("---")
    )
    result = dict(zip(prompts.keys(), horoscopes))
    return result


def generate_todos(
    user_personality: str, prompts: dict, temperature: float, max_tokens: int
) -> dict:
    client = settings.AZURE_CLIENT

    # Construct the messages with clear instructions for each horoscope type
    messages = [
        {
            "role": "user",
            "content": "These are some Questions and Answers that the user has provided. \
                Please provide some todos based on this personality.\
                    Please don't put titles like **personal growth** or **success** in the todos."
            + user_personality,
        },
        {
            "role": "system",
            "content": "Provide the following todos and please separate them with '---'.",
        },
    ]
    for todo_type, prompt in prompts.items():
        messages.append(
            {
                "role": "system",
                "content": f"{todo_type.capitalize()} todo: {prompt}",
            }
        )

    # Call Azure OpenAI's chat completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use the deployment name of your Azure model
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Split the response content by type for each todos
    todos = response.choices[0].message.content.strip().replace("\n", "").split("---")
    todos = [todo.strip(" -") for todo in todos]
    result = dict(zip(prompts.keys(), todos))
    return result
