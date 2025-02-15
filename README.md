# Real-Time-OCR-based Video Search
<br><br>
<b>Overview</b>
<br>
This project enables real-time text recognition from an IP camera stream and uses the extracted text to search and play the most relevant video on YouTube. It leverages computer vision, OCR, and web automation techniques to create a seamless pipeline from image capture to video retrieval.
<br><br>
<b>Features</b>
-Real-Time Image Capture – Captures frames from an IP camera.<br>
-Advanced Image Processing – Enhances image quality for improved OCR accuracy.<br>
-Text Extraction with OCR – Recognizes text from images using EasyOCR.<br>
-Automated Video Search – Uses the extracted text to search for relevant videos.<br>
-YouTube Video Playback – Automatically plays the top search result.
<br><br>
<b>Project Flow</b>
<br>
1. Capture Image from IP Camera<br>
The system establishes a connection with an IP camera using OpenCV and captures a single frame from the live video stream.
<br><br>
This is done by accessing the camera's streaming URL (RTSP or HTTP-based).<br>
The captured frame is stored as an image for further processing.<br><br>
2. Preprocess Image for OCR<br>
Raw images from the camera often contain noise, shadows, or low contrast, making text difficult to recognize.<br>
To improve OCR accuracy, multiple image enhancement techniques are applied:
<br><br>
-Grayscale Conversion: Removes color information, keeping only intensity values.<br>
-Gaussian Blur: Smoothens the image to reduce random noise.<br>
-CLAHE (Contrast Limited Adaptive Histogram Equalization): Increases text visibility by improving contrast.<br>
-Bilateral Filtering: Preserves edges while reducing noise.<br>
-Otsu’s Thresholding: Converts the image to black-and-white, isolating the text from the background.<br>
-Morphological Transformations: Cleans up unwanted artifacts using dilation and erosion techniques.<br>
-Resizing: Enlarges the image to improve OCR readability.<br>
At the end of this step, the image is clear, high-contrast, and noise-free, making it ideal for OCR.
<br><br>
3. Extract Text using OCR<br>
The enhanced image is now passed through EasyOCR, a deep learning-based Optical Character Recognition engine.<br>
<br><br>
EasyOCR scans the image and detects regions containing text.<br>
It extracts the text and returns a structured output containing the recognized words.<br>
The extracted text is stored as a string.
<br><br>
4. Search for a Video on YouTube<br>
Once the text is extracted, it is used as a search query to find relevant videos on YouTube.<br>
This is done using Selenium, a web automation tool that:
<br><br>
Opens YouTube in a web browser.<br>
Locates the search bar and types in the extracted text.<br>
Triggers the search by pressing Enter.<br>
At this stage, YouTube displays a list of videos most relevant to the extracted text.
<br><br>
5. Automate YouTube Playback<br>
After retrieving search results, the script:
<br><br>
Identifies the first video in the search results.<br>
Ensures the video thumbnail is visible by scrolling the page (to avoid hidden elements).<br>
Clicks on the video to start playback automatically.<br>
Result: The system plays the most relevant YouTube video based on the extracted text, completing the process seamlessly.
<br><br>

<b>Tech Stack</b><br>
Python – Core programming language.<br>
OpenCV – Capturing and processing images.<br>
EasyOCR – Optical Character Recognition for text extraction.<br>
Selenium – Web automation for YouTube search and playback.<br>
Matplotlib & NumPy – Image processing and visualization.<br>
<br>

<b>How to Run the Project</b><br>
1. Install Dependencies<br>
pip install opencv-python numpy matplotlib easyocr selenium<br>
2. Set Up ChromeDriver<br>
Download the correct version of ChromeDriver based on your Chrome version.<br>
Add it to your system’s PATH or keep it in the same directory as the script.<br>
3. Configure IP Camera URL<br>
Update the IP_CAMERA_URL variable in the script with your camera’s streaming URL.<br>
4. Run the Script<br>
The system will process an image, extract text, search for a related video, and play it on YouTube.
<br><br>
<b>Conclusion</b>
This project automates the entire process of extracting real-world text from an image and finding related content online in a fully hands-free manner. It mimics how a human would read something, search for related videos, and watch them using AI and automation. 







