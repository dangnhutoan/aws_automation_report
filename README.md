# AWS Cost Report Generator (Version 1.1.2)

## Overview

This script retrieves AWS cost data for EC2 instances, EBS volumes, and snapshots. It generates an Excel report with three sheets:

- **EC2\_Cost\_Report**: Details about EC2 instances and their costs.
- **EBS\_Cost\_Report**: Details about EBS volumes and their costs.
- **Snapshots\_Cost\_Report**: Details about snapshots, associated volumes, and estimated costs.

## Requirements

- Python 3.x
- AWS CLI configured with the appropriate credentials
- Required Python libraries:
  ```sh
  pip install boto3 openpyxl
  ```

## Usage

```sh
python aws_cost_report.py --profile <aws-profile> --region <aws-region>
```

## Sample Output

### EC2\_Cost\_Report Sheet

| EC2 Instance Name | EC2 Instance ID | EC2 Instance State | EC2 Instance Cost |
| ----------------- | --------------- | ------------------ | ----------------- |
| WebServer         | i-1234567890    | running            | 50.75             |
| DBServer          | i-0987654321    | stopped            | 30.20             |

### EBS\_Cost\_Report Sheet

| EBS Volume ID | EBS Volume Name | EBS Volume Cost |
| ------------- | --------------- | --------------- |
| vol-abcdef123 | DatabaseVolume  | 15.30           |
| vol-xyz987654 | BackupVolume    | 5.45            |

### Snapshots\_Cost\_Report Sheet

| Snapshot ID | Volume ID  | Snapshot Cost | Full Snapshot Size | Description   | Snapshot Status | Encryption | KMS Key ID |
| ----------- | ---------- | ------------- | ------------------ | ------------- | --------------- | ---------- | ---------- |
| snap-123abc | vol-abcdef | 3.25          | 100 GB             | Daily Backup  | completed       | True       | kms-xyz987 |
| snap-456def | vol-xyz789 | 2.10          | 50 GB              | Weekly Backup | pending         | False      | N/A        |

## Changelog

### Version 1.1.2

- Updated cost metric to `NetAmortizedCost`.
- Added function to retrieve snapshots and associated volume IDs.
- Retrieved snapshot costs from AWS Cost Explorer instead of using assumed costs.
- Added `Snapshots_Cost_Report` sheet to the Excel output.
- Included snapshot details: Full Snapshot Size, Volume Size, Description, Snapshot Status, Encryption, and KMS Key ID.

### Version 1.1.1

- Improved snapshot report by adding full snapshot size, volume size, description, snapshot status, encryption, and KMS Key ID.

### Version 1.1.0

- Added function to retrieve snapshots and associated volume IDs.
- Calculated monthly cost for each snapshot.
- Created a new sheet `Snapshots_Cost_Report` in the Excel output.

### Version 1.0.0

- Initial release with EC2 and EBS cost reporting.

## License

This project is licensed under the MIT License.

