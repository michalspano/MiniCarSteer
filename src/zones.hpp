/*******************************************************************************
 * zones
 * File: {@code cone_detector.h} [header file]
 * Authors: Arumeel Kaisa, Khodaparast Omid, Michal Spano, Säfström Alexander
 *
 * DIT639 Cyber Physical Systems and Sytems of Systems
 ******************************************************************************/

// Impose a header guard
#ifndef ZONE_H
#define ZONE_H

// Blue zone (active zone)
#define MIN_X_BLUE 0
#define MAX_Y_BLUE 380
#define MAX_X_BLUE 320
#define MIN_Y_BLUE 260

// Yellow zone (active zone)
#define MIN_X_YELLOW 320
#define MAX_Y_YELLOW 380
#define MAX_X_YELLOW 640
#define MIN_Y_YELLOW 260

// The increments for x, y are identical for both zones
#define INCREMENT_X 40
#define INCREMENT_Y 120

// The number of zones: dynamically computed based on the previous definitions
#define N_ZONES \
  ((MAX_X_BLUE - MIN_X_BLUE) / INCREMENT_X) * ((MAX_Y_BLUE - MIN_Y_BLUE) / INCREMENT_Y) + \
  ((MAX_X_YELLOW - MIN_X_YELLOW) / INCREMENT_X) * ((MAX_Y_YELLOW - MIN_Y_YELLOW) / INCREMENT_Y)

#endif // zones.hpp
