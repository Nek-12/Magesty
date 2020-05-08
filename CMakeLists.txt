cmake_minimum_required(VERSION 3.15)
project(ninja)
set(CMAKE_CXX_STANDARD 20)

set(GCC_COVERAGE_COMPILE_FLAGS "-municode -static -Wall -Wextra -Wfloat-equal -Wundef -Wcast-align -Wwrite-strings -Wlogical-op -Wredundant-decls -Wshadow -Woverloaded-virtual")

include_directories(include lib bin)

add_compile_definitions(SFML_STATIC)
set(SFML_STATIC_LIBRARIES TRUE)
set(SFML_DIR "./lib/cmake/SFML")

find_package(SFML 2.5 COMPONENTS system window graphics network audio REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")
add_executable(ninja main.cpp misc.h util.cpp Object.cpp Object.h)
target_link_libraries(ninja sfml-system sfml-window sfml-graphics sfml-network sfml-audio)
set( CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR} )