import wandb

# Start a wandb run
run = wandb.init(project="nyc_airbnb", entity="seane13-western-governors-university", job_type="reference_data")

# Create and add your reference file
artifact = wandb.Artifact('clean_data.csv', type='dataset')
artifact.add_file('/Users/seanendicott/Documents/Education/WGU/ML-DevOps/Build-an-ML-Pipeline-starter/Project-Build-an-ML-Pipeline-Starter/data/clean_data.csv')


# Log the artifact with 'reference' alias
run.log_artifact(artifact, aliases=['latest', 'reference'])

# End the wandb run
run.finish()
