variable "aws_region" {
  description = "AWS region used by the Terraform Option B deployment."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "IPv4 CIDR block for the Terraform-managed VPC."
  type        = string
  default     = "10.127.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "vpc_cidr must be a valid IPv4 CIDR block."
  }
}

variable "public_subnet_cidr" {
  description = "IPv4 CIDR block for the Terraform-managed public subnet."
  type        = string
  default     = "10.127.1.0/24"

  validation {
    condition     = can(cidrhost(var.public_subnet_cidr, 0))
    error_message = "public_subnet_cidr must be a valid IPv4 CIDR block."
  }
}

variable "availability_zone" {
  description = "Optional AWS Availability Zone for the public subnet. Leave null to let AWS select one."
  type        = string
  default     = null
}

variable "instance_type" {
  description = "EC2 instance type for the Terraform Option B deployment."
  type        = string
  default     = "t3.large"
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name used for SSH access."
  type        = string

  validation {
    condition     = trimspace(var.key_name) != ""
    error_message = "key_name must not be empty."
  }
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
  description = "Repository branch cloned by the EC2 bootstrap process for the laboratory."
  type        = string
  default     = "main"
}

variable "repo_url" {
  description = "Git repository URL used by the EC2 bootstrap process."
  type        = string
  default     = "https://github.com/irtaza400/exam-final-repo.git"
}
