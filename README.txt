Real-time Data Processing with Kafka and Docker
Name: Karan Chawla
Email: karanchawla@alumni.usc.edu

File Structure:
take_home
-- consumer.py
-- docker-compose.yml
-- README.txt

-- Steps to set up and run this project (For Mac):
1. Open a terminal on your machine

2. Verify that docker is installed on your machine using this command: docker --version

3. If Docker is installed, you will see output similar to: Docker version 20.10.17, build 100c701

4. If docker is not installed, install docker through this link: https://www.docker.com/products/docker-desktop/ for your system. 
I have performed this project on a Mac with apple silicon, so I have installed and worked with that version. 
Install it on your system and verify the installation using the command in step 2 and step 3.

5. Create a new project directory in the terminal using the command: mkdir take_home

6. Open this newly created directory using command: cd take_home

7. Use this command to create a new file named 'docker-compose.yml' : touch docker-compose.yml

8. Open the docker-compose.yml file using a text editor of your choice. I prefer using VScode, you may use that too. 

9. Add the content present in the docker-compose.yml in this repository to YOUR docker-compose.yml file

10. Save the docker-compose.yml file and run the following command in your terminal to start the services: docker-compose up -d
This command will download the necessary Docker images, create and start the containers in the background for Zookeeper, Kafka, and your data generator.
Alternatively, if the containers are already created:
- You can start the containers from the docker destop app by clicking on the "Play" button or using this command in the terminal to start all containers: docker start $(docker ps -aq)
- You can stop the containers from the docker destop app by clicking on the "Stop" button or using this command in the terminal to stop all containers: docker-compose stop

11. Use the following command to see the list of the running containers: docker ps
You should see entries for Zookeeper, Kafka, and the data generator.

12. Create the new Kafka topic. This ensures that the topic exists and is ready to receive the processed data from the consumer.
Use this command: docker exec -it take_home-kafka-1 kafka-topics --create --topic processed-topic --bootstrap-server localhost:29092 --replication-factor 1 --partitions 1
- This command will create a new Kafka topic named processed-topic with a replication factor of 1 and a single partition. 
- For local development, setting the replication factor to 1 and using a single partition simplifies the setup and reduces resource usage. 
- This makes debugging easier and avoids managing multiple replicas. 
- In production, we should increase the replication factor to 2 or 3 for high availability and use multiple partitions for scalability and parallel processing.

13. Verify the Topic Creation using this command: docker exec -it take_home-kafka-1 kafka-topics --list --bootstrap-server localhost:29092

14. Create a new python file consumer.py in your take_home folder. 
Add the content from the consumer.py in the repository to your new python file and save it. 

15. Pick a programming language of your choice. I have picked Python 3

16. (Optional) Open the terminal to create a new virtual environment. You should do this to isolate the dependencies. 
    Use the command : 
    python3 -m venv test_env
    source test_env/bin/activate

    To Deativate the virtual environment after completion of the project, use the command:
    deactivate
    rm -rf test_env

17. Install the required Kafka library using : pip3 install kafka-python OR pip install kafka-python

18. Now Start the Kafka consumer using this command: python3 consumer.py OR python consumer.py

19. The logs show that the consumer:
- Successfully connects to the Kafka broker.
- Subscribes to the user-login topic.
- Receives data messages.
- Processes each message by extracting relevant information.
- Sends processed data to the processed-topic.

20. Stop the program gracefully by entering this in the terminal: (Ctrl+C)

21. Stop the active containers and remove them using the command: docker-compose down. Refer to Alternate instructions in step 10 to Stop containers without removing them completely.

22. consumer.py:
- This script sets up a Kafka consumer to read messages from the 'user-login' topic, where it's configured to start from the earliest available offset to ensure we don't miss any data. 
- As messages come in, the script processes each one, converting timestamps into a more readable format and extracting key information. 
- To showcase how we might derive insights in real-time, it logs any users who are using app version 2.3.0. 

- After processing, the script uses a Kafka producer to send the transformed data to a new topic called 'processed-topic'. 
- There is error handling to manage any hiccups in message processing, and we use JSON for serialization. 
- To make the project robust, I've implemented graceful shutdown handling and added logging for debugging and monitoring.


Additional Questions:
1. How would you deploy this application in production?
- I'd go with Kubernetes for orchestration since it's good for managing containerized apps at scale. 
- We'd want to set up a solid CI/CD pipeline using Jenkins or GitHub Actions to automate our testing and deployment. 
- For Kafka, I'd recommend a managed service like AWS or Confluent.

2. What other components would you want to add to make this production ready?
- We need robust authentication and access control. 
- Data backup and recovery is a must. 
- Auto-scaling is a good idea to handle traffic spikes. 
- Unit and integration testing would be a good addition.

3. How can this application scale with a growing dataset?
- Partitioning is key here - we can increase Kafka topic partitions to spread the load. 
- Using consumer groups will let us process data in parallel. 
- We should horizontally scale our services - Kubernetes would be ideal for this. 
- For really large datasets, we might want to look at cloud storage solutions like Amazon S3 or Google Cloud Storage. 
- If we need more processing power, integrating with something like Apache Flink could be worth exploring.