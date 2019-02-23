#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# 
# - We'll pretend we're working as data analysts for a company that builds Android and iOS mobile apps. We make our apps available on Google Play and the App Store.
# 
# - We only build apps that are free to download and install, and our main source of revenue consists of in-app ads. This means our revenue for any given app is mostly influenced by the number of users who use our app — the more users that see and engage with the adds, the better.
# 
# -  Our goal for this project is to analyze data to help our Mobile app developers understand what kinds of apps are likely to attract more users.
# 
# 
# 
# 
# 

# ## Dataset links:
# 
# - 'googleplaystore.csv'   [Dataset](https://www.kaggle.com/lava18/google-play-store-apps/home) 
# - 'AppleStore.csv'  [Dataset](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home)

# In[2]:


ios_open_file=open('AppleStore.csv')
and_open_file=open('googleplaystore.csv')

from csv import reader

ios_read=reader(ios_open_file)
and_read=reader(and_open_file)

ios_apps_data=list(ios_read)
and_apps_data=list(and_read)
ios_head=ios_apps_data[0]
and_head=and_apps_data[0]

ios_apps_data=ios_apps_data[1:]
and_apps_data=and_apps_data[1:]

def explore(dataset,start,end,rows_n_columns=False): 
    dataset_slice=dataset[start:end]
    for row in dataset_slice:
        print(row)
        print("\n")
    if rows_n_columns:
        print("Number of rows ",len(dataset))
        print("Number of Columns",len(dataset[0]))
        print("\n")

explore(ios_apps_data,0,6,True)
explore(and_apps_data,0,6,True)


# # Data Cleaning 
# 
# - As company needs only free apps and english language apps we need to clean the unrelated data for further analysis.

# In[3]:


#print(and_apps_data[10472])
del and_apps_data[10472]
print(and_apps_data[10472])


# # Duplicate check
# 
# - Here we are categorising the unique and duplicates
# - After that we remove the duplicate apps
# - Duplicates are removed based on the higher number of reviews 

# In[4]:


def divide_apps(dataset):
    duplicate=[]
    unique=[]
    dup_count={}
    for row in dataset:
        if row[0] in unique:
            duplicate.append(row[0])
        else:
            unique.append(row[0])
    
    print(len(duplicate))
    return duplicate,unique

duplicate,unique=divide_apps(and_apps_data)
    


# In[5]:


print(and_head)

print(ios_head)


# In[6]:


reviews_max={}
for row in and_apps_data:
    name=row[0]
    n_reviews=float(row[3])
    if name in reviews_max:
        if reviews_max[name] < n_reviews:
            reviews_max[name]=n_reviews
    if name not in reviews_max:
        reviews_max[name]=n_reviews
print(len(reviews_max))
    


# In[7]:


android_clean=[]
already_added=[]

for row in and_apps_data:
    name=row[0]
    n_reviews=float(row[3])
    if n_reviews==reviews_max[name] and name not in already_added:
        android_clean.append(row)
        already_added.append(name)
        
explore(android_clean,0,6,True)       
    
    


# In[8]:


print(len(already_added))


# In[9]:


def charCheck(string):
    flag=False
    count=0
    for i in string:
        if ord(i)>=0 and ord(i)<=127:
            flag=True
        else:
            count+=1
            if count==4:
                return False
                
            
    return flag

print(charCheck('Instagram'))
print(charCheck('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(charCheck('Docs To Go™ Free Office Suite'))
print(charCheck('Instachat 😜'))
            


# In[10]:


def filter_non_eng(dataset1,dataset2):
    
    new_list1=[]
    new_list2=[]
    for row in dataset1:
        name=row[0]
        if(charCheck(name)):
            new_list1.append(row)
    for row in dataset2:
        name=row[1]
        if(charCheck(name)):
            new_list2.append(row)
    
    return new_list1,new_list2
            
    


# In[11]:


android_clean,ios_clean=filter_non_eng(android_clean,ios_apps_data)
explore(android_clean,0,6,True)       
explore(ios_clean,0,6,True)       


# In[14]:


ios_apps=[] #4
and_apps=[] #7

for row in ios_clean:
    price=float(row[4])
    if price == 0:
        ios_apps.append(row)
        
        

for row in android_clean:
    price=row[6]
    if price.upper() =='FREE' :
        and_apps.append(row)
        
print(len(ios_apps))
print(len(and_apps))
    
    


# ## So far in the data cleaning process, I : 
# 
# - Removed inaccurate data
# - Removed duplicate app entries
# - Removed non-English apps
# - Isolated the free apps

# ** To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps: **
# 
# 
# - Build a minimal Android version of the app, and add it to Google Play.
# - If the app has a good response from users, we then develop it further.
# - If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.

# In[15]:


print(and_head) #9
print(ios_head) #11


# In[17]:


def freq_table(dataset,index):
    freq={}
    for row in dataset:
        if row[index] in freq:
            freq[row[index]]+=1
        elif row[index] not in freq:
            freq[row[index]]=1
            
    return freq
            
    


# In[18]:


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        


# In[20]:


display_table(ios_apps,11)
#display_table(and_apps,9)
#display_table(and_apps,1)


# In[21]:


display_table(and_apps,9)


# In[22]:


display_table(and_apps,1)


# In[23]:


ios_freq=freq_table(ios_apps,11)


# In[24]:


print(ios_freq)


# In[29]:


avg=[]
for genre in ios_freq:
    total=0
    len_genre=0
   
    for row in ios_apps:
        genre_app=row[11]
        if genre_app==genre:
            n_ratings=float(row[5])
            total+=n_ratings
            len_genre+=1

    avg.append((total/len_genre,genre))
print(avg)
    
            


# In[30]:


print(sorted(avg))


# In[31]:


display_table(and_apps, 5) # the Installs columns


# In[33]:


categories_android = freq_table(and_apps, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in and_apps:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# In[34]:


under_100_m = []

for app in and_apps:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# In[35]:


for app in and_apps:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# In[ ]:




