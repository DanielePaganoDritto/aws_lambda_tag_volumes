# aws_lambda_tag_volumes

Python Lambda Function than scans all the existing EBS volumes inside an AWS account tagging those than don't have a Name Tag with the name of the instance their attached to.


SNS Notifications
After every function run the template send an email to an SNS Topic containing a confirmation message for the execution.

For this to work is necessary to pass the Topic Arn and the AWS Account description to which send the notification by creating a test event before running the Lambda function. The test event should have the following structure:

 

{ "TopicArn": "arn:aws:sns::AccountNumber:TopicName", "AccountDescription": "Account_Name" }

 

IAM Role and Policy
To run the Lambda function you need to create/use an IAM Role with the following policies to interact with all the resources needed:

Role Name: AWSLambdaVolumesTaggingRole
Role Policy:
Policy 1 Name: Ec2-VolumestaggingPolicy
    -  "ec2:Describe*"
    -  "ec2:CreateTags"

Policy 2 Name: SNS-VolumesTaggingPolicy
    - "sns:Publish*"

** N.B The example ARN above refers to the Topic ARN to use for sending the SNS notification. Change it accordingly when creating the Lambda function on any different account. **