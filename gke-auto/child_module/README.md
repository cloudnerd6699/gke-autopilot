# To Create a Terraform Autopilot cluster_autoscaling

This is a code created for GKE Autopilot Cluster with private cluster having the public endpoints
```

  project_id                      = ""
  name                            = ""
  regional                        = true
  region                          = "us-central1"
  network                         = local.network_name
  subnetwork                      = local.subnet_name 
  ip_range_pods                   = local.pods_range_name
  ip_range_services               = local.svc_range_name
  release_channel                 = "REGULAR"
  enable_vertical_pod_autoscaling = true
  enable_private_endpoint         = false  
  #Because we are  creating a private cluster with public endpints, if you want to create a private cluster with private endpoint then  change it to false
  enable_private_nodes            = true
  # It enable us to create a private cluster, if we change it to false , then public cluster will be creating
  master_ipv4_cidr_block          = "192.168.10.64/28"
  datapath_provider               = "ADVANCED_DATAPATH"
  master_global_access_enabled	  = true

  master_authorized_networks = [
    {
      cidr_block   = "10.60.0.0/17"
      display_name = "VPC"
    },
      {
      cidr_block   = "117.196.121.104/32"
      display_name = "sanket-cidr"
    },
  ]






















```