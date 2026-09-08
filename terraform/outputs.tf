output "vpc_id" {
  description = "ID of the Terraform-created VPC."
  value       = aws_vpc.topic127.id
}

output "subnet_id" {
  description = "ID of the Terraform-created public subnet."
  value       = aws_subnet.public.id
}

output "internet_gateway_id" {
  description = "ID of the Terraform-created Internet Gateway."
  value       = aws_internet_gateway.topic127.id
}

output "route_table_id" {
  description = "ID of the Terraform-created public route table."
  value       = aws_route_table.public.id
}

output "instance_id" {
  description = "ID of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_option_b.id
}

output "instance_name" {
  description = "Name tag of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_option_b.tags["Name"]
}

output "public_ip" {
  description = "Public IPv4 address of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_option_b.public_ip
}

output "private_ip" {
  description = "Private IPv4 address of the Terraform-created EC2 instance."
  value       = aws_instance.terraform_option_b.private_ip
}

output "security_group_id" {
  description = "ID of the Terraform-created security group."
  value       = aws_security_group.terraform_option_b.id
}

output "ssh_command" {
  description = "Generic SSH command for connecting to the new EC2 instance."
  value       = "ssh -i <path-to-your-private-key.pem> ubuntu@${aws_instance.terraform_option_b.public_ip}"
}
