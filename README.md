# ***Mandelbrot Parallelism***

## **Description**

The program consists of two applications, which together renders parts of the Mandelbrot set and saves the output as a PNG file.
* One is a Quart based server that accepts requests on a HTTP interface.
* The other is a client, which can spread the workload over a
set of servers by dividing the workload into chunks.

Example image output: *mandelbrot.png*.

## **Getting Started**


### **Installing**

* Clone the GitHub repo to your computer.
* Set up a virtual environment using  ```venv -m env```
* Activate the environment using ```env\Scripts\activate```
* Install the prerequisites using ```pip install -r requirements.txt```

### **Starting the Servers**

* Start the server by entering ```python server.py {port}``` in different terminals
  * Any number of servers can be used as long as they are listening on different ports

Example:
```
$ python server.py 3000
$ python server.py 9000
...
```
### **Running the Client Script**
```
$ python client.py min_c_re min_c_im max_c_re max_c_im max_n x y divisions [server_list]
```
Example:
```
$ python client.py -2 -1 1 1 100 10000 10000 2 localhost:9000 localhost:3000
```

## Discussion
Dividing workload between workers yields quicker rendering times, however sending several chunks to the same worker will not speed up rendering time as compared to sending the entire workload in one request.

The Client is very bare bones and can be improved upon by enhancing the speed with which the workload division is made, perhaps using a system such as JIT, as well as adding more error handling over all.

Using JIT for the server calculations increased performance by over 50x depending on the in-parameters.

The resulting image is also rotated 90 degrees clockwise. But let's call that a feature!


## Authors

***Hannes Gustafsson***