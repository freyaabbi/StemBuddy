import cv2
import os
import face_recognition
import pickle
from datetime import datetime

ENCODINGS_FILE = "encodings.pickle"
IMAGE_DIR = "registered_faces"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Load existing encodings
if os.path.exists(ENCODINGS_FILE):
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)
    known_encodings = data["encodings"]
    known_names = data["names"]
else:
    known_encodings = []
    known_names = []

# Capture image
def capture_image(filename="capture.jpg"):
    print("[INFO] Capturing image...")
    os.system(f"libcamera-still -t 1000 -o {filename} --width 640 --height 480 --nopreview")
    return filename

# Draw boxes and recognize/register
def process_image(image_path):
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    print(f"[INFO] Found {len(face_encodings)} face(s).")

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"

        if known_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            if any(matches):
                best_match_index = distances.argmin()
                name = known_names[best_match_index]

        if name == "Unknown":
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 255), 2)
            cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.imshow("New Face - Unknown", image)
            cv2.waitKey(1000)

            # Ask for name via terminal
            input_name = input("🧠 I see a new face! What's your name? ").strip()
            if input_name:
                known_encodings.append(face_encoding)
                known_names.append(input_name)

                # Save updated encodings
                with open(ENCODINGS_FILE, "wb") as f:
                    pickle.dump({"encodings": known_encodings, "names": known_names}, f)

                # Save image with name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(IMAGE_DIR, f"{input_name}_{timestamp}.jpg")
                cv2.imwrite(filename, image)
                name = input_name
                print(f"[INFO] Registered {name} successfully.")

        # Draw final bounding box with name
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(image, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return image

# Main
if __name__ == "__main__":
    img_path = capture_image()
    result = process_image(img_path)

    cv2.imshow("Face Recognition", result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
