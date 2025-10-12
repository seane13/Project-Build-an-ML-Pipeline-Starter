import wandb

# --- CONFIGURE THESE VARIABLES ---
project_name = "nyc_airbnb"           # Your W&B project name
artifact_name = "trainval.csv"        # The file and artifact name
artifact_type = "trainval_data"       # Artifact type
artifact_desc = "Train/validation data for model training"  # Artifact description
# ----------------------------------

run = wandb.init(project=project_name, job_type="upload_trainval")
artifact = wandb.Artifact(artifact_name, type=artifact_type, description=artifact_desc)
artifact.add_file(artifact_name)
run.log_artifact(artifact)
run.finish()

print(f"Uploaded {artifact_name} to W&B project '{project_name}' as type '{artifact_type}'")
