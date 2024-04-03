import json
import boto3
import uuid
import datetime

client = boto3.client('polly')
s3 = boto3.client('s3')

def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v1_description(event, context):
    body = {
        "message": "TTS api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v2_description(event, context):
    body = {
        "message": "TTS api version 2."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response




def lambda_generate_audio(event, context):
    
    json_data = json.loads(event['body'])
    phrase = json_data["phrase"]
    
    response = client.synthesize_speech(
        Text=phrase,
        VoiceId='Joanna',
        OutputFormat="mp3"
    )

    body = response['AudioStream'].read()
    
    unique_name = str(uuid.uuid4())
    file_name = f"{unique_name}.mp3"
    response = s3.put_object(Body=body,Bucket="generatedaudiopolly2",Key=file_name)
    
    # Montar o URL do objeto no bucket S3
    audio_url = f"https://generatedaudiopolly2.s3.amazonaws.com/{file_name}"

    body = {
                "received_phrase": phrase,
                "url_to_audio": audio_url,
                "created_audio": datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
    
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    