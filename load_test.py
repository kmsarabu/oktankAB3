#!/usr/bin/python3

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "http://ab3elb-appserverloadbalancer-1644308260.us-east-1.elb.amazonaws.com/"
query_list1 = [ "products/bicycles/Alfa",
          "products/bicycles/Micro%20Juliet",
          "products/apparels/Lodge",
          "products/fashion/Ring%2056%20in%20Silver",
          "products/jewelry/14k%20Solid%20Bloom%20Earrings"
	]
query_list2 = [ "products/bicycles/Zulu",
 "products/bicycles/YNOT%20Saddle%20Roll",
 "products/bicycles/Yankee",
 "products/bicycles/X-Ray",
 "products/bicycles/Wooden%20City%20Crate",
 "products/bicycles/Whiskey",
 "products/bicycles/Water%20Bottle%20Holder",
 "products/bicycles/Warranty%20Item",
 "products/bicycles/Victor",
 "products/bicycles/Versair%20Mini%20Pump",
 "products/bicycles/Uniform",
 "products/bicycles/Truvativ%20Square%20Taper%20Bottom%20Bracket",
 "products/bicycles/Truvativ%20Powerspline%20Bottom%20Bracket",
 "products/bicycles/Triangle%20Bicycle%20Shelf",
 "products/bicycles/Topeak%20Mini%20Dual%20DXG%20Hand%20Pump",
 "products/bicycles/Thickslick%20700x25-28c%20Freedom%20Sport%20Tire",
 "products/bicycles/The%20Tango",
 "products/bicycles/The%20Nikola",
 "products/bicycles/The%20Lima",
 "products/bicycles/The%20Golf",
 "products/fashion/Zoulou%20Coat%20in%20Black",
 "products/fashion/Zola%20Coat%20in%20Black",
 "products/fashion/Zipper%20Jacket",
 "products/fashion/Zipper%20Jacket",
 "products/fashion/Zipper%20Dress",
 "products/fashion/Zip%20Back%20Circle%20Blouse%20in%20Black",
 "products/fashion/Zig%20Coat%20in%20Evening",
 "products/fashion/Zepo%20Brushed%20Cotton%20Blazer",
 "products/fashion/Zepo%20Brushed%20Cotton%20Blazer",
 "products/fashion/Zepo%20Blazer",
 "products/fashion/Zepella%20Sandal",
 "products/fashion/Zepella%20Sandal",
 "products/fashion/Yeps%20Shirt%20in%20V-Neck",
 "products/fashion/Yank%20Crewneck%20Tee",
 "products/fashion/Yank%20Crewneck%20Tee",
 "products/fashion/Wrinkled%20Tux%20Shirt%20in%20Navy",
 "products/fashion/Wrap%20Snap%20Skirt%20in%20Black",
 "products/fashion/Wrap%20Sandal%20in%20Black/Steel",
 "products/fashion/Wrapped%20Up%20Hat%20in%20Straw/White",
 "products/fashion/Wrapped%20Golf%20Shoe",
 "products/jewelry/18k%20Wire%20Bloom%20Earrings",
 "products/jewelry/18k%20Solid%20Bloom%20Earrings",
 "products/jewelry/18k%20Pedal%20Ring",
 "products/jewelry/18k%20Intertwined%20Earrings",
 "products/jewelry/18k%20Interlinked%20Earrings",
 "products/jewelry/18k%20Fluid%20Lines%20Necklace",
 "products/jewelry/18k%20Dangling%20Pendant%20Earrings",
 "products/jewelry/18k%20Dangling%20Pendant%20Earrings",
 "products/jewelry/18k%20Dangling%20Obsidian%20Earrings",
 "products/jewelry/18k%20Bloom%20Pendant",
 "products/jewelry/18k%20Bloom%20Earrings",
 "products/jewelry/14k%20Wire%20Bloom%20Earrings",
 "products/jewelry/14k%20Solid%20Bloom%20Earrings",
 "products/jewelry/14k%20Intertwined%20Earrings",
 "products/jewelry/14k%20Interlinked%20Earrings",
 "products/jewelry/14k%20Dangling%20Pendant%20Earrings",
 "products/jewelry/14k%20Dangling%20Pendant%20Earrings",
 "products/jewelry/14k%20Dangling%20Obsidian%20Earrings",
 "products/jewelry/14k%20Bloom%20Earrings"
 "products/apparels/Whitney%20Pullover",
 "products/apparels/The%20Scout%20Skincare%20Kit",
 "products/apparels/The%20Field%20Report%20Vol.%202",
 "products/apparels/Scout%20Backpack",
 "products/apparels/Red%20Wing%20Iron%20Ranger%20Boot",
 "products/apparels/Pennsylvania%20Notebooks",
 "products/apparels/Mud%20Scrub%20Soap",
 "products/apparels/Moon%20Cycle",
 "products/apparels/Mola%20Headlamp",
 "products/apparels/Long%20Sleeve%20Swing%20Shirt",
 "products/apparels/Lodge",
 "products/apparels/Hudderton%20Backpack",
 "products/apparels/Harriet%20Chambray",
 "products/apparels/Guaranteed",
 "products/apparels/Gertrude%20Cardigan",
 "products/apparels/Duckworth%20Woolfill%20Jacket",
 "products/apparels/Double%20Wall%20Mug",
 "products/apparels/Derby%20Tier%20Backpack",
 "products/apparels/Dawson%20Trolley",
 "products/apparels/Cydney%20Plaid" ]

def process_request(url, product):
    res = requests.get("{}/{}".format(url, product))
    if res.status_code != 200:
        print ("Request {}/{} failed to process, {}".format(url,product,res.content))

def process_all_requests():
    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for product in query_list2:
            threads.append(executor.submit(process_request, url, product))
            for product1 in query_list1:
                threads.append(executor.submit(process_request, url, product1))

        for task in as_completed(threads):
            print (task.result())

if __name__=="__main__":
    #process_request(url, query_list2[3])
    process_all_requests()
