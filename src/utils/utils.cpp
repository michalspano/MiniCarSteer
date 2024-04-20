/*******************************************************************************
 * utils - utility functions
 * File: {@code utils.cpp} [source file]
 * Authors: Arumeel Kaisa, Khodaparast Omid, Michal Spano, Säfström Alexander
 *
 * DIT639 Cyber Physical Systems and Sytems of Systems
 ******************************************************************************/

#include "utils.hpp"

/* DEBUG MODE */
#if defined(DEBUG_ON)
/**
 * A utility function to showcase the zones (and regions) on the image stream.
 * Supported only in the debug mode.
 *
 * @param colorId - yellow/blue zone
 * @param igm     - pointer to the image buffer
 */
void displayZones(int colorId, cv::Mat img) {
  // Color configuration (default: blue/0)
  unsigned int minX = MIN_X_BLUE,
               minY = MIN_Y_BLUE,
               maxX = MAX_X_BLUE,
               maxY = MAX_Y_BLUE;

  switch (colorId) {
  case 1: // Yellow
    minX = MIN_X_YELLOW;
    minY = MIN_Y_YELLOW;
    maxX = MAX_X_YELLOW;
    maxY = MAX_Y_YELLOW;
    break;
  }

  // Decide on the color based on the colorId
  cv::Scalar color = !colorId ? cv::Scalar(255, 0, 0) : cv::Scalar(0, 255, 255);

  // Go over each region of the zone
  for (int y = minY; y <= maxY - INCREMENT_Y; y += INCREMENT_Y) {
    for (int x = minX; x <= maxX - INCREMENT_X; x += INCREMENT_X) {
      cv::rectangle(
          img, cv::Point(x, y),
          cv::Point(x + INCREMENT_X, y + INCREMENT_Y),
          color);
    }
  }
}
#endif
