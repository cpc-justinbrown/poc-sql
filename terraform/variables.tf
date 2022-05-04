variable "tenant_id" {
  default = "88b6c77b-f4e0-40c5-9fbb-df51a927179a"
}

variable "subscription_id" {
  default = "8169f36e-e8cc-4e49-84ff-21ee67a4dd9a"
}

variable "tags" {
  default = {
    "Description" = "Digital Transformation Sandbox for BROWNJL"
    "ManagedBy"   = "DT"
    "Department"  = "Digital Transformation"
    "CostCenter"  = "P3601"
  }
}

variable "ad-brownjl_object_id" {
  default = "268f5e47-eb76-485b-a9fb-59a68d444af3"
}

variable "cpchem_ip_address" {
  default = "64.129.107.15"
}