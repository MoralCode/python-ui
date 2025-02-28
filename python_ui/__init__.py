from pathlib import Path
from datetime import datetime
import csv
from helpers import save_to_csv
class Terminal:

    @staticmethod    
    def _prompt_until_response(prompt, default=True, require_explicit_answer=False):
        
        answer = None
        while answer is None:
            response = input(prompt)

            if len(response) >= 1:
                return response
            elif require_explicit_answer:
                print("A response is required.")
            else:
                return default


    @staticmethod    
    def boolean_choice(prompt, default=True, add_directions=True, require_explicit_answer=False):

        # TODO: possiby refactor the user interaction into a library that
        # abstracts things and allows the choice to be made via CSV file,
        # interactive CLI, or web interface

        positive_answer = "Y" if default is not None and default is True else "y"
        negative_answer = "N" if default is not None and default is False else "n"

        prompt_ending = f" ({positive_answer}/{negative_answer}): "

        if add_directions:
            prompt += prompt_ending

        answer = Terminal._prompt_until_response(prompt, default=default, require_explicit_answer=require_explicit_answer)
        answer = answer.lower()
        if answer is True or answer.startswith("y"):
            return True
        elif answer is False or answer.startswith("n"):
            return False



class CSV:

    @staticmethod
    def group_data(data, group_heading="Group", default_group=True, grouping_filename="grouped.csv", additional_headings=None, additional_defaults=None):
        grouped_csv_data = []
        for entry in data:
            grouped = {group_heading: default_group if default_group else ""}
            
            if additional_headings is not None and additional_defaults is not None:
                grouped.update({ k:v for (k,v) in zip(additional_headings, additional_defaults)})

            grouped.update(entry)
            grouped_csv_data.append(grouped)

        grouped_path = Path(grouping_filename)
        reuse_file = False
        if grouped_path.exists():
            reuse_file = True
            # prompt user to either reuse the existing file or overwrite it

            reuse_file = Terminal.boolean_choice(f"An existing '{grouped_path}' groupings file found. Would you like to reuse it?", default=True)

        if not reuse_file:
            # archive the file by adding the timestamp to the file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            archive_name = grouped_path.with_name(f"{grouped_path.stem}_{timestamp}{grouped_path.suffix}")
            grouped_path.rename(archive_name)

            save_to_csv(grouped_csv_data, grouped_path)
            input("Waiting for time entries to be grouped. "
            f"Edit {grouped_path} to group the entries and press enter when complete...")

        grouped_data = {}

        with grouped_path.open('r', encoding='utf-8') as grouped_csv:
            reader = csv.DictReader(grouped_csv)
            entries = list(reader)
            # if any entry has been given an ID
            if any(map(lambda e: e.get(group_heading, "") != "", entries)):
                for entry in entries:
                    group_id = entry.get(group_heading, "")
                    if group_id not in grouped_data:
                        grouped_data[group_id] = []
                    del entry[group_heading]
                    grouped_data[group_id].append(entry)
                
            else: #none were IDed
                grouped_data[""] = entries
        
        return grouped_data