### Overview

This app is acts as a preprocessing component for an EDR backend that reads submissions from sensors, validates them and publishes that data. It was completed as part of a job application and was my first experience working with AWS and my first attempt at writing python code, on my own, from scratch.

### Usage

To make the program run, from the root of the repository run the following command line (NB: the program was developed in a MacOs environment and has not been tested on other systems):

`python3 main.py arg1 arg2`

arg1 represents the number of messages to read from the queue at a time (min = 1, max = 10)
arg2 represents the duration those messages should be visible after being received (min = 0, max = 43200) (time in seconds)

The program will run without displaying any information and will stop running once the queue is empty. It can be stopped at any time with a simple `ctrl-c` interrupt

### Project Requirements

The telemetry data submitted by the sensors used JSON format. It includes a unique identifier, a device identifier, a timestamp and two lists of events. The program ensures that all this information is present and valid. Any submissions containing invalid or missing data will not be published to the output stream. All events are grouped in the context of the original submission in that output stream, and submissions are always deleted after they have been successfully published.

Furthermore, a requirement of the project was that the number of messages read and their visibility timeout could be configured by the user. This can be done via the command line input described above.

### What I learned and things to improve

Given that this was my first attempt at python programming with AWS, I learned a lot in the short space of time I was given for this project, and there are certainly some things to improve.

Primarily, two main points of improvement come to mind:

Firstly, I would like to have spent a bit more time expanding upon and refining my validation process. There are a lot of tools for analysing strings within Python, and it is a language which makes traversing JSON data very simple. What I have implemented provides a basic checking process and the irrelevant data is being dropped, but this could be made a lot more robust.

Secondly, I would like to have given some more attention to the formatting of the data which is ultimately being pushed to the kinesis stream. At present, the valid telemetry is being pushed without making any changes.

A couple of other minor points of improvement would be to add key-detection to allow the user to quit the program without having to interrupt. Also, some visual feedback in the standard output regarding what the program is doing as it runs would be nice.

Unfortunately, my lack of experience with AWS and Python meant it took a lot of time to organise how to get the program to communicate properly with the SQS and Kinesis API's. This left little time to focus on the above two areas. Regardless, I'm proud of what I have managed to learn and accomplish in this project.
