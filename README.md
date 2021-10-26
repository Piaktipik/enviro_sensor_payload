# UAV Sensor Payload

This repository contains an implementation of a remote sensing payload intended to be mounted on an Unmanned Aerial Vehicle. This was created with the aim of assisting research paper at the Queensland University of Technology.

## Hardware Requirements

* [Enviro+ Air Quality Sensor Board](https://shop.pimoroni.com/products/enviro?variant=31155658457171)

* [Raspberry Pi (3b / 4)](https://core-electronics.com.au/raspberry-pi-3-model-b.html)

## Software Requirements

* [ROS Noetic](http://wiki.ros.org/noetic) - Robot Operating System

* [enviroplus-python](https://github.com/pimoroni/enviroplus-python) - Python library to interface with sensor board

## Contents

The [sensor_payload](https://github.com/stebucur/enviro_sensor_payload/tree/main/sensor_payload) folder contains the ROS package.

The publisher and subscriber can be found within the [scripts](https://github.com/stebucur/enviro_sensor_payload/tree/main/sensor_payload/scripts) folder

The [sensors_standalone.py](https://github.com/stebucur/enviro_sensor_payload/blob/main/sensors_standalone.py) script is a standalone implementation of the sensor board, designed to run without ROS.

## Topic

**/sensor_data** is the topic created that sends lux data at a rate of 1Hz.
