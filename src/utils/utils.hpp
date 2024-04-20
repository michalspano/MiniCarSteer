#ifndef UTILS_H
#define UTILS_H

// Library imports
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

// Custom module imports
#include "../zones.hpp"

// Toggle on/off the debug mode
#define DEBUG_ON 1

// Function prototypes for the debug mode
#if defined(DEBUG_ON)

// Display the individual zones
void displayZones(int colorId, cv::Mat img);

#endif

#endif // utils.h
