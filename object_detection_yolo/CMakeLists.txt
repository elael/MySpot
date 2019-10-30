cmake_minimum_required(VERSION 2.8.12)

project(object_detection_yolo)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(object_detection_yolo object_detection_yolo.cpp)
target_link_libraries(object_detection_yolo ${OpenCV_LIBS})
