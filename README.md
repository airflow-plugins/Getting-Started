# Getting Started with Airflow Plugins

## Table of Contents
A full list of available plugins can be found [here](https://github.com/airflow-plugins/Getting-Started/blob/master/table-of-contents.md).
Generally one repo is made per plugin with related operators and hooks are grouped together in one plugin when possible.

## Hello, World.
Tutorials can be found in the `Tutorials` folder. Example tutorials currently available include:
- [Creating a Hook](https://github.com/airflow-plugins/Getting-Started/blob/master/Tutorial/creating-hook.md)
- [Creating an Operator](https://github.com/airflow-plugins/Getting-Started/blob/master/Tutorial/creating-operator.md)
- [Adding UI Modifications](https://github.com/airflow-plugins/Getting-Started/blob/master/Tutorial/creating-ui-modification.md)

## Google Authentication
Because Google Cloud Platform's authentication requires a keyfile for a service account, accessing tools like BigQuery from a containerized environment (without persistent local storage) can be somewhat complex. The GCP Base Hook solves this in Airflow 1.9 by allowing the contents of the keyfile to be put in an Airflow connection object but, for those still using 1.8 and lower, we've put together [a quick tutorial](Tutorial/gcp_example/README.md) on how to used modified hooks to as a workaround.

## Contributions
If you have a plugin that you've built or nefariously acquired (no judgement), we'd be more than happy to have it added to the org. General guidelines for how to get your plugin into shape can be found [here](https://github.com/airflow-plugins/Getting-Started/blob/master/Contributing/contribution-guidelines.md).

## Example DAGs
All example DAGs that use the plugins can be found in the [Example Airflow DAGs](https://github.com/airflow-plugins/Example-Airflow-DAGs) repo.

## License
Unless otherwise specified, everything in the airflow-plugins org is by default licensed under Apache 2.0. This was chosen to follow suit with the core Apache Airflow project.
