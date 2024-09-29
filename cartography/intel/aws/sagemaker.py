import boto3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_sagemaker_notebooks_info(region='us-east-1'):
    """
    Fetches information about SageMaker notebook instances and extracts the region from the ARN.
    """
    session = boto3.Session(region_name=region)
    sagemaker_client = session.client('sagemaker')

    logging.info("Fetching list of SageMaker notebook instances...")
    print("Fetching list of SageMaker notebook instances...")

    try:
        response = sagemaker_client.list_notebook_instances()
        notebooks = response.get('NotebookInstances', [])
        
        if not notebooks:
            logging.warning("No SageMaker notebooks found.")
            print("No SageMaker notebooks found.")
            return []

        notebook_details = []
        
        for notebook in notebooks:
            notebook_instance_name = notebook['NotebookInstanceName']
            logging.info(f"Fetching details for notebook: {notebook_instance_name}")
            print(f"Fetching details for notebook: {notebook_instance_name}")

            notebook_details_response = sagemaker_client.describe_notebook_instance(
                NotebookInstanceName=notebook_instance_name
            )

            is_public = notebook_details_response.get('DirectInternetAccess') == 'Enabled'
            ec2_instance_type = notebook_details_response.get('InstanceType')
            creator_arn = notebook_details_response.get('NotebookInstanceArn')

            # Extract region from the ARN
            notebook_arn = notebook_details_response.get('NotebookInstanceArn')
            region_from_arn = notebook_arn.split(":")[3]  # Extract the region part from ARN

            notebook_info = {
                'Notebook Name': notebook_instance_name,
                'Is Public': is_public,
                'EC2 Instance Type': ec2_instance_type,
                'Owner': creator_arn,
                'Region': region_from_arn  # Include the extracted region
            }
            
            notebook_details.append(notebook_info)

            # Print notebook details in the desired format
            print(f"Notebook Name: {notebook_info['Notebook Name']}")
            print(f"Is Public: {notebook_info['Is Public']}")
            print(f"EC2 Instance Type: {notebook_info['EC2 Instance Type']}")
            print(f"Owner: {notebook_info['Owner']}")
            print(f"Region: {notebook_info['Region']}")
            print("-" * 40)

    except Exception as e:
        logging.error(f"Error fetching SageMaker notebook instances: {str(e)}")
        print(f"Error fetching SageMaker notebook instances: {str(e)}")
        return []

    return notebook_details

def get_sagemaker_studio_info(region):
    """
    Fetches information about SageMaker Studio notebooks using the provided region.
    """
    session = boto3.Session(region_name=region)
    sagemaker_client = session.client('sagemaker')

    logging.info("Fetching list of SageMaker Studio notebooks (apps)...")
    print("Fetching list of SageMaker Studio notebooks (apps)...")

    try:
        response = sagemaker_client.list_apps()
        apps = response.get('Apps', [])

        if not apps:
            logging.warning("No SageMaker Studio notebooks found.")
            print("No SageMaker Studio notebooks found.")
            return []

        studio_notebook_details = []

        for app in apps:
            app_name = app['AppName']
            logging.info(f"Fetching details for Studio notebook: {app_name}")
            print(f"Fetching details for Studio notebook: {app_name}")

            app_type = app.get('AppType', 'Unknown')
            domain_id = app.get('DomainId', 'Unknown')
            user_profile_name = app.get('UserProfileName', 'Unknown')

            app_info = {
                'App Name': app_name,
                'App Type': app_type,
                'Domain ID': domain_id,
                'User Profile Name': user_profile_name,
            }
            
            studio_notebook_details.append(app_info)

            # Print Studio notebook details in the desired format
            print(f"App Name: {app_info['App Name']}")
            print(f"App Type: {app_info['App Type']}")
            print(f"Domain ID: {app_info['Domain ID']}")
            print(f"User Profile Name: {app_info['User Profile Name']}")
            print("-" * 40)

    except Exception as e:
        logging.error(f"Error fetching SageMaker Studio notebooks: {str(e)}")
        print(f"Error fetching SageMaker Studio notebooks: {str(e)}")
        return []

    return studio_notebook_details


# NOTE: The following main function is included for testing and understanding purposes only.
if __name__ == "__main__":
    # Fetch notebook instances
    print("### SageMaker Notebook Instances ###")
    notebooks_info = get_sagemaker_notebooks_info()
    
    # Extract the region from the first notebook's info, if available
    region = notebooks_info[0]['Region'] if notebooks_info else 'us-east-1'

    # Fetch Studio notebooks using the extracted region
    print("\n### SageMaker Studio Notebooks ###")
    studio_info = get_sagemaker_studio_info(region)
    print(studio_info)

    
