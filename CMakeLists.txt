cmake_minimum_required(VERSION 3.2)
project(helloworld)
set(CMAKE_CXX_STANDARD 11)
set (CMAKE_CXX_COMPILE_FEATURES "-Wall --coverage -fprofile-arcs -ftest-coverage")
set(SOURCES src/helloworld.cpp src/PrimeChecker.cpp src/TestPrimeChecker.cpp)
add_executable(${PROJECT_NAME} ${CMAKE_CURRENT_SOURCE_DIR}/src/helloworld.cpp ${CMAKE_CURRENT_SOURCE_DIR}/src/PrimeChecker.cpp)

enable_testing()
add_executable(${PROJECT_NAME}-Runner ${CMAKE_CURRENT_SOURCE_DIR}/src/TestPrimeChecker.cpp ${CMAKE_CURRENT_SOURCE_DIR}/src/PrimeChecker.cpp)
add_test(NAME ${PROJECT_NAME}-Runner COMMAND ${PROJECT_NAME}-Runner)

add_custom_target(coverage
    COMMAND ./helloworld
    DEPENDS ./helloworld
    COMMAND ./helloworld-Runner
    DEPENDS ./helloworld-Runner
    COMMAND gcov ${SOURCES}
    COMMAND lcov --directory ./build --capture --output-file coverage.info
    COMMAND lcov --list coverage.info
)
