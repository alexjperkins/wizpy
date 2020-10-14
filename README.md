# WizPy: A wizard for all

The wizard of all wizards. WizPy aims to help developers turn classes
and functions into a custom wizard, that walks the user through parameter
gathering and execution.

This is a WIP - use at your own risk.


### Using WizPy

The wizpy is designed to be used with class definitions of an `API`. The API should be stateless,
meaning it shouldn't be instantiated and thus regular methods on the class won't show in the wizard.
The API class essentially will act as a thin wrapper around a group of functions, this allows the
wizard to group functions into menus.

In the future, the wizard may be accepting of instantiated classes, however this was a design choice t
keep the codebase consistent and opinionated, rather than implementation difficulties.

In must be said that both type annotations and succinct docstrings greatly improve the user
experience when using the wizard, and as such are highly recommended through the codebase.
To check typing, please use the `mypy` package or similar.


#### Registering

To register an API class to the wizard use the `register_wizard` decorator:

```
import boto3

from wizard import register_wizard


@register_wizard
class SageMakerAPI:

    @classmethod
    def list_endpoints(cls):
        cli = boto3.client('sagemaker')
        return cli.list_endpoints()
```

The `register_wizard` decorator can take a parameter that defines which functions in the class definition 
will be visible to the wizard by default, this is called `description`. If no parameters are passed as above
then ALL functions will be visible

Please NOTE: that the API defined here only contains a `classmethod`. Only these methods can be used with
wizard for now - this is a design decision to avoid having to instantiate and provide config to API instances.

If regular methods do indeed become required, such that the class needs to be instantiated, and gains enough support, then this can change and be raised as a feature.

#### Adding descriptions to parameters

This all works great, but what if the user of the wizard has no knowledge about the param they're suppose to pass?

Well a description can be added with the following decorator: `add_parameter_description`
This decorator takes two args and one optional keyword

```
import boto3

from wizard import register_wizard


@register_wizard
class SageMakerAPI:

    @classmethod
    def list_endpoints(cls):
        cli = boto3.client('sagemaker')
        return cli.list_endpoints()

    @classmethod
    @add_parameter_description(
        parameter="endpoint_name",
        description="this is the endpoint_name: it requires a string"
    )
    def update_endpoint(cls, endpoint_name, endpoint_config_name):
        # do something
```

This will now add a description to the wizard as it instructs the user to input a value for this arg


#### Adding default values to parameters

As mentioned above, there is the option to pass in an optional keyword argument to this decorator: `options`
This is to define what values the wizard can choose from, it can either be a list of values or a callback function.

```
import boto3

from wizard import register_wizard


def list_endpoint_config_names_view():
    cli = boto3.client('sagemaker')
    return cli.list_endpoint_configs()  # [config_1, config_2,... config_n]


@register_wizard
class SageMakerAPI:

    @classmethod
    def list_endpoints(cls):
        cli = boto3.client('sagemaker')
        return cli.list_endpoints()

    @classmethod
    @add_parameter_description(
        parameter="endpoint_config_name",
        description="this is the endpoint_name: it requires a string",
        options=list_endpoint_config_names_view

    )
    def update_endpoint(cls, endpoint_name, endpoint_config_name):
        # do something
```

NOTE: The callback function must return either a `List, Dict or str`.
