from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from datetime import datetime
import pytz




def age_of_cluster(cluster):
    #This block of code return the age of cluster in days
    UTC = pytz.utc
    create_time = cluster['createTime']
    create_time = create_time[0:19]
    cluster_creation_date = datetime.strptime(create_time,'%Y-%m-%dT%H:%M:%S')
    cluster_creation_date = cluster_creation_date.date()
    current_date = datetime.now(UTC).date()
    difference = current_date - cluster_creation_date
    days = difference.days
    return days



def get_cluster_list(project_id, credentials):
    #This block of code will return a list which contain the name and location of cluster
    #which need to be deleted
    service = discovery.build('container', 'v1', credentials=credentials)
    parent = 'projects/'+project_id+'/locations/-' 
    request = service.projects().locations().clusters().list(parent=parent)
    response = request.execute()
    
    if not response:        #check wheather any cluster is present or not
        return 

    clusters = response['clusters']
    cluster_list = []
    
    disk_type_allowed = ['pd-standard']                                 # list of disk-type allowed
    machine_type_allowed = ['e2-micro','e2-small','e2-medium','e2-standard-2']                # list of machine type that are allowed
    
    IST = pytz.timezone('Asia/Kolkata')
    time=datetime.now(IST)
    current_time = time.time()
    time_hour_part = int(str(current_time)[0:2])
    

    for cluster in clusters:
        temp_dic ={}                                                    # temporary dictionary to store name & location of cluster
        temp_dic['name'] = cluster['name']
        temp_dic['cluster_location'] = cluster['location']        
        locations=cluster['nodePools'][0]['locations']                  # This contains the different nodes location, if cluster is regional in nature
                                                                        # it will have more than one value

        age = age_of_cluster(cluster)                                   # will get the age of cluster in days

        #To check weather labels are present or not, if present contains the correct labels
        
        try:
            if cluster['resourceLabels']:
                if 'owner' not in cluster['resourceLabels'] and 'Owner' not in cluster['resourceLabels']:
                    cluster_list.append(temp_dic)               # appending the cluster details i.e name and location which fails the condition
                    continue
        except:                                                 # Labels are not present
            cluster_list.append(temp_dic)
            continue
        
        #condition for regional cluster
        if len(locations)>1:
            if "allow-regional" not in cluster['resourceLabels']:    
                cluster_list.append(temp_dic)
                continue    
        
        #To check wheather the cluster age is greater than or equal to 90 days
        if age>=90:
            cluster_list.append(temp_dic)
            continue
        
        #To check weather nodes are preemtible or not
        try:
            preemtible_status = cluster['nodeConfig']['preemptible']
            if preemtible_status == True:
                pass
        except:
            if "allow-ondemand" not in cluster['resourceLabels']:    
                cluster_list.append(temp_dic)
                continue
        
        #check weather cluster is running between 2 AM and 6 AM IST
        if cluster['nodePools'][0]['status']=='RUNNING' and (time_hour_part >=2 and time_hour_part <= 6):
            if "allow-24-7" not in cluster['resourceLabels']:
                cluster_list.append(temp_dic)
                continue   
            
        # Check weather nodes are greater than 3
        if cluster['currentNodeCount'] > 3:        
            if "allow-nodes" not in cluster['resourceLabels']:
                cluster_list.append(temp_dic)
                continue    
        
        # Check weather disk type is allowed or not    
        if cluster['nodeConfig']['diskType'] not in disk_type_allowed:
            if "allow-ssd" not in cluster['resourceLabels']:    
                cluster_list.append(temp_dic)
                continue    
        
        # Check weather machine type is allowed    
        if cluster['nodeConfig']['machineType'] not in machine_type_allowed:
            if "allow-performance" not in cluster['resourceLabels']:    
                cluster_list.append(temp_dic)
                continue

    return cluster_list

def delete_cluster_list(cluster_list, project_id, credentials):
    #section to delete the clusters
    service = discovery.build('container', 'v1', credentials=credentials)
    for cluster in cluster_list:
        name = cluster['name']
        location = cluster['cluster_location']
        cluster_name = 'projects/'+project_id+'/locations/'+location+'/clusters/'+name # TODO: Update placeholder value.
        request = service.projects().locations().clusters().delete(name=cluster_name)
        response_delete = request.execute()
    return

def main(): 
    project_id="gcp-practice-trainning"
    credentials = GoogleCredentials.get_application_default()   
    cluster_list = get_cluster_list(project_id,credentials)
    print(cluster_list)
    if cluster_list:
        delete_cluster_list(cluster_list, project_id, credentials)
    return
