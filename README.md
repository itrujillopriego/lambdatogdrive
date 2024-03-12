# lambdatogdrive
This repo is a quick proof of concept for how to run a lambda s3 trigger that uploads a file to google drive upon having a new "object" on the s3 bucket. 


The libraries needed for this project are AWS boto3 and google-api . For your convenienve a requirements.txt file is provided with all packages needed to be installed with specific versions that have been tested to work together. 

You will need to have python 3 (3.12 recommened) and pip installed in your computer 

To test this project 

Create a virtual environment 
python3 -m venv lambda  # you can replace lambda for whichevere name you want 
source lambda/bin/activate 

Install dependencies 
pip install requirements.txt


After you have installed all dependenices, you will need to create a GCP project , enable the Drive api, create a service account and associtated keys for the account to be used to interface with google-api.

You will need to add the .json credentials files to this directory and add the path to that file in the index.py file

Lastly, the script expect you to add a "folder id" which is the id of the google drive folder where the upload will occur. 

Once you have done all of the above, you will need to package your code . You can use .zip or wheel . 

To use .zip you can follow the instructions in this link :
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-dependencies

The next step (or you can do this before hand) will be to create a lambda function and associate it with the S3 bucket you want to set the triger for . 
You can follow this tutorial to setup the lambda function https://docs.aws.amazon.com/lambda/latest/dg/with-s3-example.html
