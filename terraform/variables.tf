variable "aws_region" {
  description = "AWS region used by the Terraform experiment."
  type        = string
  default     = "us-east-1"
}

variable "vpc_id" {
  description = "Existing VPC ID to reuse. Terraform does not create or manage this VPC."
  type        = string
  default     = "vpc-05f48cac498c5a1d3"
}

variable "subnet_id" {
  description = "Existing subnet ID to reuse. Terraform does not create or manage this subnet."
  type        = string
  default     = "subnet-0a5124faa4548ffb6"
}

variable "ami_id" {
  description = "Verified Ubuntu 24.04 LTS amd64 AMI in us-east-1."
  type        = string
  default     = "ami-0f8a61b66d1accaee"
}

variable "instance_type" {
  description = "EC2 instance type for the Terraform experiment."
  type        = string
  default     = "t3.large"
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name."
  type        = string
  default     = "project_key"
}

variable "root_volume_size" {
  description = "Encrypted gp3 root volume size in GiB."
  type        = number
  default     = 30

  validation {
    condition     = var.root_volume_size >= 8
    error_message = "root_volume_size must be at least 8 GiB."
  }
}

variable "admin_cidr" {
  description = "IPv4 CIDR allowed to access SSH, Grafana, and FUXA. Use your public IP as /32."
  type        = string

  validation {
    condition     = can(cidrhost(var.admin_cidr, 0))
    error_message = "admin_cidr must be a valid IPv4 CIDR block."
  }
}

variable "project_branch" {
  description = "Repository branch cloned by the EC2 bootstrap process."
  type        = string
  default     = "terraform-experiment"
}

variable "repo_url" {
  description = "Git repository URL used by the EC2 bootstrap process."
  type        = string
  default     = "https://github.com/irtaza400/exam-final-repo.git"
}
