#-----26/07/2019-----#
#--- Script for update the volume tags in which is missing, with instance name tag---
#!/usr/bin/env python
 
import boto3
 
ec2 = boto3.resource('ec2')
ec2client = boto3.client('ec2')

 
#-----Define Lambda function-----#
def lambda_handler(event, context):
 
#-----Check& filter Instances which  Kloud_managed equal true-----#
    instances = ec2client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['*']}])
 
#-----Define dictionary to store Tag Key & value------#
    dict={}
 
#-----Store Key & Value of Instance Tag:“Name” ------#
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
           for tag in instance['Tags']: 
                if tag['Key'] == 'Name':
                    print ( instance['InstanceId'],tag['Value'])
                    dict[instance['InstanceId']]= tag['Value']
         
    #List all the existing volumes
    volumes = ec2.volumes.all()
    
    #Scan the list of volumes
    for volume in volumes:
        
        for a in volume.attachments:
                for key, value in dict.items():
                    if a['InstanceId'] == key:
                        
                        #Filter the volumes without any tag
                        if not volume.tags:
      
                            #Add name Tag to volume
                            volume.create_tags(Tags=[{'Key': 'Name', 'Value': value}])
                            
                        #Check all the volumes that have tags
                        elif volume.tags:
                            for tag in volume.tags:
                                #if Name tag exist but has no value
                                if tag['Key'] == 'Name' and tag['Value'] == '':
                                    volume.create_tags(Tags=[{'Key': 'Name', 'Value': value}])
                                #of tag name doesn't exits
                                if not tag['Key'] == 'Name':
                                    volume.create_tags(Tags=[{'Key': 'Name', 'Value': value}])
                                    
    #Prepare SNS message 
    SFCAccount=event['AccountDescription'] 
    message = ("Volume Tagging Lambda executed for account: %s" % SFCAccount) 
    subject = ("Lambda Function - Volumes tagging function executed for account %s" % SFCAccount) 
     
    #Send notification     
    sns.publish(TopicArn=event['TopicArn'], Message=(message), Subject=(subject))