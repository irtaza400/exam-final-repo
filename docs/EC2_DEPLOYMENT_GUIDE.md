# EC2 Deployment Guide — Terraform Option B

## Purpose

Terraform Option B provisions the complete AWS deployment foundation for the Topic 127 laboratory.

```text
Terraform
   ↓
AWS VPC
   ↓
Public Subnet
   ↓
Internet Gateway + Route Table
   ↓
Security Group
   ↓
EC2 / Ubuntu
   ↓
Docker Compose + Host-side Python
```

## Prerequisites

- AWS credentials with permission to create the required EC2/VPC resources
- Terraform 1.16 or newer
- An existing EC2 key pair in the selected AWS region
- The corresponding private `.pem` key
- Your current public IPv4 address in `/32` CIDR notation

## 1. Clone the repository

```bash
git clone https://github.com/irtaza400/exam-final-repo.git
cd exam-final-repo/terraform
```

## 2. Configure local Terraform variables

Create the local variables file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Set the environment-specific values in `terraform.tfvars`:

```text
key_name   = "YOUR_EC2_KEY_PAIR_NAME"
admin_cidr = "YOUR.PUBLIC.IP.ADDRESS/32"
```

Do not commit `terraform.tfvars`.

## 3. Validate and provision

```bash
terraform init
terraform validate
terraform plan -out=option-b.tfplan
terraform apply option-b.tfplan
```

Terraform creates the VPC, public subnet, Internet Gateway, public route table, route table association, Security Group and EC2 instance.

## 4. Connect to the Terraform-created EC2 instance

Get the public IP:

```bash
terraform output -raw public_ip
```

Connect using the existing private key:

```bash
ssh -i /path/to/project_key.pem ubuntu@$(terraform output -raw public_ip)
```

## 5. Verify automatic bootstrap

After the first SSH login, wait for cloud-init to complete:

```bash
cloud-init status --wait
```

Expected:

```text
status: done
```

The Terraform EC2 bootstrap automatically clones the repository `main` branch and installs the required Python, Docker and Docker Compose environment.

## 6. Run the Topic 127 laboratory

From the automatically cloned repository on the EC2 instance:

```bash
cd ~/exam-final-repo
bash ./scripts/run_exam_demo.sh
```

This is the primary examiner workflow. It validates the repository, starts Docker services, runs the complete laboratory workflow, executes the controlled security demonstrations, and generates evidence and reports.

## 7. External and internal endpoints

Terraform Option B permits external administrator access only to:

```text
22    SSH
3000  Grafana
1881  FUXA
```

The following endpoints are used internally by the EC2-hosted laboratory and are not opened by the Terraform Security Group for external administrator access:

```text
1883  Mosquitto MQTT
8086  InfluxDB
4840  OPC-UA
5020  Modbus
```

## 8. Cleanup

When the laboratory or examination session is finished:

```bash
exit
cd /path/to/exam-final-repo/terraform
terraform plan
terraform destroy
terraform state list
```

After destruction, the Terraform state should contain no managed resources.

## 9. Architecture boundary

Terraform provisions the AWS infrastructure layer. The Topic 127 application remains the existing Docker Compose and host-side Python laboratory.

Terraform Option B does not imply Kubernetes, EKS, ECS, multi-node high availability, or other future cloud-native capabilities.
