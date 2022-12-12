import pandas as pd
import os
import glob

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

# Load the data set
def __fetch():
    master_data = "static"
    
    data = []
    
    kinds = os.listdir(master_data)
    for kind in kinds:
        files = []
        for extension in ALLOWED_EXTENSIONS:
            files += glob.glob(pathname=f'{master_data}/{kind}/*.{extension}')
        
        data += [[kind, path] for path in files]
            
    df = pd.DataFrame(data=data, columns=['kind', 'path'])
    
    return df
    
def sample(kind):
    df = __fetch()
    return df.loc[df['kind'] == kind, 'path'].sample(n=1).values[0]

def sample_random(n):
    df = __fetch()
    return df.groupby(by='kind').sample(n=n)