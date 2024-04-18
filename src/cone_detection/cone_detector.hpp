/*******************************************************************************
 * cone_detection
 * File: {@code cone_detector.h} [header file]
 * Authors: Arumeel Kaisa, Khodaparast Omid, Michal Spano, Säfström Alexander
 *
 * DIT639 Cyber Physical Systems and Sytems of Systems
 ******************************************************************************/

// Impose a header guard
#ifndef CONE_DETECTOR_H
#define CONE_DETECTOR_H

// Imports
#include <iostream>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

// Define blue HSV filter [id:0]
#define BLUE_HUE_MIN 115
#define BLUE_HUE_MAX 137
#define BLUE_SATURATION_MIN 101
#define BLUE_SATURATION_MAX 213
#define BLUE_VALUE_MIN 33
#define BLUE_VALUE_MAX 97

// Define yellow HSV filter [id:1]
#define YELLOW_HUE_MIN 16
#define YELLOW_HUE_MAX 39
#define YELLOW_SATURATION_MIN 58
#define YELLOW_SATURATION_MAX 255
#define YELLOW_VALUE_MIN 0
#define YELLOW_VALUE_MAX 255

// Function prototypes
int checkZone(cv::Mat HSV, int minX, int maxX, int minY, int maxY, int color);

#endif
