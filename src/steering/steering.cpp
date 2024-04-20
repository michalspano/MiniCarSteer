/*******************************************************************************
 * steering
 * File: {@code steering.cpp} [source file]
 * Authors: Arumeel Kaisa, Khodaparast Omid, Michal Spano, Säfström Alexander
 *
 * DIT639 Cyber Physical Systems and Sytems of Systems
 ******************************************************************************/

#include "steering.hpp"

// FIXME: this function is WIP and does not work fully for now.
double calculateSteering(std::vector<int> pixels, bool isLeft) {
  double multiplier = 0;
  if (isLeft) {
    // Left-hand side region
    for (int i = 0; i < pixels.size(); i++) {
      if (pixels[i] > MIN_PIXELS_THRESHOLD) {
        std::cout << i << std::endl;
        multiplier = i + 1.0;
        break;
      }
    }
  } else {
    // Right-hand side region
    for (int i = pixels.size() - 1; i > 0; i--) {
      if (pixels[i] > MIN_PIXELS_THRESHOLD) {
        multiplier = (pixels.size() - i + 1.0) * -1.0;
        break;
      }
    }
  }

  // Logs
  // Steering angle calculation
  std::cout << "m: " << multiplier << std::endl;
  double angle = multiplier / pixels.size() * 0.3;
  std::cout << "Angle: " << angle << std::endl;
  return angle;
}

// Compare the steering afainst the 'ground' steering
bool isValidSteeringAngle(double actual, double predicted) {
  double minInterval = 0.75 * actual;
  double maxInterval = 1.25 * actual;

  return predicted >= minInterval && predicted <= maxInterval;
}

// Count the number of pixels each a color within a region of a single frame.
std::vector<int> getDataPointsPerFrame(int colorId, cv::Mat hsv) {
  int pixelCount;
  std::vector<int> pixels;

  // Color configuration
  int minY, maxY, minX, maxX;
  switch (colorId) {
  case 0:
    minX = MIN_X_BLUE;
    minY = MIN_Y_BLUE;
    maxX = MAX_X_BLUE;
    maxY = MAX_Y_BLUE;
    break;
  case 1:
    minX = MIN_X_YELLOW;
    minY = MIN_Y_YELLOW;
    maxX = MAX_X_YELLOW;
    maxY = MAX_Y_YELLOW;
    break;
  default:
    break;
  }

  for (int y = minY; y <= maxY - INCREMENT_Y; y += INCREMENT_Y) {
    for (int x = minX; x <= maxX - INCREMENT_X; x += INCREMENT_X) {
      pixelCount =
          checkZone(hsv, x, x + INCREMENT_X, y, y + INCREMENT_Y, colorId);
      pixels.push_back(pixelCount);
    }
  }
  return pixels;
}
