provider "aws" {
    region = "ap-south-2"
  
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

resource "aws_iam_user_policy_attachment" "terrefpasswordchangepolicy" {
    user = aws_iam_user.terrefiamuser.name
    policy_arn = "arn:aws:iam::aws:policy/IAMUserChangePassword"
  
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

resource "aws_iam_role_policy" "test_iam_role_policy" {
  name = "test_policy"
  role = aws_iam_role.terrefrole.id

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListObject"
        ]
        
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_instance_profile" "terrefinstanceprofile" {
    name = "ec2-test-profile"
    role = aws_iam_role.terrefrole.name
  
}

resource "aws_instance" "terrefinstance" {
    ami = "ami-0199ac7c9fbf9ed83"
    instance_type = "t3.micro"
    key_name = "mynewkey"
    vpc_security_group_ids = ["sg-04f5fe61a0b53d5e1"]
    iam_instance_profile = aws_iam_instance_profile.terrefinstanceprofile.name
  
}




