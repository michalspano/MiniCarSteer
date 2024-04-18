/*******************************************************************************
 * cone_detection
 * File: {@code cone_detector.h} [header file]
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
#define ORIGIN_X 320
#define ORIGIN_Y 380
#define MIN_PIXELS_THRESHOLD 10

struct datapoint {
  double distance;
  int occurrences;
};

// Function prototypes
double calculateSteering(std::vector<datapoint> distances);
double calculateDistance(int x, int y, int incrementX, int incrementY);
#endif
