cmake_minimum_required(VERSION 3.16)
project(qrunGenomeSMC)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -std=c++11 -Wall -Werror -Wno-ignored-attributes")

# Nlohmann JSON dependency
include(FetchContent)
FetchContent_Declare(json GIT_REPOSITORY https://github.com/ArthurSonzogni/nlohmann_json_cmake_fetchcontent GIT_TAG v3.9.1)
FetchContent_GetProperties(json)
if(NOT json_POPULATED)
    FetchContent_Populate(json)
    add_subdirectory(${json_SOURCE_DIR} ${json_BINARY_DIR} EXCLUDE_FROM_ALL)
endif()


INCLUDE_DIRECTORIES($ENV{HOME} $ENV{HOME}/qlibscapi/install/include
        $ENV{HOME}/qlibscapi/install/include)

set(SOURCE_FILES qApp.cpp src/qHamParties.cpp src/qmatrixDist.cpp include/etsi_qkd_004.hpp)


link_directories($ENV{HOME}/qlibscapi/install/lib)


add_executable(${PROJECT_NAME} ${SOURCE_FILES})

TARGET_LINK_LIBRARIES(${PROJECT_NAME}
        $ENV{HOME}/qlibscapi/libscapi.a gmp
        boost_system boost_thread pthread crypto dl ssl z rt nlohmann_json::nlohmann_json)



# Example executable
#add_executable(example_etsi_qkd_004 example.cpp etsi_qkd_004.hpp)
#target_link_libraries(example_etsi_qkd_004 PRIVATE nlohmann_json::nlohmann_json)
