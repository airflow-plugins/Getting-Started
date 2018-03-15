# Creating a hook

## Extending the HTTP Hook
If accessing a REST API, it's generally advisable to extend the HTTP Hook.

For our example, we'll be building a hook to access Github's API. While Github has a few community contributed Python SDKs, none are officially supported so we're going to just build our hook to access the API itself.

#### Note: The full plugin can be found [here](https://github.com/airflow-plugins/github_plugin).

First we're going to import the HttpHook class, which we'll be using as the base for our GithubHook.
```
from airflow.hooks.http_hook import HttpHook
```
Then we're going to instantiate our `GithubHook` class and extend the `__init__` function to first look for a token in the `extras` section of the specified Airflow connection on instantiation.

The [`get_connection`](https://github.com/apache/incubator-airflow/blob/master/airflow/hooks/base_hook.py#L76) method is used to retrieve to the connection fields.
```
class GithubHook(HttpHook):

    def __init__(self, github_conn_id):
        self.github_token = None
        conn_id = self.get_connection(github_conn_id)
```
We can use the [`extra_dejson`](https://github.com/apache/incubator-airflow/blob/master/airflow/models.py#L751) method, included as part of the Connection model, to parse the dictionary in the `extras` section and retrieve our `token`. Then we're going to inherit the `__init__` method from the `HttpHook` using `super()`.

```
        if conn_id.extra_dejson.get('token'):
            self.github_token = conn_id.extra_dejson.get('token')
        super().__init__(method='GET', http_conn_id=github_conn_id)
```

Because we want to build our hook to accept both Basic and Token Authentication, we're going to modify the existing [`get_conn`](https://github.com/apache/incubator-airflow/blob/master/airflow/hooks/http_hook.py#L33) method that is included in the `HttpHook` class.

If a dictionary exists in the `Extras` section of the specified  connection with key `token`, it is passed in the header with the appropriate authorization formatting and invalidates the `session.auth` which is created by default using the `username`/`password` (which here are not set).

```
    def get_conn(self, headers):
        if self.github_token:
            headers = {'Authorization': 'token {0}'.format(self.github_token)}
            session = super().get_conn(headers)
            session.auth = None
            return session
```
If the token is not found, the hook looks for a `username` and `password` in the respective connection fields.
```
        return super().get_conn(headers)
```

In either case, it is important to ensure your privacy
settings for your desired authentication method allow read access to user, org, and repo information.

## Extending the Base Hook
Coming soon...
