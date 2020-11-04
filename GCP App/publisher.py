from google.cloud import pubsub_v1

# TODO(developer)
project_id = GCP_PROJECT
topic_id = TOPIC_ID

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

topic = publisher.create_topic(request={"name": topic_path})

print("Created topic: {}".format(topic.name))