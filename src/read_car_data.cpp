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
void debug(cv::Mat img, int x, int y, double distance, int color) {
  int textX = (x + BLUE_ZONE_INCREMENT_X / 2);
  int textY = (y + BLUE_ZONE_INCREMENT_Y / 2);
  cv::Scalar colorCode;
  if (!color) {
    colorCode = cv::Scalar(255, 0, 0);
  } else {
    colorCode = cv::Scalar(0, 255, 255);
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
      od4.dataTrigger(opendlv::proxy::GroundSteeringRequest::ID(),
                      onGroundSteeringRequest);

      int correctCount = 0, incorrectCount = 0;

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

          std::vector<int> datapoints;

          datapoints = getDataPointsPerFrame(0, hsv);

          double leftSideSteering = calculateSteering(datapoints, true);
          datapoints.clear();

          datapoints = getDataPointsPerFrame(1, hsv);
          double rightSideSteering = calculateSteering(datapoints, false);

          // std::cout << "blue steering angle opinion: " << blueSteeringOpinion
          // << std::endl; std::cout << "yellow steering angle opinion: " <<
          // yellowSteeringOpinion << std::endl;

          std::lock_guard<std::mutex> lck(gsrMutex);
          double expectedSteering = gsr.groundSteering();

          double actualSteering;
          if (std::abs(rightSideSteering) > std::abs(leftSideSteering)) {
            actualSteering = rightSideSteering;
          } else {
            actualSteering = leftSideSteering;
          }
          std::cout << "actual steering: " << expectedSteering << std::endl;
          // actual, predicted
          if (isValidSteeringAngle(actualSteering, expectedSteering)) {
            correctCount++;
          } else {
            incorrectCount++;
          }

          std::cout << "Correct count: " << correctCount << std::endl;
          std::cout << "Incorrect count: " << incorrectCount << std::endl;

          std::string steering_string =
              std::to_string(gsr.groundSteering()) + "\n";
          std::ofstream ofs("/tmp/steering.txt", std::ios_base::app);
          ofs << steering_string;
          ofs.close();
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
