import pandas as pd
import os
import glob

# Load the data set
def __isolate():
    global df
    
    master_data = "static"
    
    data = []
    
    kinds = os.listdir(master_data)
    for kind in kinds:
        sub_categories = [path for path in os.listdir(f'{master_data}/{kind}')
                          if os.path.isdir(f'{master_data}/{kind}/{path}')]
        # ./Apple/Apple A -> sub_categories = ['Apple A']
        # ./Banana/71Banana02034.png -> sub_categories = []
        for sub_category in sub_categories:
            data += [[sub_category, path] for path in 
                     glob.glob(pathname=f'{master_data}/{kind}/{sub_category}/*.png')]
            continue
        
        data += [[kind, path] for path in glob.glob(pathname=f'{master_data}/{kind}/*.png')]
            
    df = pd.DataFrame(data=data, columns=['kind', 'path'])
    
__isolate()

def sample(kind):
    return df.loc[df['kind'] == kind, 'path'].sample(n=1).values[0]

def sample_random(n):
    return df.groupby(by='kind').sample(n=n)