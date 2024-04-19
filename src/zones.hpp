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

// FIXME: will be removed.
#define BLUE_ZONE_INCREMENT_X 40
#define BLUE_ZONE_INCREMENT_Y 120

// Yellow zone
#define MIN_X_YELLOW 320
#define MAX_Y_YELLOW 380
#define MAX_X_YELLOW 640
#define MIN_Y_YELLOW 260

// FIXME: will be removed.
#define YELLOW_ZONE_INCREMENT_X 40
#define YELLOW_ZONE_INCREMENT_Y 120

#define INCREMENT_X 40
#define INCREMENT_Y 120

#define N_ZONES 16
#endif
