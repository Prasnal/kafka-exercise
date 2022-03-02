### How to run the project?
 1. Fill the csv file `producer/input.csv` with urls (you can also use default links that are already in the file)
 2. In the main directory, run `docker-compose up --build`
 3. Wait until producer_1 finishes
 4. Check output file available in `consumer` directory

### How to run tests?
1. Create virtual env `python3 -m venv venv`
2. Run virtual env `source venv/bin/activate`
3. Install requirements `pip install -r requirements.txt` both from consumer and producer
4. Run pytest (in consumer and producer dir) by using commend `pytest tests_consumer.py` or `pytest tests_producer.py`

### Additional suggestions and improvements:
- It's possible to add more zookeeper and kafka instances if needed
- In case of bigger project I would use separated repos for consumer and producer
- Saving in file in consumer could be done async as well
- Async kafka client can be used to improve performance
- Start fetching next url right after one is 
finished without waiting for the whole batch would be also 
possible to improve performance
- In normal project, in the Docker files, instead of sleep 
I would wait until kafka is ready


Regarding task about Trimming the oldest queue entries if queue size balloons -
I've set up KAFKA_LOG_RETENTION_BYTES to 200MB, so if the queue reach this size
kafka will remove the oldest messages.
