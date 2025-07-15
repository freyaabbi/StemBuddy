import pickle

# Path to your encodings file
encodings_path = "encodings.pickle"

# Names you want to remove (case-sensitive)
names_to_remove = {"Shreya"}  # <-- change to names you want to delete

# Load the encodings
with open(encodings_path, "rb") as file:
    data = pickle.load(file)

# Filter out unwanted names
filtered_encodings = {
    "encodings": [],
    "names": []
}

for encoding, name in zip(data["encodings"], data["names"]):
    if name not in names_to_remove:
        filtered_encodings["encodings"].append(encoding)
        filtered_encodings["names"].append(name)

# Save the filtered data back
with open(encodings_path, "wb") as file:
    pickle.dump(filtered_encodings, file)

print(f"Removed: {', '.join(names_to_remove)}")
print("Updated encodings.pickle successfully.")
