provider "aws" {
    region = "ap-south-2"
  
}

resource "aws_iam_user" "terrefuser" {
  name = "my_user"
  path = "/system/"

  tags = {
    tag-key = "myuserlabel"
  }
}

resource "aws_iam_user_login_profile" "terrefuserloginprofile" {
    user = aws_iam_user.terrefuser.name
    password_length = 14
    password_reset_required = true
}

resource "aws_iam_user_policy_attachment" "terrefpolicyattachmentpasswordchange" {
    user = aws_iam_user.terrefuser.name
    policy_arn = "arn:aws:iam::aws:policy/IAMUserChangePassword"
}

resource "aws_iam_user_policy_attachment" "terrefpolicyattachmentec2access" {
    user = aws_iam_user.terrefuser.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_user_policy_attachment" "terrefpolicyattachments3access" {
    user = aws_iam_user.terrefuser.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
  
}

resource "aws_iam_role" "myterrefrole" {
  name = "mynew_test_role"

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
    tag-key = "testrole"
  }
}

resource "aws_iam_role_policy" "terrefpolicy" {
  name = "mynew_test_policy"
  role = aws_iam_role.myterrefrole.id


  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_instance_profile" "terrefprofile" {
  name = "test_profile"
  role = aws_iam_role.myterrefrole.name
}

resource "aws_instance" "terrefinstance" {
    ami = "ami-0304448c82662e9ac"
    instance_type = "t3.micro"
    key_name = "mynewkey"
    vpc_security_group_ids = ["sg-0f042558973f95dbf"]
    iam_instance_profile =aws_iam_instance_profile.terrefprofile.id
    
    tags = {
      Name = "myinstance"
    }

  
}
