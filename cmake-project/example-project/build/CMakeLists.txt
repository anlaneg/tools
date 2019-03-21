cmake_minimum_required(VERSION 3.5)
#project name  
PROJECT(example-project)

add_definitions("-Wall -lpthread -g")


#head file path
INCLUDE_DIRECTORIES(
../src/include/
)

#source directory
AUX_SOURCE_DIRECTORY(../src DIR_SRCS)
add_executable(example-project ../src/main/main.c)
