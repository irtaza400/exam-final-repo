resource "aws_vpc" "topic127" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "topic127-terraform-option-b-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.topic127.id
  cidr_block              = var.public_subnet_cidr
  availability_zone       = var.availability_zone
  map_public_ip_on_launch = true

  tags = {
    Name = "topic127-terraform-option-b-public-subnet"
  }
}

resource "aws_internet_gateway" "topic127" {
  vpc_id = aws_vpc.topic127.id

  tags = {
    Name = "topic127-terraform-option-b-igw"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.topic127.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.topic127.id
  }

  tags = {
    Name = "topic127-terraform-option-b-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
