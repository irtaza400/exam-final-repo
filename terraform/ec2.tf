resource "aws_instance" "terraform_experiment" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnet.existing.id
  vpc_security_group_ids      = [aws_security_group.terraform_experiment.id]
  key_name                    = var.key_name
  associate_public_ip_address = true

  user_data = templatefile("${path.module}/user_data.tftpl", {
    repo_url    = var.repo_url
    repo_branch = var.project_branch
  })

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  root_block_device {
    volume_size           = var.root_volume_size
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  tags = {
    Name       = "topic127-terraform-experiment"
    Purpose    = "Terraform Option A"
    BaseBranch = var.project_branch
  }
}
