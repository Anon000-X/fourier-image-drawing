# Fourier Image Drawing

A Python program that I made to reconstruct an image using Fourier coefficients and rotating circles.

## Description

The program takes the input image, converts it to a grayscale image, detects the line art in the picture and then converts all the line art into contours; for each contour, it performs a Fourier transform to represent it as a series of rotating circles, each of which is defined by its Fourier coefficient, frequency, and starting phase.

Each point on a contour is treated as a complex number:

`z = x + iy`

The Fourier transform breaks down this sequence of points into Fourier coefficients, each corresponding to a rotating circle. The magnitude of the coefficient gives the radius of the circle, and the frequency of the coefficient determines both the speed and the direction of rotation of the circle. The phase of the coefficient determines the initial angle of the circle.

The circles are linked together in the form of a chain; the centre of the first circle is at the origin of the coordinate system, the endpoint of the first circle becomes the centre of the second circle, the endpoint of the second circle becomes the centre of the third circle, and so on.

In the animation, the position of each circle is determined by its frequency, radius, phase, and the current time, and the point at which the last circle ends is the point currently being drawn on the contour.

The circles are therefore a set of rotating vectors; when all of them are added together, the position of the resultant vector follows the shape of the original contour, and by plotting the path followed by this endpoint over time, the program slowly reconstructs the original image.

The Fourier coefficients are arranged in order of their magnitude, with the coefficient having larger magnitudes selected first. In this way, the general shape of the contour can be reconstructed using the most important components before the smaller details are included.

## How It Works

The program can be divided into several main steps:

### 1. Image Processing

The input image is first converted from a color image into grayscale. Otsu's thresholding method is then used to separate the line art from the background.

The resulting binary image is inverted so that the line art can be detected as the foreground.

OpenCV's `findContours()` function is then used to detect the contours in the image. Very small contours are filtered out because they are usually insignificant for the final reconstruction.

### 2. Converting Contours into Complex Numbers

Each contour consists of a sequence of points with `x` and `y` coordinates. These points are represented as complex numbers:

`z = x + iy`

This allows the contour to be treated as a complex-valued signal, which can then be processed using the Fourier transform.

### 3. Fourier Transform

For each contour, the program calculates the Discrete Fourier Transform using NumPy's FFT implementation.

The result is a set of Fourier coefficients. Each coefficient contains information about one component of the contour.

For a coefficient `C`:

- `abs(C)` determines the radius of the corresponding circle.
- `angle(C)` determines its starting phase.
- Its frequency determines how fast and in which direction the circle rotates.

The coefficients are then sorted according to their magnitude. Only a selected number of the largest coefficients are used for the reconstruction.

The number of coefficients can be changed using:

```python
n_harmonics = min(50, N)
```

Increasing this value allows more components of the original contour to be reproduced, resulting in a more detailed reconstruction.

### 4. Drawing the Rotating Circles

During the animation, the circles are connected together to form a chain.

The first circle starts at the origin. Its endpoint becomes the center of the next circle, whose endpoint becomes the center of the following circle, and so on.

For each Fourier component, the current angle is calculated using:

```text
angle = 2πft + phase
```

The position of the endpoint is then calculated from the radius and angle of the component.

The endpoint of the final circle is the point that is used to draw the reconstructed contour.

### 5. Reconstructing the Image

The position of the final endpoint is recorded at every frame of the animation.

As time progresses, these recorded points form a path. Since the Fourier components describe the original contour, the path gradually reproduces the shape of that contour.

The same process is performed for every detected contour, allowing all of them to be reconstructed and displayed together.

---

## Installation

### Requirements

You need:

- Python 3.x
- OpenCV
- NumPy
- Matplotlib

You can install the required Python libraries using:

```bash
pip install opencv-python numpy matplotlib
```

### Getting the Program

You can download the repository from GitHub itself and extract it.

### Running the Program

Open the Python file and specify the path to your input image:

```python
img_path = "path/to/your/image.jpg"
```

Then run the program:

```bash
python main.py
```

The program will first display the detected contours and then start the Fourier drawing animation.
