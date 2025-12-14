# 1st-Sem-Jackfruit-Problem-Image-processing-


# Project Report

## Project Title
**Image Processing Application Using wxPython and PIL**

---

## Team Members’ Names with SRN, Name and Section

1. **Name:** Rahul Sridara Shetty  
   **SRN:** PES1UG25EC344  
   **Section:** P13  

2. **Name:** Rathanga Parthasarathy  
   **SRN:** PES1UG25EC345  
   **Section:** P13  

3. **Name:** Naman Goyal  
   **SRN:** PES1UG25EC355  
   **Section:** P13  

4. **Name:** Manith H P  
   **SRN:** PES1UG25AM499  
   **Section:** P13  

---

## Problem Statement

Digital images often require basic processing such as color transformation, enhancement, filtering, and analysis before being used in real-world applications. Most professional image editing tools are complex, costly, and not suitable for beginners who want to understand image processing fundamentals.

**Note:**  
This is just a prototype of what a software like this could be capable of and not the software itself.

---

## Approach

### 1. GUI Development
- The graphical user interface is built using **wxPython**, which provides native-looking windows and controls.
- A main frame (`MainFrame`) is created to display the image, dropdown menu, and buttons.

### 2. Image Processing
- **Pillow (PIL)** library is used for image manipulation.
- Images are loaded in **RGBA format** to preserve color and transparency.
- Each filter is applied using either built-in PIL functions or custom pixel-level processing.

### 3. Filter Selection and Execution
- A dropdown (`wx.Choice`) allows the user to select an image operation.
- On clicking the **Apply** button, the selected filter is processed and displayed.

### 4. Color Palette Extraction
- The image is resized for efficiency.
- **Color quantization (Median Cut algorithm)** is applied.
- The most frequent colors are extracted and displayed in a separate palette window.

### 5. Palette Visualization
- A toggle button displays a new frame showing color swatches with corresponding **hex values**.

---

## Sample Input / Output

### Input
- **Input File:** `sample.jpg`
- **Selected Operation:** Sepia
- **Toggle Button:** Show Top 5 colours

### Output
- Processed image with sepia filter applied
- Separate window displaying the top 5 dominant colors with hex codes

---

## Challenges Faced

- Image format conversion between **wxPython** and **PIL**, GUI refresh handling, and performance optimization for large images.
- Managing compatibility between different versions of **Pillow** and **wxPython**.
- Converting between `wx.Image` and `PIL.Image` while preserving color and transparency.

---

## Scope for Improvement

- Support for multiple images
- Undo/redo functionality
- Slider-based controls for filters
- Saving processed images
- Advanced image processing filters
