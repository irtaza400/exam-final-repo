resource "aws_instance" "terraform_option_b" {
  ami                         = data.aws_ssm_parameter.ubuntu_2404_amd64.value
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.terraform_option_b.id]
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
    Name       = "topic127-terraform-option-b"
    Purpose    = "Terraform Option B"
    BaseBranch = var.project_branch
  }
}
