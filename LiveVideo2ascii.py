import cv2
import sys
import time
from colorama import Style, init

# Initialize colorama for colored terminal output
init()

# ASCII characters sorted by brightness (from dark to light)
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def pixel_to_ascii(pixel_value):
    """
    Maps a grayscale pixel value (0-255) to an ASCII character.
    """
    scale = len(ASCII_CHARS)  # Number of ASCII characters
    return ASCII_CHARS[int(pixel_value / 256 * scale)]

def rgb_to_ansi(r, g, b):
    """
    Converts an RGB color to an ANSI escape code for terminal output.
    """
    return f"\033[38;2;{r};{g};{b}m"  # 24-bit color (true color)

def frame_to_ascii_color(frame, width=100):
    """
    Converts a video frame to a colored ASCII representation.
    - frame: The input video frame (BGR format).
    - width: The desired width for the ASCII art in characters.
    """
    # Resize frame to match the terminal aspect ratio
    height, original_width, _ = frame.shape
    aspect_ratio = 0.55  # Adjust for terminal font height
    new_height = int(height / original_width * width * aspect_ratio)
    resized_frame = cv2.resize(frame, (width, new_height))

    # Build ASCII frame with colors
    ascii_frame = []
    for row in resized_frame:
        ascii_row = []
        for pixel in row:
            b, g, r = pixel  # OpenCV uses BGR
            ascii_char = pixel_to_ascii((r + g + b) // 3)  # Use brightness for ASCII
            ascii_row.append(f"{rgb_to_ansi(r, g, b)}{ascii_char}")
        ascii_frame.append("".join(ascii_row))
    
    return "\n".join(ascii_frame) + Style.RESET_ALL

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access the camera.")
        return

    # Get the dimensions of the terminal
    try:
        _, term_width = os.popen('stty size', 'r').read().split()
        term_width = int(term_width)
    except:
        term_width = 100  # Default width if terminal size is unavailable

    try:
        # Store the previous frame to reduce unnecessary screen clearing
        prev_output = None

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame.")
                break

            # Convert frame to colored ASCII
            ascii_art = frame_to_ascii_color(frame, width=term_width)

            # Check if the output differs; only update if needed
            if ascii_art != prev_output:
                sys.stdout.write("\033[H")  # Move cursor to the top-left corner
                sys.stdout.write(ascii_art)
                sys.stdout.flush()
                prev_output = ascii_art

            # Control frame rate (limit to ~15 FPS for smoothness)
            time.sleep(1 / 15)

            # Quit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the camera
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")

if __name__ == "__main__":
    main()



