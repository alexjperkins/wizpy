# ~ Verv Scripts ~

### Setup & Requirements

- python3.8
- awscli
- aws credentials in your env

```
# activate virtual env and python path

	$ python -m venv venv && . ./venv/bin/activate && ./venv/bin/pip install -r ./requirements.txt
	$ export PYTHONPATH=$PYTHONPATH:$PWD
```

This script requires for the python virtual enviroment to be active ( this is recommend over installing python packages globally )
This script pulls AWS credentials via the environment, this means that the credentials must be exported in order for
the script to pull them and connect external to aws. These credentials are as follows:

AWS_SECRET_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_SESSION_TOKEN (Optional - only required if not using an IAM)

To get these credentials, the quickest way is to go to `https://verv.awsapps.com/start#/` and login.
From there you should see numerous different AWS accounts that you can enter into the console for. Clicking on 
one you should see two options (for each access level eg AdministratorAccess, VERV_Product etc).
Click the option `Command line or programmatic access` and finally over Option 1, you should now have the
command to export these to your env. Go ahead and do so.

NOTE: These credentials will expire after 12 hours

Alternatively use the credentials associated to an IAM. Contact `alex.p@verv.energy` or `simon.h@verv.energy` to create one for
you if you do not know how to yourself - please mention the account, access-level you need and that you require programmatic access only


## Scripts

NOTE: all scripts are located at `verv-scripts/scripts`; these are the entrypoints into defined sevices

## Sagemaker


### Requirements

Please ensure you have read the above Setup & Requirements otherwise these scripts do NOT work

All of the below jsons must be constructed by yourself, there are examples you can use as templates located at the following:
`./verv-scripts/fixtures`

For different accounts you will ideally want to construct these JSONs, since certain params will be different for
different accounts.

These files can live anywhere you please, they are passed by reference to the scripts and act as a configuration 

It is recommended that you use an IDE when creating or editing JSON as to make your life easier,
if you're not familar with IDEs then a recommendation would be either of the following:

`https://atom.io/`
`https://www.sublimetext.com/`

If you're also not familar with the the syntax of JSON a good start is here:

`https://www.digitalocean.com/community/tutorials/an-introduction-to-json`

To verfiy your JSON files syntax and format, you can check that here:

`https://jsonlint.com/`

Now that you're happy with the concept of JSON, you can start to construct your own. A short guide is below:

NOTE: all values enclosed with angle braces (`<>`) are there to be interpolated. Please edit these values.
      all values encloses in just quotation marks (`""`) please leave as is - these will act as default values

```
# container.json
{
	"Image": "<full-uri-to-ecr-image>",
	"Mode": "SingleModel"
}
```
Image: The Full URI to the Docker Image located in ECR - this can found either using the aws console under the `ECR` service header
       or if skilled with the command line using the awscli command line tool and the ECR api
Mode: The Sagemaker mode (single model or multi model - use single model for now unless you're experimenting)

For further information and options see: `https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_model` look specifically at the `PrimaryContainer` argument since that is what this json file is populating.
 

```
# vpc.json
{
	"SecurityGroupIds": [
		"<security-group-id>"
	],
	"Subnets": [
		"<subnet-id-1>",
		...
		"<subnet-id-n>"
	]
}
```
SecurityGroupIds: The ID of the security group you would like to use

These values can be found in the AWS console under the EC2 service. Under `Network & Security` on the LHS you should see `Security Groups`.
This header will list all security groups on that account - you will most likely want the security group that has `sagemaker` in the name.
The id will look something along the lines of: `sg-0f941257979940573`

Subnets: The list of subnet IDs you would like to use - please use more than one, 3 is preferable

These values can be found in the AWS console under the VPC service. Under `Virtual Private Cloud` on the LHS you should see `Subnets`
This will list all the subnets on that account - you want all 3 subnets. Collect the IDs for each one.
The id will look something like: `subnet-f1dfb798`

NOTE: On some accounts there could be more than 3 subnets: in that case please contact `alex.p@verv.energy` or `simon.h@verv.energy`
      for help; mention that you would like help gathering the correct subnets for a Sagemaker change via the scripts (switcheroo)

```
# variant.json
{
	"VariantName": "<variant-name>",
	"InitialInstanceCount": 2,
	"InstanceType": "ml.t2.medium",
}
```

VariantName: The name of the variant - this is arbitary really, is must be unique and without underscores ( `_` )
IntialInstanceCount: The number of instances (containers running in parallel)
InstanceType: The size of type of each instances (think compute)

More information on possible options here can be found at: 
`https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_endpoint_config`
You will want to look at the argument `ProductionVariants`. The script uses the JSON as this parameter. The script is currently setup
to only use one ProductionVariant, so do not worry about enclosing in a list

Now you should be ready to run the scripts: A full definition is given below.


### Switcheroo

For this you probably will only want to call the update endpoint script:

`./verv-scripts/sagemaker/update-existing-endpoint.sh`

A full guide on how to use is given below under the `API Definition`


### API Defintion

### TL/DR

Glossary:

model: The sagemaker definiton of the model, this contains all model logic via a path the Docker Image on ECR and vpc information
endpoint config: The configuration that an endpoint will use; contains the instance size, type and more
endpoint: The endpoint itself, this is configured by an endpoint config

Scripts:
```
	create-endpoint.sh: Creates an endpoint given an existing endpoint config
	create-model-and-endpoint-from-config.sh: Creates a model, endpoint config and an endpoint (fullstack)
	create-model-with-endpoint-config.sh: Creates a model and a endpoint config (but not the endpoint)
	list-existing-endpoint-configs.sh: Lists existing endpoint configs
	update-existing-endpoint.sh: Updates an existing endpoint with a new model (endpoint config)
```

### Detailed

#### Create Model, Endpoint Config & Endpoint

This will given a tarbell, upload it to s3 in the bucket name provided, with the
key equal to that of the model name. Once uploaded, it will create a model definition
in Sagemaker with the container definition (container.json), this will include a path to
the model Image on ERC, this also requires the vpc setup and used the vpc config (vpc.json)

Following this, an endpoint config can the be created using a primary variant definition
(variant.json)

And finally an endpoint is created. The name of the endpoint and endpoint config will
be created from the model name

```
    $ ./create-model-and-endpoint-from-config.sh <model-tarbell-path> <bucket-name> 
         <model-name> <container.json> <vpc.json> <execution-role-arn> <primary-variant.json>

    or

    Example:
    $ ./create-model-and-endpoint-from-config.sh \
    	../../artifacts/cnn/belt_tension.tar.gz \
	test-bucket \
	cnn-belt-tension-11 \
        ../../fixtures/cnn/container.json \
	../../fixtures/cnn/vpc.json \
	arn:aws:iam::xx5448893890:role/service-role/AmazonSageMaker-ExecutionRole-x0200xx3T092946 \
	../../fixtures/cnn/endpoint_variants/cnn-belt-tension.json 
```

model-tarbell-path: the local path to the tarbell
bucket-name: the s3 bucket name (those from the python world; underscores are not allowed - aws restriction)
model-name: the name of the model
execution-role-arn: the sagemaker execution arn; this is found in the AWS console in the IAM service, under roles
    or one may use the awscli or boto.client('iam') service to search and find.

There are 3 json files that are required for this script:
  - container.json
  - vpc.json
  - primary-variant.json

See the requirements header for more detail

NOTE: These files can be called absolutely anything, there are NO checks; simply point the script
to them

 Examples of these can be found under `verv-scripts/fixtures/cnn/`.
 The code is setup up currently to only use one variant and this will
 be the de facto primary variant

 More detailed information can be found at the following page:

 `https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html`

 see the functions: `create_model, create_endpoint_config, create_endpoint`


#### Create model & endpoint config

This difference between this step and the above is that this doesn't go all the way and create the
endpoint as well - this just creates the model given a local tarbell path in s3 and the endpoint config in
sagemaker

```
    $ ./create_model_with.sh <model-tarbell-path> <bucket-name> 
         <model-name> <container.json> <vpc.json> <execution-role-arn> <primary-variant.json>

    or
    
    Example:
    $ ./create-model.sh \
   	 ../../artifacts/cnn/belt_tension.tar.gz \
	 test-bucket \
	 cnn-belt-tension-1 \
	 ../../fixtures/cnn/container.json \
         ../../fixtures/cnn/vpc.json \
	 arn:aws:iam::xx5448893890:role/service-role/AmazonSageMaker-ExecutionRole-xx201513T092947 \
	 ../../fixtures/cnn/endpoint_variants/cnn-belt-tension.json
```

See above for more detail on the args required.


#### Create Endpoint


Creates a new endpoint, provided the endpoint config already exists.

If the endpoint config doesn't exist, then follow the instructions or `Create model & endpiont config`

```
	$ ./create-endpoint.sh <desired_endpoint_name> <existing_endpoint_config_name>
```


#### List Endpoint Configs

As simple as the name suggests
```
	$ ./list-existing-endpoint-configs.sh
```


#### Update Existing Endpoint

Updates an existing endpoint with an existing endpoint config

NOTE: the endpoint config must already exist in Sagemaker, if it doesn't please call the `Create model & endpoint config` script.
      To check available endpoint configs you make look in the AWS console under the sagemaker service and then `Endpoint Config`,
      Alternatively you can you the script: `List Endpoint Config`

```
	$ ./update-existing-endpoint.sh <existing-endpoint-name> <existing-endpoint-config-name>
```

This will update `existing-endpoint-name` to have the config of `existing-endpoint-config-name`


#### Testing Sagemaker Endpoint

```
	$ ./test-endpoint-runtime.sh <endpoint-name> <test-binary-file-path> <source-id> <timestamp (ISO formatted)>
```

endpoint-name: the name of the endpoint one would like to test
test-binary-file-path: the path to a binary file of source data to test with
source-id: the serial number of the source (arbitary really)
timestamp: timestamp - must be ISO formatted
