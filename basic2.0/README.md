# Setup Guide
```
pip install -r requirements.txt
```
## Run the nameserver
```
python3 rmi_nameserver.py
```
## Run the nodes
```
python3 supernode.py
```
Run for how many nodes you want, eg. run it 3 times for 3 nodes.
```
python3 subnode.py 
```
```
uvicorn client:app --reload
```