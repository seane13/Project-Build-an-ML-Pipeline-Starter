import wandb

# Set these to your values if different
entity = "seane13-western-governors-university"
project = "nyc_airbnb"
artifact_name = "clean_sample.csv:reference"

api = wandb.Api()

try:
    artifact = api.artifact(f"{entity}/{project}/{artifact_name}", type="cleaned_data")
    print("Artifact found!")
    print(f"Artifact name: {artifact.name}")
    print(f"Aliases: {artifact.aliases}")
    print(f"Version: {artifact.version}")
    print(f"File names: {[f.name for f in artifact.files()]}")
except wandb.errors.CommError as e:
    print("Could not find artifact:", str(e))
except Exception as e:
    print("Error occurred:", str(e))
