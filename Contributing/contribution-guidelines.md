# Contribution Guidelines

### Documentation
Please include a `README.md` with a description of what can be found in the plugin and all dependencies that should be included.

Within each plugin, a brief description of required fields, behavior to note, etc. should be included.
```
class GithubToS3Operator(BaseOperator):
    """
    Github To S3 Operator
    :param github_conn_id:           The Github connection id.
    :type github_conn_id:            string
    :param github_org:               The Github organization.
    :type github_org:                string
    :param github_repo:              The Github repository. Required for
                                     commits, commit_comments, issue_comments,
                                     and issues objects.
    :type github_repo:               string
    :param github_object:            The desired Github object. The currently
                                     supported values are:
                                        - commits
                                        - commit_comments
                                        - issue_comments
                                        - issues
                                        - members
                                        - organizations
                                        - pull_requests
                                        - repositories
    :type github_object:             string
    :param payload:                  The associated github parameters to
                                     pass into the object request as
                                     keyword arguments.
    :type payload:                   dict
    :param s3_conn_id:               The s3 connection id.
    :type s3_conn_id:                string
    :param s3_bucket:                The S3 bucket to be used to store
                                     the Github data.
    :type s3_bucket:                 string
    :param s3_key:                   The S3 key to be used to store
                                     the Github data.
    :type s3_key:                    string
    """
```

### Formatting

#### Imports
For consistency, please format your imports in the following order:
```
# Widely Available Packages -- if it's a core Python package or on PyPi, put it here.
from tempfile import NamedTemporaryFile
from dateutil.parser import parse
from flatten_json import flatten
import logging
import json

# Airflow Base Classes
from airflow.models import BaseOperator, SkipMixin
from airflow.utils.decorators import apply_defaults

# Airflow Extended Classes  
from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.http_hook import HttpHook

# Custom Modules
from anything import your_code
```

#### Tabs vs. Spaces
....we don't really care.

#### File Structure
Each hook and operator is kept in a separate file so that they can be easily reorganized without issue. In a typical plugin, you'll see the following structure.

```
├── my_awesome_plugin
├── __init__.py
├── operators
|   ├── my_first_operator.py
|   └── my_second_operator.py
├── hooks
|   ├── my_first_hook.py
|   ├── my_second_hook.py
|   └── my_third_hook.py
```

Each of these should then be imported into the top-level `__init__` and which will contain a single instance of the Airflow Plugins Manager.

```
from airflow.plugins_manager import AirflowPlugin

from my_awesome_plugin.operators.my_first_operator import MyFirstOperator
from my_awesome_plugin.operators.my_second_operator import MySecondOperator
from my_awesome_plugin.hooks.my_first_hook import MyFirstHook
from my_awesome_plugin.hooks.my_second_hook import MySecondHook
from my_awesome_plugin.hooks.my_third_hook import MyThirdHook


class my_awesome_plugin(AirflowPlugin):
    name = "my_awesome_plugin"
    operators = [MyFirstOperator, MySecondOperator]
    hooks = [MyFirstHook, MySecondHook, MyThirdHook]
    # Leave in for explicitness even if not using
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
```

### Schemas
Many of the plugins added involve moving data from one place to another. In cases where this data is going to be in a predictable structure (i.e. from a publicly available API like Stripe, Salesforce, Hubspot, etc.), it is best practice to include a schema in the plugin for each available endpoint. For the sake of simplicity, datatypes conforming to the [ANSI SQL](https://www.w3schools.com/sql/sql_intro.asp) standard are typically used.

See the schema mapping in the [Stripe Plugin](https://github.com/airflow-plugins/stripe_plugin/tree/master/schemas) for an example of how to organize the schemas.

### Licensing
As mentioned in the readme, all repos in the `airflow-plugins` org have an Apache 2.0 license. If a contribution is made with a stipulation that another license must be use, we will unfortunately be forced to decline.
