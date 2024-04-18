/*
 * Copyright (C) 2020  Christian Berger
 *
 * Co-authored by:
 * - Arumeel Kaisa
 * - Khodaparast Omid
 * - Michal Spano
 * - Säfström Alexander
 * (C) 2024, DIT639 Cyber Physical Systems and Systems of Systems
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

// Include the single-file, header-only middleware libcluon to create
// high-performance microservices
#include "cluon-complete.hpp"

// Include the OpenDLV Standard Message Set that contains messages that are
// usually exchanged for automotive or robotic applications
#include "opendlv-standard-message-set.hpp"

// Include the GUI and image processing header files from OpenCV
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <vector>

// Custom imports from pre-made modules
#include "cone_detection/cone_detector.hpp"
#include "steering/steering.hpp"
#include "zones.hpp"
#include <cmath>
void debug(cv::Mat img, int x, int y, double distance,int color) {
  int textX = (x + BLUE_ZONE_INCREMENT_X / 2);
  int textY = (y + BLUE_ZONE_INCREMENT_Y / 2);
  cv::Scalar colorCode;
  if (!color){
    colorCode=cv::Scalar(255,0,0);
  } else {
    colorCode=cv::Scalar(0,255,255);
  }
  cv::putText(img, std::to_string(distance), cv::Point(textX, textY),
              cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 255), 2);
  cv::rectangle(img, cv::Point(x, y),
                cv::Point(x + BLUE_ZONE_INCREMENT_X, y + BLUE_ZONE_INCREMENT_Y),
                colorCode);
}

// The main entry point of the program
int32_t main(int32_t argc, char **argv) {
  int32_t retCode = 1;

  // Parse the command line parameters as we require the user to specify some
  // mandatory information on startup.
  auto commandlineArguments = cluon::getCommandlineArguments(argc, argv);
  if ((0 == commandlineArguments.count("cid")) ||
      (0 == commandlineArguments.count("name")) ||
      (0 == commandlineArguments.count("width")) ||
      (0 == commandlineArguments.count("height"))) {
    std::cerr << argv[0]
              << " attaches to a shared memory area containing an ARGB image."
              << std::endl;
    std::cerr << "Usage:   " << argv[0]
              << " --cid=<OD4 session> --name=<name of shared memory area> "
                 "[--verbose]"
              << std::endl;
    std::cerr << "         --cid:    CID of the OD4Session to send and receive "
                 "messages"
              << std::endl;
    std::cerr << "         --name:   name of the shared memory area to attach"
              << std::endl;
    std::cerr << "         --width:  width of the frame" << std::endl;
    std::cerr << "         --height: height of the frame" << std::endl;
    std::cerr << "Example: " << argv[0]
              << " --cid=253 --name=img --width=640 --height=480 --verbose"
              << std::endl;
  } else {
    // Extract the values from the command line parameters
    const std::string NAME = commandlineArguments["name"];
    const bool VERBOSE = commandlineArguments.count("verbose") != 0;

    const uint32_t WIDTH{
        static_cast<uint32_t>(std::stoi(commandlineArguments["width"]))};
    const uint32_t HEIGHT{
        static_cast<uint32_t>(std::stoi(commandlineArguments["height"]))};

    // Attach to the shared memory.
    std::unique_ptr<cluon::SharedMemory> sharedMemory{
        new cluon::SharedMemory{NAME}};

    if (sharedMemory && sharedMemory->valid()) {
      // Print that we are attached to memmory
      std::clog << argv[0] << ": Attached to shared memory '"
                << sharedMemory->name() << " (" << sharedMemory->size()
                << " bytes)." << std::endl;

      // Interface to a running OpenDaVINCI session where network messages are
      // exchanged. The instance od4 allows you to send and receive messages.
      cluon::OD4Session od4{
          static_cast<uint16_t>(std::stoi(commandlineArguments["cid"]))};

      std::mutex gsrMutex;
      opendlv::proxy::GroundSteeringRequest gsr;

      auto onGroundSteeringRequest = [&gsr,
                                      &gsrMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(gsrMutex); // Acquite lock for data
        gsr = cluon::extractMessage<opendlv::proxy::GroundSteeringRequest>(
            std::move(env));
      };

      // Endless loop; end the program by pressing Ctrl-C.
      while (od4.isRunning()) {
        // OpenCV data structure to hold an image.
        cv::Mat img;

        // Wait for a notification of a new frame.
        sharedMemory->wait();

        // Lock the shared memory.
        sharedMemory->lock();
        {

          // Copy the pixels from the shared memory into our own data structure.
          cv::Mat wrapped(HEIGHT, WIDTH, CV_8UC4, sharedMemory->data());
          img = wrapped.clone();
        }

        // Unlock the shared memory.
        sharedMemory->unlock();
        {
          // Transform the image to HSV
          cv::Mat hsv(HEIGHT, WIDTH, CV_8UC3);
          cv::cvtColor(img, hsv, cv::COLOR_BGR2HSV);
          int yellowPixels, bluePixels;
          int zone = 0;
          std::vector<datapoint> datapoints;

          for (int y = MIN_Y_BLUE; y <= MAX_Y_BLUE - BLUE_ZONE_INCREMENT_Y;
               y += BLUE_ZONE_INCREMENT_Y) {
            for (int x = MIN_X_BLUE; x <= MAX_X_BLUE - BLUE_ZONE_INCREMENT_X;
                 x += BLUE_ZONE_INCREMENT_X) {
              // Check the 'blue zone'
              yellowPixels = checkZone(hsv, x, x + BLUE_ZONE_INCREMENT_X, y,
                                       y + BLUE_ZONE_INCREMENT_Y, 1);

              double distance = calculateDistance(x + BLUE_ZONE_INCREMENT_X / 2,
                                                  y + BLUE_ZONE_INCREMENT_Y / 2,
                                                  BLUE_ZONE_INCREMENT_X,
                                                  BLUE_ZONE_INCREMENT_Y) *
                                100;
              distance = ((int)distance) / 100.0;
              struct datapoint point = {distance, yellowPixels};
              datapoints.push_back(point);
              debug(img, x, y, distance,0);
              zone++;
            }
          }
            double blueSteeringOpinion = calculateSteering(datapoints);
            datapoints.clear();

            std::cout << "blue steering angle opinion: " << blueSteeringOpinion
                      << std::endl;
            zone = 0;

            for (int y = MIN_Y_YELLOW;
                 y <= MAX_Y_YELLOW - YELLOW_ZONE_INCREMENT_Y;
                 y += YELLOW_ZONE_INCREMENT_Y) {
              for (int x = MIN_X_YELLOW;
                   x <= MAX_X_YELLOW - YELLOW_ZONE_INCREMENT_X;
                   x += YELLOW_ZONE_INCREMENT_X) {
                zone++;
                // Check the 'yellow zone'
                bluePixels = checkZone(hsv, x, x + YELLOW_ZONE_INCREMENT_X, y,
                                       y + YELLOW_ZONE_INCREMENT_Y, 0);

                double distance =
                    calculateDistance(x + YELLOW_ZONE_INCREMENT_X / 2,
                                      y + YELLOW_ZONE_INCREMENT_Y / 2,
                                      YELLOW_ZONE_INCREMENT_X,
                                      YELLOW_ZONE_INCREMENT_Y) *
                    100;
                distance = ((int)distance) / 100.0;
                struct datapoint point = {distance, bluePixels};
                datapoints.push_back(point);
                debug(img, x, y, distance,1);
              }
            }
          
          double yellowSteeringOpinion = calculateSteering(datapoints);
          std::cout << "yellow steering angle opinion: "
                    << yellowSteeringOpinion << std::endl;
        }

        // Display image on your screen.
        if (VERBOSE) {
          cv::imshow(sharedMemory->name().c_str(), img);
          cv::waitKey(1);
        }
      }
    }
    retCode = 0;
  }
  return retCode;
}
