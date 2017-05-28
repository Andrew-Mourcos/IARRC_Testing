from math import *

def real_slope(y, x, camerastats):
    h = float(camerastats['cameraHeight'])
    f = float(camerastats['focalLength'])
    m = float(camerastats['middleFOV'])
    b = float(camerastats['bottomFOV'])
    p = float(camerastats['pixelHeight'])
    pw= float(camerastats['pixelWidth'])
    R = sqrt(h ** 2 + m ** 2)
    sinA = h / R
    cosA = m / R
    smallToBig = sqrt(h ** 2 + m ** 2) / f  # Conversion between real and camera triangles (cm)
    screenHeight = 2 * f * (h * m - h * b) / (m * b + h ** 2)  # Height of camera screen (cm)
    pixToReal = screenHeight / p
    realTriangle = h / (f * sinA + (p / 2 - y) * pixToReal * cosA)
    smallTriangleResult = f * cosA - (p / 2 - y) * pixToReal * sinA
    vertResult = realTriangle * smallTriangleResult

    # HORIZONTAL STUFF
    horiConversion = sqrt((h ** 2 + vertResult ** 2) / (f ** 2 + ((p / 2 - y) * pixToReal) ** 2))
    horiResult = (pw / 2 - x) * pixToReal * horiConversion

    return (horiResult, vertResult)
