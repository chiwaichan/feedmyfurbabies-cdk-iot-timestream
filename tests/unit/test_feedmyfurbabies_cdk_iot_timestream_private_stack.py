import aws_cdk as core
import aws_cdk.assertions as assertions
from feedmyfurbabies_cdk_iot_timestream_private.feedmyfurbabies_cdk_iot_timestream_private_stack import FeedmyfurbabiesCdkIotTimestreamPrivateStack


def test_sqs_queue_created():
    app = core.App()
    stack = FeedmyfurbabiesCdkIotTimestreamPrivateStack(app, "feedmyfurbabies-cdk-iot-timestream-private")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = FeedmyfurbabiesCdkIotTimestreamPrivateStack(app, "feedmyfurbabies-cdk-iot-timestream-private")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
