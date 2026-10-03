import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Tou can change the path to your image here
img_path = "C:\\Users\\hnfdn\\Pictures\\Project\\maxresdefault.jpg"
image = cv2.imread(img_path)

# Checking if image actually loaded
if image is None:
    print("Error: couldn't load image. Check the path!")
    exit()

# Convert the image to grayscale and extract the line art
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

binarized_image = cv2.bitwise_not(thresh)

# Find every contour in the line art
contours, hierarchy = cv2.findContours(
    binarized_image,
    cv2.RETR_LIST,
    cv2.CHAIN_APPROX_NONE
)

# Filtering out the super small and insignificant contours
good_contours = []
for c in contours:
    if cv2.contourArea(c) > 10:
        good_contours.append(c)

contours = good_contours
print("Got this many contours:", len(contours))

# Display the extracted contours to check if they look correct
plt.figure()
for cnt in contours:
    cnt = cnt.reshape(-1, 2)
    plt.plot(cnt[:, 0], cnt[:, 1], linewidth=0.5)

plt.gca().invert_yaxis()
plt.axis("equal")
plt.title("Contours check")

fourier_contours = []

for cnt in contours:
    cnt = cnt.reshape(-1, 2)
    x = cnt[:, 0]
    y = cnt[:, 1]

    # Represent each contour point as a complex number
    z = x + 1j * y
    
    N = len(z)

    # Apply the Fourier transform to decompose the contour into individual rotating components
    fourier_result = np.fft.fft(z) / N

    # Get the frequency associated with each Fourier coefficient
    freqs = np.fft.fftfreq(N) * N
    freqs = freqs.astype(int)

    # The magnitude of each coefficient determines the radius of its corresponding rotating circle
    mags = np.abs(fourier_result)

    # Sort the coefficients from largest to smallest magnitude
    sorted_idx = np.argsort(mags)[::-1]

    # You can change the number of Fourier components used here 
    n_harmonics = min(50, N)
    sorted_idx = sorted_idx[:n_harmonics]

    fourier_contours.append({
        "fourier": fourier_result,
        "frequencies": freqs,
        "indices": sorted_idx
    })

fig, ax = plt.subplots(figsize=(8, 8))
# You can change the number of frames here
total_frames = 300 
time_steps = np.linspace(0, 1, total_frames)

drawn_paths = [[] for _ in fourier_contours]

def animate_draw(frame):
    ax.clear()

    # Last frame = trace only
    if frame == total_frames:
        for p in drawn_paths:
            pass

        ax.set_aspect("equal")
        ax.set_xlim(0, image.shape[1])
        ax.set_ylim(0, image.shape[0])
        ax.invert_yaxis()

        for p in drawn_paths:
            pts = np.array(p)

            if len(pts) > 1:
                ax.plot(pts.real, pts.imag, linewidth=1.2, color="red")

        ax.set_title("Fourier drawing complete")

        return

    # Clear previous paths when the animation starts
    if frame == 0:
        for p in drawn_paths:
            p.clear()

    ax.set_aspect("equal")
    ax.set_xlim(0, image.shape[1])
    ax.set_ylim(0, image.shape[0])
    ax.invert_yaxis()

    current_t = time_steps[frame]

    for i, item in enumerate(fourier_contours):

        fourier = item["fourier"]
        frequencies = item["frequencies"]
        indices = item["indices"]

        # Start the chain of rotating circles at the origin
        current_pos = 0 + 0j

        for idx in indices:

            coeff = fourier[idx]

            # Magnitude = radius of the circle
            radius = np.abs(coeff)
            
            # Phase = starting angle of the circle
            phase = np.angle(coeff)

            # Frequency = rotation speed and direction
            freq = frequencies[idx]

            # Calculate the current angle of this rotating component
            angle = 2 * np.pi * freq * current_t + phase

            # Calculate the endpoint of the current rotating vector
            next_pos = (current_pos + radius * np.exp(1j * angle))

            # Generate points used to draw the circle
            theta_vals = np.linspace(0, 2 * np.pi, 60)

            cx = (current_pos.real + radius * np.cos(theta_vals))
            cy = (current_pos.imag + radius * np.sin(theta_vals))

            ax.plot(cx, cy, linewidth=0.2, color="gray", alpha=0.5)
            
            # Draw the vector connecting this circle to the next one
            ax.plot([current_pos.real, next_pos.real], [current_pos.imag, next_pos.imag], linewidth=0.6, color="blue")
            current_pos = next_pos
            
        # Store the endpoint of the final circle to create the trace
        drawn_paths[i].append(current_pos)

        pts = np.array(drawn_paths[i])

        if len(pts) > 1:
            ax.plot(pts.real, pts.imag, linewidth=1.2, color="red")
            
        # Mark the current drawing point
        ax.plot(current_pos.real, current_pos.imag, "ro", markersize=2)

    ax.set_title(f"Epicycles drawing... frame {frame + 1}/{total_frames}")

# run the animation
anim = FuncAnimation(fig, animate_draw, frames=total_frames + 1, interval=15, repeat=False)

plt.show() 
