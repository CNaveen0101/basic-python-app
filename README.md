provider "aws"  {
  region = "us-east-1"  
}

resource "aws_vpc" "terrefvpc" {
    cidr_block = "10.0.0.0/24"
    tags = {
      Name = "myvpc"
    } 
}

resource "aws_subnet" "terrefpublicsubnet" {
  vpc_id     = aws_vpc.terrefvpc.id
  cidr_block = "10.0.0.0/25"

  tags = {
    Name = "mypublicsubnet"
  }
}

resource "aws_subnet" "terrefprivatesubnet" {
  vpc_id     = aws_vpc.terrefvpc.id
  cidr_block = "10.0.0.128/26"

  tags = {
    Name = "myprivatesubnet"
  }
}
  
resource "aws_internet_gateway" "terrefigw" {
  vpc_id = aws_vpc.terrefvpc.id

  tags = {
    Name = "myigw"
  }
}

resource "aws_eip" "terrefeip" {
    domain = "vpc"

    tags = {
        Name = "myeip25"
    }
}

resource "aws_nat_gateway" "terrefnat" {
  allocation_id = aws_eip.terrefeip.id
  subnet_id     = aws_subnet.terrefpublicsubnet.id

  tags = {
    Name = "MY NAT"
  }

  # To ensure proper ordering, it is recommended to add an explicit dependency
  # on the Internet Gateway for the VPC.
  depends_on = [aws_internet_gateway.terrefigw]
}

resource "aws_route_table" "terrefpubroutetable" {
  vpc_id = aws_vpc.terrefvpc.id

  route {
    cidr_block = "10.0.0.0/24"
    gateway_id = aws_internet_gateway.terrefigw.id
  }

  tags = {
    Name = "mypublicroutetable"
  }
}

resource "aws_route_table" "terrefpriroutetable" {
  vpc_id = aws_vpc.terrefvpc.id

  route {
    cidr_block = "10.0.0.0/24"
    gateway_id = aws_nat_gateway.terrefnat.id
  }

  tags = {
    Name = "mypriroutetable"
  }
}

resource "aws_route_table_association" "terrefpubroutetableassociation" {
  subnet_id      = aws_subnet.terrefpublicsubnet.id
  route_table_id = aws_route_table.terrefpubroutetable.id
}

resource "aws_route_table_association" "terrefpriroutetableassociation" {
  subnet_id      = aws_subnet.terrefprivatesubnet.id
  route_table_id = aws_route_table.terrefpriroutetable.id
}





