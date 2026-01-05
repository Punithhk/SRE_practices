terraform uses providers to manage cloud providers API.

Terraform registry for public terraform providers modules

provider "aws" {
  region = "us-west-2"
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  tags = {
    Name = "learn-terraform"
  }
}


- Provider Block 
- Data Block --  Data source IDs are prefixed with data, followed by the block's type and name. In this example, the data.aws_ami.ubuntu data source loads an AMI for the most recent Ubuntu Noble Numbat release in the region configured for your provide
- Resource block - here the resource address is aws_instance.app_server.

terraform fmt (formatting)

terraform state list 
terraform show  
