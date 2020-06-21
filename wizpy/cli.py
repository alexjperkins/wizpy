from aws.sagemaker.api import SageMakerAPI
from aws.s3.api import S3API
from display.console import prettyprint
from wizard.handler import WizardHandler


ROUTER = {
    "sagemaker": {
        "create-fullstack": SageMakerAPI.create_fullstack,
        "create-model": SageMakerAPI.create_model_and_endpoint_config,
        "create-endpoint": SageMakerAPI.create_endpoint,
        "update-endpoint": SageMakerAPI.update_existing_endpoint,
        "list": SageMakerAPI.list_endpoint_configs
    },
    "s3": {
        "create-bucket": S3API.create_bucket,
        "toggle-event": S3API.toggle_bucket_lambda_event,
    },
    "wizard": WizardHandler,
}

if __name__ == "__main__":
    import sys
    service = sys.argv[1]
    try:
        operation, *args = sys.argv[2:]
    except ValueError:
        if service == 'wizard':
            try:
                WizardHandler.handle()
            except KeyboardInterrupt:
                sys.exit(-1)

        if service == 'help':
            prettyprint(
                "Available services: "
            )
            prettyprint(list(ROUTER.keys()))

        else:
            prettyprint(
                f"Please provide at least: \n"
                f"Service: the service to use\n"
                f"Operation: the service operation to call\n"
                f"\nService options are as follows:"
            )
            prettyprint(list(ROUTER.keys()))
    else:
        api = ROUTER.get(service, {"fallback": "service did not exist"})
        callback = api.get(operation, lambda *x: "Cannot find operation")
        execution = callback(*args)

        print(
            f"Calling: {callback} from {api}...",
            execution
        )
