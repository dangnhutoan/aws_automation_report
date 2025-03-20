import unittest
from unittest.mock import patch, MagicMock
import script

class TestAWSReport(unittest.TestCase):
    @patch('script.boto3.Session')
    def setUp(self, mock_boto_session):
        """Setup mock AWS session"""
        self.mock_session = MagicMock()
        mock_boto_session.return_value = self.mock_session
        self.start_date = "2025-02-01"
        self.end_date = "2025-02-28"

    @patch('script.boto3.Session.client')
    def test_get_ec2_costs(self, mock_client):
        """Test EC2 cost retrieval"""
        mock_ce = MagicMock()
        mock_client.return_value = mock_ce
        mock_ce.get_cost_and_usage.return_value = {
            'ResultsByTime': [{
                'Groups': [{'Keys': ['t3.micro'], 'Metrics': {'NetAmortizedCost': {'Amount': '50.75'}}}]
            }]
        }
        costs = script.get_ec2_costs(self.mock_session, self.start_date, self.end_date)
        self.assertEqual(costs, {'t3.micro': 50.75})

    @patch('script.boto3.Session.client')
    def test_get_ebs_costs(self, mock_client):
        """Test EBS cost retrieval"""
        mock_ce = MagicMock()
        mock_client.return_value = mock_ce
        mock_ce.get_cost_and_usage.return_value = {
            'ResultsByTime': [{
                'Groups': [{'Keys': ['EBS:VolumeUsage.gp2'], 'Metrics': {'NetAmortizedCost': {'Amount': '15.30'}}}]
            }]
        }
        costs = script.get_ebs_costs(self.mock_session, self.start_date, self.end_date)
        self.assertEqual(costs, {'gp2': 15.30})

    @patch('script.boto3.Session.client')
    def test_get_snapshots_costs(self, mock_client):
        """Test Snapshot cost retrieval"""
        mock_ce = MagicMock()
        mock_client.return_value = mock_ce
        mock_ce.get_cost_and_usage.return_value = {
            'ResultsByTime': [{
                'Groups': [{'Keys': ['EBS:SnapshotUsage'], 'Metrics': {'NetAmortizedCost': {'Amount': '3.25'}}}]
            }]
        }
        costs = script.get_snapshots_cost(self.mock_session, self.start_date, self.end_date)
        self.assertEqual(costs, {'SnapshotUsage': 3.25})

    @patch('script.boto3.Session.client')
    def test_get_ec2_instances(self, mock_client):
        """Test EC2 instance retrieval"""
        mock_ec2 = MagicMock()
        mock_client.return_value = mock_ec2
        mock_ec2.describe_instances.return_value = {
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'i-1234567890',
                    'State': {'Name': 'running'},
                    'InstanceType': 't3.micro',
                    'Tags': [{'Key': 'Name', 'Value': 'WebServer'}],
                    'BlockDeviceMappings': [{'Ebs': {'VolumeId': 'vol-abcdef'}}]
                }]
            }]
        }
        data = script.get_ec2_instances(self.mock_session, {'t3.micro': 50.75})
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 'WebServer')
        self.assertEqual(data[0][1], 'i-1234567890')

    @patch('script.boto3.Session.client')
    def test_get_ebs_volumes(self, mock_client):
        """Test EBS volume retrieval"""
        mock_ec2 = MagicMock()
        mock_client.return_value = mock_ec2
        mock_ec2.describe_volumes.return_value = {
            'Volumes': [{
                'VolumeId': 'vol-abcdef',
                'VolumeType': 'gp2',
                'State': 'in-use',
                'Attachments': [{'InstanceId': 'i-1234567890'}]
            }]
        }
        data = script.get_ebs_volumes(self.mock_session, {'gp2': 15.30})
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 'vol-abcdef')
        self.assertEqual(data[0][4], 15.30)

    @patch('script.boto3.Session.client')
    def test_get_snapshots(self, mock_client):
        """Test snapshot retrieval"""
        mock_ec2 = MagicMock()
        mock_client.return_value = mock_ec2
        mock_ec2.describe_snapshots.return_value = {
            'Snapshots': [{
                'SnapshotId': 'snap-123abc',
                'VolumeId': 'vol-abcdef',
                'VolumeSize': 100,
                'State': 'completed',
                'Encrypted': True,
                'KmsKeyId': 'kms-xyz987',
                'Description': 'Daily Backup'
            }]
        }
        data = script.get_snapshots(self.mock_session, {'SnapshotUsage': 3.25})
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 'snap-123abc')
        self.assertEqual(data[0][1], 'vol-abcdef')
        self.assertEqual(data[0][2], 3.25)

if __name__ == '__main__':
    unittest.main()
