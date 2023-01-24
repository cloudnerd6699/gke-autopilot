

locals {
  cluster_type           = var.cluster_type
  network_name           = var.network_name
  subnet_name            = var.subnet_name
  master_auth_subnetwork = var.master_auth_subnetwork
  pods_range_name        = var.pods_range_name
  svc_range_name         = var.svc_range_name
}

module "gke" {
  source  = "../parent_module/"
  project_id                      = var.project_id
  name                            = var.name
  regional                        = true
  region                         = var.region
  network                         = local.network_name
  subnetwork                      = local.subnet_name 
  ip_range_pods                   = local.pods_range_name
  ip_range_services               = local.svc_range_name
  release_channel                 = var.release_channel
  enable_vertical_pod_autoscaling = true
  enable_private_endpoint         = false   #Becaue we creating a private cluster, if you want to create a public cluster , just change it to false
  enable_private_nodes            = true
  master_ipv4_cidr_block          = var.master_ipv4_cidr_block
  datapath_provider               = "ADVANCED_DATAPATH"
  master_global_access_enabled    = true

  master_authorized_networks = [
    {
      cidr_block   = var.cidr_block_1
      display_name = var.display_name_1
    },
      {
      cidr_block   = var.cidr_block_2
      display_name = var.display_name_2
    },
    {
      cidr_block = var.cidr_block_3 
      display_name = var.display_name_3
    }
  ]
  
}
