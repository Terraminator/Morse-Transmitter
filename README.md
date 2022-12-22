# morse transmitter
Sending and receiving morse signals via python

## light transmission
calculating resistance of led:
R=U/I ( Ohmsches Gesetz )

R=3.3V(output of pin)-2V(input of led) / I

R=1.3V/0.004A

R = 325Ohm -> 330 Ohm  

![image](https://github.com/Terraminator/Morse-Transmitter/blob/717114cba0968b9210b8442ad04d6a3351ccd1bb/Light_Transmission/image1.png)  


![image](https://gpiozero.readthedocs.io/en/stable/_images/pin_layout.svg)



Setup:
<pre>cd Light_Transmission</pre>  
<pre>pip install -r requirements.txt </pre>  

Usage of morse sender:  
<pre>python3 sender.py "message"</pre>  

Usage of morse receiver: 
<pre>python3 receiver.py</pre>  

##audio transmission
