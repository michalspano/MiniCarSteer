/*******************************************************************************
 * steering
 * File: {@code steering.h} [header file]
 * Authors: Arumeel Kaisa, Khodaparast Omid, Michal Spano, Säfström Alexander
 *
 * DIT639 Cyber Physical Systems and Sytems of Systems
 ******************************************************************************/

// Impose a header guard
#ifndef STEERING_H
#define STEERING_H

// Imports
#include <iostream>
#include <vector>
#include "../zones.hpp"
#include "../cone_detection/cone_detector.hpp"

#define ORIGIN_X 320
#define ORIGIN_Y 380
#define MIN_PIXELS_THRESHOLD 10

struct datapoint {
  double distance;
  int occurrences;
};

// Function prototypes
bool isValidSteeringAngle(double actual, double predicted);
double calculateSteering(std::vector<int> pixels, bool isLeft);
std::vector<int> getDataPointsPerFrame(int colorId, cv::Mat hsv);

#endif
