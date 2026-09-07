provider "aws" {
  region  = var.aws_region
  profile = "terraform"

  default_tags {
    tags = {
      Project     = "Topic127"
      Repository  = "exam-final-repo"
      Environment = "terraform-experiment"
      ManagedBy   = "Terraform"
    }
  }
}

data "aws_vpc" "existing" {
  id = var.vpc_id
}

data "aws_subnet" "existing" {
  id = var.subnet_id
}
