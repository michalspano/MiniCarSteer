#include "cone_detector.hpp"
#include <iostream>
cv::Mat checkZone(cv::Mat HSV, int minX, int maxX, int minY, int maxY, int color, int imageid) {
  cv::Mat filtered(480, 640, CV_8UC3);
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
  cv::inRange(HSV, cv::Scalar(hueMin, satMin, valMin),
              cv::Scalar(hueMax, satMax, valMax), filtered);
  int occurrences = 0;
  // Loop through zone
  for (int i = minX; i < maxX; i++) {
    for (int j = minY; j < maxY; j++) {
      int color1 = filtered.at<cv::Vec3b>(j, i)[0];
      int color2 = filtered.at<cv::Vec3b>(j, i)[1];
      int color3 = filtered.at<cv::Vec3b>(j, i)[2];
      if (filtered.at<cv::Vec3b>(j, i)[0] == 0 &&
          filtered.at<cv::Vec3b>(j, i)[1] == 0 &&
          filtered.at<cv::Vec3b>(j, i)[2] == 255) {
        occurrences++;
      }
    }

    std::cout << occurrences << "/" << imageid << std::endl;
    return filtered;
  }
}