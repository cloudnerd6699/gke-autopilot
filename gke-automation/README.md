# GKE-Automation
The code will check different conditions on the Various Cluster if any of the condtion fails it will delete the cluster.

## Function Structure 

There are three different functions, we have created to achieve the task of deleting the cluster which fails the parameters of approval.

age_of_cluster() : This function is to calculate the age of the cluster.
Logic: This function will check the creation time of gke cluster and current time, then find the diffrence between the these two dates. That will be age of cluster and the value will be return in the number of days.

get_cluster_list() : This function will return the list of dictionaries containing name and location of all those cluster which fail the conditions of approval.

delete_cluster_list(): This function will delete the list of cluster passed through as parameter. 

## conditions for approval 

The following are the different condition of deletion

1. Cluster is regional
2. After 90 days by default
3. Disk-type is pd-balanced or pd-ssd
4. Owner Labels is not present or no labels are present
5. Node Pool is not PVM
6. Number of nodes greter than 3
7. Running between 2:00 AM - 6:00 AM IST
8. Machine type other than e2-micro,e2-small,e2-medium,e2-standard-2

![image](/uploads/653bdd03833d7d6638e4ccaff009c49a/image.png)




## Install dependencies

The different depedencies that are necessary for the execution of the code are mentioned in the requirements.txt file.
You can install them seperately by pip one after the other or can run the following command

```
pip install -r requirements.txt

```

## Different Labels to by pass deletion conditions

There are some by pass conditions that have been placed in order to retain the clusters even if they fail the approval

To activate these by pass conditions one can add the following labels at the cluster level

1. owner: This is mandatory label for the cluster to be activate otherwise it will be deleted immediately
2. allow-regional: This will allow the cluster to be regional
3. allow-nodes: This will allow the cluster to have more than 3 nodes
4. allow-24-7: This will allow the cluster to run between 2AM and 6AM.
5. allow-ondemand: This will allow cluster to use nodes other than preemtible
6. allow-ssd: This will allow the disk type to be pd-balanced and pd-ssd
7. allow-perfomance: This will allow the machine type to be other than approved ones

