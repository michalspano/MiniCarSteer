/*******************************************************************************
 * cone_detection
 * File: {@code cone_detector.cpp} [source file]
 * Authors: Arumeel Kaisa, Khodaparast Omid, Michal Spano, Säfström Alexander
 *
 * DIT639 Cyber Physical Systems and Sytems of Systems
 ******************************************************************************/

// Include the header API
#include "cone_detector.hpp"

// Function to check a zone for a particular color
int checkZone(cv::Mat HSV, int minX, int maxX, int minY, int maxY, int color) {

  cv::Mat filtered(480, 640, CV_8UC3); // FIXME: extract magic numbers

  // FIXME: make this more modular.
  int hueMin, hueMax, satMin, satMax, valMin, valMax;
  switch (color) {
  case 0:
    hueMin = BLUE_HUE_MIN;
    hueMax = BLUE_HUE_MAX;
    satMin = BLUE_SATURATION_MIN;
    satMax = BLUE_SATURATION_MAX;
    valMin = BLUE_VALUE_MIN;
    valMax = BLUE_VALUE_MAX;
    break;
  case 1:
    hueMin = YELLOW_HUE_MIN;
    hueMax = YELLOW_HUE_MAX;
    satMin = YELLOW_SATURATION_MIN;
    satMax = YELLOW_SATURATION_MAX;
    valMin = YELLOW_VALUE_MIN;
    valMax = YELLOW_VALUE_MAX;
    break;
  default:
    break;
  }

  // Apply the HSV filter based on a chosen color
  cv::inRange(HSV, cv::Scalar(hueMin, satMin, valMin),
              cv::Scalar(hueMax, satMax, valMax), filtered);

  int occurrences = 0;
  for (int i = minX; i < maxX; i++) {
    for (int j = minY; j < maxY; j++) {
      if (filtered.at<uchar>(j, i) == 255) { // detect a white pixel
        occurrences++;
      }
    }
  }

  return occurrences;
}
