import csv

def save_to_csv(time_entries, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = time_entries[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(time_entries)