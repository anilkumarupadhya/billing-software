#!/usr/bin/env python3
import boto3
import sys
import time

def modify_ebs_volume():
    """
    Modify an existing EBS volume attached to an EC2 instance.
    Prompts for AWS account ID, profile, region, instance ID, volume ID, and new size in GiB.
    """

    print("=== EC2 EBS Volume Resize Script ===")

    # Input details
    aws_account_id = input("Enter AWS Account ID (e.g., 835776289100): ").strip()
    profile = input("Enter AWS profile (e.g., spring-prod): ").strip()
    region = input("Enter AWS region (e.g., us-west-2): ").strip()
    instance_id = input("Enter EC2 Instance ID (e.g., i-00b9cb3bbe0e9e952): ").strip()
    volume_id = input("Enter Volume ID (e.g., vol-1234567890abcdef0): ").strip()

    # Prompt for new volume size
    while True:
        try:
            new_size = int(input("Enter new volume size in GiB (e.g., 40): ").strip())
            if new_size <= 0:
                print("Volume size must be a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for volume size.")

    # Initialize boto3 session
    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        ec2 = session.client("ec2")
    except Exception as e:
        print(f"Error initializing AWS session: {e}")
        sys.exit(1)

    # Modify the EBS volume
    try:
        print(f"\nModifying volume {volume_id} attached to instance {instance_id} "
              f"in account {aws_account_id} to {new_size} GiB in {region}...")
        response = ec2.modify_volume(
            VolumeId=volume_id,
            Size=new_size
        )
        print("\nModification request submitted successfully:")
        print(response)

        # Poll for volume modification status
        print("\nWaiting for volume modification to complete...")
        for attempt in range(40):  # ~20 minutes max if sleep=30
            mods = ec2.describe_volumes_modifications(VolumeIds=[volume_id])
            mod_state = mods["VolumesModifications"][0]["ModificationState"]
            progress = mods["VolumesModifications"][0].get("Progress", 0)

            print(f"Attempt {attempt+1}: State = {mod_state}, Progress = {progress}%")

            if mod_state in ["completed", "failed"]:
                break
            time.sleep(30)

        if mod_state == "completed":
            print("\n✅ Volume modification completed successfully!")
        elif mod_state == "failed":
            print("\n❌ Volume modification failed. Check AWS console for details.")
        else:
            print("\n⚠️ Modification is still in progress. Check again later.")

    except Exception as e:
        print(f"\nError while modifying volume: {e}")
        sys.exit(1)

if __name__ == "__main__":
    modify_ebs_volume()

