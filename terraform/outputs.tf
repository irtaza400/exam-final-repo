output "instance_id" {
  description = "ID of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_experiment.id
}

output "instance_name" {
  description = "Name tag of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_experiment.tags["Name"]
}

output "public_ip" {
  description = "Public IPv4 address of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_experiment.public_ip
}

output "private_ip" {
  description = "Private IPv4 address of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_experiment.private_ip
}

output "security_group_id" {
  description = "Terraform-created security group ID."
  value       = aws_security_group.terraform_experiment.id
}

output "ssh_command" {
  description = "Generic SSH command for connecting to the new EC2 instance."
  value       = "ssh -i <path-to-project_key.pem> ubuntu@${aws_instance.terraform_experiment.public_ip}"
}
