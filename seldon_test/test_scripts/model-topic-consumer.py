from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from v2_dataplane_pb2 import ModelInferResponse
from google.protobuf.json_format import MessageToJson

def consume_messages(broker, group, topics):
    # Consumer configuration
    conf = {
        'bootstrap.servers': broker,
        'group.id': group,
        'auto.offset.reset': 'latest'#'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(conf)

    # Subscribe to topics
    consumer.subscribe(topics)

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f'{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}')
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Proper message
                res = ModelInferResponse()
                res.ParseFromString(msg.value())
                # print(f'Received message: {msg.value().decode("utf-8")}')
                # print(f'Parsed message: {res}')
                # print(f'shape tensor: {res.outputs[0].shape}')
                # print(f"json: {json.dumps(res)}") # error
                json_res = MessageToJson(res)
                print(f"json: {json_res}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'Exception: {e}')
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

if __name__ == "__main__":
    broker = '127.0.0.1:9092'
    group = 'my-consumer-group'
    topics = ['seldon.default.model.iris-hehe.outputs']

    consume_messages(broker, group, topics)