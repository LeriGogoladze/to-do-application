# სამომავლოდ,დავალებებთან სამუშაოდ აგენერირებს თითოეული დავალების აიდის.
def generate_unique_id(tasks): 
    id = str(len(tasks)).zfill(5)  
    return id 


