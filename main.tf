provider "mongodbatlas" {
  public_key  = var.public_key
  private_key = var.private_key
}

# create mongodb project
resource "mongodbatlas_project" "this" {
  org_id = var.atlas_org_id
  name = var.atlas_project_name
}

# create cluster
resource "mongodbatlas_advanced_cluster" "this" {
  project_id   = mongodbatlas_project.this.id
  name         = var.cluster_name
  cluster_type = var.cluster_type

  replication_specs {
    region_configs {
      electable_specs {
        instance_size = var.provider_instance_size_name
      }
      provider_name         = var.provider_name
      backing_provider_name = var.backing_provider_name
      region_name           = var.region_name
      priority              = var.priority
    }
  }
}

# Create a Database User
resource "mongodbatlas_database_user" "this" {
  username = var.username
  password = var.password
  project_id = mongodbatlas_project.this.id
  auth_database_name = "admin"
  roles {
    role_name     = "readWrite"
    database_name = "ris_data_collection"
  }
}
