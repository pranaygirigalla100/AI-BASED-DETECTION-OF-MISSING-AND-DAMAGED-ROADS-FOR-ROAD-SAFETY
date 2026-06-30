# AI-Based Detection of Missing and Damaged Roads for Road Safety

An AI-powered web application that detects road damages — such as **potholes** and **cracks** — from uploaded images using a custom-trained **YOLOv11** model. Detected damages are highlighted with bounding boxes, helping authorities and maintenance teams quickly identify road sections that need repair, improving overall road safety.

## Features

- Upload a road image and detect potholes and cracks automatically
- Bounding boxes drawn around each detected damage
- Simple, interactive web interface built with Streamlit
- Custom-trained YOLOv11 model for accurate detection
- Dockerized for easy deployment on any system

## Tech Stack

- **Python** – core programming language
- **OpenCV** – image processing
- **YOLOv11** – object detection model
- **PyTorch** – deep learning framework
- **Streamlit** – web application interface
- **Docker** – containerization and deployment
- **NumPy** – numerical operations

## Project Structure

```text
Project/
│── app.py                 # Main Streamlit application
│── best.pt                # Trained YOLOv11 model weights
│── requirements.txt       # Python dependencies
│── Dockerfile             # Docker image configuration
│── docker-compose.yml     # (if used) multi-container setup
│── dataset/                 # Training/validation/test dataset
│── README.md
```

## Dataset

A custom dataset containing labeled images of **potholes** and **cracks** was used to train the YOLOv11 model, enabling it to accurately detect and localize road damage in real-world images.

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- (Optional) Docker installed, for containerized setup

### Option 1: Run Without Docker

1. Clone the repository
   ```bash
   git clone https://github.com/pranaygirigalla100/AI-BASED-DETECTION-OF-MISSING-AND-DAMAGED-ROADS-FOR-ROAD-SAFETY.git
   cd AI-BASED-DETECTION-OF-MISSING-AND-DAMAGED-ROADS-FOR-ROAD-SAFETY
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app
   ```bash
   streamlit run app.py
   ```

4. Open your browser and go to:
   ```
   http://localhost:8501
   ```

### Option 2: Run With Docker

1. Build the Docker image
   ```bash
   docker build -t road-damage-detector .
   ```

2. Run the container
   ```bash
   docker run -p 8501:8501 road-damage-detector
   ```

3. Open your browser and go to:
   ```
   http://localhost:8501
   ```

## How It Works

1. The user uploads a road image through the Streamlit interface.
2. The image is passed to the trained YOLOv11 model (`best.pt`).
3. The model detects regions containing potholes or cracks.
4. Bounding boxes are drawn around each detected damage on the image.
5. The annotated result is displayed back to the user in the app.

## Future Scope

- Extend detection to identify missing road segments using satellite/aerial imagery
- Add severity classification (minor, moderate, severe damage)
- Integrate GPS tagging for damage location mapping
- Build a dashboard for municipal authorities to track repairs over time

## License

This project is open-source and available for educational and research purposes.

## Acknowledgements

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for the object detection framework
- Streamlit for the web application framework
