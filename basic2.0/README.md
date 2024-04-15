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
# CRUD APIs
uvicorn client:app --reload --port=8000

# Seeder API
uvicorn multthreaded_seeder:app --reload --port=5002
http://127.0.0.1:5002/docs

```