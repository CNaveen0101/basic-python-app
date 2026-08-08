provider "aws" {
    region = "ap-south-1"
  
}

resource "aws_iam_user" "terrefiamuser" {
    name = "Developer1"  

    tags = {
      name = "Developerlabelpurpose"
      Environment = "Dev"
    }
}

resource "aws_iam_user_login_profile" "terrefuserlogin" {
    user = aws_iam_user.terrefiamuser.name
    password_length = 16
    password_reset_required = "true"
  
}
resource "aws_iam_access_key" "terrefaccesskey" {
    user = aws_iam_user.terrefiamuser.name
    status = "Active"  
}

resource "aws_iam_role" "terrefrole" {
  name = "test_role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    tag-key = "newrole"
  }
}



