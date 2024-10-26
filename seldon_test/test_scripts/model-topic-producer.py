from confluent_kafka import Producer

import create_infer
from google.protobuf.json_format import MessageToJson, Parse

from v2_dataplane_pb2 import ModelInferRequest

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Kafka configuration
conf = {
    'bootstrap.servers': '127.0.0.1:9092',  # Kafka broker
}

# Create Producer instance
producer = Producer(**conf)

# Produce a message
topic = 'seldon.default.model.iris-hehe.inputs'
json_message = '{"id":"dolphin1234", "inputs":[{"name":"zxc","contents":{"fp32_contents":[1.5,2,3,4]},"datatype":"FP32","shape":[1,4]}]}'
# id: "dolphin1234" could be x-request-id, not sure. But it sure is included in the response, can be used for tracing

"""Key: null
Partition: 0
Offset: 6
Headers:
  - seldon-pipeline-errors: iris-hehe <<<--- this is the model name
  - traceparent: 00-9aede12ed3a7faf4bb3c0bf381bca14d-6ec599aad03b4a30-01
Value:
rpc error: code = Internal desc = builtins.ValueError: cannot reshape array of size 3 into shape (1,4)
"""


# req = create_infer.model_req
req = ModelInferRequest() # dont have to manually create the object. We should parse the json message to the object
Parse(json_message, req)

message = req.SerializeToString()

producer.produce(topic, message, callback=delivery_report)
# Wait up to 1 second for events. Callbacks will be invoked during
# this method call if the message is acknowledged.
producer.poll(1)

# Wait for any outstanding messages to be delivered and delivery reports
# to be received.
producer.flush()


    