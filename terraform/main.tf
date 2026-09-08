provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "Topic127"
      Repository  = "exam-final-repo"
      Environment = "terraform-option-b"
      ManagedBy   = "Terraform"
    }
  }
}

data "aws_ssm_parameter" "ubuntu_2404_amd64" {
  name = "/aws/service/canonical/ubuntu/server/24.04/stable/current/amd64/hvm/ebs-gp3/ami-id"
}
