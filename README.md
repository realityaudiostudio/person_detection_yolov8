# **Person Detection using YOLOv8**

This repository contains a **YOLOv8-based person detection system** that accesses the **device camera** to detect people in real time.

---

## **Installation & Setup**

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### **2️⃣ Create a Virtual Environment**  
It is recommended to use a **virtual environment** to manage dependencies.

For **Windows (PowerShell)**:  
```powershell
python -m venv venv
venv\Scripts\activate
```

For **Mac/Linux**:  
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## **3️⃣ Install Dependencies**  
Run the following command to install the required Python packages:  
```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not available, manually install:  
```bash
pip install ultralytics opencv-python matplotlib
```

---

## **4️⃣ Run the Person Detection Script**  
Ensure your **webcam is connected**, then run:  
```bash
py test.py
```
The script will access your **camera** and perform **real-time person detection**.

---

## **📂 Repository Structure**  

```
📁 your-repo-name/
|-- .venv                # Virtual environment of the project 
│-- 📄 best.pt          # Trained YOLOv8 model
│-- 📄 test.py          # Script to access camera & detect persons
│-- 📄 .gitignore       # Ignore unnecessary files (e.g., images, venv)
│-- 📄 README.md        # Documentation
```

---

## **📌 Notes**  
- If you face issues with `cv2.VideoCapture(0)`, try changing the `0` to `1` or `2`.
- Ensure your **camera is not being used** by another application.  
- Use **Ctrl+C** in the terminal to stop the script.  

---

## **🔗 References**  
- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)  

🚀 Happy Coding! 🎯
