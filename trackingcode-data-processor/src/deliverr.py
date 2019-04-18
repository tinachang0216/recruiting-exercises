"""
Introduction to the project.

I designed the server to mimic a warehouse management system.
The storage and distribution of the warehouse was the original input that should a json file, with order coming first, then warehouse infomation.
"""

"""
Introduction to classes and algorithm.

inventory: items would be gradually added into warehouse out of the input map that was a json file.
order: items would be gradually added to form a map, input was a string in json format.
InventoryAllocator: use the inventory information to check and allocate items, input should be a map.
Read_to_Json: read_warehouse is to read order and warehouse distribution in singlejson file.
main function: read file to inventory, read orders one by one and give ans, the allocation method or empty map because of order exceeding inventory.
"""

"""
terminal appearance:

->cat testcase1.json | python deliverr.py
->cat testcase2.json | python deliverr.py
->cat testcase3.json | python deliverr.py
->cat testcase4.json | python deliverr.py

testcase.json
[  {                      # order
   "apple":4
   },
   {                      # original warehouse
      "name":"owd",
      "inventory":{
         "apple":5
      }
   },
   {
      "name":"dm",
      "inventory":{
         "banana":5
      }
   }
]
"""

import sys
import collections
import json
import ast

def main():

    class inventory:
        def __init__(self):
            self.storage_map=collections.defaultdict(dict)   #keys by warehouse name, then by items inside every warehouse

        def add(self,name,item,val):
            if item not in self.storage_map[name]:
                self.storage_map[name][item]=val
            else:
                self.storage_map[name][item]+=val

        def collect(self):
            self.ref_cnt_dic=collections.defaultdict(int)     #count the total amount of items
            self.ref_wh_dic=collections.defaultdict(list)     #record items distributions
            for wh in self.storage_map:
                for item in self.storage_map[wh]:
                    self.ref_cnt_dic[item]+=self.storage_map[wh][item]
                    self.ref_wh_dic[item].append(wh)

        def minus(self,name,item,val):
            self.storage_map[name][item]-=val
            self.ref_cnt_dic[item]-=val
            if not self.storage_map[name][item]:
                del self.storage_map[name][item]
                #self.ref_wh_dic[item].remove(name)
            if not self.storage_map[name]:
                del self.storage_map[name]

    class order:
        def __init__(self):
            self.request_map=collections.defaultdict(int)   #record order by item then quantity

        def add(self,item,val):
            self.request_map[item]+=val


    class InventoryAllocator(inventory):
        """
        Allocate function will check item by item. When checking every single item, it will collect by name of warehouse.
        It will try to take all of one item from one warehouse first.
        """
        def __init__(self):
            self.storage_map=inventory.storage_map
            self.ref_cnt_dic=inventory.ref_cnt_dic
            self.ref_wh_dic=inventory.ref_wh_dic

        def allocate(self,order):
            request_map=order
            output_map=collections.defaultdict(dict)
            for item in request_map:
                if request_map[item]<=self.ref_cnt_dic[item]:
                    cnt=request_map[item]
                    for wh in self.ref_wh_dic[item]:
                        curr=min(self.storage_map[wh][item],cnt)
                        if item not in output_map[wh]: output_map[wh][item]=curr
                        else: output_map[wh][item]+=curr
                        inventory.minus(wh,item,curr)
                        cnt-=curr
                        if cnt==0: break
            return output_map


    class Read_to_Json():
        def read_warehouse(self):
            #f1=open(sys.stdin.readlines())
            #f1,f2=open(sys.stdin.readline()),open(sys.stdin.readline())
            storage_array=json.load(sys.stdin)
            #order_map=json.load(sys.stdin)
            return storage_array[0],storage_array[1:]


    inventory=inventory()
    Read_to_Json=Read_to_Json()
    order_map,storage_array = Read_to_Json.read_warehouse()
    if not storage_array:
        print("{}")
        return
    for dic in storage_array:
        if not dic: continue
        for b in dic["inventory"]:
            inventory.add(dic["name"],b,dic["inventory"][b])
    print("Warehouse:")
    print(storage_array)
    inventory.collect()
    InventoryAllocator=InventoryAllocator()
    order=order()
    if not order_map:
        print("Invalid input")
    for item in order_map:
        order.add(item,order_map[item])
    print("Order:")
    print(order_map)
    output=InventoryAllocator.allocate(order_map)
    print("Allocation:")
    print(dict(output))




if __name__ == '__main__':
    main()
