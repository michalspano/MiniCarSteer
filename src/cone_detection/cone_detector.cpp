#include "cone_detector.hpp"
#include <opencv2/imgproc/imgproc.hpp>

// Define blue HSV filter
#define BLUE_HUE_MIN 115 
#define BLUE_HUE_MAX 137
#define BLUE_SATURATION_MIN 101
#define BLUE_SATURATION_MAX 213
#define BLUE_VALUE_MIN 33
#define BLUE_VALUE_MAX 97

// Define yellow SHV filter
#define YELLOW_HUE_MIN 16
#define YELLOW_HUE_MAX 39
#define YELLOW_SATURATION_MIN 58
#define YELLOW_SATURATION_MAX 255
#define YELLOW_VALUE_MIN 0
#define YELLOW_VALUE_MAX 255
