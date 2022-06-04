import argparse

from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, IntegerType, FloatType, ShortType, DoubleType
from pyspark.sql import functions as f
from pyspark.sql import Window as w

parser = argparse.ArgumentParser()
parser.add_argument("--broker", help="IP:Port of the kafka broker to which attempt connection.")
parser.add_argument("--intopic", help="Name of the topic from which consume data.")
parser.add_argument("--outtopic", help="Name of the topic on which output data should be produced.")

args = parser.parse_args()

if args.broker :
    kafkaBroker=args.broker
else :
    raise TypeError('(--broker) A Kafka broker must be specified as an IP:PORT pair.')

if args.intopic :
    inputTopic=args.intopic
else :
    raise TypeError('(--intopic) An input topic must be specified.')

if args.outtopic :
    outputTopic=args.outtopic
else :
    raise TypeError('(--outtopic) An output topic must be specified.')

print('Kafka entry point:', kafkaBroker)
print('Fetching raw input data from topic:', inputTopic)
print('Writing processed data to topic:', outputTopic)

# From groupedDF we process the differences into diffDF -> AnomalyScore
# The difference is calculated by perfoming an euclidean distance between the mean of speed and RPM of a lap
# and the mean of speed and RPM of the previous lap
def forEachBatchFunc(dataFrame, batchID) :

    print('Batch: ', batchID)

    windowSpec = w.orderBy('LapIdx')

    diffDF = dataFrame.select(

        f.pow(dataFrame['avg(Speed)'] - f.lag(dataFrame['avg(Speed)'], 1, 0.0)  \
                .over(windowSpec), 2).alias('diff(Speed)'),
        f.pow(dataFrame['avg(RPM)'] - f.lag(dataFrame['avg(RPM)'], 1, 0.0)      \
                .over(windowSpec), 2).alias('diff(RPM)'),
        dataFrame['LapIdx']
    )

    distDF = diffDF.select(

        f.sqrt(diffDF['diff(Speed)'] + diffDF['diff(RPM)']).alias('AnomalyScore'),
        dataFrame['LapIdx']
    )

    # Writing to the kafka topic
    distDF.select(f.to_json(f.struct('AnomalyScore', 'LapIdx')) \
        .alias('value')).selectExpr('CAST(value AS STRING)')    \
        .write \
        .format('kafka') \
        .option('kafka.bootstrap.servers', kafkaBroker) \
        .option('topic', outputTopic) \
        .save()

    # printing on console (TO REMOVE)
    distDF.show()
##########################################################################################################

spark = SparkSession.builder.appName('StructuredNaiveAnomalyDetection').getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

# Defining the data schema: the structure of the data published on the kafka topic
dataSchema = StructType([
    StructField("RPM", IntegerType()),
    StructField("Speed", FloatType()),
    StructField("nGear", ShortType()),
    StructField("Throttle", FloatType()),
    StructField("Time", DoubleType()),
    StructField("X", FloatType()),
    StructField("Y", FloatType()),
    StructField("LapIdx", ShortType())])

# Subscribe to the kafka topic
rawDF = spark.readStream.format('kafka')                \
        .option('kafka.bootstrap.servers', kafkaBroker) \
        .option('subscribe', inputTopic)                \
        .option('startingOffsets', 'latest').load()

# Convert the dict (kafka data stored in rawDF) into a row for the spark dataframe
parsedDF = rawDF.selectExpr('CAST(value AS STRING)')    \
        .select(f.from_json(f.col('value'), dataSchema) \
        .alias('value')).select(f.col('value.*'))   

# Get the Speed and RPM from the row and calculate the mean
inputDF = parsedDF.select('Speed', 'RPM', 'LapIdx')
groupedDF = inputDF.groupBy('LapIdx').mean('Speed', 'RPM').orderBy('LapIdx')

# Launch stream-processing in a background thread.
# Trigger processing of batch i as soon as processing of batch i-1 has ended.
# Additional processing on grouped table is performed in forEachBatchFunc() function.
# forEachBatchFunc() function writes the resulting table on a kafka topic.
query = groupedDF.writeStream.outputMode('complete').foreachBatch(forEachBatchFunc).start()

query.awaitTermination()
