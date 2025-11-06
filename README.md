## Lazy Head Scroller: Head-Motion Scrolling

An innovative Python script for the truly **lazy**\! This allows you to scroll up and down in any document or webpage by simply nodding your head forward or backward, eliminating the need to use your hands for scrolling.

It uses computer vision to detect changes in your **face orientation** and translates those movements into mouse scroll events.

-----

### Features

  * **Hands-Free Scrolling:** Scroll through long papers or articles with a simple head roll.
  * **Real-time Head Tracking:** Uses `cvzone` (built on MediaPipe) and `OpenCV` for accurate face and orientation detection.
  * **Automatic Calibration:** Calibrates your resting head position upon startup for personalized sensitivity.
  * **Cross-Platform Mouse Control:** Integrates `pynput` for sending universal scroll commands.

-----

### Prerequisites

You need a working webcam and Python installed on your system.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Kr0issant/lazy-head-scroller.git
    cd lazy-head-scroller
    ```

2. **Create and activate a python virtual environment:**
    For Windows:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
    For Linux/MacOS:
    ```bash
    python -m venv .venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install cvzone opencv-python numpy pynput mediapipe
    ```
    OR
    ```bash
    uv sync
    ```

### Usage

1.  **Run the script:**

    ```bash
    python main.py
    ```
    OR
    ```bash
    uv run main.py
    ```

2.  **Calibration:**

      * The application will start a **120-frame calibration period**.
      * During this time, **keep your head steady and centered** facing the screen.

3.  **Scroll with your head:**

      * **Roll your head forward** (like looking down at your chest) to **scroll down**.
      * **Roll your head backward** (like looking up at the ceiling) to **scroll up**.

4.  **Stop the script:**

      * Close the console window or press `Ctrl + C` in the terminal.

-----

### Note

  * **Performance:** Performance depends on your webcam quality and CPU speed.
  * **Lighting:** Ensure you are in a well-lit environment for the best face detection results.
  * **Sensitivity:** The current scroll threshold is set in the code (`-10` and `10` degrees difference from the calibrated roll). You may need to **adjust the thresholds** in the `main()` function if your head movements aren't registering correctly or are too sensitive.