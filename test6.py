print("======")
    


def PackColl(col):
    length = len(col)
    
    if (length == 1):
        return [col[0], ""]
    if (length == 2):
        return [col[1], col[0]]
        
    tmpcollect = [col[1], col[0]]
    for i in range(2, length - 1):
        tmpcollect = [tmpcollect, col[i]]
        tmpcollect.reverse()
    
    tmpcollect = [col[length - 1], tmpcollect]
        
    return tmpcollect
    
    
def GetSub___(tmp, sub):
    if (not isinstance(sub, list)):
        tmp.append(sub)
        return tmp
        
    for i in sub:
        tmp = GetSub(tmp, i)
            
    return tmp
    


def GetCollectionsListFrom(col_hierarchy, col):
    collect = []
    
    def GetSub(sub):
        nonlocal collect
        if (not isinstance(sub, list)):
            collect.append(sub)
            return collect
            
        for i in sub:
            collect = GetSub(i)
                
        return collect
    
    print()
    
    
    GetSub(col_hierarchy)
    
    if (col in collect):
        indx = collect.index(col)
        return collect[:indx + 1]

    return None

coll_3 = ["col_3_3","col_3_2","col_3_1","col_3"]
coll_2 = ["col_2_4","col_2_3","col_2_2","col_2_1","col_2"]
coll_1 = ["col_1_1", "col_1"]
coll_0 = ["col_0"]

col_hierarchy = PackColl(coll_2)
print(col_hierarchy)
col_list = GetCollectionsListFrom(col_hierarchy, "col_2_3")
print(col_list)




