output "web_instance_a1_ip" {
  value = aws_instance.web_instance_a1.public_ip
}

output "web_instance_b1_ip" {
  value = aws_instance.web_instance_b1.public_ip
}

output "db_instance_a1_ip" {
  value = aws_instance.db_instance_a1.public_ip
}

output "db_instance_b1_ip" {
  value = aws_instance.db_instance_b1.public_ip
}

output "notification_email" {
  value = var.email
}

