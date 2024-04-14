# from concurrent import futures

# import sys      #pip3 install sys
# sys.path.append('./generated')
# sys.path.append('./proto')
# sys.path.append('./utils')
# import grpc
# import fileService_pb2_grpc
# import fileService_pb2
# import heartbeat_pb2_grpc
# import heartbeat_pb2
# import sys
# import time
# import yaml
# import threading
# import os

# def getFileData():
#     fileName = input("Enter filename:")
#     outfile = os.path.join('files', fileName)
#     file_data = open(outfile, 'rb').read()
#     fileData = fileService_pb2.FileData(fileName=fileName, data=file_data)
#     return fileData

# def getFileChunks():
#      # Maximum chunk size that can be sent
#     CHUNK_SIZE=4000000

#     username = input("Enter Username: ")
#     fileName = input("Enter filename: ")

#     outfile = os.path.join('files', fileName)
    
#     sTime=time.time()
#     with open(outfile, 'rb') as infile:
#         while True:
#             chunk = infile.read(CHUNK_SIZE)
#             if not chunk: break

#             # Do what you want with each chunk (in dev, write line to file)
#             yield fileService_pb2.FileData(username=username, filename=fileName, data=chunk, seqNo=1)
#     print("Time for upload= ", time.time()-sTime)

# def downloadTheFile(stub):
#     userName = input("Enter Username: ")
#     fileName = input("Enter file name: ")
#     data = bytes("",'utf-8')
#     sTime=time.time()
#     responses = stub.DownloadFile(fileService_pb2.FileInfo(username=userName, filename=fileName))
#     for response in responses:
#         fileName = response.filename
#         data += response.data
    
#     print("Time for Download = ", time.time()-sTime)
#     filePath=os.path.join('downloads', fileName)
#     saveFile = open(filePath, 'wb')
#     saveFile.write(data)
#     saveFile.close()
    
#     print("File Downloaded - ", fileName)


# def uploadTheFileChunks(stub):
#     response = stub.UploadFile(getFileChunks())
#     print(response)
#     if(response.success): print("File successfully Uploaded")
#     else:
#         print("Failed to upload. Message - ", response.message)

# def deleteTheFile(stub):
#     userName = input("Enter Username: ")
#     fileName = input("Enter file name: ")
#     response = stub.FileDelete(fileService_pb2.FileInfo(username=userName, filename=fileName))
#     print(response.message)

# def isFilePresent(stub):
#     userName = input("Enter Username: ")
#     fileName = input("Enter file name: ")
#     response = stub.FileSearch(fileService_pb2.FileInfo(username=userName, filename=fileName))

#     if(response.success==True):
#         print(response.message)
#     else:
#         print(response.message)

# def sendFileInChunks(username, filename, i):
#      # Maximum chunk size that can be sent
#     CHUNK_SIZE=4000000

#     outfile = os.path.join('files', fileName)
    
#     with open(outfile, 'rb') as infile:
#         while True:
#             chunk = infile.read(CHUNK_SIZE)
#             if not chunk: break
#             yield fileService_pb2.FileData(username=username+"_"+str(i), filename=fileName, data=chunk, seqNo=1)

# def sendFileMultipleTimes(stub):
#     userName = input("Enter Username: ")
#     fileName = input("Enter file name: ")
#     numberOfTimes = input("How many times you want to send this file?")

#     for i in range(1, numberOfTimes+1):
#         response = stub.UploadFile(sendFileInChunks(userName, fileName, i))
#         if(response.success): 
#             print("File successfully Uploaded for sequence : ", str(i))
#         else:
#             print("Failed to upload for sequence : ", str(i))

# def updateFile(stub):
#     response = stub.UpdateFile(getFileChunks())
#     if(response.success): 
#             print("File successfully updated")
#     else:
#         print("Failed to update the file")

# def getListOfAllTheFilesForTheUser(stub):
#     userName = input("Enter Username: ")
#     FileListResponse = stub.FileList(fileService_pb2.UserInfo(username=userName))
#     print(FileListResponse.Filenames)


# def handleUserInputs(stub):
#     print("===================================")
#     print("1. Upload a file")
#     print("2. Download a file.")
#     print("3. Delete a file")
#     print("4. Check if a file is present")
#     print("5. Update a file.")
#     print("6. Get a list of all the files for an user")
#     print("7. Send a file 100 times")
#     print("===================================")
#     option = input("Please choose an option.")

#     if(option=='1'):
#         uploadTheFileChunks(stub)
#     elif(option=='2'):
#         downloadTheFile(stub)
#     elif(option=='3'):
#         deleteTheFile(stub)
#     elif(option=='4'):
#         isFilePresent(stub)
#     elif(option=='5'):
#         updateFile(stub)
#     elif(option=='6'):
#         getListOfAllTheFilesForTheUser(stub)
#     elif(option=='7'):
#         sendFileMultipleTimes(stub)

# def run_client(serverAddress):
#     with grpc.insecure_channel(serverAddress) as channel:
#         try:
#             grpc.channel_ready_future(channel).result(timeout=1)
#         except grpc.FutureTimeoutError:
#             print("Connection timeout. Unable to connect to port ")
#             #exit()
#         else:
#             print("Connected")
#         stub = fileService_pb2_grpc.FileserviceStub(channel)
#         handleUserInputs(stub)


# if __name__ == '__main__':
#     run_client('127.0.0.1:9000')






from concurrent import futures
import grpc
import fileService_pb2_grpc
import fileService_pb2


import sys
import time
import os

def getFileData():
    fileName = input("Enter filename:")
    outfile = os.path.join('files', fileName)
    file_data = open(outfile, 'rb').read()
    fileData = fileService_pb2.FileData(fileName=fileName, data=file_data)
    return fileData

def getFileChunks():
    # Maximum chunk size that can be sent
    CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB

    username = input("Enter Username: ")
    fileName = input("Enter filename: ")

    outfile = os.path.join('files', fileName)
    
    start_time = time.time()
    with open(outfile, 'rb') as infile:
        while True:
            chunk = infile.read(CHUNK_SIZE)
            if not chunk: break
            yield fileService_pb2.FileData(username=username, filename=fileName, data=chunk, seqNo=1)
    print("Time for upload =", time.time() - start_time)

def downloadTheFile(stub, time_offset):
    userName = input("Enter Username: ")
    fileName = input("Enter file name: ")
    data = bytes("", 'utf-8')
    start_time = time.time()
    responses = stub.DownloadFile(fileService_pb2.FileInfo(username=userName, filename=fileName))
    for response in responses:
        fileName = response.filename
        data += response.data
    
    print("Time for Download =", time.time() - start_time)
    server_download_time = (start_time + time_offset) * 1000
    filePath = os.path.join('downloads', fileName)
    with open(filePath, 'wb') as saveFile:
        saveFile.write(data)
    
    print("File Downloaded -", fileName)
    print("Server download time:", server_download_time, "ms")

def uploadTheFileChunks(stub, time_offset):
    client_upload_time = time.time() * 1000
    response = stub.UploadFile(getFileChunks())
    if response.success:
        server_upload_time = client_upload_time + time_offset
        print(f"File successfully uploaded. Server upload time: {server_upload_time} ms")
    else:
        print(f"Failed to upload. Message - {response.message}")

def deleteTheFile(stub):
    userName = input("Enter Username: ")
    fileName = input("Enter file name: ")
    response = stub.FileDelete(fileService_pb2.FileInfo(username=userName, filename=fileName))
    print(response.message)

def isFilePresent(stub):
    userName = input("Enter Username: ")
    fileName = input("Enter file name: ")
    response = stub.FileSearch(fileService_pb2.FileInfo(username=userName, filename=fileName))

    if response.success:
        print(response.message)
    else:
        print(response.message)

def sendFileInChunks(username, filename, i):
    # Maximum chunk size that can be sent
    CHUNK_SIZE = 4 * 1024 * 1024  # 4 MB

    outfile = os.path.join('files', fileName)
    
    with open(outfile, 'rb') as infile:
        while True:
            chunk = infile.read(CHUNK_SIZE)
            if not chunk: break
            yield fileService_pb2.FileData(username=username + "_" + str(i), filename=fileName, data=chunk, seqNo=1)

def sendFileMultipleTimes(stub):
    userName = input("Enter Username: ")
    fileName = input("Enter file name: ")
    numberOfTimes = int(input("How many times do you want to send this file?"))

    for i in range(1, numberOfTimes + 1):
        response = stub.UploadFile(sendFileInChunks(userName, fileName, i))
        if response.success:
            print(f"File successfully uploaded for sequence: {i}")
        else:
            print(f"Failed to upload for sequence: {i}")

def updateFile(stub):
    response = stub.UpdateFile(getFileChunks())
    if response.success:
        print("File successfully updated")
    else:
        print("Failed to update the file")

def getListOfAllTheFilesForTheUser(stub):
    userName = input("Enter Username: ")
    FileListResponse = stub.FileList(fileService_pb2.UserInfo(username=userName))
    print(FileListResponse.Filenames)

def synchronize_client_clock(stub):
    # Request server time
    server_time_response = stub.GetServerTime(fileService_pb2.Empty())
    server_time = server_time_response.serverTime
    
    # Get client time in milliseconds
    client_time = int(time.time() * 1000)
    
    # Calculate time offset (server time - client time)
    time_offset = server_time - client_time
    
    # Print the time offset for verification
    print(f"Time offset between client and server: {time_offset} ms")
    
    return time_offset

def handleUserInputs(stub, time_offset):
    print("===================================")
    print("1. Upload a file")
    print("2. Download a file.")
    print("3. Delete a file")
    print("4. Check if a file is present")
    print("5. Update a file")
    print("6. Get a list of all the files for a user")
    print("7. Send a file multiple times")
    print("===================================")
    option = input("Please choose an option.")

    if option == '1':
        uploadTheFileChunks(stub, time_offset)
    elif option == '2':
        downloadTheFile(stub, time_offset)
    elif option == '3':
        deleteTheFile(stub)
    elif option == '4':
        isFilePresent(stub)
    elif option == '5':
        updateFile(stub)
    elif option == '6':
        getListOfAllTheFilesForTheUser(stub)
    elif option == '7':
        sendFileMultipleTimes(stub)

def run_client(serverAddress):
    with grpc.insecure_channel(serverAddress) as channel:
        try:
            grpc.channel_ready_future(channel).result(timeout=1)
        except grpc.FutureTimeoutError:
            print("Connection timeout. Unable to connect to port")
            sys.exit(1)
        else:
            print("Connected")
        
        # Create a stub for the service
        stub = fileService_pb2_grpc.FileserviceStub(channel)
        
        # Synchronize client clock with server time
        time_offset = synchronize_client_clock(stub)
        
        # Handle user inputs and pass the time offset to functions that need it
        handleUserInputs(stub, time_offset)

if __name__ == '__main__':
    run_client('127.0.0.1:9000')
