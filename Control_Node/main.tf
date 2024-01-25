variable "username" {}
variable "email" {}

provider "aws" {
  region     = "eu-central-1"
}

resource "aws_vpc" "main" {
  cidr_block           = "11.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${var.username}-VPC"
  }
}

resource "aws_subnet" "web_subnet-1a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "11.0.8.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.username}-Public-Subnet"
  }
}

resource "aws_subnet" "db_subnet-1a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "11.0.16.0/24"
  availability_zone       = "eu-central-1a"

  tags = {
    Name = "${var.username}-Private-Subnet"
  }
}

resource "aws_subnet" "web_subnet-1b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "11.0.9.0/24"
  availability_zone       = "eu-central-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.username}-Public-Subnet"
  }
}

resource "aws_subnet" "db_subnet-1b" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "11.0.17.0/24"
  availability_zone       = "eu-central-1b"

  tags = {
    Name = "${var.username}-Private-Subnet"
  }
}

resource "aws_security_group" "web_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.username}-Security-Group"
  }
}

resource "aws_security_group" "db_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["11.0.16.0/24", "11.0.17.0/24"]
  }

  tags = {
    Name = "${var.username}-DB-Security-Group"
  }
}

resource "aws_instance" "web_instance_a1" {
  ami                    = "ami-04e601abe3e1a910f"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.web_subnet-1a.id
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name = "${var.username}-EC2-Instance-a1"
  }
}

resource "aws_instance" "web_instance_b1" {
  ami                    = "ami-04e601abe3e1a910f"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.web_subnet-1b.id
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.web_sg.id]

  tags = {
    Name = "${var.username}-EC2-Instance-b1"
  }
}

resource "aws_instance" "db_instance_a1" {
  ami                    = "ami-04e601abe3e1a910f"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.db_subnet-1a.id
  associate_public_ip_address = false
  vpc_security_group_ids = [aws_security_group.db_sg.id]

  tags = {
    Name = "${var.username}-DB-Instance-a1"
  }
}

resource "aws_instance" "db_instance_b1" {
  ami                    = "ami-04e601abe3e1a910f"
  instance_type          = "t2.micro"
  subnet_id              = aws_subnet.db_subnet-1b.id
  associate_public_ip_address = false
  vpc_security_group_ids = [aws_security_group.db_sg.id]

  tags = {
    Name = "${var.username}-DB-Instance-b1"
  }
}
 
resource "null_resource" "send_email" {
  depends_on = [
    aws_instance.web_instance_a1,
    aws_instance.web_instance_b1,
    aws_instance.db_instance_a1,
    aws_instance.db_instance_b1
  ]

  provisioner "local-exec" {
    command = "python3 /scripts/send_email.py '${aws_instance.web_instance_a1.public_ip}' '${aws_instance.web_instance_b1.public_ip}' '${aws_instance.db_instance_a1.public_ip}' '${aws_instance.db_instance_b1.public_ip}' '${var.email}'"
  }
}

