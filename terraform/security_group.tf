resource "aws_security_group" "terraform_option_b" {
  name        = "topic127-terraform-option-b"
  description = "Security group for the isolated Topic 127 Terraform Option B environment"
  vpc_id      = aws_vpc.topic127.id

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
    Name = "topic127-terraform-option-b-sg"
  }
}
