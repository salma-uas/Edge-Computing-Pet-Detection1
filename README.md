# Dog/Cat detector

## Project Summary:

This is a project of cloud computing to build a solution for detecting DOG/CAT on a Sensor node and send the detection data to a Cluster (Here Kubernetes Cluster).
Along with the DOG/CAT detection application in the sensor node, this project includes several mini-applications on the Kubernetes Cluster which are:

1. Data storage to store images
2. Data Storage to store capture-related data
3. RestAPI to accept and store data in the database
4. Frontend to visualize the summary of the collected data
5. Telegram Bot to send notifications if any DOG/Cat is detected
