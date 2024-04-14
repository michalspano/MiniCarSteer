/*
 * Copyright (C) 2020  Christian Berger
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

int32_t main(int32_t argc, char **argv) {
  int32_t retCode{1};
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
    const std::string NAME{commandlineArguments["name"]};
    const uint32_t WIDTH{
        static_cast<uint32_t>(std::stoi(commandlineArguments["width"]))};
    const uint32_t HEIGHT{
        static_cast<uint32_t>(std::stoi(commandlineArguments["height"]))};
    const bool VERBOSE{commandlineArguments.count("verbose") != 0};

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

      opendlv::proxy::GroundSteeringRequest gsr;
      opendlv::proxy::AngularVelocityReading avr;
      opendlv::proxy::MagneticFieldReading mag;
      opendlv::logic::sensation::Geolocation geo;
      opendlv::proxy::AccelerationReading acc;
      std::mutex magMutex;
      std::mutex accMutex;

      std::mutex gsrMutex;
      std::mutex geoMutex;

      auto onGroundSteeringRequest = [&gsr,
                                      &gsrMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(gsrMutex); // Acquite lock for data
        gsr = cluon::extractMessage<opendlv::proxy::GroundSteeringRequest>(
            std::move(env));
      };

      std::mutex avrMutex;
      auto onAngularVelocityReading = [&avr,
                                       &avrMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(avrMutex);
        cluon::data::TimeStamp time = env.sampleTimeStamp();
        int64_t current_time_microseconds =
            cluon::time::toMicroseconds(time); // Convert time to microseconds
        std::string time_as_string = std::to_string(current_time_microseconds);
        avr = cluon::extractMessage<opendlv::proxy::AngularVelocityReading>(
            std::move(env));
      };
      auto onMagneticFieldReading = [&mag,
                                     &magMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(magMutex);
        mag = cluon::extractMessage<opendlv::proxy::MagneticFieldReading>(
            std::move(env));
      };
      auto onAccelerationReading = [&acc,
                                    &accMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(accMutex);
        acc = cluon::extractMessage<opendlv::proxy::AccelerationReading>(
            std::move(env));
      };
      auto onGeolocationReading = [&geo,
                                   &geoMutex](cluon::data::Envelope &&env) {
        std::lock_guard<std::mutex> lck(geoMutex);
        geo = cluon::extractMessage<opendlv::logic::sensation::Geolocation>(
            std::move(env));
      };

      od4.dataTrigger(opendlv::logic::sensation::Geolocation::ID(),
                      onGeolocationReading);
      od4.dataTrigger(opendlv::proxy::GroundSteeringRequest::ID(),
                      onGroundSteeringRequest);
      od4.dataTrigger(opendlv::proxy::AngularVelocityReading::ID(),
                      onAngularVelocityReading);
      od4.dataTrigger(opendlv::proxy::MagneticFieldReading::ID(),
                      onMagneticFieldReading);
      od4.dataTrigger(opendlv::proxy::MagneticFieldReading::ID(),
                      onMagneticFieldReading);
      od4.dataTrigger(opendlv::proxy::AccelerationReading::ID(),
                      onAccelerationReading);

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

        /**
         * getTimeStamp returns two properties, first and second.
         * if first is true then second contains timestamp value
         * if first is false then second contains 0
         */
        cluon::data::TimeStamp time_point = sharedMemory->getTimeStamp().second;
        // Convert time point to microseconds
        int64_t time_point_microseconds =
            cluon::time::toMicroseconds(time_point);

        // Get current time
        cluon::data::TimeStamp now{cluon::time::now()}; // Get current time
        int64_t current_time_microseconds =
            cluon::time::toMicroseconds(now); // Convert time to microseconds
        auto current_time_in_secs =
            current_time_microseconds / 1000000; // Convert to secs

        // Convert the time from seconds to a tm struct
        std::tm now_in_utc; // phind-codellama:34b-v2-q2_K
        gmtime_r(&current_time_in_secs,
                 &now_in_utc); // phind-codellama:34b-v2-q2_K

        // Create a buffer and use `strftime` to format the time into this
        // buffer
        char buf[1024]; // phind-codellama:34b-v2-q2_K
        std::strftime(buf, sizeof(buf), "%Y-%m-%dT%XZ",
                      &now_in_utc); // phind-codellama:34b-v2-q2_K

        // Use the buffer to construct a std::string
        std::string timeStr(buf); // phind-codellama:34b-v2-q2_K
        std::string text = "Now: " + timeStr +
                           "; ts: " + std::to_string(time_point_microseconds) +
                           "; Safstrom, Alexander";

        sharedMemory->unlock();

        cv::rectangle(img, cv::Point(50, 50), cv::Point(100, 100),
                      cv::Scalar(0, 0, 255));
        cv::putText(img, text, cv::Point(20, 50), 5, 0.5,
                    cv::Scalar(255, 255, 255));

        // If you want to access the latest received ground steering, don't
        // forget to lock the mutex:
        {
          std::cout << "v" << std::endl;
          ;
          std::lock_guard<std::mutex> lck(avrMutex);
          std::string angular_z_string =
              std::to_string(avr.angularVelocityZ()) +
              "\n"; // phind-codellama:34b-v2-q2_K
          std::ofstream ofs("/tmp/velocity.txt",
                            std::ios_base::app); // phind-codellama:34b-v2-q2_K
          ofs << angular_z_string;               // phind-codellama:34b-v2-q2_K
          ofs.close();

          /*

          std::cout << "main: groundSteering = " << gsr.groundSteering() <<
          std::endl;*/
        }
        {
          std::cout << "s" << std::endl;
          ;

          std::lock_guard<std::mutex> lck(gsrMutex);
          std::string steering_string = std::to_string(gsr.groundSteering()) +
                                        "\n"; // phind-codellama:34b-v2-q2_K
          std::ofstream ofs("/tmp/steering.txt",
                            std::ios_base::app); // phind-codellama:34b-v2-q2_K
          ofs << steering_string;                // phind-codellama:34b-v2-q2_K
          ofs.close();
        }
        {
          std::cout << "m" << std::endl;
          ;

          std::lock_guard<std::mutex> lck(magMutex);
          std::string magnetic_string =
              std::to_string(mag.magneticFieldX()) + ";" +
              std::to_string(mag.magneticFieldY()) + ";" +
              std::to_string(mag.magneticFieldZ()) +
              "\n"; // phind-codellama:34b-v2-q2_K
          std::ofstream ofs("/tmp/mag.txt",
                            std::ios_base::app); // phind-codellama:34b-v2-q2_K
          ofs << magnetic_string;                // phind-codellama:34b-v2-q2_K
          ofs.close();
        }
        {
          std::cout << "g" << std::endl;
          ;

          std::lock_guard<std::mutex> lck(geoMutex);
          std::string geo_string = std::to_string(geo.heading()) +
                                   "\n"; // phind-codellama:34b-v2-q2_K
          std::ofstream ofs("/tmp/geo.txt",
                            std::ios_base::app); // phind-codellama:34b-v2-q2_K
          ofs << geo_string;                     // phind-codellama:34b-v2-q2_K
          ofs.close();
        }
        {
          std::cout << "a" << std::endl;
          ;

          std::lock_guard<std::mutex> lck(accMutex);
          std::string acc_string = std::to_string(acc.accelerationX()) + ";" +
                                   std::to_string(acc.accelerationY()) + ";" +
                                   std::to_string(acc.accelerationZ()) +
                                   "\n"; // phind-codellama:34b-v2-q2_K
          std::ofstream ofs("/tmp/acc.txt",
                            std::ios_base::app); // phind-codellama:34b-v2-q2_K
          ofs << acc_string;                     // phind-codellama:34b-v2-q2_K
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
