from email.policy import default
from constructs import Construct
from aws_cdk import (
    Duration,
    CfnOutput,
    Stack,
    CustomResource,
    aws_iot as iot,
    aws_iam as iam,
    aws_timestream as timestream,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions
)
import aws_cdk as cdk
import logging


class FeedmyfurbabiesPipelineCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)

        cat_feeder_thing_lambda_action_topic_name = cdk.CfnParameter(self, "CatFeederThingLambdaActionTopicName", type="String", default="cat-feeder/action")
        cat_feeder_thing_controller_states_topic_name = cdk.CfnParameter(self, "CatFeederThingControllerStatesTopicName", type="String", default="cat-feeder/states")

        iot_database = timestream.CfnDatabase(self, "IoT",
                                          database_name="IoT"
                                         )

                                         
        cat_feeders_states_table = timestream.CfnTable(
            self, "CatFeedersStates",
            database_name=iot_database.database_name,
            table_name="catFeedersStates",
            retention_properties={
                "memoryStoreRetentionPeriodInHours": "24",
                "magneticStoreRetentionPeriodInDays": "7"
            }
        )

        cat_feeders_states_table.add_dependency(iot_database)




        cat_feeders_states_iot_rule_role = iam.Role(
            self, "CatFeedersStatesIoTRuleRole",
            assumed_by=iam.ServicePrincipal("iot.amazonaws.com")
        )

        cat_feeders_states_timestream_describe_endpoints_policy = iam.PolicyStatement(
            actions=[
                "timestream:DescribeEndpoints"
            ],
            resources=["*"]  
        )

        cat_feeders_states_timestream_write_records_policy = iam.PolicyStatement(
            actions=[
                "timestream:WriteRecords"
            ],
            resources=[f"arn:aws:timestream:{self.region}:{self.account}:database/{iot_database.database_name}/table/{cat_feeders_states_table.attr_name}"]
        )
       
        cat_feeders_states_iot_rule_role.add_to_policy(cat_feeders_states_timestream_describe_endpoints_policy)
        cat_feeders_states_iot_rule_role.add_to_policy(cat_feeders_states_timestream_write_records_policy)





        cat_feeders_states_iot_rule = iot.CfnTopicRule(
            self, "CatFeedersStatesRule",
            rule_name="CatFeedersStatesTimestreamRule",
            topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                rule_disabled=False,
                sql=f"SELECT food_capacity FROM '{cat_feeder_thing_controller_states_topic_name.value_as_string}'",
                actions=[
                    iot.CfnTopicRule.ActionProperty(
                        timestream=iot.CfnTopicRule.TimestreamActionProperty(
                            database_name=iot_database.database_name,
                            table_name=cat_feeders_states_table.attr_name,
                            role_arn=cat_feeders_states_iot_rule_role.role_arn,
                            dimensions=[
                                iot.CfnTopicRule.TimestreamDimensionProperty(
                                    name="device_location",
                                    value="${device_location}"
                                )
                            ]
                        )
                    )
                ]
            )
        )







        cat_feeders_actions_table = timestream.CfnTable(
            self, "CatFeedersActions",
            database_name=iot_database.database_name,
            table_name="catFeedersActions",
            retention_properties={
                "memoryStoreRetentionPeriodInHours": "24",
                "magneticStoreRetentionPeriodInDays": "7"
            }
        )

        cat_feeders_actions_table.add_dependency(iot_database)



        cat_feeders_actions_iot_rule_role = iam.Role(
            self, "CatFeedersActionsIoTRuleRole",
            assumed_by=iam.ServicePrincipal("iot.amazonaws.com")
        )

        cat_feeders_actions_timestream_describe_endpoints_policy = iam.PolicyStatement(
            actions=[
                "timestream:DescribeEndpoints"
            ],
            resources=["*"]  
        )

        cat_feeders_actions_timestream_write_records_policy = iam.PolicyStatement(
            actions=[
                "timestream:WriteRecords"
            ],
            resources=[f"arn:aws:timestream:{self.region}:{self.account}:database/{iot_database.database_name}/table/{cat_feeders_actions_table.attr_name}"]
        )
       
        cat_feeders_actions_iot_rule_role.add_to_policy(cat_feeders_actions_timestream_describe_endpoints_policy)
        cat_feeders_actions_iot_rule_role.add_to_policy(cat_feeders_actions_timestream_write_records_policy)





        cat_feeders_actions_iot_rule = iot.CfnTopicRule(
            self, "CatFeedersActionsRule",
            rule_name="CatFeedersActionsTimestreamRule",
            topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                rule_disabled=False,
                sql=f"SELECT event FROM '{cat_feeder_thing_lambda_action_topic_name.value_as_string}'",
                actions=[
                    iot.CfnTopicRule.ActionProperty(
                        timestream=iot.CfnTopicRule.TimestreamActionProperty(
                            database_name=iot_database.database_name,
                            table_name=cat_feeders_actions_table.attr_name,
                            role_arn=cat_feeders_actions_iot_rule_role.role_arn,
                            dimensions=[
                                iot.CfnTopicRule.TimestreamDimensionProperty(
                                    name="event_source",
                                    value="${event_source}"
                                )
                            ]
                        )
                    )
                ]
            )
        )


