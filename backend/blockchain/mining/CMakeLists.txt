cmake_minimum_required(VERSION 3.10)
project(neutron_miner)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenSSL REQUIRED)
include_directories(${OPENSSL_INCLUDE_DIR})

add_executable(miner miner.cpp)
target_link_libraries(miner OpenSSL::SSL OpenSSL::Crypto)
