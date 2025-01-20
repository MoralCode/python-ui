
def interactive_user_boolean_choice(prompt, default=True, add_directions=True, require_explicit_answer=False):

    # TODO: possiby refactor the user interaction into a library that
    # abstracts things and allows the choice to be made via CSV file,
    # interactive CLI, or web interface

    positive_answer = "Y" if default is not None and default is True else "y"
    negative_answer = "N" if default is not None and default is False else "n"

    prompt_ending = f" ({positive_answer}/{negative_answer}): "

    if add_directions:
        prompt += prompt_ending

    answer = None
    while answer is None:
        response = input(prompt)

        response = response.lower()
        if response == "":
            answer = default
        elif response == "y":
            answer = True
        elif response == "n":
            answer = False
        
        if require_explicit_answer and answer is None:
            print("A response is required.")

        if answer is not None:
            return answer