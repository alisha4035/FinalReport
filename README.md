# FinalReport-CDK to build a Software Delivery Pipeline (Step by Step Instructions)

Preparation:

To deploy a SW Delivery Pipeline using CDK, you will need the following resources:

•	AWS CLI (We will be using Cloud9, so AWS CLI is already installed)
•	AWS account and associated credentials (We are using Cloud9 so we should already have this)

 Steps:
 
1.	Log into your AWS account and navigate to AWS Cloud9. Select create environment to set up a virtual environment using AWS Cloud9.
•	Add the name- cdk-swdeliverypipeline
•	Environment type- New EC2 instance
•	Instance Type: m5.large 
•	Platform: Amazon Linux 2023
•	Connection: AWS systems Manager
•	Click Create 

2.	It will take a couple of minutes for AWS to set up the new environment.



3.	Open the cloud9 environment once it is successfully created. We will first prepare the working environment.

•	Ensure the latest security updates and bug fixes are installed.
sudo yum -y update

•	Install Node Version Manage, for installing Node.js later using the following command:

nvm --version (To check/confirm) 
nvm install node (If not found)

•	Install the AWS CDK using the following command:
cdk --version (To check/confirm)
npm install -g aws -cdk (If not found)

•	Use command below to bootstrap to ensure dedicated S3 buckets and other containers are available to AWS CloudFormation during deployment:
cdk bootstrap aws://ACCOUNT-NUMBER/REGION

4.	Ensure you have pipenv installed in your environment. To install, enter the following command:
pip install pipenv

5.	Now, we will create the CDK app

•	Use the following command to create a project directory. Then, navigate to that directory
mkdir sw-pipeline
cd sw-pipeline

•	Then, enter the following command to initialize the app:
cdk init app --language python

•	Now, activate the app’s Python virtual environment and install the AWS CDK core dependencies by entering the following command:
source .venv/bin/activate
python -m pip install -r requirements.txt.

6.	Once the activation is successful, edit your sw_pipeline_stack.py file and add the code listed under the sw_pipeline_stack.py file. Also, upload your Java-Project.zip file to your sw_pipeline folder.

7.	After updating the code as mentioned above, synthesize the cdk configuration files from the existing code using the following command:
cdk synth

8.	Upon successful synthetization, a new folder named cdk.out will be created which contains your JSON configuration files.

9.	Now deploy your application using the following command:
 cdk deploy

10.	Once your application is successfully deployed, validate that all resources were created, and the pipeline was properly built.

11.	After ensuring everything works properly, make sure you delete all resources you’ve created to avoid unnecessary charges.


