resource "aws_security_group" "terraform_experiment" {
  name        = "topic127-terraform-experiment"
  description = "Security group for the isolated Topic 127 Terraform experiment"
  vpc_id      = data.aws_vpc.existing.id

  ingress {
    description = "SSH administration"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  ingress {
    description = "Grafana web interface"
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  ingress {
    description = "FUXA HMI web interface"
    from_port   = 1881
    to_port     = 1881
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  egress {
    description = "Allow outbound access required for package installation and lab operation"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "topic127-terraform-experiment-sg"
  }
}
