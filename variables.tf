variable "name" {
  type        = string
  description = "name to greet"
  default     = "World"
}

variable "environment" {
  type        = string
  description = "(required) The environment within which Terraform is expected to run"
  default     = "sandbox"
}