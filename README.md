# Fourier Image Drawing

A program in Python which I made for reconstructing an image by means of Fourier coefficients and rotating circles.

## Description

The program will take the input image, convert it to a grayscale image, detect the line art in the picture and then convert all the line art into contours; for each contour it will carry out a Fourier transform in order to represent it as a series of rotating circles, each of which is defined by its Fourier coefficient, frequency, and starting phase.

Each point on a contour is treated as a complex number:

`z = x + iy`

The Fourier transform breaks down this sequence of points into Fourier coefficients, each corresponding to a rotating circle. The magnitude of the coefficient gives the radius of the circle, and the frequency of the coefficient determines both the speed and the direction of rotation of the circle. The phase of the coefficient determines the initial angle of the circle.

The circles are linked together in the form of a chain; the centre of the first circle is at the origin of the coordinate system, the end point of the first circle becomes the centre of the second circle, the end point of the second circle becomes the centre of the third circle, and so on.

In the animation, the position of each circle is determined by its frequency, radius, phase, and the present time, and the point at which the last circle ends is the point currently being drawn on the contour.

The circles are therefore a set of rotating vectors; when all of them are added together, the position of the resultant vector follows the shape of the original contour, and by plotting the path followed by this endpoint over time, the programme slowly reconstructs the original image.

The coefficients of Fourier are arranged in order of their magnitude, with the larger circles being taken first; in this way, the general shape of the contour can be reconstructed using the most important components before the smaller details are included.

