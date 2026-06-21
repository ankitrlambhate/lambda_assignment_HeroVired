import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = 'vol-096b75463060935cf'

RETENTION_DAYS = 30

def lambda_handler(event, context):

    # Create snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=f'Automated snapshot for {VOLUME_ID}'
    )

    snapshot_id = snapshot['SnapshotId']

    ec2.create_tags(
        Resources=[snapshot_id],
        Tags=[
            {'Key': 'CreatedBy', 'Value': 'LambdaBackup'}
        ]
    )

    print(f"Created Snapshot: {snapshot_id}")

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    snapshots = ec2.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'tag:CreatedBy',
                'Values': ['LambdaBackup']
            }
        ]
    )

    deleted_snapshots = []

    for snap in snapshots['Snapshots']:

        if snap['StartTime'] < cutoff_date:

            ec2.delete_snapshot(
                SnapshotId=snap['SnapshotId']
            )

            deleted_snapshots.append(
                snap['SnapshotId']
            )

            print(f"Deleted Snapshot: {snap['SnapshotId']}")

    return {
        'created_snapshot': snapshot_id,
        'deleted_snapshots': deleted_snapshots
    }