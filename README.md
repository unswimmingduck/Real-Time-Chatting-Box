# Real-Time-Chatting-Box


![Static Badge](https://img.shields.io/badge/3.6%2B-make?style=for-the-badge&logo=python&logoColor=white&label=python&labelColor=blue&color=gray)
![Static Badge](https://img.shields.io/badge/Socket-make?style=for-the-badge&logo=python&logoColor=white&labelColor=blue&color=gray)
![Static Badge](https://img.shields.io/badge/hashlib-make?style=for-the-badge&logo=python&logoColor=white&labelColor=blue&color=gray)
![Static Badge](https://img.shields.io/badge/PYQT5-make?style=for-the-badge&logo=qt&logoColor=white&labelColor=green&color=gray)
![Static Badge](https://img.shields.io/badge/QtDesinger-make?style=for-the-badge&logo=qt&logoColor=white&labelColor=green&color=gray)
![Static Badge](https://img.shields.io/badge/opencv-make?style=for-the-badge&logo=opencv&logoColor=white&labelColor=red&color=green)

![Static Badge](https://img.shields.io/badge/win10-make?style=for-the-badge&logo=windows&logoColor=white&labelColor=blue&color=blue)
![Static Badge](https://img.shields.io/badge/vscode-make?style=for-the-badge&logo=vscode&logoColor=white&labelColor=blue&color=blue)
## 1. Introduction
&emsp;&emsp;This is a chatting box based on TCP and UDP that can achieve text chatting, real-time video chatting and file transfer.   
&emsp;&emsp;**It is definitiley that a good and concise GUI is a significant role in the chatting box. So, after many researching, I chose [PyQT5](https://doc.qt.io/qtforpython-6/) to construct my chatting-box interactive interference because PyQt5 is a powerful and flexible GUI development tool that combines the simplicity and ease of use of Python with the cross-platform nature and richness of the Qt framework. It is suitable for a variety of GUI development projects from simple widgets to large applications.  
&emsp;&emsp;What's more, in order to providing better using experinece, we use threading to receive and send messages, using UDP protocol to realizing real-time-video-chatting so that we could save internet resources, and we also apply hashirstlib to tackle TCP packet fragmentation in TCP file transfer。**

  
  
## 2. Environment and Dependencies

### 2.1 Construct environment and install prerequisites

```bash
# create virtual env
$ mkdir chatting_box && cd chatting_box
$ conda create -n chat_env python=3.7
$ conda activate chat_env
# install opencv
$ conda install opencv-python
	 
# git clone the project to current folder
$ git clone https://github.com/unswimmingduck/Real-Time-Chatting-Box.git
```

### 2.2 Run the chatting-box
&emsp;&emsp; Firstly, we should start the server. **Or, the chatting-box cannot run normally**.
```bash
# start the server
$ python chatting-box\test\server_start.py
```
**&emsp;&emsp; Secondly, we should run two client in different terminals, you should repeat the below steps in two different terminals so that you can use and test the functions of this chatting-box.**
```bash
# open one terminal in your computer and activate the virtual env
$ conda activate chat_env
$ python chatting-box\test\main.py
```
&emsp;&emsp; Then, there will be a register box and you should register your username. If the username is registered by other before, you will be required to use other username to register.

## 3. Function details
&emsp;&emsp; **In the following parts, I will introduce how I realize those fuction: Interactive Interface, Text Chatting, Real-Time-Video Chatting, File Transfer.**
* Interactivate Interface: **PyQt5, QtDesigner**
* Text Chatting: **TCP protocol, sepecial message encoding and decoding**
* Real-Time-Video Chatting: **UDP protocol, OpenCV**
&emsp;&emsp;
### 3.1 Interactive interface
&emsp;&emsp; **In the design of the interaction interface we divided it into four modules: registration interaction interface, main interaction interface, small chat interface, and small pop-up box.**  
&emsp;&emsp; **Firstlt, I used [QtDesigner](https://doc.qt.io/qt-6/qtdesigner-manual.html) to design the primary interactive interface**. Qt Designer is a visual interface design tool in the Qt Development Kit that allows developers to design interfaces quickly and intuitively using a graphical interface. QtDesigner allows the user to directly convert the ui into relavent python or C++ code. **At the same time, I added the auto-complete function to the search box on the main interactive interface, which makes the user experience better. If you want to know more details of them, you can see code in [Client\client.py](https://github.com/unswimmingduck/Real-Time-Chatting-Box/blob/main/Client/client.py)**  
&emsp;&emsp; **Secondly, in order to have a better notification system in this chatting-box, I used [QtWidgets.QDialog()](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QDialog.html) in Qt5 to construct the Registration Interactive Interface and Mini pop-up window. if you want to know more details of these, you can see code in [Message\Register_Msg.py](https://github.com/unswimmingduck/Real-Time-Chatting-Box/blob/main/Message/Register_Msg.py) and [Message\Reminder_Msg.py](https://github.com/unswimmingduck/Real-Time-Chatting-Box/blob/main/Message/Reminder_Msg.py) to know how to realize Registration Interactive Interface and Mini pop-up window respectively**.   
&emsp;&emsp;  
![image](https://github.com/unswimmingduck/Real-Time-Chatting-Box/assets/111033998/d05477a7-be17-4f58-9dae-d263d99d4566)
&emsp;&emsp;   
### 3.2 Text Chatting
&emsp;&emsp; **Since TCP is a peer-to-peer communication protocol, the chat interface we designed is intended to enable contact with multiple other clients. So just connecting the client to the client with TCP protocol is not able to realize our goal. Therefore, we build a server with data processing capability based on TCP protocol, and let the server act as a signal relay station to realize peer-to-peer communication between multiple clients.The following image shows the rough machinsm of text chatting function**   
&emsp;&emsp;![image](https://github.com/unswimmingduck/Real-Time-Chatting-Box/assets/111033998/53a9ea45-9721-4fe2-b517-3d00199f6bd7)
&emsp;&emsp;**Besides, We make a specific encapsulation encoding of the specific content to be sent by the client, and then send it to the Server server, which will decode the encapsulated message sent, and then send it to the specified client according to the information after decoding.The following image manifests how we do the encoding job.**  
&emsp;&emsp;![image](https://github.com/unswimmingduck/Real-Time-Chatting-Box/assets/111033998/cabdfacb-0888-42be-8cdf-3f6fce4782f5)


&emsp;&emsp; **At the same time, we hope that the loop of receiving messages and the loop of the interactive interface can not interfere with each other, so we need to introduce the operation of threads, and put the loop of receiving messages in a thread, so that the loop of receiving messages can be executed independently without interference.   
&emsp;&emsp;The following gif shows the reslut of text chatting function.**    
  &emsp;&emsp;![com](https://github.com/unswimmingduck/Real-Time-Chatting-Box/assets/111033998/f039926c-8f1d-45ef-bd27-1cfc13e6c291)

### 3.3 Real-Time-Video Chatting
&emsp;&emsp; **In Real-Time_Video Chatting, we have chose UDP protocol, which is very different from TCP: UDP has the risk of packet loss during transmission, but small packet loss during a real-time video call will not affect the whole video call process too much. At the same time, UDP transmission has a much faster transmission efficiency, which is very suitable for solving the problem of video calls in real time, such as a short period of time a large amount of information transmission process. Secondly, UDP and TCP can be used in the same address at the same time and do not interfere with each other, so the use of UDP for real-time video data dissemination can be done to make full use of the benefits of resources, while in the process of video calls can also be text communication. If you want to know more details of this fuction, you can see the codes in [Client\client.py](https://github.com/unswimmingduck/Real-Time-Chatting-Box/blob/main/Client/client.py)**  
![image](https://github.com/unswimmingduck/Real-Time-Chatting-Box/assets/111033998/1d656030-b725-4a1a-b911-6707d510eae4)  
&emsp;&emsp; **Waht's more, thanks to the Threading, we also can send text message when we use Real-Time-Video Chatting. The following gif shows how the function works. You also can [click here](https://github.com/unswimmingduck/Real-Time-Chatting-Box/blob/main/result/video.gif) to see how the Real-Time-Video Chatting works.**  
![image](https://github.com/unswimmingduck/Real-Time-Chatting-Box/blob/main/result/video.gif)
### 3.4 File Transfer
&emsp;&emsp; **We have chosen the TCP protocol for the file transfer process because we need to ensure the accuracy of the file transfer. What's more, in order to ensure the correctness of the file transfer, we also need to introduce MD5 encryption to further ensure the correctness of the file transfer**
&emsp;&emsp; **However, I meet a problem in filing transfer. We introduce MD5 encryption to ensure the correctness of the file transfer, but there always exist an erro that the file transfer occur an erro. Nevertheless, contrasting the sending file with the received file, there dosenot have any visual difference. After I searchinng many information, I konw that the erro happen because I didnot pay attention to the common problem in file transfer: the problem of TCP packet fragmentation. The following gif shows the problem of TCP packet fragmentation in file transfer.**  
![image](https://github.com/unswimmingduck/Real-Time-Chatting-Box/blob/main/result/file_transition.gif)
&emsp;&emsp; **So, we need to solve the problem of sticky packets in the process of sending files, we can solve the problem of sticky packets by reading the file size before sending the file and adjusting the length of the last received file when the reading is about to be completed.**   
&emsp;&emsp; **In the following image, you can see the structure of how we achieve the function of file transfer.**
![image](https://github.com/unswimmingduck/Real-Time-Chatting-Box/assets/111033998/322583e6-4918-4d12-9748-5aeb5621e9f7)
