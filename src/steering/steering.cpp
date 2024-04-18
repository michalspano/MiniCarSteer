#include "steering.hpp"
#include <algorithm>
#include <cmath>

/*

*/
double calculateSteering(std::vector<datapoint> distances) {
  double multiplier = 0;
  if (distances[0].distance > distances.back().distance) {
    // Left
    for (size_t i = 0; i < distances.size(); ++i) {
      if (distances[i].occurrences > MIN_PIXELS_THRESHOLD) {
        multiplier = distances[i].distance * -1;
        break;
      }
    }
  } else {
    // Right
    for (size_t i = distances.size(); i-- > 0;) {
      if (distances[i].occurrences > MIN_PIXELS_THRESHOLD) {
        multiplier = distances[i].distance;
        break;
      }
    }
  }
  // Steering angle calculation
  return ((multiplier / 10) * 0.8 + 0.06);
}

double calculateDistance(int x, int y, int incrementX, int incrementY) {
  // Euclidean distance calculation
  double deltaY = std::abs(y - ORIGIN_Y) / incrementY;
  double deltaX = std::abs(x - ORIGIN_X) / incrementX;
  double c2 = std::pow(deltaX, 2) + std::pow(deltaY, 2);
  return std::sqrt(c2);
}