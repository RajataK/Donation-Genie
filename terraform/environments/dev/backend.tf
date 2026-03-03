terraform {
  backend "s3" {
    bucket         = "donation-genie-tf-state"
    key            = "env/dev/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "donation-genie-terraform-locks"
    encrypt        = true
  }
}
